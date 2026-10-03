import os
import sys
from datetime import datetime, timedelta

# Add backend directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models.models import (
    User, UserProfile, KnowledgeConcept, CodeAnalysis, KnowledgeVaultItem,
    WeeklyPlan, WeeklyTask, Assessment, ChatMessage, CareerProfile, AptitudeAttempt
)
from app.services.assessment_service import QUESTION_BANK
from app.services.aptitude_service import APTITUDE_DAILY_QUESTIONS

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    print("Checking existing data...")
    existing_user = db.query(User).filter(User.email == "demo@codepilot.dev").first()
    if existing_user:
        print("Demo data already seeded. Skipping.")
        db.close()
        return

    print("Seeding demo friend user: Arjun Sharma (demo@codepilot.dev)...")
    demo_user = User(
        email="demo@codepilot.dev",
        hashed_password=get_password_hash("Demo1234!"),
        full_name="Arjun Sharma (Demo Profile)",
        role="USER",
        is_active=True
    )
    db.add(demo_user)
    db.commit()
    db.refresh(demo_user)

    # Admin User
    admin_user = User(
        email="admin@codepilot.dev",
        hashed_password=get_password_hash("Admin1234!"),
        full_name="System Administrator",
        role="ADMIN",
        is_active=True
    )
    db.add(admin_user)
    db.commit()

    # User Profile
    profile = UserProfile(
        user_id=demo_user.id,
        target_role="Backend Software Engineer",
        experience_level="Intermediate",
        learning_goals="Targeting Senior Backend roles. Mastering advanced DP state transitions, distributed caching, and Kafka streaming pipelines.",
        weekly_hours=8,
        onboarding_completed=True
    )
    profile.current_technologies = ["Python", "Java", "PostgreSQL", "Redis", "Docker"]
    profile.interests = ["DSA", "System Design", "Backend", "Distributed Systems"]
    db.add(profile)

    # Personal Technical Memory Concepts (Evidence-driven)
    concepts_data = [
        {
            "name": "Binary Search",
            "category": "DSA",
            "status": "STRONG",
            "confidence": 0.88,
            "practice_count": 14,
            "success_rate": 0.86,
            "mistakes": ["Potential integer overflow with (low + high) / 2 in 32-bit runtimes"],
            "related": ["Arrays", "Boundary Invariants"]
        },
        {
            "name": "Sliding Window",
            "category": "DSA",
            "status": "STRONG",
            "confidence": 0.82,
            "practice_count": 9,
            "success_rate": 0.80,
            "mistakes": ["Shrinking window condition check before updating global max"],
            "related": ["Arrays", "Two Pointers"]
        },
        {
            "name": "Dynamic Programming",
            "category": "DSA",
            "status": "NEEDS_REVISION",
            "confidence": 0.54,
            "practice_count": 7,
            "success_rate": 0.57,
            "mistakes": [
                "Off-by-one boundary on memoization table initialization",
                "Incorrect state recurrence for 2D knapsack variants"
            ],
            "related": ["Recursion", "Memoization", "Optimal Substructure"]
        },
        {
            "name": "Graph BFS/DFS",
            "category": "DSA",
            "status": "PRACTICED",
            "confidence": 0.70,
            "practice_count": 8,
            "success_rate": 0.75,
            "mistakes": ["Tracking visited nodes at push time vs pop time in BFS queue"],
            "related": ["Graphs", "Queue"]
        },
        {
            "name": "System Design",
            "category": "System Design",
            "status": "LEARNING",
            "confidence": 0.50,
            "practice_count": 4,
            "success_rate": 0.60,
            "mistakes": ["Overlooking single point of failure in load balancer topology"],
            "related": ["Caching", "Load Balancing"]
        },
        {
            "name": "Caching",
            "category": "System Design",
            "status": "LEARNING",
            "confidence": 0.52,
            "practice_count": 4,
            "success_rate": 0.65,
            "mistakes": ["Cache stampede / thundering herd mitigation under traffic spikes"],
            "related": ["System Design", "Hash Table"]
        },
        {
            "name": "Kafka",
            "category": "Backend",
            "status": "LEARNING",
            "confidence": 0.42,
            "practice_count": 3,
            "success_rate": 0.50,
            "mistakes": ["Consumer group rebalance lag during heavy batching"],
            "related": ["Distributed Systems"]
        }
    ]

    for c in concepts_data:
        concept = KnowledgeConcept(
            user_id=demo_user.id,
            name=c["name"],
            category=c["category"],
            status=c["status"],
            confidence=c["confidence"],
            practice_count=c["practice_count"],
            success_rate=c["success_rate"],
            last_practiced=datetime.utcnow() - timedelta(days=2)
        )
        concept.repeated_mistakes = c["mistakes"]
        concept.related_concepts = c["related"]
        db.add(concept)

    # Code Analyses History
    analyses = [
        {
            "title": "Search in Rotated Sorted Array",
            "lang": "java",
            "code": """public int search(int[] nums, int target) {\n    int low = 0, high = nums.length - 1;\n    while (low <= high) {\n        int mid = low + (high - low) / 2;\n        if (nums[mid] == target) return mid;\n        if (nums[low] <= nums[mid]) {\n            if (target >= nums[low] && target < nums[mid]) high = mid - 1;\n            else low = mid + 1;\n        } else {\n            if (target > nums[mid] && target <= nums[high]) low = mid + 1;\n            else high = mid - 1;\n        }\n    }\n    return -1;\n}""",
            "approach": "Modified Binary Search with Sorted Half Detection",
            "time": "O(log n)",
            "space": "O(1)",
            "score": 9,
            "concepts": ["Binary Search", "Divide and Conquer", "Boundary Invariants"]
        },
        {
            "title": "Longest Substring Without Repeating Characters",
            "lang": "python",
            "code": """def lengthOfLongestSubstring(s: str) -> int:\n    char_map = {}\n    left = 0\n    max_len = 0\n    for right, char in enumerate(s):\n        if char in char_map and char_map[char] >= left:\n            left = char_map[char] + 1\n        char_map[char] = right\n        max_len = max(max_len, right - left + 1)\n    return max_len""",
            "approach": "Sliding Window with Hash Map Index Pointer",
            "time": "O(n)",
            "space": "O(min(m, n))",
            "score": 9,
            "concepts": ["Sliding Window", "Two Pointers", "Hash Table"]
        },
        {
            "title": "Coin Change 2 (Combination Count)",
            "lang": "python",
            "code": """def change(amount: int, coins: list[int]) -> int:\n    dp = [0] * (amount + 1)\n    dp[0] = 1\n    for coin in coins:\n        for x in range(coin, amount + 1):\n            dp[x] += dp[x - coin]\n    return dp[amount]""",
            "approach": "1D Tabulation Dynamic Programming",
            "time": "O(amount * len(coins))",
            "space": "O(amount)",
            "score": 8,
            "concepts": ["Dynamic Programming", "Optimal Substructure", "State Transition"]
        }
    ]

    for a in analyses:
        analysis_record = CodeAnalysis(
            user_id=demo_user.id,
            problem_title=a["title"],
            language=a["lang"],
            user_code=a["code"],
            approach_detected=a["approach"],
            is_correct=True,
            time_complexity=a["time"],
            space_complexity=a["space"],
            code_quality_score=a["score"],
            code_quality_summary=f"Strong, idiomatic {a['lang']} solution demonstrating optimal asymptotic boundaries.",
            hint_1="Review edge cases with empty or single-element inputs.",
            hint_2="Confirm state transition preserves non-negative invariants.",
            deeper_explanation=f"Achieves optimal {a['time']} time complexity while keeping space tightly bounded at {a['space']}.",
            optimized_approach=f"Canonical {a['approach']} pattern with minimal auxiliary space."
        )
        analysis_record.concepts_detected = a["concepts"]
        analysis_record.strengths = [f"Optimal {a['time']} complexity", "Concise state update"]
        analysis_record.improvements = ["Consider adding explicit boundary assertions"]
        analysis_record.optimization_suggestions = ["Benchmark with maximum constraint inputs"]
        analysis_record.suggested_concepts = a["concepts"]
        db.add(analysis_record)

    # Knowledge Vault Pre-seeded Items
    vault_items = [
        {
            "type": "note",
            "title": "JWT Architecture & Stateless Revocation Strategies",
            "content": """JWT consists of Header, Payload, and Signature (HMAC-SHA256 or RSA).
Best practices for stateless session management:
1. Short-lived Access Token (15-30 mins).
2. Long-lived Refresh Token in HttpOnly cookie.
3. For immediate revocation: maintain a Redis bloom filter or lightweight blocklist of revoked jti (JWT IDs) keyed with TTL equal to the remaining token lifetime. This preserves sub-millisecond lookup while avoiding hitting the main relational database.""",
            "topic": "Backend Security",
            "folder": "Backend",
            "tags": ["jwt", "authentication", "redis", "security"],
            "concepts": ["JWT", "Redis", "Authentication", "System Design"],
            "fav": True
        },
        {
            "type": "formula",
            "title": "Master Theorem for Divide & Conquer Recurrences",
            "content": """Formula: T(n) = a*T(n/b) + f(n)
Case 1: If f(n) = O(n^(log_b(a) - e)) -> T(n) = Theta(n^(log_b(a)))
Case 2: If f(n) = Theta(n^(log_b(a)) * log^k(n)) -> T(n) = Theta(n^(log_b(a)) * log^(k+1)(n))
Case 3: If f(n) = Omega(n^(log_b(a) + e)) -> T(n) = Theta(f(n))

Binary Search: a=1, b=2, f(n)=O(1) -> log_2(1) = 0 -> Case 2 with k=0 -> T(n) = O(log n).
Merge Sort: a=2, b=2, f(n)=O(n) -> log_2(2) = 1 -> Case 2 with k=0 -> T(n) = O(n log n).""",
            "topic": "Algorithms",
            "folder": "DSA",
            "tags": ["algorithms", "time-complexity", "master-theorem"],
            "concepts": ["Time Complexity", "Divide and Conquer", "Binary Search"],
            "fav": True
        },
        {
            "type": "code",
            "title": "Sliding Window Maximum with Monotonic Deque",
            "content": """from collections import deque

def maxSlidingWindow(nums: list[int], k: int) -> list[int]:
    # Deque stores indices of elements in monotonically decreasing order
    q = deque()
    result = []
    
    for i, num in enumerate(nums):
        # Remove elements outside the current window
        while q and q[0] <= i - k:
            q.popleft()
            
        # Maintain monotonic decreasing property
        while q and nums[q[-1]] < num:
            q.pop()
            
        q.append(i)
        
        # Once we've reached at least k elements, add max to result
        if i >= k - 1:
            result.append(nums[q[0]])
            
    return result
# Time Complexity: O(n) - each index pushed/popped at most once
# Space Complexity: O(k) for the deque""",
            "topic": "DSA",
            "folder": "DSA",
            "tags": ["sliding-window", "monotonic-queue", "deque", "python"],
            "concepts": ["Sliding Window", "Queue", "Two Pointers"],
            "fav": False
        },
        {
            "type": "link",
            "title": "Kafka Partition Rebalancing & Consumer Lag Optimization",
            "content": "https://kafka.apache.org/documentation/#design_consumer\nDetailed architectural overview of consumer group rebalance protocols, cooperative sticky assignor, and avoiding heartbeat timeouts under heavy backpressure.",
            "topic": "Distributed Systems",
            "folder": "Backend",
            "tags": ["kafka", "distributed-systems", "streaming"],
            "concepts": ["Kafka", "Distributed Systems", "Concurrency"],
            "fav": False
        }
    ]

    for v in vault_items:
        v_item = KnowledgeVaultItem(
            user_id=demo_user.id,
            content_type=v["type"],
            title=v["title"],
            content=v["content"],
            topic=v["topic"],
            folder=v["folder"],
            is_favorite=v["fav"],
            ai_summary=f"Key technical reference for {v['title']}. Covers complexity bounds and implementation caveats."
        )
        v_item.tags = v["tags"]
        v_item.extracted_concepts = v["concepts"]
        db.add(v_item)

    # Active Weekly Plan
    plan = WeeklyPlan(
        user_id=demo_user.id,
        week_title="Targeted Sprint: Dynamic Programming & Boundary Invariants",
        focus_area="Dynamic Programming & Distributed Caching",
        rationale="Tailored for Arjun: Reinforces DP boundary states where previous mistakes occurred, while advancing Backend Engineer readiness.",
        is_active=True
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)

    plan_tasks = [
        ("Monday", "Revise DP Recurrence & Memo Table Initialization", "Review boundary base cases for 2D DP grids. 15 mins.", "Dynamic Programming", 15, True),
        ("Tuesday", "Solve LeetCode 322 (Coin Change) with Code Analyzer", "Test your solution in Code Analyzer and verify space trade-offs.", "Dynamic Programming", 20, True),
        ("Wednesday", "Inspect Saved Caching Notes in Knowledge Vault", "Read write-through vs cache-aside strategies.", "Caching", 15, False),
        ("Thursday", "Practice 1 Monotonic Queue Problem", "Timed 20-min session to build boundary speed.", "Sliding Window", 20, False),
        ("Friday", "Aptitude Sprint & Placement Preparation", "Complete 5 daily questions across Quant & Logic.", "Aptitude", 15, False),
        ("Saturday", "Adaptive Interview Practice: Distributed Systems", "Explain token bucket rate limiting in the Interview module.", "Technical Interview", 15, False),
        ("Sunday", "Weekend Synthesis Assessment", "Complete 5-question test to evaluate weekly retention.", "Assessment", 20, False),
    ]

    for day, title, desc, concept, mins, done in plan_tasks:
        task = WeeklyTask(
            plan_id=plan.id,
            day_of_week=day,
            title=title,
            description=desc,
            target_concept=concept,
            estimated_minutes=mins,
            is_completed=done,
            completed_at=datetime.utcnow() if done else None
        )
        db.add(task)

    # Weekend Assessment
    assessment = Assessment(
        user_id=demo_user.id,
        title="Weekly Synthesis & Boundary Assessment",
        status="PENDING",
        total_score=100.0
    )
    assessment.topics = ["Binary Search", "Sliding Window", "Dynamic Programming", "System Design", "Caching"]
    assessment.questions = QUESTION_BANK
    assessment.user_answers = {}
    db.add(assessment)

    # Career Profile
    career = CareerProfile(
        user_id=demo_user.id,
        target_role="Backend Software Engineer",
        readiness_score=78.5
    )
    career.strong_skills = ["Binary Search", "Sliding Window", "SQL & Relational DBs", "Java & Python Core", "REST API Architecture"]
    career.gap_skills = ["Distributed Caching (Redis)", "Kafka Event Streaming", "System Scalability & Sharding"]
    career.recommended_actions = [
        {"skill": "Distributed Caching (Redis)", "priority": "High", "why": "Critical differentiator for backend engineering interviews; directly fixes latency bottlenecks."},
        {"skill": "Kafka Partitioning", "priority": "Medium", "why": "Enables decoupled event-driven service design."}
    ]
    career.recommended_projects = [
        {
            "title": "High-Throughput Distributed Rate Limiter",
            "description": "Design an in-memory token bucket rate limiter supporting sliding window counters with Redis and Lua scripts.",
            "skills": ["Distributed Systems", "Redis", "Concurrency"],
            "why": "Proves system scalability and concurrency competence expected in senior backend roles."
        },
        {
            "title": "Event-Driven Log Processing Pipeline",
            "description": "Construct an asynchronous consumer pipeline using Kafka partitions with batch inserts into PostgreSQL.",
            "skills": ["Kafka", "Streaming", "Database Optimization"],
            "why": "Demonstrates practical production-grade data engineering patterns."
        }
    ]
    career.recommended_certifications = [
        {"title": "AWS Certified Solutions Architect - Associate", "why": "Validates cloud infrastructure and managed microservices deployment."},
        {"title": "Confluent Certified Developer for Apache Kafka", "why": "Solidifies streaming pipeline mastery."}
    ]
    db.add(career)

    # Pre-seeded Chat History
    user_chat = ChatMessage(
        user_id=demo_user.id,
        role="user",
        content="Why did my DP solution for Coin Change fail on extreme amounts?"
    )
    user_chat.context_used = []
    
    asst_chat = ChatMessage(
        user_id=demo_user.id,
        role="assistant",
        content="""Looking at your personal DSA profile, you have strong recursive fundamentals (demonstrated in your Tree and Binary Search solutions), but you have recently run into **boundary initialization errors in 2D memo tables**.

For Coin Change with large amounts:
1. **Unreachable State Sentinel**: If you initialize your array with `float('inf')` or a 32-bit sentinel, verify that adding `1 + dp[amount - coin]` does not overflow in languages like Java or C++.
2. **Base Invariant**: `dp[0]` must explicitly equal `0` (zero coins needed to form amount 0), whereas all other positions should start at `amount + 1`.
3. **Space Optimization**: Since each transition only requires the current coin's offset, you can collapse the state into a 1D array rather than allocating an unnecessary `len(coins) * amount` matrix.""",
        created_at=datetime.utcnow()
    )
    asst_chat.context_used = [
        "Target: Backend Software Engineer",
        "Recent mistake in DP: Off-by-one boundary initialization",
        "Proven strength: Recursion & Binary Search"
    ]
    db.add(user_chat)
    db.add(asst_chat)

    db.commit()
    db.close()
    print("Demo data seeded successfully for Arjun Sharma!")

if __name__ == "__main__":
    seed()
