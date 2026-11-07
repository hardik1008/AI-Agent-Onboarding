import sqlite3
from datetime import datetime
from database import get_connection

INDIAN_REGION_MAP = {
    # North
    "Delhi": "North", "Punjab": "North", "Haryana": "North", "Uttar Pradesh": "North",
    "Himachal Pradesh": "North", "Uttarakhand": "North", "Chandigarh": "North",
    "Jammu and Kashmir": "North", "Ladakh": "North", "Rajasthan": "North",
    # West
    "Maharashtra": "West", "Gujarat": "West", "Goa": "West", "Madhya Pradesh": "West",
    "Daman and Diu": "West", "Dadra and Nagar Haveli": "West",
    # South
    "Karnataka": "South", "Tamil Nadu": "South", "Telangana": "South",
    "Andhra Pradesh": "South", "Kerala": "South", "Puducherry": "South",
    # East
    "West Bengal": "East", "Bihar": "East", "Odisha": "East", "Jharkhand": "East",
    "Assam": "East", "Sikkim": "East", "Meghalaya": "East", "Tripura": "East",
    "Mizoram": "East", "Manipur": "East", "Nagaland": "East", "Arunachal Pradesh": "East"
}

def get_region_from_state(state: str) -> str:
    if not state:
        return "North"
    for s_name, reg in INDIAN_REGION_MAP.items():
        if s_name.lower() in state.lower():
            return reg
    return "North"

def evaluate_abac_policy(subject: dict, resource: dict, action: str, environment: dict = None) -> dict:
    """
    NIST SP 800-162 Standard Attribute-Based Access Control PDP (Policy Decision Point)
    Evaluates:
      Subject Attributes: role, id, region, clearance_level, shift_hours
      Resource Attributes: id, state, region, is_hard_case, risk_score, owner_id
      Action: 'view_analytics', 'view_ops', 'review_case', 'approve_case', 'reject_case', 'read_case'
      Environment: current_time, ip_address
    """
    if environment is None:
        environment = {}

    role = subject.get("role", "APPLICANT")
    sub_region = subject.get("assigned_region", "North")
    clearance = int(subject.get("clearance_level", 1) or 1)
    sub_id = subject.get("mobile") or subject.get("id", "ANONYMOUS")

    res_id = resource.get("application_id") or resource.get("id", "RESOURCE")
    res_state = resource.get("state") or resource.get("declared_state", "")
    res_region = resource.get("region") or get_region_from_state(res_state)
    is_hard_case = bool(resource.get("is_hard_case", False))
    risk_score = float(resource.get("risk_score", 0.0) or 0.0)
    owner_id = resource.get("owner_id") or resource.get("mobile")

    timestamp = datetime.now().isoformat()

    decision = "DENY"
    policy_matched = "DEFAULT_DENY"
    reason = "No matching permit policy rule."

    # RULE 0: SUPER_ADMIN Overriding Privilege
    if role == "SUPER_ADMIN":
        decision = "PERMIT"
        policy_matched = "POLICY_ABAC_0_SUPER_ADMIN_OVERRIDE"
        reason = "Super Admin executive clearance (Clearance Level 3) allows global cross-regional audit and administration."
        log_abac_decision(sub_id, role, sub_region, res_id, res_state, action, decision, policy_matched, reason, timestamp)
        return {"decision": decision, "policy_matched": policy_matched, "reason": reason, "timestamp": timestamp}

    # RULE 1: APPLICANT Role Boundary & Tenant Isolation
    if role == "APPLICANT":
        if action in ["view_analytics", "view_ops", "review_case", "approve_case", "reject_case", "retrain_ai"]:
            decision = "DENY"
            policy_matched = "POLICY_ABAC_1_APPLICANT_INTERNAL_ISOLATION"
            reason = f"Applicants cannot perform administrative or operational action '{action}'."
        elif action in ["read_case", "submit_case", "update_case"]:
            if owner_id and sub_id and owner_id != sub_id:
                decision = "DENY"
                policy_matched = "POLICY_ABAC_1_TENANT_ISOLATION_VIOLATION"
                reason = "Cross-tenant data access violation: applicant cannot view other candidates' records."
            else:
                decision = "PERMIT"
                policy_matched = "POLICY_ABAC_1_APPLICANT_SELF_SERVICE"
                reason = "Applicant permitted to access own onboarding application."
        else:
            decision = "DENY"
            policy_matched = "POLICY_ABAC_1_APPLICANT_UNAUTHORIZED_ACTION"
            reason = f"Unauthorized action '{action}' for applicant role."
            
        log_abac_decision(sub_id, role, sub_region, res_id, res_state, action, decision, policy_matched, reason, timestamp)
        return {"decision": decision, "policy_matched": policy_matched, "reason": reason, "timestamp": timestamp}

    # OPS_REVIEWER checks
    if role in ["OPS_REVIEWER", "EXECUTIVE"]:
        # Action: Analytics Command Center
        if action == "view_analytics":
            if role == "EXECUTIVE" or clearance >= 2:
                decision = "PERMIT"
                policy_matched = "POLICY_ABAC_ANALYTICS_EXECUTIVE_CLEARANCE"
                reason = "Senior Reviewer/Executive granted read-only telemetry dashboard access."
            else:
                decision = "DENY"
                policy_matched = "POLICY_ABAC_ANALYTICS_INSUFFICIENT_CLEARANCE"
                reason = "Analytics Command Center requires Senior Clearance (Level 2+) or Super Admin."
            log_abac_decision(sub_id, role, sub_region, res_id, res_state, action, decision, policy_matched, reason, timestamp)
            return {"decision": decision, "policy_matched": policy_matched, "reason": reason, "timestamp": timestamp}

        # Action: View Ops Cockpit
        if action == "view_ops":
            decision = "PERMIT"
            policy_matched = "POLICY_ABAC_OPS_COCKPIT_ACCESS"
            reason = "Operational workforce permitted to access review queue."
            log_abac_decision(sub_id, role, sub_region, res_id, res_state, action, decision, policy_matched, reason, timestamp)
            return {"decision": decision, "policy_matched": policy_matched, "reason": reason, "timestamp": timestamp}

        # Action: Reviewing or Approving an Application
        if action in ["review_case", "approve_case", "reject_case", "read_case"]:
            # RULE 2: Regional Ops Jurisdiction
            if sub_region != "ALL" and res_region and sub_region.lower() != res_region.lower():
                decision = "DENY"
                policy_matched = "POLICY_ABAC_2_REGIONAL_JURISDICTION_MISMATCH"
                reason = f"Regional Jurisdiction Violation: Reviewer assigned to {sub_region} region cannot adjudicate cases originating from {res_region} ({res_state or 'Unknown'})."
                log_abac_decision(sub_id, role, sub_region, res_id, res_state, action, decision, policy_matched, reason, timestamp)
                return {"decision": decision, "policy_matched": policy_matched, "reason": reason, "timestamp": timestamp}

            # RULE 3: Clearance Level Escalation for Hard/High-Risk Cases
            if (is_hard_case or risk_score > 70.0) and clearance < 2:
                decision = "DENY"
                policy_matched = "POLICY_ABAC_3_INSUFFICIENT_CLEARANCE_FOR_HARD_CASE"
                reason = f"Clearance Escalation Required: Application marked as High Risk / Hard Case (Score: {risk_score:.1f}) requires Senior Reviewer (Clearance Level 2+) approval."
                log_abac_decision(sub_id, role, sub_region, res_id, res_state, action, decision, policy_matched, reason, timestamp)
                return {"decision": decision, "policy_matched": policy_matched, "reason": reason, "timestamp": timestamp}

            # If passed regional and clearance checks:
            decision = "PERMIT"
            policy_matched = "POLICY_ABAC_4_OPS_AUTHORIZATION_PASSED"
            reason = f"Authorized: Reviewer {sub_id} ({sub_region}, Level {clearance}) meets jurisdiction and risk criteria for application {res_id}."
            log_abac_decision(sub_id, role, sub_region, res_id, res_state, action, decision, policy_matched, reason, timestamp)
            return {"decision": decision, "policy_matched": policy_matched, "reason": reason, "timestamp": timestamp}

    log_abac_decision(sub_id, role, sub_region, res_id, res_state, action, decision, policy_matched, reason, timestamp)
    return {"decision": decision, "policy_matched": policy_matched, "reason": reason, "timestamp": timestamp}

def log_abac_decision(sub_id, role, sub_region, res_id, res_state, action, decision, policy_matched, reason, timestamp):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute('''
        INSERT INTO abac_access_logs (
            subject_id, subject_role, subject_region, resource_id, resource_state,
            action, decision, policy_matched, reason, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (str(sub_id), str(role), str(sub_region), str(res_id), str(res_state), str(action), str(decision), str(policy_matched), str(reason), str(timestamp)))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"ABAC Log write error: {e}")
