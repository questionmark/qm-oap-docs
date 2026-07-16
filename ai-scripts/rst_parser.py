"""Extract od: domain directives from Sphinx RST into a normalized inventory.

Directive syntax (see src/qmdomain.py and src/*/*.rst):
    .. od:feed::   <SetName> <Type>
    .. od:type::   <Type>
    .. od:prop::   <Name> <EdmType>       (+ :key: :notnull: :collection:)
    .. od:action:: <Name> [<ReturnType>]  (+ :collection: :input: P T, P T)

Properties attach to the nearest preceding od:type in the same file. Actions
attach to the nearest preceding od:type OR od:feed (mirroring qmdomain.py's
parent resolution), which yields the type the action is bound to - the join
key that keeps same-named actions on different types apart. Stdlib only.
"""
from __future__ import annotations

import glob
import os
import re
from dataclasses import dataclass, field

FEED_RE = re.compile(r"^\s*\.\.\s+od:feed::\s+(\S+)\s+(\S+)")
TYPE_RE = re.compile(r"^\s*\.\.\s+od:type::\s+(\S+)")
PROP_RE = re.compile(r"^\s*\.\.\s+od:prop::\s+(\S+)\s+(\S+)")
ACTION_RE = re.compile(r"^\s*\.\.\s+od:action::\s+(\S+)(?:\s+(\S+))?")
OPT_RE = re.compile(r"^\s*:(key|notnull|collection|input):\s*(.*)$")


def _short(t: str) -> str:
    t = (t or "").strip()
    if t.startswith("Collection(") and t.endswith(")"):
        t = t[len("Collection("):-1]
    return t.rsplit(".", 1)[-1]


@dataclass
class RstProp:
    name: str
    type: str
    # The verbatim second token, before namespace stripping. Needed to catch
    # doc bugs the short form hides, e.g. a nav prop written `Edm.RulesOf...`
    # shortens to the correct target name and would otherwise compare clean.
    raw: str = ""
    is_key: bool = False
    is_collection: bool = False
    is_notnull: bool = False


@dataclass
class RstType:
    name: str
    props: dict = field(default_factory=dict)
    file: str = ""


@dataclass
class RstAction:
    name: str
    return_type: str | None = None
    is_collection: bool = False
    params: list = field(default_factory=list)
    file: str = ""
    binding: str | None = None  # short type name the action is documented under


@dataclass
class RstInventory:
    feeds: dict = field(default_factory=dict)    # setName -> type (short)
    feed_files: dict = field(default_factory=dict)
    types: dict = field(default_factory=dict)    # name -> RstType
    actions: dict = field(default_factory=dict)  # (binding, name) -> RstAction


def _parse_params(val: str):
    out = []
    for chunk in val.split(","):
        parts = chunk.strip().split()
        if len(parts) >= 2:
            out.append((parts[0], _short(" ".join(parts[1:]))))
    return out


def _parse_file(fp: str, inv: RstInventory) -> None:
    cur_type = cur_prop = cur_action = None
    # ('type', TypeName) or ('feed', SetName): whichever directive appeared
    # last is the context an od:action belongs to, matching how qmdomain.py
    # parents actions and how the docs are actually laid out (actions under a
    # feed precede the first type; actions under a type follow it).
    last_ctx = None
    with open(fp, encoding="utf-8") as fh:
        for line in fh:
            m = FEED_RE.match(line)
            if m:
                inv.feeds[m.group(1)] = _short(m.group(2))
                inv.feed_files[m.group(1)] = fp
                last_ctx = ("feed", m.group(1))
                cur_prop = cur_action = None
                continue
            m = TYPE_RE.match(line)
            if m:
                cur_type = m.group(1)
                inv.types.setdefault(cur_type, RstType(cur_type, file=fp))
                last_ctx = ("type", cur_type)
                cur_prop = cur_action = None
                continue
            m = PROP_RE.match(line)
            if m and cur_type:
                p = RstProp(
                    name=m.group(1), type=_short(m.group(2)), raw=m.group(2)
                )
                inv.types[cur_type].props[p.name] = p
                cur_prop, cur_action = p, None
                continue
            m = ACTION_RE.match(line)
            if m:
                if last_ctx and last_ctx[0] == "type":
                    binding = last_ctx[1]
                elif last_ctx and last_ctx[0] == "feed":
                    # A feed-level action is bound to the feed's entity type
                    # ($metadata expresses the binding as the type, never the
                    # set), so resolve the feed to its type for the join key.
                    binding = inv.feeds.get(last_ctx[1])
                else:
                    binding = None
                a = RstAction(
                    name=m.group(1),
                    return_type=_short(m.group(2)) if m.group(2) else None,
                    file=fp,
                    binding=binding,
                )
                inv.actions[(a.binding, a.name)] = a
                cur_action, cur_prop = a, None
                continue
            m = OPT_RE.match(line)
            if m:
                key, val = m.group(1), m.group(2).strip()
                if key == "input" and cur_action is not None:
                    cur_action.params = _parse_params(val)
                elif key == "collection":
                    if cur_action is not None:
                        cur_action.is_collection = True
                    elif cur_prop is not None:
                        cur_prop.is_collection = True
                elif key == "key" and cur_prop is not None:
                    cur_prop.is_key = True
                elif key == "notnull" and cur_prop is not None:
                    cur_prop.is_notnull = True


def parse_dir(path: str) -> RstInventory:
    inv = RstInventory()
    pattern = os.path.join(path, "**", "*.rst")
    for fp in sorted(glob.glob(pattern, recursive=True)):
        _parse_file(fp, inv)
    return inv
