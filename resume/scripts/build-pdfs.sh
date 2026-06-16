#!/usr/bin/env bash
# Compile all latex/*.tex files to pdf/<basename>.pdf via Docker.
# Requires Docker Desktop (or docker CLI) and network on first run to pull the image.
set -euo pipefail

IMAGE="ghcr.io/xu-cheng/texlive-debian:latest"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if ! command -v docker >/dev/null 2>&1; then
  echo "error: docker not found — install Docker Desktop or the docker CLI" >&2
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  echo "error: docker daemon is not running — start Docker Desktop" >&2
  exit 1
fi

mkdir -p "${ROOT}/pdf"

docker run --rm --platform linux/amd64 \
  -v "${ROOT}:/work" \
  -w /work/latex \
  "${IMAGE}" \
  bash -ec '
    shopt -s nullglob
    failed=0
    for tex in *.tex; do
      base="${tex%.tex}"
      echo "==> Building ${tex}"
      pdflatex -interaction=nonstopmode "$tex" > /dev/null
      pdflatex -interaction=nonstopmode "$tex" > /dev/null
      if [[ ! -f "${base}.pdf" ]]; then
        echo "ERROR: ${base}.pdf was not produced" >&2
        tail -30 "${base}.log" 2>/dev/null || true
        failed=1
        continue
      fi
      mv -f "${base}.pdf" "../pdf/${base}.pdf"
      rm -f "${base}.aux" "${base}.log" "${base}.out"
    done
    exit "$failed"
  '

echo "PDFs written to ${ROOT}/pdf/"

PORTFOLIO_RESUME="${PORTFOLIO_RESUME:-forward-deployed-engineer}"
if [[ -f "${ROOT}/pdf/${PORTFOLIO_RESUME}.pdf" ]]; then
  "$(dirname "$0")/sync-portfolio-resume.sh"
else
  echo "note: ${PORTFOLIO_RESUME}.pdf not produced; skipping portfolio resume sync" >&2
fi
