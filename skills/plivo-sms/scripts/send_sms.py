#!/usr/bin/env python3
"""
Send SMS via the Plivo Messages API
"""
import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

PLIVO_API_BASE = "https://api.plivo.com/v1/Account"

def load_env():
    """Load environment variables from .env file if it exists"""
    env_file = Path(__file__).parent.parent / '.env'
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

def send_sms(dst, text, src=None, auth_id=None, auth_token=None):
    """Send an SMS via the Plivo Messages API"""

    auth_id = auth_id or os.getenv('PLIVO_AUTH_ID')
    auth_token = auth_token or os.getenv('PLIVO_AUTH_TOKEN')
    src = src or os.getenv('PLIVO_SRC')

    if not auth_id or not auth_token or not src:
        print("ERROR: Plivo credentials not found!", file=sys.stderr)
        print("\nPlease set credentials using one of these methods:", file=sys.stderr)
        print("\n1. Environment variables:", file=sys.stderr)
        print("   export PLIVO_AUTH_ID='your-auth-id'", file=sys.stderr)
        print("   export PLIVO_AUTH_TOKEN='your-auth-token'", file=sys.stderr)
        print("   export PLIVO_SRC='+14150000000'", file=sys.stderr)
        print("\n2. Create a .env file in skills/plivo-sms/:", file=sys.stderr)
        print("   PLIVO_AUTH_ID=your-auth-id", file=sys.stderr)
        print("   PLIVO_AUTH_TOKEN=your-auth-token", file=sys.stderr)
        print("   PLIVO_SRC=+14150000000", file=sys.stderr)
        print("\nGet your Auth ID and Auth Token at:", file=sys.stderr)
        print("   https://cx.plivo.com", file=sys.stderr)
        sys.exit(1)

    url = f"{PLIVO_API_BASE}/{auth_id}/Message/"
    payload = json.dumps({'src': src, 'dst': dst, 'text': text}).encode('utf-8')
    credentials = base64.b64encode(f"{auth_id}:{auth_token}".encode('utf-8')).decode('ascii')

    request = urllib.request.Request(url, data=payload, method='POST')
    request.add_header('Authorization', f"Basic {credentials}")
    request.add_header('Content-Type', 'application/json')

    try:
        print(f"Sending SMS to {dst}...", file=sys.stderr)
        with urllib.request.urlopen(request) as response:
            status = response.getcode()
            body = json.loads(response.read().decode('utf-8'))

        if status == 202:
            uuids = body.get('message_uuid', [])
            print(f"✓ SMS queued to {dst} (message_uuid: {', '.join(uuids)})")
            return True

        print(f"ERROR: unexpected status {status}: {body}", file=sys.stderr)
        return False

    except urllib.error.HTTPError as e:
        detail = e.read().decode('utf-8', 'replace')
        print(f"ERROR: Plivo API returned {e.code}: {detail}", file=sys.stderr)
        return False
    except urllib.error.URLError as e:
        print(f"ERROR: Failed to reach Plivo API: {e.reason}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description='Send SMS via the Plivo Messages API')
    parser.add_argument('--to', required=True, help='Destination number(s) in E.164; join multiple with "<"')
    parser.add_argument('--text', required=True, help='Message body')
    parser.add_argument('--from', dest='src', help='Sender ID (default: PLIVO_SRC env var)')
    parser.add_argument('--auth-id', dest='auth_id', help='Plivo Auth ID (default: PLIVO_AUTH_ID env var)')
    parser.add_argument('--auth-token', dest='auth_token', help='Plivo Auth Token (default: PLIVO_AUTH_TOKEN env var)')

    args = parser.parse_args()

    load_env()

    success = send_sms(
        dst=args.to,
        text=args.text,
        src=args.src,
        auth_id=args.auth_id,
        auth_token=args.auth_token,
    )

    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
