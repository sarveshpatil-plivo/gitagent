# AGENTS.md — plivo-sms skill

Integration-specific context for the Plivo SMS skill.

## What this is
A gitagent skill that sends SMS text messages through the Plivo Messages API. It ships a
`SKILL.md` with `name`/`description` frontmatter plus a stdlib-only Python script under
`scripts/`, so `discoverSkills()` in `src/skills.ts` auto-registers it. No registration edits
are required — the directory name `plivo-sms` must match the `name` field in `SKILL.md` and be
kebab-case.

## Plivo contract (verified)
- Endpoint: `POST https://api.plivo.com/v1/Account/{AUTH_ID}/Message/`
- Auth: HTTP Basic, `AUTH_ID:AUTH_TOKEN`
- Body (JSON): `{ "src", "dst", "text" }`
- Success: HTTP `202`, response carries `message_uuid` (a list, one per recipient).
  `202` means *queued*, not delivered.
- Multiple recipients: join `dst` numbers with `<`, not commas or arrays.

## Conventions
- Credentials come from `PLIVO_AUTH_ID` / `PLIVO_AUTH_TOKEN` / `PLIVO_SRC` (env or a `.env`
  in the skill dir). Never hardcode secrets.
- stdlib only (`urllib`); no external dependencies.
- Console and signup links point at `cx.plivo.com`, never `console.plivo.com`.

## Testing
Requires a live Plivo account, a rented sender number, and a reachable destination. Needs
manual verification with real credentials plus screenshots of a delivered message.
