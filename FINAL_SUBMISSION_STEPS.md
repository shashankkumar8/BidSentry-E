# BidSentry-E — Final Submission Guide

**Team:** Syntax Squad  
**Project:** BidSentry-E — Evidence-Verified Tender X-Ray for Indian MSMEs  
**Event:** Kritical Hacks 2026 — AI/ML Track, Open Innovation  
**Prepared:** 22 October 2026 (IST)

> **Immediate priority:** The current official Unstop listing shows a registration and submission deadline of **22 October 2026, 11:59 PM IST**. Another listing variant has shown an earlier deadline. Open your registered application and confirm the deadline/status immediately. This guide cannot inspect or submit to your personal Unstop account.

## 1. Which file should I upload?

> **Archive scope:** This ZIP is technical source + documentation and intentionally contains no PPT, presentation PDF, slide images or deck generators. The 9-slide shortlist PPTX and its optional PDF are separate files. Do not search for them inside this archive.


**Upload the 9-slide shortlist deck first:**

`Syntax_Squad_BidSentry_Kritical_Hacks_2026_Shortlist.pptx`

Its matching PDF is:

`Syntax_Squad_BidSentry_Kritical_Hacks_2026_Shortlist.pdf`

The concise deck gives reviewers the project in a short sequence: problem, user moment, solution workflow, evidence ledger, competitive positioning, TinyFish architecture, AI/ML and trust, validation, impact/business hypotheses and next steps.

If requested for technical review, keep the **18-slide extended deck** (`Syntax_Squad_BidSentry_Kritical_Hacks_2026.pptx` and its PDF) as a detailed companion for questions or later-stage evaluation. Unless the portal explicitly requests both, submit the shortlist PPT rather than overwhelming the initial reviewer with two decks. Upload its PDF as a companion only if the form allows or requests it.

## 2. Submission requirements crosswalk

| Official brief item | Where it appears in the 9-slide deck | What to emphasise |
|---|---|---|
| Problem statement | Slide 2 | The bottleneck is pre-bid review and evidence gathering, not simply finding tenders. |
| Proposed solution | Slides 3–4 | Search → Fetch → Extract → Verify → Compare → Re-check; inspectable clause ledger. |
| Target users / use case | Slide 3 | MSME owners, bid coordinators and tender advisers screening an opportunity. |
| AI/ML / technical approach | Slide 7 | TF-IDF cosine similarity + token overlap for research priority; transparent rules and conservative states. |
| TinyFish integration | Slide 6 | Search and Fetch plus explicit Agent escalation and independent Fetch quote verification. |
| Expected impact | Slides 2 and 8 | A hypothesis to test; no invented savings or accuracy. GeM figures provide ecosystem scale only. |
| Feasibility | Slide 8 | 68 locally passing tests; clearly distinguish mocked/local checks from live API verification. |
| Future scope | Slide 9 | Pilot evaluation before broadening to more sources, alerts or workspaces. |

Official event listing: https://api.unstop.com/hackathons/kritical-hacks-2026-igdtuw-delhi-1760989

The listing says the initial PPT is required and a demo video/GitHub URL are optional at initial submission. However, it also states that a **meaningful, functional TinyFish integration is mandatory** and may need to be demonstrated at later evaluation. Do not confuse “optional link in round one” with “TinyFish use optional.”

## 3. Fill in Unstop carefully

1. Sign into the same Unstop account used for registration: https://unstop.com/o/1760989
2. Open the registered Kritical Hacks 2026 opportunity and check whether submission is open, your registration is valid, and the active deadline shown in your application.
3. Verify the roster. The listing specifies **2–5 team members**. Include only real participants who have agreed to be listed. The separately delivered deck uses the team name **Syntax Squad**; use that spelling consistently.
4. Select the category that actually fits your team (Student or Professional) and the track already registered/allowed by the organiser. Do not select a category purely for perceived scoring advantage.
5. Use the following project fields, adapting labels to the form:

**Project name**  
BidSentry-E — Evidence-Verified Tender X-Ray for Indian MSMEs

**Team name**  
Syntax Squad

**Track**  
AI/ML Track — Open Innovation

**Short description**  
BidSentry is an evidence-first tender-readiness copilot for Indian MSMEs. TinyFish Search and Fetch discover and retrieve public tender pages; a user-triggered Web Agent extracts structured requirements. Proposed blockers are checked against a separate source fetch before they can influence a profile assessment. Supplier rules surface matches, potential blockers and unknowns; source rechecks flag text changes. BidSentry never certifies eligibility or submits bids automatically.

6. Upload the **9-slide shortlist PPTX**. If PDF upload is supported, add the matching 9-page PDF only if the portal accepts a companion file.
7. Review the uploaded file name and preview. Recheck that the team, track and category are correct and there are no placeholder links in the form.
8. Click the final **Submit** action. Wait for the confirmation page/status. Save a screenshot or confirmation email and revisit the application to ensure the submission is recorded.

## 4. What can be submitted later / only if verified

- **GitHub:** use a public repository URL only after the repo exists, contains the intended code, has a useful README and excludes `.env`, keys, local databases, personal profiles, virtual environments and caches. The organiser says GitHub is optional in the initial PPT round, but TinyFish still must be used meaningfully.
- **Demo video:** record only after the flow works. A conceptual video is acceptable as a concept walkthrough only when labelled that way. Do not show synthetic fixture results as live tenders.
- **Social post:** do not state performance or customer results that have not been measured. Check whether it is required for the active round before spending time on it.
- **API key:** keep it in local `.env` only. Never send it in chat or place it in the deck, video, GitHub or form.

## 5. Local setup and verification (after securing the submission)

Requirements: Python 3.11+, internet for dependencies, and your own TinyFish API key. On Windows PowerShell, open a terminal in the extracted project directory, where `requirements.txt` is located:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

In the local `.env`, set `TINYFISH_API_KEY=your_actual_key` (do not include angle brackets, and do not share the file). Then run:

```powershell
python -m pytest -q
python -m compileall -q app tests
node --check app/static/app.js
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

### Live smoke-test order

1. Click **Search live tenders**. Verify that the app shows URLs actually returned by TinyFish and that the source page is fetched.
2. Choose a result from an official public government/NIC domain and inspect its source evidence.
3. Click **Deep inspect · Agent**. Record the real response/run status and the structured output.
4. Verify that Agent quotes are checked against a **separate Fetch response** and labelled verified or unverified.
5. Confirm missing supplier facts stay **Unknown / information missing** instead of being treated as zero.
6. Try **Recheck** after a snapshot exists. Confirm the app compares an actual later fetch with the saved baseline. A text diff is not proof every linked annexure/corrigendum was found.
7. Confirm no API key appears in screen recordings, console logs, Git or submitted files.

**Expected local test state in this prepared release:** `48 passed`. Tests include mocked integrations and synthetic examples. Passing them is not proof that the key works or that live tender extraction is accurate.

If a live request fails, preserve the actual error and mark that part as unverified. You may switch to **Explore sample** for a product walkthrough, but say “synthetic example” clearly.

## 6. 90-second demo sequence (if requested)

- **0–10 sec:** “Finding a tender is only step one; a supplier needs to know which requirements to verify before investing effort.”
- **10–25 sec:** Run live Search and click through to the actual source URL.
- **25–40 sec:** Show Fetch text, requirement quote, evidence status and the declared supplier value.
- **40–55 sec:** Trigger Agent inspection and show its real response.
- **55–70 sec:** Show the independent Fetch quote check and one Unknown / human-review case.
- **70–82 sec:** Re-check the same source and explain the text difference and its limits.
- **82–90 sec:** “BidSentry prioritises review; it does not certify eligibility or submit bids.”

If any live step is broken, do not fake it. Present the sample flow as synthetic and describe live verification as a remaining gate.

## 7. Judge-safe one-liners

**What is innovative?**  
“Rather than treating an AI summary as proof, BidSentry connects a potential qualification issue to source text, checks Agent quotes against a separate Fetch, keeps uncertainty visible, and records what changed between page snapshots. We are testing whether that evidence path is more useful than existing tender tools.”

**Where is the AI/ML?**  
“The current ranker uses TF-IDF cosine similarity and token overlap to prioritise relevant notices; transparent pattern rules identify candidate clauses. We do not claim a custom-trained eligibility model or a probability of winning/qualifying.”

**Is TinyFish working?**  
“Local tests pass, including mocked API contracts. A live account-backed Search/Fetch/Agent run is only claimed after we perform and record it with our own key.”

**Does it decide who qualifies?**  
“No. It is a pre-screening aid. Missing or unverified data remain unknown/review, and the team must check the complete tender documents and applicable policies.”

## 8. Claim and evidence discipline

Do not claim any of these unless you have proof: guaranteed shortlisting, “10/10”, “zero hallucinations”, eligibility certification, 100% live integration, exact time/cost savings, validated revenue or paid customers, complete monitoring of all portal changes, or public GitHub/video/submission completion.

Market scale: a Ministry of Commerce & Industry release states 1,175,001 MSMEs were registered on GeM as of 30 July 2026, and MSME order value on GeM was ₹237,235 crore in FY 2025–26. This supports ecosystem scale, not a measured BidSentry impact claim. Source: https://www.pib.gov.in/PressReleaseIframePage.aspx?PRID=2297820&lang=2&reg=48

Competitor discipline: Tender247 already markets tender discovery, AI eligibility summaries and corrigendum tracking. Do not say those categories are unique to BidSentry. Position the evidence chain as a hypothesis to validate. Source: https://www.tender247.com/aboutus

## 9. Final checklist

- [ ] The registered Unstop application shows the deadline and a valid submission path.
- [ ] Team name is `Syntax Squad` and roster includes 2–5 real members.
- [ ] Correct Student/Professional category and AI/ML Track are selected.
- [ ] Short description is copied and reviewed.
- [ ] 9-slide shortlist PPTX is attached and preview checked.
- [ ] No placeholder URLs or unsupported results are in the deck/form.
- [ ] Final Submit action completed and confirmation saved.
- [ ] Live TinyFish test is either completed and evidenced, or described honestly as not yet verified.
- [ ] Public repo/video/social links are real and accessible before being entered.

## 10. References

- Kritical Hacks 2026 official Unstop listing: https://api.unstop.com/hackathons/kritical-hacks-2026-igdtuw-delhi-1760989
- TinyFish Search API: https://docs.tinyfish.ai/api-reference/search-the-web
- TinyFish Fetch API: https://docs.tinyfish.ai/fetch-api/reference
- TinyFish Agent API: https://docs.tinyfish.ai/agent-api/reference
- TinyFish Python SDK 0.9.0: https://pypi.org/project/tinyfish/0.9.0/
- Ministry of Commerce & Industry / PIB: https://www.pib.gov.in/PressReleaseIframePage.aspx?PRID=2297820&lang=2&reg=48
- Tender247 product page: https://www.tender247.com/aboutus
- Agent-E research (inspiration, not reproduced validation): https://arxiv.org/abs/2407.13032
- ALCE grounded citation evaluation: https://aclanthology.org/2023.emnlp-main.398/
- NIST Generative AI Risk Management Profile: https://doi.org/10.6028/NIST.AI.600-1
