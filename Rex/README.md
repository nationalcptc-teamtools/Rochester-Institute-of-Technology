# Report Rex

Write pentest reports in Markdown. Get professional PDFs.

Report Rex converts structured Markdown directories into polished PDF reports via LaTeX, with full support for custom branding, modular templates, and Docker-based reproducible builds.

---

## Installation (fresh Linux, e.g. Kali)

Report Rex can run either fully containerized (Docker, recommended — no LaTeX
packages to manage) or natively (faster iteration, but you own the TeX Live
install).

### Option A: Docker (recommended)

```bash
sudo apt update
sudo apt install -y git docker.io

# Add your user to the docker group so you don't need sudo for every build
sudo usermod -aG docker "$USER"
newgrp docker   # or log out/in for the group change to take effect

git clone https://gitlab.com/your-org/report-rex.git && cd report-rex

# Build the runtime image (bundles pandoc + TeX Live + XeLaTeX + report-rex-core)
docker build -t report-rex:latest .

# Render the example report
./build.sh --dir reporting/example --output example-report.pdf
```

### Option B: Native (no Docker)

Requires pandoc, XeLaTeX, and Python ≥3.11. On Kali/Debian/Ubuntu:

```bash
sudo apt update
sudo apt install -y git pandoc python3-venv python3-pip fontconfig \
  texlive-xetex texlive-latex-extra texlive-fonts-extra

git clone https://gitlab.com/your-org/report-rex.git && cd report-rex

# Install the core Python package
python3 -m venv .venv
.venv/bin/pip install -e "core/[dev]"

# Render the example report
.venv/bin/report-rex build --dir reporting/example --templates-root templates \
  --output example-report.pdf
# or via the wrapper script:
./build.sh --dir reporting/example --output example-report.pdf --no-docker
```

`texlive-latex-extra` and `texlive-fonts-extra` are large (~1-2 GB) but cover
every LaTeX package the bundled templates need (`tcolorbox`, `fancyhdr`, `pgf`,
`tikz`, `booktabs`, `tex-gyre`, etc.) without hunting down individual `tlmgr`
packages. If disk space is tight, install `texlive` (the smaller base set)
first and add missing packages with `tlmgr install <name>` as pandoc/xelatex
errors surface them.

## Quick Start

```bash
# Build the example report (Docker required)
./build.sh --dir reporting/example --output example-report.pdf

# Or natively (requires pandoc, xelatex, python ≥3.11)
./build.sh --dir reporting/example --output example-report.pdf --no-docker
```

## Project Structure

```
report-rex/
├── core/               Python package: parsing, assembly, pandoc orchestration
├── templates/          LaTeX templates (self-contained, shareable as zip)
│   ├── rit-cptc/       RIT CPTC full report (default for new reports)
│   ├── rit-cptc-comm/  RIT CPTC one-pager (default for new quick-comms)
│   ├── rex-default/    Generic pentest report with cover page and severity boxes
│   └── quick-comm/     Lightweight one-pager for mid-engagement updates
├── reporting/          Example report directory structure
│   ├── example/        Full report example (sections, findings, appendices)
│   └── communication/  Quick communication example
├── vuln-templates/     Default, copy-pasteable finding write-ups (CSRF, SSRF, XXE, ...)
├── docs/               Docusaurus documentation site
├── Dockerfile          Runtime image (pandoc + TeX Live + Python)
├── build.sh            User-facing build script
└── .gitlab-ci.yml      CI/CD: lint, test, pages, package publish
```

## Report Directory Structure

```
my-engagement/
├── index.md            Wire up everything; holds all report metadata
├── sections/
│   ├── exec_summ.md
│   └── methodology.md
├── reports/
│   ├── vuln-1.md       YAML frontmatter with severity/CVSS + markdown write-up
│   └── vuln-2.md
├── appendices/
│   └── 1.md
└── assets/
    └── screenshots/
```

### index.md

```yaml
---
title: "Web Application Penetration Test"
client: "ACME Corporation"
date: "2024-01-15"
version: "1.0"
confidentiality: "Confidential"
template: "rit-cptc"
authors:
  - name: "Jane Doe"
    role: "Lead Penetration Tester"
logo:
  path: "assets/logo.png"
  width: "4cm"
structure:
  sections:
    - sections/exec_summ.md
    - sections/methodology.md
  reports:
    - reports/vuln-1.md
  appendices:
    - appendices/1.md
---
```

### Vulnerability File

```markdown
---
title: "SQL Injection in Login Endpoint"
severity: "Critical"
cvss_score: 9.8
status: "Open"
affected_urls:
  - "https://example.com/api/login"
---

## Description

...

## Impact

...

## Replication

...

## Remediation

...
```

## build.sh Options

```
--dir PATH       Report directory   (default: reporting/example)
--template NAME  Template override  (default: from index.md)
--output FILE    Output PDF path    (default: report.pdf)
--final          Final report, no DRAFT watermark (default: draft, renamed to <name>-draft.pdf)
--force          Skip QA-gate checks; build even with validation errors
--no-docker      Native mode (needs pandoc, xelatex, python)
--image TAG      Docker image tag   (default: report-rex:latest)
```

## Templates

Templates are self-contained directories that can be zipped and shared:

```bash
# Package your template
zip -r my-company-template.zip templates/my-template/

# Install someone else's template
unzip their-template.zip -d templates/

# Use it
./build.sh --template my-template
```

A template contains:
- `report-rex.yaml` — manifest
- `template.tex` — pandoc LaTeX template
- `theme.yaml` — default color/font values
- `filters/vuln_filter.lua` — Lua filter for severity boxes
- `assets/` — logo, fonts, graph scripts

## Documentation

Full documentation is available at the GitLab Pages site for this project, or run locally:

```bash
cd docs && npm install && npm start
```

## Development

```bash
# Install the core package in editable mode
pip install -e "core/[dev]"

# Run tests
cd core && pytest tests/ -v

# Lint
ruff check core/src/

# Prose/grammar lint (report content + docs)
vale --config .vale.ini reporting/ docs/docs/

# ...or via the container, without installing vale locally
docker run --rm --entrypoint vale \
  -v "$(pwd)/reporting/example:/report:ro" \
  report-rex:latest \
  --config /opt/report-rex/.vale.ini /report
```

## License

MIT
