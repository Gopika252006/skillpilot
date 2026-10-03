# CodePilot AI Architecture & Open Innovation

## 1. Provider Abstraction

CodePilot interacts with open-weight models through a unified `BaseAIProvider` interface:

```python
class BaseAIProvider(ABC):
    def analyze_code(self, problem_title, problem_statement, language, user_code, user_context) -> Dict
    def answer_question(self, message, user_context) -> Dict
    def extract_concepts(self, text) -> List[str]
    def generate_weekly_plan(self, user_context) -> Dict
    def evaluate_assessment(self, questions, answers, user_context) -> Dict
    def evaluate_interview_answer(self, question, user_answer, user_context) -> Dict
    def generate_career_analysis(self, user_context) -> Dict
    def analyze_vault_item(self, title, content, content_type) -> Dict
    def ask_vault_document(self, document_content, question) -> Dict
```

## 2. Supported Runtimes

1. **Ollama Provider (`OllamaProvider`)**:
   - Calls the local Ollama daemon at `http://localhost:11434`.
   - Uses local open-weight models such as `llama3.2:3b`, `qwen2.5-coder:7b`, `mistral`, or `deepseek-r1`.
   - Enforces structured JSON output via `format: "json"`.
   - Configurable timeout and automatic retry logic.

2. **Local Fallback Engine (`FallbackInferenceEngine`)**:
   - AST and algorithmic pattern detector.
   - Calculates time & space complexity, detects recursion, boundary invariants, hash-based lookups, two-pointers, sliding windows, and dynamic programming patterns.
   - Generates progressive hints (structural direction, invariant hint, deeper explanation, and optimal solution).
   - Ensures the entire product functions offline with zero runtime errors.

3. **AI Orchestrator (`AIOrchestrator`)**:
   - Manages graceful failover: Attempts local Ollama first; if unreachable, falls back to the deterministic local inference engine and sets `ai_model_used` indicator.

## 3. Grounding & Personal Context Assembly

Every query to the AI is augmented with the user's personal technical history:

```
[USER PERSONAL TECHNICAL PROFILE]
* Target Role: Backend Software Engineer (Intermediate)
* Core Interests: DSA, System Design, Backend, Distributed Systems
* Known Strong Areas: Binary Search (88%), Sliding Window (82%)
* Current Revision Focus: Dynamic Programming State Transitions (54%)
* Recurring Blind Spots: Off-by-one boundary handling in 2D memo tables
* Recent Problems Analyzed: Search in Rotated Sorted Array, Longest Substring
```

This guarantees answers are **never generic**, but explicitly reference what the user has previously practiced and where they struggle.
