import requests

base = 'http://127.0.0.1:8000/api'

# 1. Login demo user
r = requests.post(f'{base}/auth/login', json={'email': 'demo@codepilot.dev', 'password': 'Demo1234!'})
print('1. Login:', r.status_code, r.json()['user']['full_name'])
token = r.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

# 2. Profile
r = requests.get(f'{base}/profile', headers=headers)
print('2. Profile:', r.status_code, r.json()['target_role'])

# 3. Analyze code
r = requests.post(f'{base}/code/analyze', headers=headers, json={
    'problem_title': 'Longest Palindromic Substring',
    'language': 'python',
    'user_code': 'def longestPalindrome(s):\n    res = ""\n    for i in range(len(s)):\n        pass\n    return res'
})
print('3. Code Analyzer:', r.status_code, r.json()['approach_detected'], r.json()['time_complexity'], r.json()['ai_model_used'])

# 4. Knowledge concepts
r = requests.get(f'{base}/knowledge/concepts', headers=headers)
print('4. Knowledge Concepts count:', len(r.json()))

# 5. Knowledge Vault create & list
r = requests.post(f'{base}/vault/items', headers=headers, json={
    'content_type': 'note',
    'title': 'Raft Consensus Protocol Note',
    'content': 'Leader election requires a majority of votes across heartbeat intervals.',
    'topic': 'Distributed Systems',
    'folder': 'Backend'
})
print('5. Vault Create:', r.status_code, r.json()['title'])

r = requests.get(f'{base}/vault/items', headers=headers)
print('5b. Vault List count:', len(r.json()))

# 6. Ask My AI Chat
r = requests.post(f'{base}/chat/message', headers=headers, json={'message': 'Why did my DP solution have boundary errors?'})
print('6. Ask My AI:', r.status_code, 'Context used:', r.json()['context_used'])

# 7. Weekly plan
r = requests.get(f'{base}/plan/current', headers=headers)
print('7. Weekly Plan:', r.status_code, r.json()['week_title'], 'Tasks:', len(r.json()['tasks']))

# 8. Career Path
r = requests.get(f'{base}/career/path', headers=headers)
print('8. Career Path:', r.status_code, 'Readiness:', r.json()['readiness_score'], 'Strong skills:', len(r.json()['strong_skills']))

# 9. Health & Open AI
r = requests.get('http://127.0.0.1:8000/health')
print('9. Health:', r.status_code, r.json()['ai']['active_runtime'])

# 10. Frontend check
rf = requests.get('http://127.0.0.1:5173')
print('10. Frontend HTML status:', rf.status_code, 'Contains root div:', '<div id="root">' in rf.text)
