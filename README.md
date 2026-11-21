# UnitySVC Labs notification services

Notification delivery and incoming-message integrations published by UnitySVC Labs. Service parameters are under `services/specs/`, with shared definitions under `services/templates/`.

The ntfy services now live in [unitysvc-compute-services](https://github.com/unitysvc-labs/unitysvc-compute-services):

- `binwiederhier/ntfy-sh`: private ntfy instances on the compute cluster.
- `labs/msg-to-ntfy`: gateway delivery to ntfy.sh or another ntfy destination.

The moved service keeps its existing marketplace name and service ID. Add compute services and ntfy changes to the compute catalog.

Run `usvc_seller specs validate`, `usvc_seller specs format --check services` and `python scripts/check_channel_binding.py` from this repository root before uploading the notification catalog.
