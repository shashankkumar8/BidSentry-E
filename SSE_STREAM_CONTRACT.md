# TinyFish Agent SSE contract in BidSentry-E

## Purpose

The workbench uses `POST /api/v1/inspect/stream` to expose a real TinyFish Agent REST stream without exposing the API key to the browser. The existing `POST /api/v1/inspect` route remains a synchronous official Python SDK compatibility route. Search/Fetch REST parameters and SDK method arguments must remain separate.

## Sequence

1. Validate that the submitted tender URL is public HTTPS on a government/NIC domain.
2. Open TinyFish Agent REST SSE at `https://agent.tinyfish.ai/v1/automation/run-sse` with a schema-constrained read-only tender extraction goal.
3. Forward minimal provider trace fields (event type/status, run ID, streaming URL, progress/message) to the UI. Do not forward API keys or the entire arbitrary provider payload.
4. Wait for a terminal completion event. If the terminal event omits result or step metadata and has a run ID, request the provider run record from `/v1/runs/{id}`.
5. Reject failed, inconsistent or nonterminal statuses, and reject missing/invalid structured result. Never generate a qualification result from progress events or from a failed stream.
6. Only after successful Agent output, Fetch each cited source URL independently and verify the exact normalized quote with `app/evidence.py`. Unverified quotes stay out of the text used for profile assessment.
7. Show provider-reported `num_of_steps` only when present. SSE frames observed are telemetry, **not billable steps**. Any dollar cost is a configurable estimate; provider billing is authoritative.
8. Deliver the final result event and a completion event. On error, deliver an error event and no result event.

## Application event frames

Each frame is one JSON object in a `data:` line. The UI understands these application-level event types:

- `phase`: app lifecycle information (`agent`, `quote_verification`).
- `provider_event`: minimal provider event fields for visible trace.
- `result`: final evidence-checked assessment payload; emitted only after successful terminal output and quote-check stage.
- `error`: run failure, missing terminal status, malformed result or provider error; no assessment accompanies this event.
- `done`: clean end after the result event.

This is the app’s event envelope, not a claim that the provider emits exactly the same event set for every account/run. The actual provider may omit `STREAMING_URL`, may use different progress events, or may complete with no useful extraction. The system must preserve these distinctions.

## Observability behavior

The stream response cannot place its final end-to-end duration in headers before its body finishes. Therefore it uses the literal `X-Execution-Time-Ms: stream-completion-reported-in-SSE` and writes measured full duration into the local metadata-only audit ledger after stream iteration. The final result includes `inspection_elapsed_ms`. Event count and provider step count are separate fields.

## Live validation required

Tests use a mocked SSE stream and mocked Fetch result. Before describing the integration as live-proven, run one inspection with the team’s own key; capture actual provider events, the terminal status/run ID, provider step metadata where available, an independently checked quote and a screenshot showing any streaming URL. Never ship API keys or a live signed session URL in the public repository.
