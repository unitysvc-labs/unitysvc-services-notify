# UnitySVC Labs notification services

Notification delivery and incoming-message integrations published by UnitySVC Labs. Service parameters are under `services/specs/`, with shared definitions under `services/templates/`.

The container-backed compute services live in [unitysvc-compute-services](https://github.com/unitysvc-labs/unitysvc-compute-services):

- `binwiederhier/ntfy-sh`: private ntfy instances on the compute cluster.
- `kadxy/weixin-ilink-gateway`: private Weixin iLink gateways on the compute cluster.

The moved Weixin gateway keeps its existing marketplace name and service ID. Add future compute services to the compute catalog. Notification integrations, including `labs/msg-to-ntfy`, `labs/msg-to-weixin` and `labs/weixin-to-msg`, remain here.

Run `usvc_seller specs validate`, `usvc_seller specs format --check services` and `python scripts/check_channel_binding.py` from this repository root before uploading the notification catalog.
