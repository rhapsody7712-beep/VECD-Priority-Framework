#!/usr/bin/env bash
# =============================================================================
# create_gitlab_labels.sh
# Creates VECD priority framework labels in a GitLab project via the REST API.
#
# USAGE
#   export GITLAB_TOKEN="glpat-xxxxxxxxxxxxxxxxxxxx"
#   export PROJECT_ID="123"                        # numeric ID or URL-encoded path
#   bash scripts/create_gitlab_labels.sh
#
# OPTIONAL ENVIRONMENT VARIABLES
#   GITLAB_URL   Base URL of your GitLab instance (default: https://gitlab.com)
#   DRY_RUN      Set to "true" to print API calls without executing them
#
# REQUIREMENTS
#   curl, jq
#
# EXIT CODES
#   0  All labels created or already exist
#   1  Missing required environment variable or dependency
#   2  One or more API calls failed
# =============================================================================

set -euo pipefail

# ── Colour codes for terminal output (suppressed when not a TTY) ──────────────
if [[ -t 1 ]]; then
  C_RED='\033[0;31m'
  C_GRN='\033[0;32m'
  C_YLW='\033[0;33m'
  C_BLU='\033[0;34m'
  C_MAG='\033[0;35m'
  C_CYN='\033[0;36m'
  C_DIM='\033[2m'
  C_BLD='\033[1m'
  C_RST='\033[0m'
else
  C_RED='' C_GRN='' C_YLW='' C_BLU='' C_MAG='' C_CYN='' C_DIM='' C_BLD='' C_RST=''
fi

# ── Logging helpers ───────────────────────────────────────────────────────────
log_info()    { echo -e "${C_BLU}[INFO ]${C_RST}  $*"; }
log_ok()      { echo -e "${C_GRN}[OK   ]${C_RST}  $*"; }
log_skip()    { echo -e "${C_CYN}[SKIP ]${C_RST}  $*"; }
log_warn()    { echo -e "${C_YLW}[WARN ]${C_RST}  $*"; }
log_error()   { echo -e "${C_RED}[ERROR]${C_RST}  $*" >&2; }
log_dry()     { echo -e "${C_MAG}[DRY  ]${C_RST}  $*"; }
log_section() { echo -e "\n${C_BLD}$*${C_RST}"; }

# ── Preflight checks ──────────────────────────────────────────────────────────
check_deps() {
  local missing=()
  for cmd in curl jq; do
    if ! command -v "$cmd" &>/dev/null; then
      missing+=("$cmd")
    fi
  done
  if [[ ${#missing[@]} -gt 0 ]]; then
    log_error "Required tools not found: ${missing[*]}"
    log_error "Install them and retry."
    exit 1
  fi
}

check_env() {
  local missing=()
  [[ -z "${GITLAB_TOKEN:-}" ]] && missing+=("GITLAB_TOKEN")
  [[ -z "${PROJECT_ID:-}"   ]] && missing+=("PROJECT_ID")
  if [[ ${#missing[@]} -gt 0 ]]; then
    log_error "Required environment variables are not set: ${missing[*]}"
    echo ""
    echo "  export GITLAB_TOKEN=\"glpat-xxxxxxxxxxxxxxxxxxxx\""
    echo "  export PROJECT_ID=\"123\""
    echo ""
    exit 1
  fi
}

# ── Label definitions ─────────────────────────────────────────────────────────
# Format: "Name|color|description"
# Names use the GitLab scoped label syntax (::) for priority labels so they
# are mutually exclusive — only one priority:: label can be active at a time.
declare -a LABELS=(
  "Priority::Critical|#FF0000|Immediate action required. VECD score 35–40."
  "Priority::High|#FF6600|Schedule in current or next cycle. VECD score 25–34."
  "Priority::Medium|#FFCC00|Backlog — plan within 1–2 quarters. VECD score 15–24."
  "Priority::Low|#999999|Defer, revisit at roadmap review, or close. VECD score 0–14."
  "Offset::Applied|#6600CC|A Leadership Offset has been applied. See issue body for approver, role, and rationale."
  "vecd::scored|#1F75CB|All four VECD dimensions have been scored and justified."
  "vecd::pending-score|#F0AD4E|Issue opened — VECD scoring not yet complete."
)

# ── Core API function ─────────────────────────────────────────────────────────
# Attempts to create a label. If it already exists (HTTP 409), skips cleanly.
# Returns 0 on success or skip, 1 on any other API error.
create_label() {
  local name="$1"
  local color="$2"
  local description="$3"

  local endpoint="${GITLAB_URL}/api/v4/projects/${PROJECT_ID_ENCODED}/labels"

  local payload
  payload=$(jq -n \
    --arg name        "$name" \
    --arg color       "$color" \
    --arg description "$description" \
    '{name: $name, color: $color, description: $description}')

  if [[ "${DRY_RUN:-false}" == "true" ]]; then
    log_dry "POST ${endpoint}"
    log_dry "     payload: ${payload}"
    return 0
  fi

  local http_code
  local response_body
  response_body=$(curl \
    --silent \
    --write-out "\n%{http_code}" \
    --request POST \
    --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" \
    --header "Content-Type: application/json" \
    --data    "$payload" \
    "${endpoint}")

  # Split body and status code (last line)
  http_code=$(echo "$response_body" | tail -n1)
  local body
  body=$(echo "$response_body" | head -n -1)

  case "$http_code" in
    201)
      local created_id
      created_id=$(echo "$body" | jq -r '.id // "unknown"')
      log_ok "Created  ${C_BLD}${name}${C_RST}  (id: ${created_id}, color: ${color})"
      ;;
    409)
      log_skip "Already exists  ${C_BLD}${name}${C_RST}  — no change made"
      ;;
    401)
      log_error "Authentication failed. Check that GITLAB_TOKEN is valid and has api scope."
      return 1
      ;;
    403)
      log_error "Permission denied for label '${name}'. Token may lack Maintainer access to project ${PROJECT_ID}."
      return 1
      ;;
    404)
      log_error "Project not found (PROJECT_ID=${PROJECT_ID}). Verify the ID or path and that the token has access."
      return 1
      ;;
    *)
      local api_message
      api_message=$(echo "$body" | jq -r '.message // .error // "no message"' 2>/dev/null || echo "unparseable response")
      log_error "Unexpected HTTP ${http_code} for label '${name}': ${api_message}"
      return 1
      ;;
  esac

  return 0
}

# ── URL-encode the project ID ─────────────────────────────────────────────────
# Numeric IDs pass through unchanged.
# String paths (e.g. "mygroup/myproject") are percent-encoded.
encode_project_id() {
  local raw="$1"
  if [[ "$raw" =~ ^[0-9]+$ ]]; then
    echo "$raw"
  else
    # Replace / with %2F (the only character that needs encoding in a project path)
    echo "${raw//\//%2F}"
  fi
}

# ── Main ──────────────────────────────────────────────────────────────────────
main() {
  check_deps
  check_env

  : "${GITLAB_URL:=https://gitlab.com}"
  # Strip trailing slash for consistent URL construction
  GITLAB_URL="${GITLAB_URL%/}"

  PROJECT_ID_ENCODED=$(encode_project_id "$PROJECT_ID")
  readonly PROJECT_ID_ENCODED

  local dry_notice=""
  [[ "${DRY_RUN:-false}" == "true" ]] && dry_notice="  ${C_MAG}(DRY RUN — no API calls will be made)${C_RST}"

  log_section "VECD GitLab Label Setup${dry_notice}"
  log_info "GitLab URL  : ${GITLAB_URL}"
  log_info "Project ID  : ${PROJECT_ID}  (encoded: ${PROJECT_ID_ENCODED})"
  log_info "Labels      : ${#LABELS[@]}"
  echo ""

  local failed=0

  for entry in "${LABELS[@]}"; do
    # Split on pipe character
    local name color description
    IFS='|' read -r name color description <<< "$entry"

    if ! create_label "$name" "$color" "$description"; then
      (( failed++ )) || true
    fi
  done

  echo ""
  if [[ $failed -eq 0 ]]; then
    log_ok "Done. All labels created or already present."
    echo ""
    echo -e "  ${C_DIM}Next steps:${C_RST}"
    echo -e "  ${C_DIM}1. Open an issue using the VECD Priority Request template.${C_RST}"
    echo -e "  ${C_DIM}2. Score all four dimensions and apply the matching Priority:: label.${C_RST}"
    echo -e "  ${C_DIM}3. Apply Offset::Applied if a Leadership Offset is in effect.${C_RST}"
    echo ""
  else
    log_error "${failed} label(s) failed to create. Review the errors above and retry."
    exit 2
  fi
}

main "$@"
