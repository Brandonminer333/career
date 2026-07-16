#!/usr/bin/env bash
# Compile a single .tex file to PDF via Docker.
# Requires Docker Desktop (or docker CLI) and network on first run to pull the image.
set -euo pipefail

IMAGE="ghcr.io/xu-cheng/texlive-debian:latest"

usage() {
  cat <<'EOF'
Usage: build-pdf.sh [-o OUTPUT_DIR] INPUT.tex

Compile a single LaTeX file to PDF via Docker.
Output directory defaults to the same directory as INPUT.tex.

Options:
  -o, --output DIR   Directory for the output PDF (default: input file directory)
  -h, --help         Show this help
EOF
}

OUTPUT_DIR=""
INPUT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -o|--output)
      OUTPUT_DIR="${2:?missing argument for $1}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      break
      ;;
    -*)
      echo "error: unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
    *)
      if [[ -n "$INPUT" ]]; then
        echo "error: unexpected argument: $1" >&2
        usage >&2
        exit 1
      fi
      INPUT="$1"
      shift
      ;;
  esac
done

if [[ -z "$INPUT" ]]; then
  echo "error: INPUT.tex is required" >&2
  usage >&2
  exit 1
fi

if [[ ! -f "$INPUT" ]]; then
  echo "error: file not found: $INPUT" >&2
  exit 1
fi

if [[ "${INPUT##*.}" != "tex" ]]; then
  echo "error: input must be a .tex file: $INPUT" >&2
  exit 1
fi

INPUT_ABS="$(cd "$(dirname "$INPUT")" && pwd)/$(basename "$INPUT")"
INPUT_DIR="$(dirname "$INPUT_ABS")"
INPUT_FILE="$(basename "$INPUT_ABS")"
STEM="${INPUT_FILE%.tex}"

if [[ -z "$OUTPUT_DIR" ]]; then
  OUTPUT_DIR_ABS="$INPUT_DIR"
else
  mkdir -p "$OUTPUT_DIR"
  OUTPUT_DIR_ABS="$(cd "$OUTPUT_DIR" && pwd)"
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "error: docker not found — install Docker Desktop or the docker CLI" >&2
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  echo "error: docker daemon is not running — start Docker Desktop" >&2
  exit 1
fi

docker run --rm --platform linux/amd64 \
  -v "${INPUT_DIR}:/in" \
  -v "${OUTPUT_DIR_ABS}:/out" \
  -w /in \
  "${IMAGE}" \
  bash -ec "
    set -euo pipefail
    tex='${INPUT_FILE}'
    stem='${STEM}'
    same_dir=$([[ \"${INPUT_DIR}\" == \"${OUTPUT_DIR_ABS}\" ]] && echo 1 || echo 0)
    echo \"==> Building \${tex}\"
    pdflatex -interaction=nonstopmode \"\${tex}\" > /dev/null
    pdflatex -interaction=nonstopmode \"\${tex}\" > /dev/null
    if [[ ! -f \"\${stem}.pdf\" ]]; then
      echo \"ERROR: \${stem}.pdf was not produced\" >&2
      tail -30 \"\${stem}.log\" 2>/dev/null || true
      exit 1
    fi
    if [[ \"\${same_dir}\" -eq 0 ]]; then
      mv -f \"\${stem}.pdf\" \"/out/\${stem}.pdf\"
    fi
    rm -f \"\${stem}.aux\" \"\${stem}.log\" \"\${stem}.out\"
  "

echo "PDF written to ${OUTPUT_DIR_ABS}/${STEM}.pdf"
