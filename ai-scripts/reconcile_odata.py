#!/usr/bin/env python3
"""Reconcile OData $metadata (source of truth) against the RST docs (od: domain).

Diffs entity sets/feeds, entity+complex types, properties (types, key flags,
nullability, nav targets and cardinality), and actions (binding, params with
types, return types) between a live/saved $metadata document and a product's
RST directory. Handles OData v3 and v4 (see edmx_parser).

Usage:
    python reconcile_odata.py --metadata <url|file> --rst-dir <dir> [--product NAME]
                              [--fail-on-diff]

Coverage limits (NOT checkable from metadata - use the controller-code pass):
  * :filter: restrictions and supported HTTP methods (GET/POST/PATCH/DELETE)
  * action return types the service omits from metadata (service bug class)
  * prose accuracy / examples / descriptions
"""
from __future__ import annotations

import argparse
import sys
import urllib.request

import edmx_parser
import rst_parser


def _load_metadata(src: str) -> str:
    if src.lower().startswith(("http://", "https://")):
        with urllib.request.urlopen(src, timeout=40) as resp:
            return resp.read().decode("utf-8-sig")
    with open(src, encoding="utf-8-sig") as fh:
        return fh.read()


def _line(sym: str, msg: str) -> str:
    return f"  {sym} {msg}"


def _diff_feeds(code, docs, out):
    out.append("== FEEDS (entity sets) ==")
    for name in sorted(code.entity_sets):
        if name not in docs.feeds:
            out.append(_line("[MISSING IN DOCS]", f"{name} ({code.entity_sets[name]})"))
        elif docs.feeds[name] != code.entity_sets[name]:
            out.append(_line("[TYPE MISMATCH]",
                             f"{name}: docs={docs.feeds[name]} "
                             f"code={code.entity_sets[name]}"))
    for name in sorted(docs.feeds):
        if name not in code.entity_sets:
            out.append(_line("[EXTRA IN DOCS]",
                             f"{name} ({docs.feed_files.get(name, '')})"))


def _merged_types(code):
    merged = dict(code.types)
    merged.update(code.complex_types)
    return merged


def _diff_types(code, docs, out):
    out.append("== TYPES ==")
    ctypes = _merged_types(code)
    for name in sorted(ctypes):
        if name not in docs.types:
            out.append(_line("[MISSING IN DOCS]", name))
    for name in sorted(docs.types):
        if name not in ctypes:
            out.append(_line("[EXTRA IN DOCS]", f"{name} ({docs.types[name].file})"))


def _diff_nav_prop(tname, p, cp, dp, out):
    # Nav targets are documented as bare type names; an `Edm.` prefix is a doc
    # bug that namespace-stripping would otherwise hide, so check the raw text.
    if dp.raw.startswith("Edm."):
        out.append(_line("[TYPE MISMATCH]",
                         f"{tname}.{p}: docs={dp.raw} code={cp.type} "
                         "(nav target must not be Edm.-prefixed)"))
    elif cp.type not in ("", "(nav)") and dp.type != cp.type:
        out.append(_line("[TYPE MISMATCH]",
                         f"{tname}.{p}: docs={dp.type} code={cp.type}"))
    if cp.is_collection != dp.is_collection:
        want = "collection" if cp.is_collection else "single"
        got = "collection" if dp.is_collection else "single"
        out.append(_line("[COLLECTION MISMATCH]",
                         f"{tname}.{p}: docs={got} code={want}"))


def _diff_props(code, docs, out):
    out.append("== PROPERTIES (types present in both) ==")
    ctypes = _merged_types(code)
    for name in sorted(set(ctypes) & set(docs.types)):
        cprops, dtype = ctypes[name].props, docs.types[name]
        for p in sorted(cprops):
            if p not in dtype.props:
                out.append(_line("[MISSING IN DOCS]", f"{name}.{p} ({cprops[p].type})"))
                continue
            dp, cp = dtype.props[p], cprops[p]
            if cp.is_key and not dp.is_key:
                out.append(_line("[KEY NOT MARKED]", f"{name}.{p}"))
            if dp.is_key and not cp.is_key:
                out.append(_line("[KEY EXTRA]",
                                 f"{name}.{p} (docs mark :key:, code does not)"))
            if cp.is_nav:
                _diff_nav_prop(name, p, cp, dp, out)
                continue
            if cp.type != dp.type:
                out.append(_line("[TYPE MISMATCH]",
                                 f"{name}.{p}: docs={dp.type} code={cp.type}"))
            if cp.is_collection != dp.is_collection:
                want = "collection" if cp.is_collection else "single"
                got = "collection" if dp.is_collection else "single"
                out.append(_line("[COLLECTION MISMATCH]",
                                 f"{name}.{p}: docs={got} code={want}"))
            # :notnull: mirrors Nullable="false"; drift in either direction
            # misleads integrators about which payload fields may be omitted.
            if not cp.nullable and not dp.is_notnull:
                out.append(_line(
                    "[NOTNULL MISSING]",
                    f"{name}.{p} (code Nullable=false, docs lack :notnull:)"))
            elif dp.is_notnull and cp.nullable:
                out.append(_line("[NOTNULL EXTRA]",
                                 f"{name}.{p} (docs mark :notnull:, code is nullable)"))
        for p in sorted(dtype.props):
            if p not in cprops:
                out.append(_line("[EXTRA IN DOCS]", f"{name}.{p}"))


def _label(key) -> str:
    binding, name = key
    return f"{binding}.{name}" if binding else name


def _compare_action(key, ca, da, out, note=""):
    suffix = f" {note}" if note else ""
    if (ca.return_type or None) != (da.return_type or None):
        out.append(_line("[RETURN MISMATCH]",
                         f"{_label(key)}: docs={da.return_type} "
                         f"code={ca.return_type}{suffix}"))
    # bindingParameter is stripped at parse time on the code side and never
    # documented in :input:; filter defensively anyway.
    cparams = {p[0]: p[1] for p in ca.params if p[0] != "bindingParameter"}
    dparams = {p[0]: p[1] for p in da.params if p[0] != "bindingParameter"}
    if set(cparams) != set(dparams):
        out.append(_line("[PARAM MISMATCH]",
                         f"{_label(key)}: only-in-docs="
                         f"{sorted(set(dparams) - set(cparams))} "
                         f"only-in-code={sorted(set(cparams) - set(dparams))}{suffix}"))
    for pname in sorted(set(cparams) & set(dparams)):
        if cparams[pname] != dparams[pname]:
            out.append(_line("[PARAM TYPE MISMATCH]",
                             f"{_label(key)}.{pname}: docs={dparams[pname]} "
                             f"code={cparams[pname]}{suffix}"))


def _diff_actions(code, docs, out):
    out.append("== ACTIONS / FUNCTIONS ==")
    matched_docs = set()
    unmatched_code = []
    for key in sorted(code.actions, key=_label):
        if key in docs.actions:
            matched_docs.add(key)
            _compare_action(key, code.actions[key], docs.actions[key], out)
        else:
            unmatched_code.append(key)
    # Same-named action documented under a different type: when the pairing is
    # unambiguous, still compare params/returns but surface where it is
    # documented - dropping to MISSING/EXTRA would hide the real drift.
    docs_leftover = [k for k in docs.actions if k not in matched_docs]
    for key in sorted(unmatched_code, key=_label):
        ca = code.actions[key]
        candidates = [k for k in docs_leftover if k[1] == key[1]]
        if len(candidates) == 1:
            dkey = candidates[0]
            docs_leftover.remove(dkey)
            out.append(_line("[BINDING MISMATCH]",
                             f"{key[1]}: docs bind to {dkey[0]} "
                             f"({docs.actions[dkey].file}), code binds to {key[0]}"))
            _compare_action(key, ca, docs.actions[dkey], out,
                            note=f"(docs under {dkey[0]})")
        else:
            out.append(_line("[MISSING IN DOCS]",
                             f"{_label(key)} -> {ca.return_type} ({ca.kind})"))
    for key in sorted(docs_leftover, key=_label):
        out.append(_line("[EXTRA IN DOCS]",
                         f"{_label(key)} ({docs.actions[key].file})"))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--metadata", required=True,
                    help="$metadata URL or saved .xml file")
    ap.add_argument("--rst-dir", required=True, help="Product RST directory")
    ap.add_argument("--product", default="", help="Optional label for the report")
    ap.add_argument("--fail-on-diff", action="store_true",
                    help="Exit 1 if any discrepancy is reported")
    ap.add_argument("--out", default="", help="Write the report to this file as UTF-8")
    args = ap.parse_args(argv)

    code = edmx_parser.parse(_load_metadata(args.metadata))
    docs = rst_parser.parse_dir(args.rst_dir)

    header = [
        f"OData reconciliation report{f' - {args.product}' if args.product else ''}",
        f"  metadata : {args.metadata}  (OData v{code.version})",
        f"  rst-dir  : {args.rst_dir}",
        f"  code: {len(code.entity_sets)} feeds, {len(_merged_types(code))} types, "
        f"{len(code.actions)} actions   "
        f"docs: {len(docs.feeds)} feeds, {len(docs.types)} types, "
        f"{len(docs.actions)} actions",
        "",
    ]
    body: list[str] = []
    _diff_feeds(code, docs, body)
    _diff_types(code, docs, body)
    _diff_props(code, docs, body)
    _diff_actions(code, docs, body)

    findings = [ln for ln in body if ln.startswith("  [")]
    report = "\n".join(header + body) + f"\n\nTOTAL findings: {len(findings)}\n"
    print(report)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(report)
    return 1 if (findings and args.fail_on_diff) else 0


if __name__ == "__main__":
    sys.exit(main())
