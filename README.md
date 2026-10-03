# CodePilot — “An AI that knows what you know.”

> **DEV.to Hacktoberfest Weekend Challenge 2026 — “Build for a Friend” Submission**  
> A private personal technical AI companion & personal second brain that learns from a developer's voluntarily provided coding and learning activity.

---

## 💡 The Real Friend & The Problem

CodePilot was built specifically for **Arjun**, a real friend and dedicated software engineer.

Arjun is already a disciplined, high-consistency learner:
- He solves LeetCode problems daily.
- He competes in algorithmic coding contests.
- He reads system design blogs, watches tech talks, and studies backend architectures.

**The Problem Was NOT "He needs to be told to study":**  
Arjun already puts massive effort into his technical craft. But his knowledge, contest submissions, boundary mistake patterns, scattered notes, saved formulas, and career preparation **were completely disconnected**. 

Whenever he studied outside (a YouTube video on Kafka, a college lecture on B+ Trees, or a PDF on distributed consensus), that knowledge lived in random desktop folders or browser bookmarks, completely invisible to any AI assistant he consulted later.

**CodePilot solves this by turning:**  
$$\text{LEARNING} \longrightarrow \text{PRACTICE} \longrightarrow \text{KNOWLEDGE MEMORY} \longrightarrow \text{FEEDBACK} \longrightarrow \text{CAREER GROWTH}$$

---

## 🌟 Core Pillars & Key Features

### 1. Personal Technical Memory (Core Differentiator)
Unlike generic chatbots with zero memory of your coding history, CodePilot maintains a private **Personal Knowledge Graph** with evidence-driven confidence states:
- `NOT_STARTED`
- `LEARNING`
- `PRACTICED`
- `STRONG`
- `NEEDS_REVISION`

Knowledge states **never** update from AI fluff; they update strictly from **verified evidence**: code submissions to the Code Analyzer, assessment outcomes, and logged study sessions. It tracks practice counts, moving-average success rates, and **repeated mistakes** (e.g., off-by-one boundary conditions in 2D memo tables).

### 2. Code Analyzer (Hero Feature)
Submit any problem and solution in **Python, Java, C++, or JavaScript**:
- Identifies approach and Big-O Time & Space complexity.
- Evaluates code quality (1-10) and boundary edge-case handling.
- **Progressive Learning Hints**: Does *not* dump optimal solutions immediately. Provides **Hint 1 (Structural)**, **Hint 2 (Algorithmic Invariant)**, **Deeper Breakdown**, and **Optional Optimal Formulation** on demand.
- **Instant Memory Feedback**: Automatically updates Personal Technical Memory with detected concepts and mistake warnings.

### 3. Knowledge Vault (Personal Technical Second Brain)
Whenever you learn outside CodePilot, capture it in seconds:
- **Rich Content Types**: Notes, Documents (PDF, Markdown, TXT), Diagrams & Architecture Screenshots, Mathematical Formulas (LaTeX / Master Theorem), Code Snippets, and Curated Links.
- **Quick Capture Action**: Global `+ Quick Capture` modal accessible anywhere.
- **Grounded "Ask This Document"**: Query your uploaded PDF or notes; answers are strictly grounded in your saved material with cited excerpts.
- **Smart Revision Integration**: When the system detects a concept marked `NEEDS_REVISION`, it highlights matching saved reference materials ready for review.

### 4. Ask My AI (Context-Aware Technical Companion)
A personal technical companion grounded in your verified technical memory.
- Uses your target role, strong skills, weak concepts, recent code analyses, and active weekly focus.
- Displays explicit **Personal Context Badges** on responses (e.g., *“Target: Backend Software Engineer”*, *“DSA History: Sliding Window & Binary Search”*).

### 5. Adaptive Weekly Plan & Weekend Assessment
- **15-20 Min / Day Mission**: Monday-style daily tasks targeting your specific knowledge gaps without causing burnout.
- **Adaptive Weekend Test**: 5-question targeted assessment evaluating retention. Scoring feeds directly back into Personal Technical Memory to adapt next week's focus.

### 6. Career Path & Skill Gap Intelligence
- Compares proven skills vs your target role (e.g. *Backend Software Engineer*).
- Identifies missing high-yield skills (Distributed Caching, Kafka, System Scalability).
- Recommends tailored portfolio projects and strategic certifications with clear rationale.

### 7. Aptitude Sprint & Mock Verbal Interview
- **Aptitude Sprint**: 5 daily questions across Quantitative, Logical, and Verbal reasoning with instant explanations.
- **Adaptive Interview**: 3-question mock verbal session assessing clarity, algorithmic depth, and follow-up trade-offs.

---

## 🛡️ Why Open Innovation Matters

CodePilot puts **Open-Weight AI at its core** for four fundamental reasons:

1. **Absolute Data Privacy**: A developer's proprietary code, weak areas, and interview prep notes never leave their machine. Zero telemetry, zero closed-API retention.
2. **Zero Recurring Toll**: Consistent developers solve dozens of problems weekly. Open models running locally via Ollama avoid per-token billing and rate limits.
3. **Model Replaceability**: Decoupled AI Orchestrator supports hot-swapping between **Llama 3.2 3B**, **Qwen 2.5 Coder 7B**, **Mistral 7B**, or **DeepSeek R1 Distill**.
4. **Offline Resilience**: Learn on planes, trains, or during hackathons without active internet.

---

## 🏗️ Architecture

```
codepilot/
├── backend/
│   ├── app/
│   │   ├── api/          # REST Endpoints (Auth, Code, Knowledge, Vault, Chat, Plan, etc.)
│   │   ├── core/         # Config, Database engine, Security & JWT
│   │   ├── models/       # SQLAlchemy models (User, KnowledgeConcept, VaultItem, etc.)
│   │   ├── schemas/      # Pydantic v2 validation schemas
│   │   ├── ai/           # OllamaProvider, FallbackInferenceEngine, AIOrchestrator
│   │   ├── services/     # KnowledgeEngine, CodeService, VaultService, etc.
│   │   ├── storage/      # Secure file storage with path-traversal prevention
│   │   └── main.py       # FastAPI application
│   ├── tests/            # Automated pytest suite (Auth, User Isolation, Code Analyzer)
│   └── seed_demo.py      # Seed script for Arjun Sharma demo profile
│
├── frontend/
│   ├── src/
│   │   ├── components/   # Layout, QuickCaptureModal, Sidebar, Header
│   │   ├── context/      # AuthContext, ToastContext
│   │   ├── pages/        # Dashboard, CodeAnalyzer, KnowledgeVault, MyKnowledge, etc.
│   │   ├── services/     # Centralized API fetch abstraction
│   │   └── App.jsx       # Route tree
│   └── package.json
└── docs/                 # Architecture, AI Engine, Database, Security guides
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- **Python 3.10+**
- **Node.js 18+** & **npm**
- *(Optional for full local open weights)*: [Ollama](https://ollama.com/) running `ollama run llama3.2:3b`.  
  *(Note: If Ollama is offline, CodePilot's built-in Local Inference Engine seamlessly handles all requests with zero downtime!)*

### 2. Backend Setup
```bash
cd backend
python -m pip install -r requirements.txt
# Or: pip install fastapi uvicorn sqlalchemy pydantic python-jose bcrypt requests

# Seed the demo database with Arjun's profile
python seed_demo.py

# Run the test suite
python -m pytest tests

# Start backend server
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```
API Documentation will be live at: `http://127.0.0.1:8000/docs`

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```
Open your browser at: `http://127.0.0.1:5173`

---

## 🔑 Demo Credentials (Instant Reviewer Access)

On the login page, click the prominent **"Login as Arjun (Friend Profile)"** button, or enter:
- **Email:** `demo@codepilot.dev`
- **Password:** `Demo1234!`

To inspect the minimal Admin Portal:
- **Email:** `admin@codepilot.dev`
- **Password:** `Admin1234!`

---

## 🧪 Testing Checklist & Verification

| Module | Verification | Status |
|---|---|---|
| **Authentication** | Registration, Login, JWT verification, PBKDF2/bcrypt hashing | ✅ Verified |
| **User Data Isolation** | User A cannot query or read User B's vault items or private code | ✅ Tested (`test_isolation.py`) |
| **Admin Authorization** | Non-admin users are strictly rejected with 403 Forbidden | ✅ Tested |
| **Code Analyzer** | Big-O detection, boundary bug alerts, progressive hints | ✅ Verified |
| **Knowledge Engine** | Evidence-driven confidence update and state transitions | ✅ Verified |
| **Knowledge Vault** | Multi-type capture, search, grounded "Ask This", AI actions | ✅ Verified |
| **Ask My AI** | Context-grounded technical companion with visible badge tags | ✅ Verified |
| **Weekly Plan** | 15-20 min/day adaptive tasks with interactive completion toggles | ✅ Verified |
| **Assessment** | 5-question adaptive quiz with scoring & feedback loop | ✅ Verified |
| **Career Path** | Target role alignment, readiness score, high-value projects | ✅ Verified |
| **Open AI Health** | Live inference runtime diagnostics and zero-telemetry guarantee | ✅ Verified |

---

## 👥 Hackathon Submission Details

- **Hackathon:** DEV.to Hacktoberfest Weekend Challenge 2026 — *“Build for a Friend”*
- **Project Name:** CodePilot
- **Tagline:** *“An AI that knows what you know.”*
- **Built With:** React, Tailwind CSS, Vite, FastAPI, SQLAlchemy, SQLite, Ollama / Local Open-Weight Inference Engine.
