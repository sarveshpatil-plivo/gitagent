---
name: plivo-voice
description: Place outbound phone calls via the Plivo Voice API using Auth ID / Auth Token authentication.
---

# Plivo Voice Skill

Place outbound phone calls via the Plivo Voice API.

## Setup

1. **Create a Plivo account and get your credentials**:
   - Sign up or log in at https://cx.plivo.com/?utm_source=github&utm_medium=oss&utm_campaign=gitagent
   - Copy your **Auth ID** and **Auth Token** from the dashboard
   - Buy or rent a Plivo phone number to use as the caller ID (`from`)

2. **Configure credentials**:
   ```bash
   export PLIVO_AUTH_ID="your-auth-id"
   export PLIVO_AUTH_TOKEN="your-auth-token"
   export PLIVO_SRC="+14150000000"
   ```

   Or create a `.env` file in the skill directory:
   ```
   PLIVO_AUTH_ID=your-auth-id
   PLIVO_AUTH_TOKEN=your-auth-token
   PLIVO_SRC=+14150000000
   ```

## Usage

When the call is answered, Plivo fetches `--answer-url` and expects call-flow XML in
response. A minimal answer URL returns Plivo `<Speak>` XML, for example:

```xml
<Response><Speak>Hello, this is a call from Plivo.</Speak></Response>
```

Place the call:

```bash
python3 scripts/make_call.py \
  --to "+14150000001" \
  --answer-url "https://your-server.example/answer.xml"
```

Override the caller ID for a single call with `--from`:

```bash
python3 scripts/make_call.py \
  --to "+14150000001" \
  --answer-url "https://your-server.example/answer.xml" \
  --from "+14159999999"
```

## Notes

- `from` and `to` must be E.164 numbers with a leading `+`.
- The answer URL must be publicly reachable and return `application/xml`.
- A successful request returns HTTP `201` and a `request_uuid`. This confirms the call was
  fired, not that it was answered.

## Requirements

- Python 3.6+
- No additional packages needed (uses stdlib urllib)
