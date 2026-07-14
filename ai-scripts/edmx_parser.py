"""Parse OData CSDL ($metadata / EDMX) into a normalized inventory.

Namespace-agnostic: elements are matched by local tag name, so the same code
handles OData v3 (edm ns .../2009/11/edm; actions as <FunctionImport>) and
OData v4 (edm ns docs.oasis-open.org/odata/ns/edm; actions as <Action>/<Function>).

Used by reconcile_odata.py. Standard library only (xml.etree).
"""
from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field


def _local(tag: str) -> str:
    """Return the local (namespace-stripped) tag name."""
    return tag.rsplit("}", 1)[-1]


def _iter_local(elem, name):
    """All descendants (any depth) whose local tag name is `name`."""
    return [e for e in elem.iter() if _local(e.tag) == name]


def _children_local(elem, name):
    """Direct children whose local tag name is `name`."""
    return [e for e in list(elem) if _local(e.tag) == name]


def _short(type_ref: str) -> str:
    """Strip Collection(...) wrapper and namespace prefix from an EDM type ref."""
    t = (type_ref or "").strip()
    if t.startswith("Collection(") and t.endswith(")"):
        t = t[len("Collection("):-1]
    return t.rsplit(".", 1)[-1]


@dataclass
class Prop:
    name: str
    type: str
    nullable: bool = True
    is_key: bool = False
    is_nav: bool = False
    is_collection: bool = False


@dataclass
class EntityType:
    name: str
    props: dict = field(default_factory=dict)  # name -> Prop
    keys: list = field(default_factory=list)


@dataclass
class Action:
    name: str
    return_type: str | None = None
    params: list = field(default_factory=list)  # list[(name, type)]
    kind: str = "Action"  # Action | Function | FunctionImport
    # Short type name the action is bound to (None for unbound actions). The
    # binding disambiguates same-named actions (e.g. Delivery has an `Upsert`
    # on Administrators AND one on Participants); keying by name alone made
    # one silently shadow the other.
    binding: str | None = None


@dataclass
class Inventory:
    version: str
    entity_sets: dict = field(default_factory=dict)    # setName -> type (short)
    types: dict = field(default_factory=dict)          # name -> EntityType
    complex_types: dict = field(default_factory=dict)  # name -> EntityType
    enum_types: dict = field(default_factory=dict)     # name -> [members]
    actions: dict = field(default_factory=dict)        # (binding, name) -> Action


def _parse_associations(root) -> dict:
    """v3 only: assoc short name -> {role: (target type short, multiplicity)}.

    v3 NavigationProperty elements carry no Type attribute - the target type
    and cardinality live on the referenced <Association>'s <End> elements, so
    they must be resolved through this map.
    """
    out: dict = {}
    for assoc in _iter_local(root, "Association"):
        ends = {}
        for end in _children_local(assoc, "End"):
            ends[end.get("Role")] = (
                _short(end.get("Type", "")),
                end.get("Multiplicity", ""),
            )
        out[assoc.get("Name")] = ends
    return out


def _parse_type(et, assocs: dict) -> EntityType:
    t = EntityType(name=et.get("Name"))
    for key in _children_local(et, "Key"):
        for pr in _children_local(key, "PropertyRef"):
            t.keys.append(pr.get("Name"))
    for p in _children_local(et, "Property"):
        name = p.get("Name")
        raw = p.get("Type", "")
        t.props[name] = Prop(
            name=name,
            type=_short(raw),
            nullable=(p.get("Nullable", "true") != "false"),
            is_key=name in t.keys,
            is_collection=raw.startswith("Collection("),
        )
    for np in _children_local(et, "NavigationProperty"):
        name = np.get("Name")
        raw = np.get("Type", "")  # v4 carries Type; v3 uses Relationship
        if raw:
            t.props[name] = Prop(
                name=name,
                type=_short(raw),
                is_nav=True,
                is_collection=raw.startswith("Collection("),
            )
        else:
            rel = _short(np.get("Relationship", ""))
            target, mult = assocs.get(rel, {}).get(
                np.get("ToRole", ""), ("(nav)", "")
            )
            t.props[name] = Prop(
                name=name,
                type=target or "(nav)",
                is_nav=True,
                is_collection=(mult == "*"),
            )
    for k in t.keys:
        if k in t.props:
            t.props[k].is_key = True
    return t


def _parse_action(a, kind: str) -> Action:
    act = Action(name=a.get("Name"), kind=kind)
    params = _children_local(a, "Parameter")
    for p in params:
        pname = p.get("Name")
        ptype = p.get("Type", "")
        # The binding parameter is the action's attach point, not a payload
        # param; both v3 (WebApi OData) and v4 (convention model builder) name
        # it "bindingParameter". Kept out of params so the docs' :input: list
        # (which rightly omits it) compares clean.
        if pname == "bindingParameter":
            act.binding = _short(ptype)
        else:
            act.params.append((pname, _short(ptype)))
    # v4 fallback: a bound action whose binding param has a non-standard name
    # still has it first by CSDL rule, so peel it off when IsBound is set.
    if act.binding is None and a.get("IsBound") == "true" and act.params:
        act.binding = act.params[0][1]
        act.params = act.params[1:]
    for r in _children_local(a, "ReturnType"):
        act.return_type = _short(r.get("Type", ""))
    # v3 FunctionImport carries ReturnType as an attribute
    if act.return_type is None and a.get("ReturnType"):
        act.return_type = _short(a.get("ReturnType"))
    return act


def parse(edmx_text: str) -> Inventory:
    """Parse EDMX text into an Inventory."""
    root = ET.fromstring(edmx_text)
    version = "4" if "oasis-open.org/odata" in edmx_text else "3"
    inv = Inventory(version=version)
    assocs = _parse_associations(root)

    for et in _iter_local(root, "EntityType"):
        t = _parse_type(et, assocs)
        inv.types[t.name] = t
    for ct in _iter_local(root, "ComplexType"):
        t = _parse_type(ct, assocs)
        inv.complex_types[t.name] = t
    for en in _iter_local(root, "EnumType"):
        inv.enum_types[en.get("Name")] = [
            m.get("Name") for m in _children_local(en, "Member")
        ]
    for es in _iter_local(root, "EntitySet"):
        inv.entity_sets[es.get("Name")] = _short(es.get("EntityType", ""))
    for kind in ("Action", "Function", "FunctionImport"):
        for a in _iter_local(root, kind):
            act = _parse_action(a, kind)
            inv.actions[(act.binding, act.name)] = act
    return inv


def parse_file(path: str) -> Inventory:
    with open(path, "r", encoding="utf-8-sig") as fh:
        return parse(fh.read())
