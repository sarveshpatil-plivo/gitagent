---
name: plivo-sms
description: Send SMS text messages via the Plivo Messages API using Auth ID / Auth Token authentication.
---

# Plivo SMS Skill

Send SMS text messages via the Plivo Messages API.

## Setup

1. **Create a Plivo account and get your credentials**:
   - Sign up or log in at https://cx.plivo.com/?utm_source=github&utm_medium=oss&utm_campaign=gitagent
   - Copy your **Auth ID** and **Auth Token** from the dashboard
   - Buy or rent a Plivo phone number to use as the sender (`src`)

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

```bash
python3 scripts/send_sms.py \
  --to "+14150000001" \
  --text "Hello from Plivo"
```

Send to multiple recipients by joining the destination numbers with `<`:

```bash
python3 scripts/send_sms.py \
  --to "+14150000001<+14150000002" \
  --text "Hello everyone"
```

Override the sender for a single message with `--from`:

```bash
python3 scripts/send_sms.py \
  --to "+14150000001" \
  --text "Hello" \
  --from "+14159999999"
```

## Notes

- `src` is a Plivo phone number, short code, or (where permitted) an alphanumeric sender ID.
- A successful request returns HTTP `202` and a `message_uuid` per recipient. Success means the message is *queued*, not yet delivered.
- Every call sends a new billable message; guard against accidental retries.

## Requirements

- Python 3.6+
- No additional packages needed (uses stdlib urllib)
