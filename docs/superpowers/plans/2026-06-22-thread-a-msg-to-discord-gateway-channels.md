# Thread A — `msg-to-discord` gateway (transformer) channels — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add two new channels to `msg-to-discord` — `gateway` (byok) and `gateway-plus` (enrollable) — that transform the canonical `{title,body,type,format}` envelope into a Discord webhook embed in the gateway and POST it to `discord.com` directly, bypassing Apprise; selectable via `@gateway` / `@gateway-plus`, default stays Apprise.

**Architecture:** The `msg-to-channel` template is shared across ~95 channels, so the Discord transform is emitted **conditionally** (only when a spec supplies `gateway_url`/`gateway_template`). Selection/billing already work today; ordering is expressed with per-channel `sort_order` (1=apprise, 2=apprise-plus, 3=gateway, 4=gateway-plus). Channel-specific connectivity/code-example **presets** are added in `unitysvc-data`. No backend change (that is Thread B).

**Tech Stack:** Jinja2 templates (`unitysvc-services-notify`), resty.template gateway `body_transformer`, `unitysvc-data` doc presets, `usvc_seller` CLI verification pipeline.

**Reference:** dev note `unitysvc/docs/dev-notes/features/channel-selection-routing.md` (PR unitysvc#1363).

**Pre-req for every CLI step:** `source ~/.zshrc` (or `zsh -ic '...'`) so `UNITYSVC_SELLER_API_KEY` / `UNITYSVC_SELLER_API_URL` / `UNITYSVC_API_KEY` are set; activate `~/unitysvc/.venv` for the Python data-test runner.

---

## File structure

- Modify `templates/msg-to-channel/offering.json.j2` — add `sort_order` to `apprise`/`apprise-plus`; conditionally add `gateway`/`gateway-plus` channels with `body_transformer` + `proxy_rewrite`.
- Modify `templates/msg-to-channel/listing.json.j2` — conditionally add `gateway`/`gateway-plus` to `list_price.channels`; add per-channel connectivity + code-example docs (tagged `meta.channels`).
- Modify `specs/labs/msg-to-discord.json` — supply `gateway_url`, `gateway_url_plus`, `gateway_body_template`, pricing descriptions, `sort_order`s, and `ops_testing_parameters` for the Discord mock.
- Create in `unitysvc-data`: `examples/msg-to-gateway/connectivity/connectivity-v1.sh.j2`, `examples/msg-to-gateway/code-example-py/code-example-v1.py.j2`, and manifest entries `msg_to_gateway_connectivity` / `msg_to_gateway_code_example_py`.
- Verify with the `usvc_seller` pipeline.

Other `msg-to-*` specs omit the `gateway_*` params, so the conditional emits nothing for them — they are unaffected.

---

## Task 1: `unitysvc-data` — gateway connectivity preset

**Files:**
- Create: `unitysvc-data/src/unitysvc_data/examples/msg-to-gateway/connectivity/connectivity-v1.sh.j2`
- Modify: `unitysvc-data/src/unitysvc_data/_manifest.json` (register `msg_to_gateway_connectivity` with params `native_body`, `channel`, `local_url`)

- [ ] **Step 1: Inspect the existing apprise preset + manifest shape**

Run: `sed -n '1,60p' unitysvc-data/src/unitysvc_data/examples/msg-to-apprise/connectivity/connectivity-v1.sh.j2` and `python3 -c "import json,sys;d=json.load(open('unitysvc-data/src/unitysvc_data/_manifest.json'));print(json.dumps([k for k in d],indent=2)[:800])"`
Expected: see the `local_testing` branch + how `msg_to_apprise_connectivity` and its `parameters` are registered.

- [ ] **Step 2: Write the gateway connectivity probe**

Create `connectivity-v1.sh.j2`:
```bash
#!/bin/bash
# Connectivity test for a UnitySVC gateway transformer channel (e.g. Discord).
#   local_testing : POST the channel-NATIVE body straight to the mock upstream.
#   gateway       : POST the canonical envelope to ${service_base_url}@{{ channel }};
#                   the gateway transforms it to the native body and forwards (Bearer auth).
set -o pipefail
{% if local_testing %}
URL="${__local_url__}"
BODY='${__native_body__}'
status=$(curl -sS --max-time 10 -X POST -H "Content-Type: application/json" \
    -d "$BODY" -o /dev/null -w "%{http_code}" "$URL" 2>/dev/null)
{% else %}
URL="{{ service_base_url }}@{{ channel }}"
status=$(curl -sS --max-time 10 -X POST -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${UNITYSVC_API_KEY}" \
    -d '{"title":"connectivity check","body":"ping","type":"info","format":"text"}' \
    -o /dev/null -w "%{http_code}" "$URL" 2>/dev/null)
{% endif %}
case "$status" in
  2??) echo "connectivity ok (HTTP $status)"; exit 0 ;;
  000) echo "connectivity failed: could not connect to $URL" >&2; exit 1 ;;
  *)   echo "connectivity failed: HTTP $status from $URL" >&2; exit 1 ;;
esac
```
(`${__native_body__}` / `${__local_url__}` are preset param substitutions, matching how `msg-to-apprise` uses `${__apprise_url__}`.)

- [ ] **Step 3: Register the preset in `_manifest.json`**

Add an entry mirroring `msg_to_apprise_connectivity` (category `connectivity_test`, mime `bash`, `file` pointing at the new example) with `"parameters": {"native_body": "", "channel": "gateway", "local_url": ""}`.

- [ ] **Step 4: Verify the preset loads**

Run: `cd unitysvc-data && python3 -c "from unitysvc_data.presets import list_presets; n,_=list_presets(); assert 'msg_to_gateway_connectivity' in n, n; print('ok')"`
Expected: `ok`

- [ ] **Step 5: Commit**

```bash
cd unitysvc-data && git add src/unitysvc_data/examples/msg-to-gateway/connectivity src/unitysvc_data/_manifest.json && \
git commit -m "feat(presets): add msg_to_gateway_connectivity for gateway transformer channels"
```

## Task 2: `unitysvc-data` — gateway Python code-example preset

**Files:**
- Create: `unitysvc-data/src/unitysvc_data/examples/msg-to-gateway/code-example-py/code-example-v1.py.j2`
- Modify: `_manifest.json` (register `msg_to_gateway_code_example_py`, params `channel`)

- [ ] **Step 1: Copy the apprise code-example as the base**

Run: `cat unitysvc-data/src/unitysvc_data/examples/msg-to-apprise/code-example-py/code-example-v1.py.j2`
Expected: a Python example POSTing the envelope to `service_base_url` with the svcpass key.

- [ ] **Step 2: Adapt it to target `@{{ channel }}`**

Create `code-example-v1.py.j2` identical to the apprise one except the request URL is `f"{BASE_URL}@{{ channel }}"` so the example exercises the transformer channel. Keep the canonical envelope body.

- [ ] **Step 3: Register `msg_to_gateway_code_example_py` in `_manifest.json`** (category `code_example`, mime `python`, `"parameters": {"channel": "gateway"}`).

- [ ] **Step 4: Verify it loads** — `python3 -c "from unitysvc_data.presets import list_presets; n,_=list_presets(); assert 'msg_to_gateway_code_example_py' in n; print('ok')"` → `ok`

- [ ] **Step 5: Commit** — `git add ... && git commit -m "feat(presets): add msg_to_gateway_code_example_py"`

> If the notify repo pins a released `unitysvc-data`, bump/point it at this working copy (editable install in `~/unitysvc/.venv`) before Task 7.

## Task 3: notify — add `sort_order` to the existing channels

**Files:** Modify `templates/msg-to-channel/offering.json.j2`

- [ ] **Step 1:** In the `apprise` channel object add `"sort_order": 1,` and in `apprise-plus` add `"sort_order": 2,` (alongside `access_method`). These are inert until Thread B but record intent.

- [ ] **Step 2: Commit** — `git add templates/msg-to-channel/offering.json.j2 && git commit -m "chore(msg-to-channel): record channel sort_order (apprise=1, apprise-plus=2)"`

## Task 4: notify — conditionally add `gateway` / `gateway-plus` channels

**Files:** Modify `templates/msg-to-channel/offering.json.j2`

- [ ] **Step 1: Add the conditional channels** after `apprise-plus`, guarded so only specs that define `gateway_url` emit them:

```jinja
{%- if gateway_url is defined %}
    ,"gateway": {
      "access_method": "http",
      "sort_order": 3,
      "base_url": {{ gateway_url | tojson }},
      "raw": {
        "request_transformer": {
          "body_transformer": { "request": { "input_format": "json", "template": {{ gateway_body_template | tojson }} } },
          "proxy_rewrite": { "headers": { "set": { "Content-Type": "application/json" } } }
        }
      }
    },
    "gateway-plus": {
      "access_method": "http",
      "sort_order": 4,
      "base_url": {{ gateway_url_plus | tojson }},
      "raw": {
        "request_transformer": {
          "body_transformer": { "request": { "input_format": "json", "template": {{ gateway_body_template | tojson }} } },
          "proxy_rewrite": { "headers": { "set": { "Content-Type": "application/json" } } }
        }
      }
    }
{%- endif %}
```
Note: `gateway_body_template` is a resty.template string (`{* ... *}`); `| tojson` embeds it safely. `{* %}` is not Jinja2 syntax so it passes through untouched.

- [ ] **Step 2: Verify Jinja renders for a non-gateway spec (no gateway channels emitted)**

Run: `usvc_seller specs populate` then `python3 -c "import json;d=json.load(open('expanded/labs/msg-to-slack/offering.json'));print(list(d['upstream_access_config']))"` (any non-discord channel)
Expected: `['apprise', 'apprise-plus']` — gateway channels absent.

- [ ] **Step 3: Commit** — `git commit -am "feat(msg-to-channel): conditional gateway/gateway-plus transformer channels"`

## Task 5: notify — pricing + per-channel docs

**Files:** Modify `templates/msg-to-channel/listing.json.j2`

- [ ] **Step 1: Conditionally add `gateway`/`gateway-plus` to `list_price.channels`**, guarded by `{% if gateway_url is defined %}`, prices defaulting to the apprise pair:

```jinja
{%- if gateway_url is defined %}
,"gateway": { "description": {{ gateway_price_description | default('Free — direct to your Discord webhook (no Apprise)') | tojson }}, "price": "0", "type": "constant" }
,"gateway-plus": { "description": {{ gateway_plus_price_description | default('$0.001 per message — extra per-enrollment destinations, direct') | tojson }}, "price": "{{ plus_price | default('0.001') }}", "type": "constant" }
{%- endif %}
```

- [ ] **Step 2: Add gateway connectivity + code-example docs (conditional), tagged with `meta.channels`:**

```jinja
{%- if gateway_url is defined %}
,"Connectivity test (gateway)": { "$doc_preset": { "name": "msg_to_gateway_connectivity", "native_body": "{{ gateway_test_body }}", "local_url": "{{ gateway_test_local_url }}", "channel": "gateway" }, "meta": { "channels": ["gateway"] } }
,"Python code example (gateway)": { "$doc_preset": { "name": "msg_to_gateway_code_example_py", "channel": "gateway" }, "meta": { "channels": ["gateway"] } }
{%- endif %}
```
Also add `"meta": { "channels": ["apprise"] }` to the existing two apprise docs so every example declares its channel.

- [ ] **Step 3: Commit** — `git commit -am "feat(msg-to-channel): gateway channel pricing + per-channel docs with meta.channels"`

## Task 6: notify — `msg-to-discord` spec params

**Files:** Modify `specs/labs/msg-to-discord.json`

- [ ] **Step 1: Add the gateway params** to the spec's `parameters` block:

```json
"gateway_url": "${ customer_secrets.DISCORD_WEBHOOK_BASE ?? https://discord.com/api/webhooks }/${ customer_secrets.DISCORD_WEBHOOK_ID }/${ customer_secrets.DISCORD_WEBHOOK_TOKEN }",
"gateway_url_plus": "${ customer_secrets.DISCORD_WEBHOOK_BASE ?? https://discord.com/api/webhooks }/${ customer_secrets.{{ params.webhook_id_secret }} }/${ customer_secrets.{{ params.webhook_token_secret }} }",
"gateway_body_template": "{\"embeds\":[{\"title\":{* _escape_json(_body.title or \"\") *},\"description\":{* _escape_json(_body.body or \"\") *},\"color\":{* ({info=3447003,success=3066993,warning=16776960,failure=15158332})[_body.type or \"info\"] or 3447003 *}}]}",
"gateway_test_body": "{\"embeds\":[{\"title\":\"connectivity check\",\"description\":\"ping\"}]}",
"gateway_test_local_url": "https://mock.unitysvc.dev/discord/api/webhooks/demo/demotoken"
```
Keep `ops_testing_parameters` such that the synthetic enrollment resolves the same `DISCORD_WEBHOOK_ID/TOKEN` for `gateway-plus` (same secrets as `apprise-plus`).

- [ ] **Step 2: Commit** — `git commit -am "feat(msg-to-discord): add gateway transformer channel params"`

## Task 7: Regenerate + validate + format

- [ ] **Step 1:** `usvc_seller specs populate` (regenerate `expanded/labs/msg-to-discord/`)
- [ ] **Step 2:** Verify four channels — `python3 -c "import json;d=json.load(open('expanded/labs/msg-to-discord/offering.json'));print(list(d['upstream_access_config']))"` → expect `['apprise','apprise-plus','gateway','gateway-plus']`
- [ ] **Step 3:** `usvc_seller data validate` → expect no errors (channels are `extra="allow"`, so `sort_order`/transform pass)
- [ ] **Step 4:** `usvc_seller data format`
- [ ] **Step 5: Commit** — `git commit -am "chore: regenerate + format msg-to-discord with gateway channels"`

## Task 8: Upstream tests (`data run-tests`)

- [ ] **Step 1:** `usvc_seller data run-tests 'labs/msg-to-discord'`
- [ ] **Step 2:** Expected: the `gateway` connectivity probe in `local_testing` mode POSTs the Discord-format body to `https://mock.unitysvc.dev/discord/api/webhooks/demo/demotoken` and returns 2xx ("connectivity ok"); apprise probes still pass. (Python example `ModuleNotFoundError: requests` is environmental — ensure `~/unitysvc/.venv` active.)

## Task 9: Upload to staging

- [ ] **Step 1:** `usvc_seller data upload 'labs/msg-to-discord'`
- [ ] **Step 2:** If it errors `Customer secret 'DISCORD_WEBHOOK_ID' … requires a seller secret`, seed: `usvc_seller secrets set DISCORD_WEBHOOK_ID --value <v>` (and `_TOKEN`) then re-upload. Commit the updated `listing.override.json`.

## Task 10: Gateway tests (`services run-tests`) — proves transform + `@channel`

- [ ] **Step 1:** `usvc_seller services run-tests 'labs/msg-to-discord' --force` (add `--id <prefix>` if the name matches >1 row)
- [ ] **Step 2:** Expected: the `gateway` probe in gateway mode POSTs the envelope to `${SERVICE_BASE_URL}@gateway`; the gateway renders the Discord embed and delivers to the mock → 2xx. Apprise channel still served by default (no `@channel`).
- [ ] **Step 3:** Manual spot-check default selection is unchanged:
```bash
zsh -ic 'source ~/.zshrc && curl -sS -o /dev/null -w "%{http_code}\n" -X POST "$UNITYSVC_API_GATEWAY/labs/msg-to-discord" -H "Authorization: Bearer $UNITYSVC_API_KEY" -H "Content-Type: application/json" -d "{\"title\":\"t\",\"body\":\"b\"}"'
```
Expected: 2xx via the default `apprise` channel.

- [ ] **Step 4: Final commit** if any override/data changed — `git commit -am "test: msg-to-discord gateway channel green through gateway"`

## Done criteria

All four gates green: `data validate`, `data format`, `data run-tests` (gateway probe local mode hits mock), `services run-tests --force` (gateway probe via `@gateway` delivers). `@gateway` selectable; default still `apprise`. Publishing (`set-visibility` / `submit`) is a separate, explicit step — not part of this plan.
