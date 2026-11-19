# WeChat iLink Gateway

Each enrollment runs a separate [Kadxy weixin-ilink-gateway](https://github.com/Kadxy/weixin-ilink-gateway) instance. The provider is Kadxy; UnitySVC Labs operates this prototype.

1. Enroll in **base**.
2. Wait for the instance to become ready. Its address is `https://<enrollment-code>.staging.unitysvc.app` on staging (HTTPS port 443).
3. The enrollment form shows a generated **Weixin API key**; keep it or replace it with your own (at least 12 characters), then save. It is stored with the enrollment (view and copy it from the enrollment's instance details) and given to the gateway as its `API_KEY`. This is an application key, not your UnitySVC API key. Changing it later restarts the instance with the new key.
4. Open `/console`, enter the instance key, and start QR login. Scan the QR code with the WeChat account you want the bot to use.
5. The form also generates a **Webhook token** (`WEBHOOK_TOKEN`). It makes `POST https://<instance>/webhook/<token>` send a text message to the WeChat account you logged in with; the endpoint needs no API key, so keep the token private. The [msg-to-wechat](/services) service uses it: save the instance host and this token as secrets and it delivers notifications through this gateway.
6. Call `/status`, `/messages/updates`, `/messages/send`, and the media endpoints using `Authorization: Bearer <your Weixin API key>`.

The upstream requires a cached context token before sending to a user: send a message from that user to the bot first. See the upstream README for the full API and webhook configuration.

## Storage

Storage is temporary. Stopping, replacing, or deleting the instance loses WeChat login state, sync cursors, and cached messages; scan the QR code again after replacement. No persistent volume is promised.

The console is publicly reachable, while the REST API requires the instance key; keep that key private.

The Compose file is plain: its `API_KEY` is a placeholder. The channel's `environment` sets `API_KEY` from the enrollment's `WEIXIN_API_KEY` parameter when UnitySVC starts the instance. For manual local Compose use, set `API_KEY` to a fresh random token of at least 12 characters.
