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

## 2. Supported Runtimes & Output Validation

1. **Ollama Provider (`OllamaProvider`)**:
   - Calls the local Ollama daemon at `http://localhost:11434`.
   - Uses local open-weight models such as `llama3.2:3b`, `qwen2.5-coder:7b`, `mistral`, or `deepseek-r1`.
   - Enforces structured JSON output via `format: "json"`.
   - **Socket Probe Liveness**: Evaluates availability via an instant 150ms raw TCP socket probe cached for 5 seconds to eliminate thread blocking when Ollama is offline.

2. **Deterministic Rule-Based Fallback Engine (`FallbackInferenceEngine`)**:
   - A robust deterministic AST and pattern analyzer.
   - Calculates time & space complexity, detects recursion, boundary invariants, hash-based lookups, two-pointers, sliding windows, and dynamic programming patterns.
   - Generates progressive hints (structural direction, invariant hint, deeper explanation, and optimal solution).
   - Ensures the entire product functions completely offline with zero runtime errors.
   - *Note: The fallback engine is deterministic and rule-based; it is never mislabeled as an open-weight model.*

3. **AI Orchestrator (`AIOrchestrator`)**:
   - Manages graceful failover and schema validation:
     ```text
     LLM output -> JSON parsing -> Schema validation -> Safe fallback on invalid schema -> Business logic
     ```
   - If the open-weight model produces malformed or incomplete output, the orchestrator logs a warning and falls back cleanly to the rule-based engine, guaranteeing that malformed AI output can never corrupt the database or application state.

## 3. Grounding & Personal Context Assembly

Every query to the AI is augmented with the user's personal technical history:

```text
[USER PERSONAL TECHNICAL PROFILE]
* Target Role: Backend Software Engineer (Intermediate)
* Core Interests: DSA, System Design, Backend, Distributed Systems
* Known Strong Areas: Binary Search (88%), Sliding Window (82%)
* Current Revision Focus: Dynamic Programming State Transitions (54%)
* Recurring Blind Spots: Off-by-one boundary handling in 2D memo tables
* Recent Problems Analyzed: Search in Rotated Sorted Array, Longest Substring
```

This guarantees answers are **never generic**, but explicitly reference what the user has previously practiced and where they struggle.
