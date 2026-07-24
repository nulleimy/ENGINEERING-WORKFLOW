package engineering.readiness_test

import rego.v1
import data.engineering.readiness

base_input := {
  "scorecard": {
    "readiness_threshold": 9.0,
    "world_class_ready": false,
    "domains": [
      {
        "id": "security",
        "applicable": true,
        "score": 5.0,
        "evidence_maturity": "DESIGNED",
        "blocking_gaps": ["GAP-SEC-001"],
      },
    ],
  },
  "gap_register": {
    "gaps": [
      {
        "id": "GAP-SEC-001",
        "priority": "P0",
        "status": "OPEN",
      },
    ],
  },
  "toolchain": {
    "policy": {
      "floating_versions_allowed": false,
      "unverified_binary_execution_allowed": false,
      "curl_pipe_shell_allowed": false,
      "tool_failure_mode": "fail-closed-or-blocked",
      "native_validator_required": true,
    },
  },
}

test_gap_closure_state_is_valid if {
  count(readiness.deny with input as base_input) == 0
}

test_false_world_class_claim_is_denied if {
  changed_scorecard := object.union(base_input.scorecard, {"world_class_ready": true})
  changed_input := object.union(base_input, {"scorecard": changed_scorecard})
  violations := readiness.deny with input as changed_input
  count(violations) == 2
}

test_score_above_maturity_cap_is_denied if {
  changed_domain := object.union(base_input.scorecard.domains[0], {"score": 6.0})
  changed_scorecard := object.union(base_input.scorecard, {"domains": [changed_domain]})
  changed_input := object.union(base_input, {"scorecard": changed_scorecard})
  violations := readiness.deny with input as changed_input
  count(violations) == 1
}

test_unknown_gap_is_denied if {
  changed_domain := object.union(base_input.scorecard.domains[0], {"blocking_gaps": ["GAP-UNKNOWN"]})
  changed_scorecard := object.union(base_input.scorecard, {"domains": [changed_domain]})
  changed_input := object.union(base_input, {"scorecard": changed_scorecard})
  violations := readiness.deny with input as changed_input
  count(violations) == 1
}

test_unverified_tool_execution_is_denied if {
  changed_policy := object.union(base_input.toolchain.policy, {"unverified_binary_execution_allowed": true})
  changed_toolchain := object.union(base_input.toolchain, {"policy": changed_policy})
  changed_input := object.union(base_input, {"toolchain": changed_toolchain})
  violations := readiness.deny with input as changed_input
  count(violations) == 1
}
