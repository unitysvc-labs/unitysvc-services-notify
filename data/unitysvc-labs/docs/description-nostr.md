# Nostr Notifications (Bring Your Own Nostr Key)

Send encrypted direct messages on the Nostr decentralized protocol using your own private key.

## Prerequisites

1. **Generate a Nostr key pair** using any Nostr client (e.g. [nostr.com](https://nostr.com/), Damus, Amethyst) or a key generation tool.
2. **Copy your nsec (private key)** — this is what the gateway uses to sign and send messages.
3. **Enroll** using your private key — stored as `NOSTR_PRIVATE_KEY` in your secrets.

## API

Send a message via `POST /send`:

```json
{
  "target": "npub1abc123def456ghi789jkl012mno345pqr678stu901vwx234yz",
  "message": "Hello from UnitySVC!",
  "format": "text"
}
```

| Field     | Type   | Required | Description                                        |
|-----------|--------|----------|----------------------------------------------------|
| `target`  | string | yes      | Recipient's Nostr public key in `npub1...` bech32 format or hex |
| `message` | string | yes      | Message text                                       |
| `format`  | string | no       | `text` (default)                                   |

## Notes

- Messages are sent as encrypted DMs (NIP-04) via the Nostr relay network. Your private key is used to sign messages; keep it secret.
- The recipient must have a Nostr account and their public key must be known.
