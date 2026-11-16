# WeChat iLink Gateway

Each enrollment runs a separate [Kadxy weixin-ilink-gateway](https://github.com/Kadxy/weixin-ilink-gateway) instance. The provider is Kadxy; UnitySVC Labs operates this prototype.

1. Enroll in **base** and approve `resource:container` creation.
2. Wait for the instance to become ready. Its address is `https://<enrollment-code>.staging.unitysvc.app` on staging (HTTPS port 443).
3. Obtain the separate, platform-generated instance API key from the enrollment's instance details. This is an application key, not your UnitySVC API key.
4. Open `/console`, enter the instance key, and start QR login. Scan the QR code with the WeChat account you want the bot to use.
5. Call `/status`, `/messages/updates`, `/messages/send`, and the media endpoints using `Authorization: Bearer <instance-api-key>`.

The upstream requires a cached context token before sending to a user: send a message from that user to the bot first. See the upstream README for the full API and webhook configuration.

## Storage

Storage is temporary. Stopping, replacing, or deleting the instance loses WeChat login state, sync cursors, and cached messages; scan the QR code again after replacement. No persistent volume is promised.

The console is publicly reachable, while the REST API requires the instance key; keep that key private.

For manual local Compose use, set `UNITYSVC_INSTANCE_API_KEY` to a fresh random token of at least 12 characters before starting. UnitySVC binds this reserved variable independently for every instance; never commit a real key in the spec.
