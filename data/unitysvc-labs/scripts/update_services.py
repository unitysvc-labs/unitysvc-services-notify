#!/usr/bin/env python3
"""
Populate notification services for unitysvc-labs.

Reads the static channel catalog in channels.py and generates 2-4
offering.json + listing.json pairs per channel under data/unitysvc-labs/services/.

Service types generated
-----------------------
{channel}-relay          free, customer stores webhook URL as fixed-name secret
{channel}-relay-multi    $0.001/use, customer provides webhook URL via params+secrets
msg-to-{channel}         free, SMTP->upstream transformer (has_transformer channels only)
msg-to-{channel}-multi   $0.001/use, transformer, customer provides creds at enrollment

Usage
-----
    python3 data/unitysvc-labs/scripts/update_services.py [--dry-run]
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterator

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent

sys.path.insert(0, str(SCRIPT_DIR))
from channels import ALL_CHANNELS, BODY_TYPE_TEMPLATES  # noqa: E402

try:
    from unitysvc_sellers.template_populate import populate_from_iterator
except ImportError:
    print("ERROR: unitysvc_sellers not installed.  Run:")
    print("  uv pip install -e /path/to/unitysvc-sellers")
    sys.exit(1)

DRY_RUN = "--dry-run" in sys.argv

TEMPLATES_DIR = DATA_DIR / "templates"
SERVICES_DIR = DATA_DIR / "services"

TIME_CREATED = "2026-06-01T00:00:00Z"

# -- Iterators -----------------------------------------------------------------


def _relay_vars(ch: dict, *, multi: bool) -> dict:
    """Template variables for a relay service (fixed or multi-enrollment)."""
    suffix = "-relay-multi" if multi else "-relay"
    cid = ch["channel_id"].upper().replace("-", "_")
    secret_env = f"{cid}_WEBHOOK_URL"

    # ops_testing_parameters: for multi, supply the default secret name so the
    # ops test framework knows which customer secret to look up.
    ops_testing_params: dict = {}
    if multi:
        ops_testing_params["webhook_url_secret"] = secret_env

    return {
        "name": f"{ch['channel_id']}{suffix}",
        "channel_id": ch["channel_id"],
        "channel_display": ch["display"],
        "tier": ch["tier"],
        "body_type": ch["body_type"],
        "tags": sorted({"notification", "relay", ch["channel_id"]} | set(ch["tags"])),
        "multi": multi,
        "secret_env": secret_env,
        "webhook_path": ch.get("webhook_path", ""),
        "ops_testing_params": ops_testing_params,
        "time_created": TIME_CREATED,
        # Pricing
        "price": "0.001" if multi else "0",
        "price_description": (
            "$0.001 per notification sent"
            if multi
            else "Free — webhook URL stored as customer secret"
        ),
    }


def _transformer_vars(ch: dict, *, multi: bool) -> dict:
    """Template variables for a transformer service (SMTP->upstream)."""
    suffix = "-multi" if multi else ""
    cid = ch["channel_id"].upper().replace("-", "_")
    secret_env = f"{cid}_WEBHOOK_URL"
    body_type = ch["body_type"]
    fixed_base_url = ch.get("fixed_base_url") or ""
    credential_params: list[dict] = ch.get("credential_params", [])

    # For multi variants, use the _multi body type template when it exists.
    # This selects e.g. "pushover_multi" over "pushover" for the multi service,
    # which uses customer_secrets/params instead of service_secrets.
    if multi:
        multi_key = f"{body_type}_multi"
        lua_template = BODY_TYPE_TEMPLATES.get(
            multi_key, BODY_TYPE_TEMPLATES.get(body_type, BODY_TYPE_TEMPLATES["json"])
        )
    else:
        lua_template = BODY_TYPE_TEMPLATES.get(body_type, BODY_TYPE_TEMPLATES["json"])

    # Build ops_testing_parameters for multi services.
    # For webhook-style channels (no fixed_base_url): supply default secret names
    # for base URL and path, matching the naming convention used elsewhere.
    # For fixed-URL channels (fixed_base_url set): only supply credential param
    # defaults (and chat_id if applicable).
    ops_testing_params: dict = {}
    if multi:
        if not fixed_base_url:
            ops_testing_params["webhook_base_url_secret"] = f"{cid}_WEBHOOK_BASE_URL"
            ops_testing_params["webhook_path_secret"] = f"{cid}_WEBHOOK_PATH"
        for cp in credential_params:
            ops_testing_params[cp["param"]] = cp["default_secret"]

    return {
        "name": f"msg-to-{ch['channel_id']}{suffix}",
        "channel_id": ch["channel_id"],
        "channel_display": ch["display"],
        "tier": ch["tier"],
        "body_type": body_type,
        "lua_template": lua_template,
        "tags": sorted(
            {"notification", "transformer", "smtp", ch["channel_id"]}
            | set(ch["tags"])
        ),
        "multi": multi,
        "secret_env": secret_env,
        "webhook_path": ch.get("webhook_path", ""),
        "auth_header": ch.get("auth_header"),
        "fixed_base_url": fixed_base_url,
        "credential_params": credential_params,
        "ops_testing_params": ops_testing_params,
        "time_created": TIME_CREATED,
        # Pricing
        "price": "0.001" if multi else "0",
        "price_description": (
            "$0.001 per notification sent"
            if multi
            else "Free — webhook URL pre-configured"
        ),
    }


def relay_fixed_iter() -> Iterator[dict]:
    for ch in ALL_CHANNELS:
        yield _relay_vars(ch, multi=False)


def relay_multi_iter() -> Iterator[dict]:
    for ch in ALL_CHANNELS:
        yield _relay_vars(ch, multi=True)


def transformer_fixed_iter() -> Iterator[dict]:
    for ch in ALL_CHANNELS:
        if ch["has_transformer"]:
            yield _transformer_vars(ch, multi=False)


def transformer_multi_iter() -> Iterator[dict]:
    for ch in ALL_CHANNELS:
        if ch["has_transformer"]:
            yield _transformer_vars(ch, multi=True)


# -- Main ----------------------------------------------------------------------

def main() -> None:
    total_written = 0

    runs = [
        ("relay-fixed", relay_fixed_iter()),
        ("relay-multi", relay_multi_iter()),
        ("transformer-fixed", transformer_fixed_iter()),
        ("transformer-multi", transformer_multi_iter()),
    ]

    for template_subdir, iterator in runs:
        templates_dir = TEMPLATES_DIR / template_subdir
        if not templates_dir.exists():
            print(f"SKIP {template_subdir}: templates dir not found at {templates_dir}")
            continue

        print(f"\n-- {template_subdir} --")
        stats = populate_from_iterator(
            iterator=iterator,
            templates_dir=templates_dir,
            output_dir=SERVICES_DIR,
            deprecate_missing=False,  # each run manages its own subset
            dry_run=DRY_RUN,
        )
        print(
            f"  written={stats['written']} skipped={stats['skipped']} "
            f"errors={stats['errors']}"
        )
        total_written += stats["written"]

    print(f"\nTotal services written: {total_written}")
    if DRY_RUN:
        print("(dry-run -- no files written)")


if __name__ == "__main__":
    main()
