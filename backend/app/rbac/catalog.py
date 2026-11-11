"""Canonical role and permission catalog. Migration 0001 seeds this exact data; a test keeps them in sync."""

from enum import Enum


class RoleCode(str, Enum):
    APPLICANT = "APPLICANT"
    REVIEWER = "REVIEWER"
    SENIOR_REVIEWER = "SENIOR_REVIEWER"
    ADMIN = "ADMIN"


ROLES: dict[RoleCode, tuple[str, str, bool]] = {
    RoleCode.APPLICANT: ("Applicant", "POSP candidate completing onboarding.", False),
    RoleCode.REVIEWER: ("Reviewer", "Onboarding Ops verification officer.", True),
    RoleCode.SENIOR_REVIEWER: (
        "Senior Reviewer",
        "Handles escalations, human-only decisions and fraud desk referrals.",
        True,
    ),
    RoleCode.ADMIN: ("Administrator", "Manages users, roles, configuration and audit.", True),
}

PERMISSIONS: dict[str, tuple[str, str]] = {
    "profile:read": ("profile", "View own profile and sessions."),
    "profile:update": ("profile", "Update own profile, password and sessions."),
    "application:create": ("application", "Create and edit own onboarding application."),
    "application:read_own": ("application", "View own onboarding application."),
    "application:read_any": ("application", "View any onboarding application (subject to ABAC)."),
    "application:review": ("application", "Work the review queue and request corrections."),
    "application:decide": ("application", "Approve or reject standard applications."),
    "application:escalate": ("application", "Escalate applications to senior review or fraud desk."),
    "application:decide_escalated": ("application", "Decide escalated and human-only cases."),
    "fraud:review": ("application", "Work fraud desk referrals."),
    "analytics:read": ("operations", "View operational analytics."),
    "users:read": ("admin", "View user accounts."),
    "users:manage": ("admin", "Invite users, change roles, activate or deactivate accounts."),
    "roles:read": ("admin", "View roles and permissions."),
    "audit:read": ("admin", "View the audit log."),
    "system:read": ("admin", "View system health and integration status."),
    "config:manage": ("admin", "Change platform configuration."),
}

_PROFILE = ["profile:read", "profile:update"]
_REVIEWER = _PROFILE + [
    "application:read_any",
    "application:review",
    "application:decide",
    "application:escalate",
]

ROLE_PERMISSIONS: dict[RoleCode, list[str]] = {
    RoleCode.APPLICANT: _PROFILE + ["application:create", "application:read_own"],
    RoleCode.REVIEWER: _REVIEWER,
    RoleCode.SENIOR_REVIEWER: _REVIEWER + ["application:decide_escalated", "fraud:review", "analytics:read"],
    # Separation of duties: administrators manage the platform but do not decide applications.
    RoleCode.ADMIN: _PROFILE
    + [
        "application:read_any",
        "analytics:read",
        "users:read",
        "users:manage",
        "roles:read",
        "audit:read",
        "system:read",
        "config:manage",
    ],
}

PERMISSIONS_ALLOWED_UNVERIFIED = {"profile:read", "profile:update"}

REGIONS = ["NORTH", "SOUTH", "EAST", "WEST", "ALL"]
