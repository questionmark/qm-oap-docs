<p align="center">
  <img src="https://img.shields.io/badge/Questionmark-OAP_API_Docs-D4AF37?style=for-the-badge&labelColor=1a1a1a" alt="Questionmark OAP API Docs"/>
</p>

<p align="center">
  <a href="https://questionmark.github.io/qm-oap-docs/">
    <img src="https://img.shields.io/badge/📚_Live_Docs-View_Site-D4AF37?style=flat-square&labelColor=1a1a1a" alt="Live Docs"/>
  </a>
  <a href="https://questionmark.github.io/qm-oap-docs/deliveryodata.html">
    <img src="https://img.shields.io/badge/🚀_Delivery-OData_v3-D4AF37?style=flat-square&labelColor=1a1a1a" alt="Delivery OData"/>
  </a>
  <a href="https://questionmark.github.io/qm-oap-docs/authoringodata.html">
    <img src="https://img.shields.io/badge/✏️_Authoring-OData_v4-D4AF37?style=flat-square&labelColor=1a1a1a" alt="Authoring OData"/>
  </a>
  <img src="https://img.shields.io/badge/Sphinx-Documentation-D4AF37?style=flat-square&labelColor=1a1a1a&logo=sphinx&logoColor=white" alt="Sphinx"/>
  <img src="https://img.shields.io/badge/License-Proprietary-D4AF37?style=flat-square&labelColor=1a1a1a" alt="License"/>
</p>

<p align="center">
  <strong>Public integration API documentation for the Questionmark Open Assessment Platform</strong>
</p>

---

## 📖 Overview

This repository contains the **source and generated HTML** for Questionmark's public OAP API documentation. It is published as a static Sphinx site to GitHub Pages.

> ⚠️ **Documentation only** — The APIs described here are implemented in their own service repositories (`qm-DeliveryOData`, `qm-AuthoringApi`, etc.)

---

## 🗂️ What's Documented

| API | Type | Source | Description |
|:---:|:----:|--------|-------------|
| 📊 | **Delivery OData** | `src/deliveryodata/` | Assessment delivery, scheduling, proctoring (v3) |
| ✏️ | **Authoring OData** | `src/authoringodata/` | Question & assessment authoring (v4) |
| 📈 | **Results OData** | `src/resultsodata.rst` | Reporting & analytics (v3) |
| 🔗 | **QMWISe** | `src/qmwise/` | Legacy SOAP integration API |
| 🐍 | **Python Client** | `src/pip.rst` | pip-installable client library |
| 📐 | **Data Model** | `src/model/` | Platform concepts & shared schema |

---

## 🏗️ Repository Structure

```
📁 qm-oap-docs/
├── 📁 src/                    # Sphinx source files
│   ├── 📄 conf.py             # Sphinx configuration
│   ├── 📄 qmdomain.py         # Custom od: and qm: domains
│   ├── 📄 index.rst           # Master toctree
│   ├── 📁 deliveryodata/      # Delivery OData feeds/types/actions
│   ├── 📁 authoringodata/     # Authoring OData entities
│   ├── 📁 qmwise/             # QMWISe SOAP methods
│   └── 📁 model/              # Data model pages
├── 📁 docs/                   # Generated HTML (GitHub Pages)
├── 📁 ai-docs/                # Reconciliation ADRs & rails
├── 📁 ai-scripts/             # Metadata reconciliation tooling
└── 📄 AGENTS.md               # Contributor workflow
```

---

## 🚀 Quick Start

### Prerequisites

```bash
pip install sphinx alabaster
```

### Build Documentation

```bash
# Using make (Linux/macOS)
make docs

# Direct command (Windows/any)
sphinx-build -b html src docs
```

### Verify Build

Resolve all Sphinx warnings before publishing. Unresolved `:od:type:` or `:od:feed:` cross-references indicate broken links.

---

## 🔧 Custom OData Markup

OData entities use custom directives from `src/qmdomain.py`:

| Directive | Purpose | Example |
|-----------|---------|---------|
| `.. od:service::` | Declares OData service context | `.. od:service:: deliveryodata` |
| `.. od:feed::` | Entity set (queryable feed) | `.. od:feed:: Assessments Assessment` |
| `.. od:type::` | Entity or complex type | `.. od:type:: Assessment` |
| `.. od:prop::` | Type property | `.. od:prop:: ID Edm.Int64` |
| `.. od:action::` | Bound/unbound action | `.. od:action:: Upsert UpsertResponse` |

**Property flags:** `:key:` · `:notnull:` · `:collection:`

**Cross-references:** `:od:feed:` · `:od:type:` · `:od:prop:` · `:od:action:`

---

## 📋 Source of Truth

```
┌─────────────────────────────────────────────────────────────┐
│  Service Code  →  $metadata  →  Documentation               │
│     (truth)        (contract)     (description)             │
└─────────────────────────────────────────────────────────────┘
```

The OData contract is **defined by the service code**, not by these docs. Authoritative sources:

| Service | Repository | Key Files |
|---------|------------|-----------|
| **Delivery** | `qm-DeliveryOData` | `ODataConfig.cs`, `Entity/*.cs`, `Controllers/*.cs` |
| **Authoring** | `qm-AuthoringApi` | `OData.Entity/*.cs`, `Data/Mapping/*.cs` |

See [`AGENTS.md`](AGENTS.md) for the verification workflow and [`ai-docs/`](ai-docs/README.md) for reconciliation tooling.

---

## 🔍 Reconciliation Tooling

This repository includes automated tooling to verify documentation against live `$metadata`:

```bash
# Fetch current metadata baselines
.\ai-scripts\fetch_baselines.ps1

# Run reconciliation check
python ai-scripts/reconcile_odata.py \
  --metadata ignore/metadata-baselines/delivery.2026-07-13.metadata.xml \
  --rst-dir src/deliveryodata \
  --product Delivery
```

See [`ai-scripts/README.md`](ai-scripts/README.md) for full usage.

---

## 📬 Feedback

<p align="center">
  <a href="mailto:developer@questionmark.com">
    <img src="https://img.shields.io/badge/Email-developer%40questionmark.com-D4AF37?style=for-the-badge&labelColor=1a1a1a&logo=gmail&logoColor=white" alt="Email"/>
  </a>
  <a href="https://github.com/questionmark/qm-oap-docs/issues">
    <img src="https://img.shields.io/badge/GitHub-Open_Issue-D4AF37?style=for-the-badge&labelColor=1a1a1a&logo=github&logoColor=white" alt="GitHub Issues"/>
  </a>
</p>

---

<p align="center">
  <sub>© Questionmark Computing Ltd. All rights reserved.</sub>
</p>
