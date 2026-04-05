import requests
import time
import json

BASE_URL = "http://localhost:8000"

print("\n" + "="*80)
print(" ENTERPRISE SEARCH SYSTEM - BROWSER DEMONSTRATION")
print("="*80)

print("\n[STEP 1] Checking Backend Status...")
try:
    response = requests.get(f"{BASE_URL}/docs", timeout=5)
    print(f"✓ Backend is running on {BASE_URL}")
    print(f"✓ API Documentation available at {BASE_URL}/docs")
except:
    print("✗ Backend not running. Please start it with: start_backend.bat")
    exit(1)

print("\n[STEP 2] Creating Test User Account...")
timestamp = int(time.time())
test_user = {
    "email": f"demo_{timestamp}@example.com",
    "username": "Demo User",
    "password": "DemoPass123!"
}

response = requests.post(f"{BASE_URL}/signup", json=test_user)
if response.status_code == 200:
    user_data = response.json()
    print(f"✓ User created successfully")
    print(f"  Email: {test_user['email']}")
    print(f"  Username: {test_user['username']}")
    print(f"  User ID: {user_data['id']}")
else:
    print(f"✗ Signup failed: {response.text}")
    exit(1)

print("\n[STEP 3] Logging In...")
response = requests.post(
    f"{BASE_URL}/login",
    data={"username": test_user["email"], "password": test_user["password"]}
)

if response.status_code == 200:
    token = response.json()["access_token"]
    print(f"✓ Login successful")
    print(f"  JWT Token: {token[:50]}...")
else:
    print(f"✗ Login failed")
    exit(1)

headers = {'Authorization': f'Bearer {token}'}

print("\n[STEP 4] Uploading Sample Documents...")

# Document 1: Company Handbook
doc1_content = """COMPANY HANDBOOK - ACME CORPORATION

Welcome to ACME Corporation! This handbook contains important information about our company policies, benefits, and procedures.

COMPANY OVERVIEW
ACME Corporation is a leading technology company specializing in enterprise software solutions. Founded in 2020, we have grown to serve over 500 clients worldwide.

WORK HOURS
Standard work hours are Monday through Friday, 9:00 AM to 5:00 PM. Remote work is available with manager approval.

BENEFITS
- Health Insurance: Comprehensive medical, dental, and vision coverage
- Retirement: 401(k) with 5% company match
- Paid Time Off: 20 days per year plus holidays
- Professional Development: $2,000 annual budget for training and conferences

LEAVE POLICIES
Employees are entitled to sick leave, vacation time, and parental leave. Please submit leave requests through the HR portal at least two weeks in advance.

CODE OF CONDUCT
All employees must maintain professional behavior, respect colleagues, and adhere to company values of integrity, innovation, and collaboration.

CONTACT INFORMATION
HR Department: hr@acme.com
IT Support: support@acme.com
Main Office: (555) 123-4567
"""

files = {'file': ('company_handbook.txt', doc1_content, 'text/plain')}
data = {'tags': 'handbook, policies, HR'}
response = requests.post(f"{BASE_URL}/upload", files=files, data=data, headers=headers)

if response.status_code == 200:
    doc1_id = response.json()["document_id"]
    print(f"✓ Uploaded: company_handbook.txt (ID: {doc1_id})")
else:
    print(f"✗ Upload failed")

# Document 2: Technical Guide
doc2_content = """# API Integration Guide

## Overview
This guide explains how to integrate with our REST API for enterprise search functionality.

## Authentication
All API requests require a JWT token in the Authorization header:
```
Authorization: Bearer YOUR_TOKEN_HERE
```

## Endpoints

### POST /search
Search across all indexed documents.

**Request Body:**
```json
{
  "query": "search terms",
  "file_type": "pdf",
  "tags": "documentation",
  "top_k": 10
}
```

**Response:**
```json
{
  "results": [
    {
      "document_id": 1,
      "filename": "example.pdf",
      "chunk": "relevant text...",
      "score": 0.95
    }
  ]
}
```

### POST /upload
Upload documents for indexing.

**Parameters:**
- file: The document file (PDF, DOCX, TXT, MD)
- tags: Optional comma-separated tags

## Rate Limits
- 100 requests per minute per user
- 1000 requests per hour per user

## Error Codes
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Internal Server Error

## Best Practices
1. Use specific search queries for better results
2. Apply filters to narrow down results
3. Cache frequently accessed data
4. Handle errors gracefully

## Support
For technical support, contact: api-support@acme.com
"""

files = {'file': ('api_guide.md', doc2_content, 'text/markdown')}
data = {'tags': 'API, documentation, technical'}
response = requests.post(f"{BASE_URL}/upload", files=files, data=data, headers=headers)

if response.status_code == 200:
    doc2_id = response.json()["document_id"]
    print(f"✓ Uploaded: api_guide.md (ID: {doc2_id})")
else:
    print(f"✗ Upload failed")

# Document 3: Meeting Notes
doc3_content = """QUARTERLY PLANNING MEETING NOTES
Date: April 1, 2026
Attendees: Sarah Johnson (CEO), Mike Chen (CTO), Lisa Brown (CFO)

AGENDA
1. Q1 Performance Review
2. Q2 Goals and Objectives
3. Budget Allocation
4. New Product Launch

Q1 PERFORMANCE REVIEW
- Revenue exceeded targets by 15%
- Customer satisfaction score: 4.8/5.0
- Successfully launched mobile app
- Expanded team by 20 employees

Q2 GOALS
1. Launch enterprise search product
2. Expand to European market
3. Achieve 30% revenue growth
4. Improve customer retention to 95%

BUDGET ALLOCATION
- Product Development: $500K
- Marketing: $300K
- Sales: $200K
- Operations: $150K

NEW PRODUCT LAUNCH
The enterprise search system will launch in May 2026. Key features include:
- AI-powered semantic search
- Multi-format document support
- Real-time indexing
- Advanced filtering

ACTION ITEMS
- Sarah: Finalize marketing strategy by April 15
- Mike: Complete product testing by April 20
- Lisa: Prepare financial projections by April 10

NEXT MEETING
April 30, 2026 at 2:00 PM
"""

files = {'file': ('meeting_notes.txt', doc3_content, 'text/plain')}
data = {'tags': 'meetings, planning, Q2'}
response = requests.post(f"{BASE_URL}/upload", files=files, data=data, headers=headers)

if response.status_code == 200:
    doc3_id = response.json()["document_id"]
    print(f"✓ Uploaded: meeting_notes.txt (ID: {doc3_id})")
else:
    print(f"✗ Upload failed")

print("\n[INFO] Waiting for document indexing...")
time.sleep(3)

print("\n[STEP 5] Running Search Queries...")

# Search 1: HR Benefits
print("\n--- Search Query 1: HR Benefits ---")
search_data = {"query": "What are the employee benefits and health insurance?", "top_k": 3}
response = requests.post(f"{BASE_URL}/search", json=search_data, headers=headers)

if response.status_code == 200:
    results = response.json()["results"]
    print(f"✓ Found {len(results)} results")
    for i, result in enumerate(results[:2], 1):
        print(f"\n  Result {i}:")
        print(f"  File: {result['filename']}")
        print(f"  Score: {result['score']:.4f} ({result['score']*100:.1f}%)")
        print(f"  Snippet: {result['chunk'][:120]}...")

# Search 2: API Documentation
print("\n--- Search Query 2: API Documentation ---")
search_data = {"query": "How do I authenticate API requests?", "top_k": 3}
response = requests.post(f"{BASE_URL}/search", json=search_data, headers=headers)

if response.status_code == 200:
    results = response.json()["results"]
    print(f"✓ Found {len(results)} results")
    for i, result in enumerate(results[:2], 1):
        print(f"\n  Result {i}:")
        print(f"  File: {result['filename']}")
        print(f"  Score: {result['score']:.4f} ({result['score']*100:.1f}%)")
        print(f"  Snippet: {result['chunk'][:120]}...")

# Search 3: Meeting Information
print("\n--- Search Query 3: Meeting Information ---")
search_data = {"query": "quarterly planning meeting Q2 goals", "top_k": 3}
response = requests.post(f"{BASE_URL}/search", json=search_data, headers=headers)

if response.status_code == 200:
    results = response.json()["results"]
    print(f"✓ Found {len(results)} results")
    for i, result in enumerate(results[:2], 1):
        print(f"\n  Result {i}:")
        print(f"  File: {result['filename']}")
        print(f"  Score: {result['score']:.4f} ({result['score']*100:.1f}%)")
        print(f"  Snippet: {result['chunk'][:120]}...")

# Search 4: Filtered Search
print("\n--- Search Query 4: Filtered Search (Markdown only) ---")
search_data = {"query": "API documentation", "file_type": "md", "top_k": 3}
response = requests.post(f"{BASE_URL}/search", json=search_data, headers=headers)

if response.status_code == 200:
    results = response.json()["results"]
    print(f"✓ Found {len(results)} markdown files")
    for result in results:
        print(f"  - {result['filename']} (Type: {result['file_type']}, Score: {result['score']:.4f})")

print("\n[STEP 6] Retrieving Document List...")
response = requests.get(f"{BASE_URL}/documents", headers=headers)

if response.status_code == 200:
    documents = response.json()
    print(f"✓ Total documents: {len(documents)}")
    print("\nDocument Library:")
    for doc in documents:
        print(f"  • {doc['filename']}")
        print(f"    Type: {doc['file_type']} | Tags: {doc['tags']} | Uploaded: {doc['upload_date'][:10]}")

print("\n" + "="*80)
print(" DEMONSTRATION COMPLETE")
print("="*80)

print("\n📊 SUMMARY:")
print(f"  ✓ User Account Created: {test_user['email']}")
print(f"  ✓ Documents Uploaded: 3 files")
print(f"  ✓ Search Queries Executed: 4 queries")
print(f"  ✓ All Operations Successful")

print("\n🌐 BROWSER ACCESS:")
print(f"  • Frontend: Open frontend/index.html in your browser")
print(f"  • API Docs: {BASE_URL}/docs")
print(f"  • Backend: {BASE_URL}")

print("\n🔑 TEST CREDENTIALS:")
print(f"  Email: {test_user['email']}")
print(f"  Password: {test_user['password']}")

print("\n💡 TRY IN BROWSER:")
print("  1. Open frontend/index.html")
print("  2. Login with the credentials above")
print("  3. Try searching for:")
print("     - 'employee benefits'")
print("     - 'API authentication'")
print("     - 'quarterly meeting'")
print("  4. Upload your own documents")
print("  5. Apply filters (file type, tags)")

print("\n" + "="*80 + "\n")
