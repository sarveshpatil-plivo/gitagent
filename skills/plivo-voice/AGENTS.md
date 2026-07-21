# AGENTS.md — plivo-voice skill

Integration-specific context for the Plivo Voice skill.

## What this is
A gitagent skill that places outbound phone calls through the Plivo Voice API. It ships a
`SKILL.md` with `name`/`description` frontmatter plus a stdlib-only Python script under
`scripts/`, so `discoverSkills()` in `src/skills.ts` auto-registers it. No registration edits
are required — the directory name `plivo-voice` must match the `name` field in `SKILL.md` and
be kebab-case.

## Plivo contract (verified)
- Endpoint: `POST https://api.plivo.com/v1/Account/{AUTH_ID}/Call/`
- Auth: HTTP Basic, `AUTH_ID:AUTH_TOKEN`
- Body (JSON): `{ "from", "to", "answer_url" }`
- Success: HTTP `201`, response carries `request_uuid`. `201` means the call was *fired*,
  not answered.
- On answer, Plivo fetches `answer_url` and expects call-flow XML (`application/xml`), e.g.
  `<Response><Speak>...</Speak></Response>`.
- This is a REST call (not audio streaming), so the 8 kHz codec rule does not apply.

## Conventions
- Credentials come from `PLIVO_AUTH_ID` / `PLIVO_AUTH_TOKEN` / `PLIVO_SRC` (env or a `.env`
  in the skill dir). Never hardcode secrets.
- Numbers are E.164 with a leading `+`.
- stdlib only (`urllib`); no external dependencies.
- Console and signup links point at `cx.plivo.com`, never `console.plivo.com`.

## Testing
Requires a live Plivo account, a rented caller-ID number, a reachable destination, and a
publicly reachable answer URL returning valid XML. Needs manual verification with real
credentials plus screenshots of a completed call.
