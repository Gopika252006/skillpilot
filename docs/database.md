# CodePilot Database Schema

CodePilot uses a normalized relational schema with foreign key cascades and user isolation indexes.

## Core Tables

### 1. `users`
- `id` (INTEGER, PK)
- `email` (VARCHAR, UNIQUE, INDEX)
- `hashed_password` (VARCHAR)
- `full_name` (VARCHAR)
- `role` (VARCHAR, default "USER")
- `is_active` (BOOLEAN, default TRUE)
- `created_at` (DATETIME)

### 2. `user_profiles`
- `id` (INTEGER, PK)
- `user_id` (INTEGER, FK -> users.id, UNIQUE, CASCADE)
- `target_role` (VARCHAR)
- `experience_level` (VARCHAR)
- `learning_goals` (TEXT)
- `weekly_hours` (INTEGER)
- `current_technologies` (JSON TEXT)
- `interests` (JSON TEXT)
- `onboarding_completed` (BOOLEAN)

### 3. `knowledge_concepts`
- `id` (INTEGER, PK)
- `user_id` (INTEGER, FK -> users.id, INDEX, CASCADE)
- `name` (VARCHAR, INDEX)
- `category` (VARCHAR, INDEX)
- `parent_concept` (VARCHAR)
- `status` (VARCHAR: NOT_STARTED, LEARNING, PRACTICED, STRONG, NEEDS_REVISION)
- `confidence` (FLOAT: 0.0 - 1.0)
- `practice_count` (INTEGER)
- `success_rate` (FLOAT)
- `repeated_mistakes` (JSON TEXT)
- `related_concepts` (JSON TEXT)
- `last_practiced` (DATETIME)
- `last_revised` (DATETIME)
- *Constraint:* UNIQUE(`user_id`, `name`)

### 4. `code_analyses`
- `id` (INTEGER, PK)
- `user_id` (INTEGER, FK -> users.id, INDEX, CASCADE)
- `problem_title` (VARCHAR)
- `language` (VARCHAR)
- `user_code` (TEXT)
- `approach_detected` (VARCHAR)
- `is_correct` (BOOLEAN)
- `time_complexity` (VARCHAR)
- `space_complexity` (VARCHAR)
- `code_quality_score` (INTEGER)
- `concepts_detected` (JSON TEXT)
- `strengths` (JSON TEXT)
- `improvements` (JSON TEXT)
- `hint_1` (TEXT)
- `hint_2` (TEXT)
- `deeper_explanation` (TEXT)
- `optimized_approach` (TEXT)

### 5. `knowledge_vault_items`
- `id` (INTEGER, PK)
- `user_id` (INTEGER, FK -> users.id, INDEX, CASCADE)
- `content_type` (VARCHAR: note, document, image, formula, code, link)
- `title` (VARCHAR)
- `content` (TEXT)
- `file_path` (VARCHAR)
- `folder` (VARCHAR, INDEX)
- `topic` (VARCHAR, INDEX)
- `tags` (JSON TEXT)
- `extracted_concepts` (JSON TEXT)
- `ai_summary` (TEXT)
- `is_favorite` (BOOLEAN)
- `is_archived` (BOOLEAN)

### 6. `weekly_plans` & `weekly_tasks`
- `weekly_plans`: `id`, `user_id`, `week_title`, `focus_area`, `rationale`, `is_active`
- `weekly_tasks`: `id`, `plan_id` (FK), `day_of_week`, `title`, `description`, `target_concept`, `estimated_minutes`, `is_completed`, `completed_at`

### 7. `assessments`
- `id`, `user_id`, `title`, `topics`, `questions`, `user_answers`, `score`, `feedback_summary`, `strong_areas`, `weak_areas`, `status`

### 8. `chat_messages`
- `id`, `user_id`, `role`, `content`, `context_used`, `created_at`
