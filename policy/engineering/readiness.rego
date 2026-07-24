package engineering.readiness

import rego.v1

maturity_caps := {
  "DESIGNED": 5.0,
  "IMPLEMENTED": 7.0,
  "VERIFIED": 8.5,
  "MEASURED": 9.5,
  "INDEPENDENTLY_REVIEWED": 10.0,
}

gap_exists(gap_id) if {
  some gap in input.gap_register.gaps
  gap.id == gap_id
}

deny contains msg if {
  some domain in input.scorecard.domains
  cap := maturity_caps[domain.evidence_maturity]
  domain.score > cap
  msg := sprintf("domain %s score %.1f exceeds evidence-maturity cap %.1f", [domain.id, domain.score, cap])
}

deny contains msg if {
  some domain in input.scorecard.domains
  domain.applicable == true
  domain.score < input.scorecard.readiness_threshold
  count(domain.blocking_gaps) == 0
  msg := sprintf("domain %s is below threshold without a blocking gap", [domain.id])
}

deny contains msg if {
  some domain in input.scorecard.domains
  some gap_id in domain.blocking_gaps
  not gap_exists(gap_id)
  msg := sprintf("domain %s references unknown gap %s", [domain.id, gap_id])
}

deny contains msg if {
  input.scorecard.world_class_ready == true
  some domain in input.scorecard.domains
  domain.applicable == true
  domain.score < input.scorecard.readiness_threshold
  msg := sprintf("world-class readiness claimed while domain %s is below threshold", [domain.id])
}

deny contains msg if {
  input.scorecard.world_class_ready == true
  some gap in input.gap_register.gaps
  gap.priority == "P0"
  gap.status == "OPEN"
  msg := sprintf("world-class readiness claimed with open P0 gap %s", [gap.id])
}

deny contains "toolchain permits floating versions" if {
  input.toolchain.policy.floating_versions_allowed == true
}

deny contains "toolchain permits unverified binary execution" if {
  input.toolchain.policy.unverified_binary_execution_allowed == true
}

deny contains "toolchain permits curl-pipe-shell execution" if {
  input.toolchain.policy.curl_pipe_shell_allowed == true
}

deny contains "toolchain failure mode is not fail-closed-or-blocked" if {
  input.toolchain.policy.tool_failure_mode != "fail-closed-or-blocked"
}

deny contains "native validator is not required" if {
  input.toolchain.policy.native_validator_required != true
}
