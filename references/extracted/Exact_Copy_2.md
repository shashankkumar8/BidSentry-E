hey what is the approach to solve a ps of hackathon to make a  hackathon wiinnning sol what is the ideal roadmap or process to do so as when i got ps i dump into diff llm like claude chatgpt and gemini to do it for me and not get even shortlised i am not sure but all others do the same and we all get the same approaches from these models and nothing happens is it how to overcome it as i have to win some hackathons for sure please tell in detailed manner

You just diagnosed the exact reason why 90% of teams get eliminated in the first round: **the "LLM Homogeneity Trap."**

When 500 teams copy-paste a Problem Statement (PS) into ChatGPT, Claude, or Gemini and ask, *"Give me a winning hackathon solution,"* all 500 teams get the exact same answer. Why? Because LLMs predict the **most statistically probable (average)** answer. If the PS is about healthcare, the LLM suggests an "AI-powered symptom checker dashboard with blockchain medical records." Judges read 80 identical PPTs proposing that exact same generic wrapper, roll their eyes, and reject all of them.

To get shortlisted and win, you must stop using LLMs as your *architect* and start using them as your *interrogator*. Follow this complete, step-by-step process to break out of the crowd and build solutions that actually win.

## 1. The Mindset Shift: Average vs. Edge Case

| What 90% of Teams Do (Eliminated)                                     | What Winning Teams Do (Shortlisted & Funded)                                          |
| --------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Dump the raw PS into an LLM and build the first idea it outputs.      | Dissect the PS to find a **hyper-specific bottleneck** nobody else noticed.           |
| Try to solve the *entire* problem with a "platform" or "dashboard".   | Solve **one specific workflow** from end-to-end with zero friction.                   |
| Slap "AI + Blockchain + IoT" onto the slide deck for buzzword points. | Use the simplest possible tech where it matters, plus **one deep technical novelty**. |
| Pitch features ("We have login, analytics, chatbot, and alerts").     | Pitch **measurable impact** ("We cut warehouse scanning latency from 14s to 0.4s").   |

## 2. The 6-Stage Hackathon Winning Process

Follow these steps strictly in order—skipping the deconstruction phase is why most projects fail before a single line of code is written.

1

**Deconstruct the PS & Sponsor Motive**

*First 2 hours — Do NOT touch an LLM yet*

Read the Problem Statement three times and ask: **Who wrote this, and why are they losing money or sleep over it?**

- **Corporate Sponsor PS:** They want a plug-and-play feature for their existing product, a way to use their API, or a fix for an expensive edge case.
- **Government / Social PS (e.g., SIH):** They care about **last-mile constraints**—offline functionality, regional languages, SMS/WhatsApp accessibility for low-end phones, and zero training required for the user.
- **Action:** Underline the *constraints* in the PS, not just the goal.

2

**Find the Ground-Truth Bottleneck**

*Why existing solutions fail in the real world*

Before ideating, spend 45 minutes researching how real humans currently deal with this problem.

- Search Reddit, YouTube comments, Play Store 1-star reviews of existing apps, or call one person who actually works in that domain.
- **Look for the "ugly reality":** For example, if the PS is *"Track agricultural supply chains,"* an LLM will say *"Build a web dashboard for farmers."* Real-world research tells you farmers won't log into a web portal—they have dirty hands in the field and 2G internet. A voice-activated WhatsApp bot or automatic SMS trigger wins instantly.

3

**Use LLMs as Critics, Not Creators**

*Flip your prompting strategy*

Once you know the real-world constraint, use Claude/ChatGPT/Gemini to **eliminate** generic ideas rather than generate them. (See the exact prompts in Section 3 below).

4

**Engineer the 'Shortlist Slide Deck'**

*How to pass Round 0 (Idea Submission)*

Evaluators spend **less than 45 seconds** looking at your PPT during shortlisting. If your deck is walls of AI-generated bullet points, you are out.

- **Slide 1 (The Hook & Micro-Problem):** Don't repeat the PS. State the exact bottleneck with a real number.
- **Slide 2 (System Architecture Diagram):** This is the #1 slide that gets teams shortlisted. Draw a clean block diagram (using Excalidraw or Eraser.io) showing the exact data flow, APIs, models, and fallback mechanisms.
- **Slide 3 (The 'Secret Sauce' / USP):** What makes your approach technically work where others fail? (e.g., "On-device quantized model for zero-internet zones").
- **Slide 4 (UI Wireframe / User Journey):** Show a 3-step visual screen flow of the product, not text describing it.

5

**Build the 'Golden Path' Prototype**

*Hours 4 to 20 of the hackathon*

Never build login pages, settings menus, "forgot password" flows, or database CRUD for irrelevant features.

- Build **one single user journey (The Golden Path)** that showcases your core innovation working live with real data.
- Hardcode or mock the boring surrounding parts so you can spend 80% of your coding time making the core algorithm/feature undeniably impressive.

6

**Deliver a Zero-Jargon, Story-Driven Pitch**

*Final 4 hours — Stop coding, start rehearsing*

Judges are exhausted during final evaluations. Do not start with *"Hello everyone, our project name is X."*

- **First 15 seconds:** Tell a 2-sentence story of a real person failing because of the problem.
- **Next 90 seconds:** Show the **live demo immediately**. Don't talk about your demo—show it working on screen.
- **Final 45 seconds:** Explain the technical magic behind what they just saw, how it scales, and answer their questions directly without bluffing.

## 3. How to Actually Prompt LLMs for Hackathons

Instead of asking *"Give me a solution for this PS,"* use this **3-Step Anti-Generic Prompt Chain**:

1. **Prompt 1 (The Filter):**
   > *"Here is a hackathon problem statement: [Paste PS]. List the 5 most common, cliché, and generic solutions that 90% of beginner teams will generate using AI for this prompt. Be specific about why judges will find them boring or impractical." (Now you have a blacklist of what **NOT** to build.)*
2. **Prompt 2 (The Edge-Case Finder):**
   > *"Forget software solutions for a moment. Act as a grumpy 15-year industry veteran working in [Domain of PS]. When people try to solve this problem in the real world, what are the top 5 hidden operational, human, hardware, or data bottlenecks that cause software tools to fail in the field?"*
3. **Prompt 3 (The Technical Co-Founder):**
   > *"I want to solve specifically bottleneck #2 from your list: [Paste bottleneck]. Propose 3 unconventional technical architectures to solve ONLY this bottleneck using open-source tools executable in 24 hours. Focus on concrete workflows, not generic dashboards."*

## 4. What to Fix Before Your Next Hackathon

If you want to guarantee a shortlist on your very next attempt, make two immediate changes to your workflow:

- **Ban the word "Platform":** Never pitch an "All-in-one AI Platform." Pitch a surgical tool: a browser extension, an automated webhook pipeline, an edge-vision hardware trigger, or a zero-UI voice agent.
- **Show proof before the hackathon starts:** During the PPT shortlisting round, include a 20-second GIF or Loom link of a working proof-of-concept (even a rough script or Figma prototype) right inside your submission. When 490 teams submit text slides and you submit a working proof-of-concept with an architecture diagram, you move straight to the top 10.

If you have a specific hackathon or Problem Statement you're looking at right now, drop it here—we can break it down together and run the Anti-Generic process on it!

#####

also whenever i wanna llm build them or give me detailed process to build  the req proj idea from scratch with any ide like antigravity or cursor or from scratch by me as well it give some random files and zip that creatre a newbie and trash like web doing only several func only not that much great that wanting what about this

Asking an LLM or an AI IDE (like Cursor or Antigravity) to *"build this whole project from scratch"* triggers the **Token Compression Trap**.

An LLM can only output roughly 4,000 to 8,000 tokens (around 300–500 lines of code) in a single turn. A real, hackathon-winning prototype requires **5,000 to 15,000 lines of code**. When you ask an AI to build the whole app at once, it mathematically *has* to shrink a 10,000-line architecture into 400 lines. To do that, it gives you:

- Ugly, barebones HTML/CSS with cliché purple-blue gradients.
- Fake buttons that just trigger `alert("Success!")` or `setTimeout()` mocks.
- Empty backend files filled with `# TODO: Add real logic here`.

To get Cursor, Antigravity, or Claude to build a **production-grade, complex application**, you have to stop treating the AI like a magic wand and start driving it like a **Senior Tech Lead managing a Junior Developer**.

## 1. Why AI Code Looks "Trash" vs. How to Fix It

| The Mistake ("Vibe Coding" Slop)                               | The Fix ("Spec-Driven" Engineering)                                                                                   |
| -------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **"Build me a full web app for [Idea]"**                       | **Never prompt the whole app.** Build one isolated module at a time (Vertical Slicing).                               |
| Letting the AI write raw CSS or basic Tailwind from scratch.   | Force the AI to use pre-built component libraries (**shadcn/ui**, **Magic UI**, **Aceternity**, or **Lucide icons**). |
| Building the UI first and trying to connect the backend later. | Build and test the **Core Engine in a raw Python/Node terminal script first**, then wrap a UI around it.              |
| Accepting mocked functions (`// simulate API call`).           | Explicitly ban mocks in your IDE rules and force real API/SDK integration per file.                                   |

## 2. The 5-Phase Workflow to Build Serious Projects in Cursor / Antigravity

Do not let the AI write application code in your first prompt. Follow this exact build order:

### Phase 1: Lock the Architecture in a `SPEC.md` File First

Open your empty project folder in Cursor or Antigravity. Before generating any code files, open a chat and make the AI write a **Technical Specification (**`SPEC.md`**)** in your root directory.

- **Your Prompt:** *"We are building [Core Bottleneck Solution]. Do NOT write any application code yet. Write a comprehensive `SPEC.md` containing: 1) Exact Tech Stack (Next.js App Router, Tailwind, shadcn/ui, FastAPI, Supabase/SQLite), 2) Folder structure tree, 3) Exact Database Schema, 4) API Endpoint contracts (request/response JSON), and 5) A 6-step incremental build checklist."*
- **Why this works:** In every future prompt, you will tag SPEC.md. The AI never loses context or invents random file names because it is anchored to your blueprint.

### Phase 2: Build the "Hard Part" as a Standalone Script First

Judges hate apps that are just pretty frontends with fake backends. Before touching HTML or React, build your **core technical novelty** in a single isolated script (`engine.py` or `worker.ts`).

- If your project uses Computer Vision, RAG, audio processing, WebSockets, or scraping, tell the AI: *"Create ONLY `engine/processor.py`. Write the complete, working implementation using [OpenCV / LangChain / PyTorch / Playwright]. No placeholders. Include a CLI test block at the bottom so I can run `python engine/processor.py` in my terminal with a real sample file and see the output."*
- Run it in your terminal. Fix the bugs with the AI right there until the terminal prints real, accurate output. **Now you have a real engine that 90% of other teams don't have.**

### Phase 3: Scaffold the UI Using High-Craft Component Systems

Never let an LLM invent its own UI styling—it will always look like a beginner's college project.

1. Initialize a real framework via terminal (`npx create-next-app@latest` + `npx shadcn@latest init`).
2. Install real components first: `npx shadcn@latest add card button badge table tabs dialog chart`.
3. Alternatively, use **v0.dev** or **Bolt.new** solely to design the visual frontend shell using shadcn components, export that clean React code into Cursor/Antigravity, and use Cursor to wire up the backend.
4. **The Design Secret:** Tell the AI to style the interface like **Linear, Vercel, or Raycast**—high-contrast dark/light mode, `1px` subtle borders (`border-zinc-800`), monospace fonts for data/metrics, and zero cheesy gradients.

### Phase 4: Build via "Vertical Slices" (One Feature Per Prompt)

Instead of asking the AI to wire up the whole app, feed it **one slice at a time** in Cursor Composer / Agent mode:

- **Slice 1:** *"Read SPEC.md. Build ONLY the FastAPI endpoint `/api/analyze` that imports our working engine/processor.py and returns the JSON schema defined in the spec."* (Test it with Postman or `curl`).
- **Slice 2:** *"Build ONLY the frontend upload/input state in `app/dashboard/page.tsx` that sends real `FormData` to `/api/analyze` and renders the real JSON response."*
- **Slice 3:** *"Add real-time streaming status updates or error handling for edge cases."*

### Phase 5: Add "Visible Telemetry" (The Judge Magnet)

Even if your backend is doing complex work, if the UI only shows a spinning loader for 5 seconds and then prints a text result, judges will think it's a basic ChatGPT wrapper.

- Ask your IDE to add a **"Live Execution Terminal / Telemetry Drawer"** on the screen that streams the real intermediate steps from your backend (e.g., `[12ms] Frame extracted -> [84ms] OCR bounding boxes detected -> [210ms] Anomaly score: 0.94`).
- Showing latency numbers, confidence scores, bounding boxes, or raw JSON payloads live on screen immediately proves your project is real engineering.

## 3. Copy-Paste This `.cursorrules` File into Every Project

Before you start coding in Cursor or Antigravity, create a file named `.cursorrules` (or put it in your IDE's **System Instructions / Rules for AI**) and paste this exact block. It physically stops the AI from generating lazy, newbie code:

**Markdown**

```
# AI Engineering Rules (Strict Hackathon Mode)

1. ZERO PLACEHOLDERS: You are strictly forbidden from writing `// TODO`, `# implement logic here`, `mockData`, or `setTimeout` to fake asynchronous operations. Every function you write must contain complete, working production logic.
2. SMALL, MODULAR FILES: Never dump an entire app into a single file. Keep files under 250 lines. Separate UI components, API routes, types, and core business logic as defined in `SPEC.md`.
3. UI/UX STANDARDS: Never write raw vanilla CSS or ugly neon/purple-blue gradients. Use Tailwind CSS with `shadcn/ui` primitives and `lucide-react` icons. Use clean neutral palettes (`zinc` or `slate`), tight typography, `1px` subtle borders, and monospace fonts (`font-mono`) for numbers, logs, and metrics.
4. REAL ERROR HANDLING: Wrap external API calls and processing pipelines in proper `try/catch` blocks that return structured error messages to the UI, never silent failures.
5. STEP-BY-STEP EXECUTION: Only modify or create the specific files requested in the current prompt. Do not rewrite unrelated files or generate zip-style boilerplate dumps. Always reference `@SPEC.md` before writing code.

```

## 4. The Golden Rule When the AI Gets Stuck in a Bug Loop

Sometimes in Cursor or Antigravity, the AI tries to fix a bug, breaks two other things, and loops 5 times until the code is ruined.

- **Stop after 2 failed AI fixes.** Run `git checkout .` (commit after every working slice!).
- Instead of saying *"It's still broken, fix it,"* tell the AI: *"Do not change any code yet. Add `console.log` / `print` statements at the exact points where data enters and leaves this function so we can see the exact payload."*
- Paste the terminal error log back in—LLMs are 10x better at fixing bugs when given a stack trace and payload printouts than when guessing blindly.

#####

Want to put this workflow into practice right now?

Generate a complete SPEC.md for a project idea

Get a starter UI prompt for a Linear/Vercel-style dashboard

Learn the ideal 24-hour Git and team split workflow generate all these one by one in detail

Save these three templates into a "Hackathon Starter Kit" folder on your machine before your next event. They are designed to work together: the `SPEC.md` anchors your AI IDE, the **UI Prompt** generates a judge-ready interface in 60 seconds, and the **24-Hour Git Workflow** ensures your team integrates code without a 4 AM merge disaster.

## Part 1: The Complete `SPEC.md` Blueprint

Drop this file into the root of your project folder before writing any code. It uses a realistic, winning-style hackathon project (**SentinelDocs: Real-Time Supply Chain Invoice & Cold-Chain Spoilage Verification Engine**) as a working reference. When you get a new Problem Statement, spend 10 minutes updating the sections marked `[CUSTOMIZE]` and tag SPEC.md in every Cursor or Antigravity prompt.

**Markdown**

````
# SPEC.md — Project Blueprint for AI IDE Execution

## 1. Project Overview & Core Bottleneck [CUSTOMIZE]
- **Project Name:** SentinelDocs (Edge-Verified Supply Chain Auditor)
- **The Micro-Bottleneck:** Warehouse clerks spend 12+ minutes manually cross-checking paper delivery manifests against IoT cold-chain temperature logs, missing 18% of spoiled pharmaceutical batches.
- **The Solution:** An automated verification workbench that ingests a photo of a paper manifest + raw sensor CSV, runs local OCR + anomaly detection in <1.5 seconds, highlights tampered/spoiled line items with bounding boxes, and fires an instant WhatsApp webhook alert.
- **The "Golden Path" Live Demo Flow (Build ONLY This):**
  1. User clicks a "Load Real Sample Batch" preset button (or uploads an invoice image + sensor log).
  2. Backend runs the 4-stage pipeline (`engine/verifier.py`) and streams live step-by-step latency logs to the UI Telemetry Drawer.
  3. Center workbench renders the annotated document, flags exact temperature violations in red, displays a Risk Score (0-100), and triggers a live webhook alert preview.

## 2. Locked Tech Stack
- **Frontend:** Next.js 14 (App Router, TypeScript), Tailwind CSS, `shadcn/ui`, `lucide-react` icons.
- **Backend:** Python 3.11+, FastAPI, Uvicorn, Pydantic v2 (strict schema validation).
- **Core Engine:** OpenCV + EasyOCR / PyMuPDF (document parsing), Pandas + Scikit-Learn IsolationForest (sensor anomaly detection), OpenAI/Gemini Structured Outputs (semantic cross-check).
- **Database:** SQLite via SQLAlchemy (local `audit_logs.db` — zero cloud latency or auth failures during demo).

## 3. Strict Directory Structure (Do Not Deviate)
project-root/
├── .cursorrules                  # Strict anti-placeholder rules
├── SPEC.md                       # This source-of-truth file
├── sample_data/                  # 3 real test cases for 1-click judge demo
│   ├── case_01_valid/
│   └── case_02_spoiled_batch/
├── backend/
│   ├── main.py                   # FastAPI entrypoint & CORS config
│   ├── models.py                 # Pydantic request/response schemas
│   ├── db.py                     # SQLite connection & audit history table
│   └── engine/
│       ├── __init__.py
│       ├── ocr_parser.py         # Extracts line items & batch IDs from image
│       ├── anomaly_detector.py   # Evaluates time-series sensor thresholds
│       └── pipeline.py           # Orchestrates engine & yields telemetry logs
└── frontend/
    └── src/
        ├── app/
        │   ├── layout.tsx
        │   └── page.tsx          # Single-screen 3-column workbench (NO landing page)
        ├── components/
        │   ├── SidebarPresets.tsx # Left panel: 1-click demo cases & system health
        │   ├── WorkbenchStage.tsx # Center panel: Upload, annotated view, KPI cards
        │   └── TelemetryDrawer.tsx# Right panel: Live monospace execution logs & JSON
        └── lib/
            ├── api.ts            # Typed fetch calls to FastAPI backend
            └── types.ts          # Mirrors backend/models.py exactly

## 4. Strict API Contract (Locked at Hour 2)
### Endpoint: `POST /api/v1/verify`
**Request (`multipart/form-data` or Preset ID):**
```json
{
  "preset_id": "case_02_spoiled_batch",
  "strict_threshold_celsius": 8.0
}

````

**Response (**`200 OK`**&#x20;— Must match this exact shape):**

**JSON**

```
{
  "audit_id": "AUD-99412",
  "status": "CRITICAL_VIOLATION",
  "risk_score": 88,
  "total_latency_ms": 642,
  "extracted_metadata": {
    "batch_id": "PHARM-2026-X89",
    "carrier": "Apex Cold Logistics",
    "declared_temp_c": 4.2,
    "actual_peak_temp_c": 11.8,
    "violation_duration_mins": 47
  },
  "anomalies": [
    {
      "code": "TEMP_EXCURSION",
      "severity": "HIGH",
      "description": "Sensor spike to 11.8C between 03:10 and 03:57 UTC exceeds 8.0C threshold.",
      "confidence": 0.97
    }
  ],
  "telemetry_trace": [
    { "step": "INGEST", "detail": "Loaded manifest (1240x1750px) & 1,440 sensor rows", "latency_ms": 38 },
    { "step": "OCR_EXTRACT", "detail": "Detected Batch ID PHARM-2026-X89 (conf: 0.96)", "latency_ms": 284 },
    { "step": "ISOLATION_FOREST", "detail": "Flagged 47m thermal excursion window", "latency_ms": 112 },
    { "step": "WEBHOOK_DISPATCH", "detail": "Alert payload queued for QA Supervisor", "latency_ms": 208 }
  ]
}

```

## 5. 6-Slice Incremental Build Checklist (Prompt One Slice at a Time)

- **Slice 1 (Standalone Engine):** Build `backend/engine/` scripts and verify via CLI (`python -m backend.engine.pipeline`) using `sample_data/case_02_spoiled_batch`.
- **Slice 2 (API & Schema):** Build `backend/models.py` and `backend/main.py` exposing `POST /api/v1/verify` and `GET /api/v1/history`.
- **Slice 3 (UI Shell):** Generate the 3-column workbench in `frontend/src/` wired to a static copy of the Section 4 JSON response.
- **Slice 4 (End-to-End Integration):** Connect `frontend/src/lib/api.ts` to live FastAPI backend.
- **Slice 5 (Preset Switcher):** Wire the 3 sidebar demo presets so clicking any preset runs the real backend pipeline in one click.
- **Slice 6 (SQLite Audit Log):** Persist every run to `audit_logs.db` and populate the bottom history table.

````

---

## Part 2: The Starter UI Prompt (Linear / Vercel Workbench Style)

Never waste hackathon hours building a marketing landing page with a "Get Started" hero section—judges want to jump straight into the working tool. Copy and paste this exact prompt into **v0.dev**, **Bolt.new**, **Cursor Composer**, or **Antigravity** to generate an executive-grade engineering interface on the first try:

```text
Build a single-screen, high-craft technical workbench dashboard in Next.js (App Router, TypeScript, Tailwind CSS, lucide-react, shadcn/ui) styled after Linear, Vercel, and Raycast. 

STRICT VISUAL RULES:
- DO NOT create a marketing landing page, hero banner, or pricing section. Open directly into the operational workbench.
- Color Palette: Deep carbon dark mode (`bg-zinc-950` background, `bg-zinc-900/50` elevated cards, crisp `1px` borders using `border-zinc-800`, subtle hover states `hover:bg-zinc-900`).
- Zero neon purple/blue AI gradients. Use restrained semantic status colors ONLY for badges and indicators: Emerald (`text-emerald-400 border-emerald-500/30 bg-emerald-500/10`) for healthy/passed, Amber for warnings, Rose (`text-rose-400 border-rose-500/30 bg-rose-500/10`) for critical anomalies.
- Typography: Clean sans-serif for headers, tight tracking (`tracking-tight`), uppercase muted micro-labels (`text-[11px] font-medium uppercase tracking-wider text-zinc-400`), and `font-mono` for ALL numbers, timestamps, IDs, latency metrics, confidence scores, and logs.

LAYOUT ARCHITECTURE (3-Column Full-Viewport Workbench, `h-screen overflow-hidden flex`):

1. LEFT SIDEBAR (`w-64 border-r border-zinc-800 bg-zinc-950 p-4 flex flex-col justify-between`):
   - Top: Compact brand header with a live pulsing green status dot ("ENGINE ONLINE • v1.4").
   - Middle ("1-Click Judge Presets"): 3 clickable scenario cards ("Case 01: Clean Manifest", "Case 02: Thermal Excursion Alert", "Case 03: OCR Tampered Batch") that trigger the analysis pipeline immediately without requiring manual file browsing.
   - Bottom: System environment specs card (`Model: YOLOv8-Quant + IsolationForest`, `Mode: Edge Local`, `Avg Latency: 410ms`).

2. CENTER WORKBENCH (`flex-1 flex flex-col overflow-y-auto p-6 space-y-6`):
   - Top KPI Strip (4 compact metric cards in a grid): "Audit Status" (Critical/Passed badge), "Composite Risk Score" (`88/100` in large `font-mono`), "End-to-End Latency" (`642ms`), and "Confidence Score" (`97.4%`).
   - Main Split View:
     - Left Half: Input Source & Annotated Evidence Panel showing the uploaded document/image or sensor waveform with toggleable bounding-box overlays and extracted key-value metadata table.
     - Right Half: Structured Anomaly Breakdown cards showing severity badges, exact threshold violations, and a "Dispatch Webhook Alert" action button with real-time confirmation state.
   - Bottom Table: Compact "Recent Audit Ledger" showing previous runs with `font-mono` Audit IDs, timestamps, status pills, and latency.

3. RIGHT TELEMETRY DRAWER (`w-80 border-l border-zinc-800 bg-zinc-950 flex flex-col`):
   - Header with two tabs: "Live Execution Trace" and "Raw JSON Payload".
   - "Live Execution Trace" Tab: A terminal-style vertical timeline showing each backend pipeline step (`INGEST`, `OCR_EXTRACT`, `ISOLATION_FOREST`, `WEBHOOK_DISPATCH`), its duration in milliseconds (`284ms`), and a visual progress bar showing percentage of total execution time.
   - "Raw JSON Payload" Tab: A scrollable, syntax-highlighted `font-mono text-xs` inspector displaying the exact response object returned by the API.

Include complete, realistic state management so clicking any of the 3 Left Sidebar presets simulates a 600ms step-by-step loading sequence in the Telemetry Drawer and updates all Center Workbench metrics and tables dynamically.

````

### Why This Specific Prompt Wins Judges Over

- **The "1-Click Judge Presets" in the Sidebar:** During live judging, file upload dialogs often freeze or you fumble looking for a test image on your desktop. Having 3 pre-loaded real test scenarios in the sidebar lets you demonstrate normal, warning, and critical edge cases in 5 seconds flat.
- **The Right Telemetry Drawer:** It makes invisible backend Python logic visually undeniable. Judges can literally see the millisecond breakdown of your OCR and anomaly detection steps alongside the raw JSON contract.

## Part 3: The Ideal 24-Hour Git & 4-Person Team Split Workflow

Hackathon teams lose at Hour 20 because everyone edits the same files, creating a massive Git merge conflict right before submission. Solve this with two rules: **Strict Directory Ownership** and **The Hour-2 JSON Contract Lock**.

### 1. The Directory Ownership Law (Zero Merge Conflicts)

Assign every teammate a dedicated folder from `SPEC.md`. **No teammate is allowed to edit a file outside their assigned directory.**

| Teammate Role                     | Owns Directory                           | Never Touches                    | Primary Responsibility                                                                                                 |
| --------------------------------- | ---------------------------------------- | -------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **1. Core AI / Engine Lead**      | `/backend/engine/`                       | `/frontend/`, `main.py`          | Builds pure Python functions that take an input file/dict and return a Python dict matching `SPEC.md`.                 |
| **2. Backend & API Lead**         | `/backend/main.py`, `models.py`, `db.py` | `/backend/engine/`, `/frontend/` | Wraps Member 1's functions into FastAPI endpoints, handles CORS, SQLite persistence, and webhooks.                     |
| **3. Frontend Workbench Lead**    | `/frontend/src/`                         | `/backend/`                      | Builds the 3-column UI workbench and wires API calls against the locked JSON schema in `SPEC.md`.                      |
| **4. Product, Data & Pitch Lead** | `/sample_data/`, `/docs/`, Slides        | Application code                 | Curates 3 real-world test datasets, records fallback demo GIFs, builds the architecture diagram, and writes the pitch. |

### 2. The "Hour-2 JSON Contract Lock" (How to Build in Parallel)

Normally, the Frontend developer sits idle for 10 hours waiting for the Backend developer to finish the API.

- **At Hour 2:** The whole team spends 15 minutes agreeing on the exact JSON response inside `SPEC.md` (Section 4 above).
- **Hours 2 to 12:**
  - The **Frontend Lead** pastes that exact JSON into `frontend/src/lib/mockPayload.json` and builds the entire UI around it.
  - The **Backend & Engine Leads** write Python code whose sole job is to output that exact same JSON structure.
- **At Hour 12:** You swap `mockPayload.json` for `fetch("http://localhost:8000/api/v1/verify")`. Because both sides built to the exact same contract, the frontend and backend snap together in 10 minutes with zero refactoring.

### 3. The 24-Hour Execution Timetable

| Time Window     | Milestone                             | What Must Be Working Before Moving On                                                                                          |
| --------------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **Hours 0–2**   | **Deconstruct & Lock&#x20;**`SPEC.md` | Problem bottleneck defined; `SPEC.md` committed to `main`; API JSON contract locked.                                           |
| **Hours 2–8**   | **Isolated Core Build**               | **Engine:** Runs in terminal on 1 real file. **Frontend:** 3-column workbench renders static JSON cleanly.                     |
| **Hours 8–12**  | **API Wrapping & Real Presets**       | FastAPI returns the locked JSON via Swagger UI (`/docs`); Member 4 finishes 3 real demo datasets in `/sample_data/`.           |
| **Hours 12–15** | **The First Integration Sync**        | Frontend connects to live FastAPI locally. Clicking "Preset 1" in the UI runs the real Python engine end-to-end.               |
| **Hours 15–19** | **Telemetry & Edge Polish**           | Live execution trace streaming added; webhook/WhatsApp alert trigger wired; SQLite audit history working.                      |
| **Hours 19–21** | **Code Freeze & Fallback Video**      | **STOP ADDING FEATURES.** Record a 90-second raw screen capture of the working Golden Path as insurance against Wi-Fi failure. |
| **Hours 21–24** | **Pitch Rehearsal & Q&A Prep**        | Rehearse the 3-minute demo transitions 5 times aloud; prepare answers for scale, latency, and security questions.              |

### 4. The 4-Command Git Playbook for Hackathons

Do not use complex Gitflow with `develop`, `staging`, and PR review queues during a 24-hour sprint. Use **Short-Lived Role Branches**:

1. **Create one branch per role at Hour 2:**

   **Bash**
   ```
   git checkout -b feat/engine    # Member 1
   git checkout -b feat/api       # Member 2
   git checkout -b feat/ui        # Member 3

   ```
2. **Commit every working vertical slice (every 60–90 minutes):**

   **Bash**
   ```
   git add . && git commit -m "slice: working OCR batch ID extractor"

   ```
3. **Sync with&#x20;**`main`**&#x20;every 4 hours (Because everyone owns separate folders, this will auto-merge cleanly):**

   **Bash**
   ```
   git checkout main && git pull origin main
   git checkout feat/engine && git merge main

   ```
4. **Never deploy for the first time at Hour 23:** Either deploy at Hour 14, or run your demo locally on `localhost` during judging using **ngrok / Cloudflare Tunnel** if you need external webhook callbacks. Judges care 100x more about a fast, crash-free live demo on your laptop than a slow cloud deployment that times out on venue Wi-Fi.

Want me to customize this SPEC.md for a specific hackathon problem statement you have?

Yes

Gemini is AI and can make mistakes.