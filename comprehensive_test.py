import requests
import json
import sys
import uuid

BASE_URL = 'http://127.0.0.1:8000'
API_URL = f'{BASE_URL}/api'

passed = 0
failed = 0

def check(name, condition, details=""):
    global passed, failed
    if condition:
        passed += 1
        print(f" [PASS] {name} {details}")
    else:
        failed += 1
        print(f" [FAIL] {name} -> {details}")

print("==================================================================")
print("  CODEPILOT END-TO-END VERIFICATION & HARDENING AUDIT ")
print("==================================================================")

# 1. Health checks
try:
    r = requests.get(f'{BASE_URL}/health', timeout=5)
    data = r.json()
    check("1. Health /health", r.status_code == 200 and data.get('status') == 'healthy', f"Runtime: {data.get('ai',{}).get('active_runtime')}")
except Exception as e:
    check("1. Health /health", False, str(e))

try:
    r = requests.get(f'{API_URL}/health', timeout=5)
    check("2. Health /api/health", r.status_code == 200, f"Status: {r.status_code}")
except Exception as e:
    check("2. Health /api/health", False, str(e))

# 2. CRITICAL SECURITY: Admin self-registration must be BLOCKED
attacker_email = f"attacker_{uuid.uuid4().hex[:8]}@example.com"
try:
    r = requests.post(f'{API_URL}/auth/register', json={
        'email': attacker_email,
        'password': 'AttackerPass123!',
        'full_name': 'Malicious User',
        'role': 'ADMIN'  # Attempt privilege escalation
    })
    user_role = r.json().get('user', {}).get('role')
    check("3. Security: Admin self-registration blocked", r.status_code == 200 and user_role == 'USER', f"Created account role: '{user_role}' (Expected: 'USER')")
except Exception as e:
    check("3. Security: Admin self-registration blocked", False, str(e))

# 3. Dynamic User Registration & Onboarding
test_user_email = f"learner_{uuid.uuid4().hex[:8]}@codepilot.dev"
user_token = None
user_headers = {}
try:
    r = requests.post(f'{API_URL}/auth/register', json={
        'email': test_user_email,
        'password': 'LearnerPass123!',
        'full_name': 'Test Learner',
        'role': 'USER'
    })
    user_token = r.json().get('access_token')
    user_headers = {'Authorization': f'Bearer {user_token}'}
    check("4. Auth: Register new learner", r.status_code == 200 and user_token is not None, f"User: {test_user_email}")
except Exception as e:
    check("4. Auth: Register new learner", False, str(e))

# 4. User Login with valid credentials
try:
    r = requests.post(f'{API_URL}/auth/login', json={'email': test_user_email, 'password': 'LearnerPass123!'})
    check("5. Auth: Login with valid credentials", r.status_code == 200 and 'access_token' in r.json(), "JWT issued")
except Exception as e:
    check("5. Auth: Login with valid credentials", False, str(e))

# 5. Negative Auth: Invalid credentials rejected (401)
try:
    r = requests.post(f'{API_URL}/auth/login', json={'email': test_user_email, 'password': 'WrongPassword123!'})
    check("6. Auth Negative: Invalid password rejected", r.status_code == 401, f"HTTP Status: {r.status_code}")
except Exception as e:
    check("6. Auth Negative: Invalid password rejected", False, str(e))

# 6. Negative Auth: Missing token rejected (401)
try:
    r = requests.get(f'{API_URL}/profile')
    check("7. Auth Negative: Missing token rejected", r.status_code == 401, f"HTTP Status: {r.status_code}")
except Exception as e:
    check("7. Auth Negative: Missing token rejected", False, str(e))

# 7. Negative Auth: Invalid token rejected (401)
try:
    r = requests.get(f'{API_URL}/profile', headers={'Authorization': 'Bearer invalid.bogus.jwt'})
    check("8. Auth Negative: Invalid token rejected", r.status_code == 401, f"HTTP Status: {r.status_code}")
except Exception as e:
    check("8. Auth Negative: Invalid token rejected", False, str(e))

# 8. Profile retrieval & update
try:
    r = requests.get(f'{API_URL}/profile', headers=user_headers)
    check("9. Profile: Get profile", r.status_code == 200, f"Role: {r.json().get('target_role')}")
    
    r = requests.put(f'{API_URL}/profile', headers=user_headers, json={
        'target_role': 'Senior Backend Engineer (Distributed Systems)',
        'weekly_hours': 10
    })
    check("10. Profile: Update target role", r.status_code == 200 and 'Senior' in r.json().get('target_role', ''), f"New role: {r.json().get('target_role')}")
except Exception as e:
    check("9-10. Profile operations", False, str(e))

# 9. Code Analyzer: Analyze code submission
try:
    code_payload = {
        'problem_title': 'Trapping Rain Water',
        'language': 'python',
        'user_code': '''def trap(height):
    if not height: return 0
    l, r = 0, len(height) - 1
    left_max, right_max = height[l], height[r]
    water = 0
    while l < r:
        if left_max < right_max:
            l += 1
            left_max = max(left_max, height[l])
            water += left_max - height[l]
        else:
            r -= 1
            right_max = max(right_max, height[r])
            water += right_max - height[r]
    return water''',
        'notes': 'Two-pointer linear approach'
    }
    r = requests.post(f'{API_URL}/code/analyze', headers=user_headers, json=code_payload)
    data = r.json()
    check("11. Code Analyzer: Complexity & invariant detection", r.status_code == 200 and 'O(n)' in data.get('time_complexity', ''), f"Detected: {data.get('approach_detected')}, Complexity: {data.get('time_complexity')}")
    
    # Submissions history
    r = requests.get(f'{API_URL}/code/submissions', headers=user_headers)
    check("12. Code Analyzer: Submissions history", r.status_code == 200 and len(r.json()) >= 1, f"Submissions: {len(r.json())}")
except Exception as e:
    check("11-12. Code Analyzer", False, str(e))

# 10. Personal Technical Memory: Concepts, Graph, Heatmap
try:
    r = requests.get(f'{API_URL}/knowledge/concepts', headers=user_headers)
    concepts = r.json()
    check("13. Knowledge Memory: Real concepts list", r.status_code == 200 and len(concepts) > 0, f"Concepts count: {len(concepts)}")
    
    r = requests.get(f'{API_URL}/knowledge/graph', headers=user_headers)
    graph = r.json()
    check("14. Knowledge Memory: Graph structure", r.status_code == 200 and 'nodes' in graph and 'edges' in graph, f"Nodes: {len(graph.get('nodes', []))}, Edges: {len(graph.get('edges', []))}")
    
    r = requests.get(f'{API_URL}/knowledge/heatmap', headers=user_headers)
    check("15. Knowledge Memory: Activity heatmap", r.status_code == 200 and 'days' in r.json(), f"Total days: {len(r.json().get('days', []))}, Activities: {r.json().get('total_activities')}")
except Exception as e:
    check("13-15. Knowledge Memory", False, str(e))

# 11. Learning Log: 'I Learned This'
try:
    r = requests.post(f'{API_URL}/knowledge/log', headers=user_headers, json={
        'topic': 'Raft Consensus Algorithm',
        'notes': 'Learned how leader election and log replication preserve linearizability across terms.',
        'source': 'Self Study',
        'time_spent_mins': 25
    })
    check("16. Knowledge Memory: Record learning log", r.status_code == 200, f"Logged topic: {r.json().get('topic')}")
except Exception as e:
    check("16. Knowledge Memory: Record learning log", False, str(e))

# 12. Knowledge Vault: Note & Code creation
vault_item_id = None
try:
    r = requests.post(f'{API_URL}/vault/items', headers=user_headers, json={
        'content_type': 'note',
        'title': 'B-Tree vs LSM-Tree Storage Engines',
        'content': 'LSM-Trees optimize write throughput via append-only SSTables. B-Trees optimize read operations with in-place updates.',
        'topic': 'Databases',
        'folder': 'Architecture',
        'tags': ['storage', 'lsm', 'b-tree']
    })
    vault_item_id = r.json().get('id')
    check("17. Knowledge Vault: Create note", r.status_code == 200, f"Item ID: {vault_item_id}, Title: {r.json().get('title')}")
    
    r = requests.post(f'{API_URL}/vault/items', headers=user_headers, json={
        'content_type': 'code',
        'title': 'Distributed Mutex with Redis Lua',
        'content': 'local val = redis.call("get", KEYS[1]) if val == ARGV[1] then return redis.call("del", KEYS[1]) else return 0 end',
        'topic': 'Concurrency',
        'folder': 'Distributed Systems'
    })
    check("18. Knowledge Vault: Create code snippet", r.status_code == 200, f"Title: {r.json().get('title')}")
except Exception as e:
    check("17-18. Knowledge Vault items", False, str(e))

# 13. Knowledge Vault: File upload & Authenticated private file streaming
vault_file_id = None
test_file_bytes = b"Architecture blueprint: Sharding strategy by user hash range."
try:
    r = requests.post(
        f'{API_URL}/vault/upload',
        headers=user_headers,
        files={'file': ('sharding_spec.txt', test_file_bytes, 'text/plain')},
        data={'topic': 'System Design', 'folder': 'Architecture'}
    )
    vault_file_id = r.json().get('id')
    # Verify no raw filesystem path is leaked in API response
    check("19. Knowledge Vault: Upload private file", r.status_code == 200 and 'file_path' not in r.json(), f"File item ID: {vault_file_id}, Filename: {r.json().get('file_name')}")
    
    # Authenticated owner streams file
    r = requests.get(f'{API_URL}/vault/items/{vault_file_id}/file', headers=user_headers)
    check("20. Knowledge Vault: Authenticated file streaming", r.status_code == 200 and r.content == test_file_bytes, f"Bytes received: {len(r.content)}")
except Exception as e:
    check("19-20. Knowledge Vault file upload & streaming", False, str(e))

# 14. CRITICAL SECURITY: User Data Isolation Check
# Create User B
user_b_email = f"user_b_{uuid.uuid4().hex[:8]}@codepilot.dev"
user_b_headers = {}
try:
    r = requests.post(f'{API_URL}/auth/register', json={
        'email': user_b_email,
        'password': 'UserBPass123!',
        'full_name': 'User B',
        'role': 'USER'
    })
    user_b_headers = {'Authorization': f"Bearer {r.json().get('access_token')}"}
    
    # User B tries to access User A's vault note
    r = requests.get(f'{API_URL}/vault/items/{vault_item_id}', headers=user_b_headers)
    check("21. Security Isolation: User B cannot access User A's vault item", r.status_code == 404, f"Status: {r.status_code} (Expected: 404)")
    
    # User B tries to download User A's private file
    r = requests.get(f'{API_URL}/vault/items/{vault_file_id}/file', headers=user_b_headers)
    check("22. Security Isolation: User B cannot stream User A's private file", r.status_code == 404, f"Status: {r.status_code} (Expected: 404)")
    
    # Unauthenticated user cannot stream private file
    r = requests.get(f'{API_URL}/vault/items/{vault_file_id}/file')
    check("23. Security Isolation: Unauthenticated file access blocked", r.status_code == 401, f"Status: {r.status_code} (Expected: 401)")
    
    # Unauthenticated user cannot trigger AI study action
    r = requests.post(f'{API_URL}/vault/action', json={'action': 'summarize', 'content': 'Sample'})
    check("24. Security Isolation: Unauthenticated AI study action blocked", r.status_code == 401, f"Status: {r.status_code} (Expected: 401)")
except Exception as e:
    check("21-24. User data isolation", False, str(e))

# 15. Knowledge Vault: Multi-field keyword search
try:
    r = requests.get(f'{API_URL}/vault/items?search=LSM', headers=user_headers)
    check("25. Knowledge Vault: Keyword search", r.status_code == 200 and len(r.json()) > 0, f"Found {len(r.json())} items for query 'LSM'")
except Exception as e:
    check("25. Knowledge Vault search", False, str(e))

# 16. Knowledge Vault: Grounded Q&A ('Ask This Document')
try:
    if vault_item_id:
        r = requests.post(f'{API_URL}/vault/items/{vault_item_id}/ask', headers=user_headers, json={
            'question': 'When are LSM-Trees preferred over B-Trees?'
        })
        ans = r.json().get('answer', '')
        check("26. Knowledge Vault: Grounded Q&A", r.status_code == 200 and len(ans) > 20, f"Answer preview: {ans[:60]}...")
except Exception as e:
    check("26. Knowledge Vault Ask This Document", False, str(e))

# 17. Knowledge Vault: Authenticated AI study action
try:
    r = requests.post(f'{API_URL}/vault/action', headers=user_headers, json={
        'action': 'summarize',
        'content': 'Write-Ahead Logging ensures that mutations are appended to disk before mutating the in-memory memtable.'
    })
    check("27. Knowledge Vault: Authenticated AI study action", r.status_code == 200 and 'result' in r.json(), "Summary generated")
except Exception as e:
    check("27. Knowledge Vault study action", False, str(e))

# 18. Smart Revision recommendations
try:
    r = requests.get(f'{API_URL}/vault/revisions', headers=user_headers)
    check("28. Knowledge Vault: Smart Revision queue", r.status_code == 200, f"Recommendations: {len(r.json())}")
except Exception as e:
    check("28. Knowledge Vault revision queue", False, str(e))

# 19. Ask My AI: Context-Aware Chat
try:
    r = requests.post(f'{API_URL}/chat/message', headers=user_headers, json={
        'message': 'How does distributed caching tie into my target Backend Software Engineer role?'
    })
    data = r.json()
    reply = data.get('reply', '')
    check("29. Ask My AI: Context-grounded response", r.status_code == 200 and len(reply) > 20, f"Model: {data.get('model_used')}, Context tags: {len(data.get('context_used', []))}")
    
    r = requests.get(f'{API_URL}/chat/history', headers=user_headers)
    check("30. Ask My AI: Chat history retrieval", r.status_code == 200 and len(r.json()) >= 1, f"Messages count: {len(r.json())}")
except Exception as e:
    check("29-30. Ask My AI chat", False, str(e))

# 20. Weekly Plan & Task Toggle
try:
    r = requests.get(f'{API_URL}/plan/current', headers=user_headers)
    plan_data = r.json()
    tasks = plan_data.get('tasks', [])
    check("31. Weekly Plan: Get active plan", r.status_code == 200 and len(tasks) > 0, f"Week: {plan_data.get('week_title')}, Tasks: {len(tasks)}")
    
    if tasks:
        t_id = tasks[0]['id']
        r = requests.post(f'{API_URL}/plan/tasks/{t_id}/toggle', headers=user_headers)
        check("32. Weekly Plan: Toggle task status", r.status_code == 200, f"Completed: {r.json().get('is_completed')}")
except Exception as e:
    check("31-32. Weekly Plan", False, str(e))

# 21. Weekend Assessment: Generate & Submit
try:
    r = requests.post(f'{API_URL}/assessment/generate', headers=user_headers)
    ass_data = r.json()
    ass_id = ass_data.get('id')
    questions = ass_data.get('questions', [])
    check("33. Weekend Assessment: Generate test", r.status_code == 200 and ass_id is not None, f"ID: {ass_id}, Questions: {len(questions)}")
    
    if ass_id and questions:
        q0 = questions[0]
        r = requests.post(f'{API_URL}/assessment/{ass_id}/submit', headers=user_headers, json={
            'answers': {str(q0['id']): 0}
        })
        check("34. Weekend Assessment: Submit & Grade", r.status_code == 200 and 'score' in r.json(), f"Score: {r.json().get('score')}%")
        
    r = requests.get(f'{API_URL}/assessment/history', headers=user_headers)
    check("35. Weekend Assessment: Assessment history", r.status_code == 200 and len(r.json()) >= 1, f"Completed tests: {len(r.json())}")
except Exception as e:
    check("33-35. Weekend Assessment", False, str(e))

# 22. Career Path & Skill Gap Analysis
try:
    r = requests.get(f'{API_URL}/career/path', headers=user_headers)
    data = r.json()
    check("36. Career Path: Readiness & skill gaps", r.status_code == 200 and 'readiness_score' in data, f"Readiness: {data.get('readiness_score')}%, Strong: {len(data.get('strong_skills', []))}, Gaps: {len(data.get('gap_skills', []))}")
except Exception as e:
    check("36. Career Path", False, str(e))

# 23. Aptitude Sprint: Daily sprint & Batch submit
try:
    r = requests.get(f'{API_URL}/aptitude/sprint', headers=user_headers)
    sprint_qs = r.json()
    check("37. Aptitude: Daily Sprint questions", r.status_code == 200 and isinstance(sprint_qs, list), f"Questions count: {len(sprint_qs)}")
    
    if sprint_qs:
        answers = {str(idx): 0 for idx in range(len(sprint_qs))}
        r = requests.post(f'{API_URL}/aptitude/submit', headers=user_headers, json={'answers': answers})
        check("38. Aptitude: Submit sprint", r.status_code == 200 and 'score' in r.json(), f"Score: {r.json().get('score')}/{r.json().get('total')}")
except Exception as e:
    check("37-38. Aptitude Sprint", False, str(e))

# 24. Adaptive Interview: Start, Answer, Complete
try:
    r = requests.post(f'{API_URL}/interview/start', headers=user_headers, json={'topic': 'DSA & Distributed Systems'})
    int_data = r.json()
    int_id = int_data.get('id')
    check("39. Adaptive Interview: Start session", r.status_code == 200 and int_id is not None, f"Session ID: {int_id}")
    
    if int_id:
        r = requests.post(f'{API_URL}/interview/{int_id}/answer', headers=user_headers, json={
            'answer': 'I would approach this by using consistent hashing across distributed cache clusters, with virtual nodes to prevent hotspots.'
        })
        check("40. Adaptive Interview: Submit verbal answer", r.status_code == 200 and 'feedback' in r.json(), f"Feedback preview: {r.json().get('feedback', '')[:50]}...")
        
        r = requests.post(f'{API_URL}/interview/{int_id}/complete', headers=user_headers)
        check("41. Adaptive Interview: Complete & Debrief", r.status_code == 200 and 'score' in r.json(), f"Final Score: {r.json().get('score')}/100")
except Exception as e:
    check("39-41. Adaptive Interview", False, str(e))

# 25. Explore: Public Showcase
try:
    r = requests.get(f'{API_URL}/knowledge/public')
    check("42. Explore: Public Showcase", r.status_code == 200 and 'concepts' in r.json(), f"Concepts count: {len(r.json().get('concepts', []))}")
except Exception as e:
    check("42. Explore Showcase", False, str(e))

# 26. Admin Authorization & Overview
# Regular user attempt (Forbidden)
try:
    r = requests.get(f'{API_URL}/admin/overview', headers=user_headers)
    check("43. Security: Regular user blocked from Admin", r.status_code == 403, f"Status: {r.status_code} (Expected: 403)")
except Exception as e:
    check("43. Security: Regular user blocked from Admin", False, str(e))

# Admin Login & Telemetry
try:
    r = requests.post(f'{API_URL}/auth/login', json={'email': 'admin@codepilot.dev', 'password': 'Admin1234!'})
    admin_token = r.json().get('access_token')
    admin_headers = {'Authorization': f'Bearer {admin_token}'}
    
    r = requests.get(f'{API_URL}/admin/overview', headers=admin_headers)
    check("44. Admin: Authorized telemetry overview", r.status_code == 200 and 'total_users' in r.json(), f"Users: {r.json().get('total_users')}, Submissions: {r.json().get('total_submissions')}")
    
    r = requests.get(f'{API_URL}/admin/users', headers=admin_headers)
    check("45. Admin: Users list", r.status_code == 200 and len(r.json()) > 0, f"Users count: {len(r.json())}")
except Exception as e:
    check("44-45. Admin authorized access", False, str(e))

# 27. Frontend Dev Server Check
try:
    r = requests.get('http://127.0.0.1:5173')
    check("46. Frontend: Vite Dev Server", r.status_code == 200 and '<div id="root">' in r.text, f"HTTP Status: {r.status_code}")
except Exception as e:
    check("46. Frontend Dev Server", False, str(e))

print("==================================================================")
print(f"  AUDIT SUMMARY: {passed} PASSED, {failed} FAILED (TOTAL: {passed + failed})")
print("==================================================================")

if failed > 0:
    sys.exit(1)
