# Release Truth Table — Feature, Evidence and Claim Language

| Capability | Baseline status | Evidence currently available | Safe pitch language | Do not claim |
|---|---|---|---|---|
| Sample workflow | Implemented | Local fixtures/tests | “Synthetic sample demonstrates the UI” | “This sample is a live tender” |
| TinyFish Search | Implemented in code; live run unverified in package build | Mocked tests; code path exists | “Integrated in the prototype; live smoke test required” | “Live API proven in this environment” |
| TinyFish Fetch | Implemented in code; live run unverified in package build | Mocked tests; code path exists | “Fetches page text via TinyFish in the configured environment” | “Every linked doc is fetched” |
| Structured Agent inspection | Implemented in code; live run unverified in package build | Mocked tests; user-triggered code path | “Optional user-triggered structured inspection” | “SSE live browser stream/raw DOM corpus” |
| Quote verification | Implemented | Exact normalized match against separate Fetch response; mocked tests | “Marks a quote verified only when found in independent fetched text” | “Eliminates hallucinations” |
| Clause extraction | Implemented, narrow | Deterministic patterns + tests | “Extracts selected common clauses; others stay Unknown/Review” | “Understands all tenders” |
| Eligibility comparison | Implemented, narrow | Rules for selected explicit thresholds vs. declared profile | “Potential gap / appears to meet extracted threshold” | “Eligible / guaranteed compliant” |
| TF-IDF relevance ranking | Implemented | sklearn-based scoring in analyzer | “Prioritizes text relevance” | “Trained AI predicts eligibility or win chance” |
| Amendment recheck | Implemented for reached page | Saved text snapshots + diff and tests | “Re-fetches the page and highlights text differences” | “Finds every corrigendum or legal change” |
| Legal exemption rules | Not implemented as a complete engine | Policy research only | “Human must verify tender-specific exemption wording” | “Udyam means automatic EMD exemption” |
| PDF/BOQ/annexure completeness | Not established | Not exhaustively traversed | “Some linked docs can be outside current coverage” | “Complete tender-document coverage” |
| Public repo / video / form submit | Not verified by package creation | No account publishing actions performed | State only actual posted URLs/confirmation | “Published/submitted” before proof |
| Accuracy / time savings / revenue | Not measured | No labeled corpus/customer pilot | “Planned validation metrics / pricing hypothesis” | Any fabricated percentage, customer or revenue result |

This document should be updated whenever the implementation changes. Do not upgrade a row's status because a code-generation tool wrote a file; rerun tests and observe the relevant behavior.
