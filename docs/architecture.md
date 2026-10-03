# CodePilot Architecture Documentation

CodePilot is built with strict separation of concerns, decoupling UI presentation, API handling, business logic, persistence, and AI orchestration.

```
┌─────────────────────────────────────────────────────────────┐
│                       React + Vite UI                       │
│  Tailwind CSS • Lucide Icons • Fira Code • Responsive Dark  │
└──────────────────────────────┬──────────────────────────────┘
                               │  REST API (JSON & Multipart)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI API Routers                      │
│   Auth • Profile • Code • Knowledge • Vault • Chat • Plan   │
└──────────────────────────────┬──────────────────────────────┘
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
┌──────────────────────────────┐    ┌──────────────────────────────┐
│        Service Layer         │    │      AI Orchestrator         │
│  KnowledgeService • Vault    │    │  BaseAIProvider Abstraction  │
│  CodeService • PlanService   │    │  Ollama ◄──► Local Fallback  │
└──────────────┬───────────────┘    └──────────────┬───────────────┘
               │                                   │
               │         Personal Context          │
               │◄──────────────────────────────────┘
               │
┌──────────────▼───────────────┐
│     SQLAlchemy ORM Layer     │
│   User • KnowledgeConcept    │
│   VaultItem • CodeAnalysis   │
└──────────────┬───────────────┘
               │
┌──────────────▼───────────────┐
│       SQLite Database        │
│   (Migratable to Postgres)   │
└──────────────────────────────┘
```

## Layer Descriptions

1. **Frontend (React 18 + Vite)**:
   - Modular pages and reusable design system tokens.
   - Centralized `api.js` client handling JWT authentication tokens and error normalization.
   - Global `QuickCaptureModal` accessible anywhere to eliminate note capture friction.
   - High-contrast developer-grade theme inspired by modern tools like Linear and GitHub.

2. **API Layer (FastAPI)**:
   - Strong schema validation using Pydantic v2.
   - Dependency injection for authentication (`get_current_user`) and role-based authorization (`get_current_admin`).
   - Exception filtering to return clean JSON error payloads.

3. **Service Layer**:
   - `KnowledgeService`: Evidence-driven state machine managing concept confidence and transitions (`NOT_STARTED` -> `LEARNING` -> `PRACTICED` -> `STRONG` -> `NEEDS_REVISION`).
   - `VaultService`: Full second-brain indexing, multi-type storage (notes, formulas, code, links, documents), and grounded Q&A.
   - `CodeService`: Submissions evaluation, Big-O calculation, progressive hints, and automated memory updating.
   - `PlanService`: Generates and manages 15-20 min/day adaptive weekly learning tasks.
   - `CareerService`: Skill gap calculation and portfolio recommendations.

4. **Persistence Layer**:
   - SQLAlchemy with SQLite for immediate local zero-config startup.
   - Clean relationships with cascade deletion and user data isolation.
