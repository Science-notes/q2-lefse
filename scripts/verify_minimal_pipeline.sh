#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   scripts/verify_minimal_pipeline.sh [command_prefix]
# Example:
#   scripts/verify_minimal_pipeline.sh "conda run -n lefse-py27"

COMMAND_PREFIX="${1:-${Q2_LEFSE_COMMAND_PREFIX:-}}"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INPUT_TABLE="${ROOT_DIR}/examples/minimal_otu.txt"
WORK_DIR="$(mktemp -d)"

cleanup() {
  rm -rf "${WORK_DIR}"
}
trap cleanup EXIT

if ! command -v qiime >/dev/null 2>&1; then
  echo "[ERROR] qiime command not found. Activate a QIIME 2 environment first." >&2
  exit 1
fi

if [[ ! -f "${INPUT_TABLE}" ]]; then
  echo "[ERROR] Missing input table: ${INPUT_TABLE}" >&2
  exit 1
fi

echo "[INFO] Work directory: ${WORK_DIR}"
echo "[INFO] Input table: ${INPUT_TABLE}"
if [[ -n "${COMMAND_PREFIX}" ]]; then
  echo "[INFO] Using LEfSe command prefix: ${COMMAND_PREFIX}"
else
  echo "[WARN] No command prefix set; LEfSe scripts must be available in current PATH"
fi

qiime tools import \
  --type 'SampleData[OTUTable]' \
  --input-path "${INPUT_TABLE}" \
  --output-path "${WORK_DIR}/otu-table.qza"

run_args=(
  lefse run
  --i-otu-table "${WORK_DIR}/otu-table.qza"
  --p-class-id 1
  --p-subclass-id 2
  --p-subject-id 3
  --p-normalization 1000000
  --p-lda-threshold 2.0
  --p-wilcoxon-alpha 0.05
  --p-kruskal-alpha 0.05
  --o-lefse-results "${WORK_DIR}/lefse-results.qza"
)

viz_args=(
  lefse visualize
  --i-otu-table "${WORK_DIR}/otu-table.qza"
  --p-class-id 1
  --p-subclass-id 2
  --p-subject-id 3
  --p-normalization 1000000
  --p-lda-threshold 2.0
  --p-wilcoxon-alpha 0.05
  --p-kruskal-alpha 0.05
  --o-visualization "${WORK_DIR}/lefse-results.qzv"
)

if [[ -n "${COMMAND_PREFIX}" ]]; then
  run_args+=(--p-command-prefix "${COMMAND_PREFIX}")
  viz_args+=(--p-command-prefix "${COMMAND_PREFIX}")
fi

qiime "${run_args[@]}"
qiime "${viz_args[@]}"

echo "[INFO] Pipeline finished successfully."
echo "[INFO] Result artifact: ${WORK_DIR}/lefse-results.qza"
echo "[INFO] Visualization:   ${WORK_DIR}/lefse-results.qzv"

echo "[INFO] To inspect visualization:"
echo "       qiime tools view ${WORK_DIR}/lefse-results.qzv"
