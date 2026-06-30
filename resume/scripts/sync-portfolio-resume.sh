#!/usr/bin/env bash
# Copy the default role PDF to portfolio/public/resume/resume.pdf for the live site.
set -euo pipefail

PORTFOLIO_RESUME="${PORTFOLIO_RESUME:-forward-deployed-engineer}"

RESUME_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "${RESUME_ROOT}/.." && pwd)"
SOURCE="${RESUME_ROOT}/pdf/${PORTFOLIO_RESUME}.pdf"
DEST="${REPO_ROOT}/portfolio/public/resume/Brandon-Miner-Resume.pdf"

if [[ ! -f "${SOURCE}" ]]; then
  echo "error: ${SOURCE} not found — run resume/scripts/build-pdfs.sh first" >&2
  exit 1
fi

mkdir -p "$(dirname "${DEST}")"
cp -f "${SOURCE}" "${DEST}"
echo "Portfolio resume synced: ${PORTFOLIO_RESUME}.pdf -> portfolio/public/resume/resume.pdf"
