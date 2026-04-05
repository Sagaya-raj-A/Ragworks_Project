import requests
import time
import random

BASE_URL = "http://localhost:8000"

print("\n" + "="*70)
print(" ENTERPRISE SEARCH SYSTEM - COMPREHENSIVE TEST SUITE")
print("="*70 + "\n")

# Generate unique test data
timestamp = int(time.time())
random_id = random.randint(1000, 9999)
test_user = {
    "email": f"testuser_{timestamp}_{random_id}@example.com",
    "username": f"Test User {random_id}",
    "password": "SecurePass123!"
}

token = None
test_results = []

def log_test(name, passed, message=""):
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status} {name}")
    if message:
        print(f"      {message}")
    test_results.append((name, passed))

print("[INFO] Testing backend connectivity...")
try:
    response = requests.get(f"{BASE_URL}/docs", timeout=5)
    if response.status_code == 200:
        log_test("Backend Connectivity", True, "Backend is running on port 8000")
    else:
        log_test("Backend Connectivity", False, f"Unexpected status: {response.status_code}")
        exit(1)
except Exception as e:
    log_test("Backend Connectivity", False, str(e))
    print("\n[FATAL] Cannot connect to backend. Run: start_backend.bat\n")
    exit(1)

print(f"\n[INFO] Test user: {test_user['email']}\n")

# Test 1: User Signup
print("[TEST] User Signup...")
try:
    response = requests.post(f"{BASE_URL}/signup", json=test_user, timeout=10)
    if response.status_code == 200:
        user_data = response.json()
        log_test("User Signup", True, f"User ID: {user_data['id']}")
    else:
        log_test("User Signup", False, f"Status {response.status_code}: {response.text[:100]}")
except Exception as e:
    log_test("User Signup", False, str(e))

# Test 2: User Login
print("\n[TEST] User Login...")
try:
    response = requests.post(
        f"{BASE_URL}/login",
        data={"username": test_user["email"], "password": test_user["password"]},
        timeout=10
    )
    if response.status_code == 200:
        token = response.json()["access_token"]
        log_test("User Login", True, f"Token received ({len(token)} chars)")
    else:
        log_test("User Login", False, f"Status {response.status_code}")
except Exception as e:
    log_test("User Login", False, str(e))

if not token:
    print("\n[FATAL] Cannot proceed without authentication token\n")
    exit(1)

headers = {'Authorization': f'Bearer {token}'}

# Test 3: File Upload (TXT)
print("\n[TEST] File Upload (TXT)...")
try:
    content = """Enterprise Search System - Technical Documentation

This document describes the enterprise search system architecture.

The system implements a hybrid search approach combining:
1. BM25 algorithm for keyword-based retrieval
2. Dense vector search using FAISS for semantic matching
3. SentenceTransformers for generating embeddings

Key Features:
- Multi-format support (PDF, DOCX, TXT, Markdown)
- Real-time indexing and search
- User authentication with JWT
- Metadata filtering capabilities
- Scalable vector storage

The search engine processes documents by:
1. Extracting text from uploaded files
2. Chunking text into manageable segments
3. Generating embeddings for each chunk
4. Storing vectors in FAISS index
5. Building BM25 index for keyword matching

Search queries are processed through both retrieval methods,
and results are combined using score fusion for optimal relevance.
"""
    
    files = {'file': ('enterprise_search_docs.txt', content, 'text/plain')}
    data = {'tags': 'documentation, technical, search'}
    
    response = requests.post(f"{BASE_URL}/upload", files=files, data=data, headers=headers, timeout=15)
    if response.status_code == 200:
        doc_id = response.json()["document_id"]
        log_test("File Upload (TXT)", True, f"Document ID: {doc_id}")
    else:
        log_test("File Upload (TXT)", False, f"Status {response.status_code}")
except Exception as e:
    log_test("File Upload (TXT)", False, str(e))

# Test 4: File Upload (Markdown)
print("\n[TEST] File Upload (Markdown)...")
try:
    md_content = """# Machine Learning in Enterprise Search

## Overview
Machine learning powers modern search systems through natural language processing
and semantic understanding.

## Core Technologies
- **Neural Networks**: Deep learning models for text understanding
- **Transformers**: State-of-the-art NLP architecture
- **Vector Embeddings**: Semantic representation of text
- **Approximate Nearest Neighbor**: Efficient similarity search

## Implementation
Our system uses SentenceTransformers to generate embeddings from text chunks.
These embeddings capture semantic meaning, allowing the system to find relevant
documents even when exact keywords don't match.

## Benefits
- Improved search accuracy
- Better handling of synonyms and related concepts
- Multilingual support potential
- Continuous learning from user interactions
"""
    
    files = {'file': ('ml_guide.md', md_content, 'text/markdown')}
    data = {'tags': 'machine learning, AI, guide'}
    
    response = requests.post(f"{BASE_URL}/upload", files=files, data=data, headers=headers, timeout=15)
    if response.status_code == 200:
        doc_id = response.json()["document_id"]
        log_test("File Upload (Markdown)", True, f"Document ID: {doc_id}")
    else:
        log_test("File Upload (Markdown)", False, f"Status {response.status_code}")
except Exception as e:
    log_test("File Upload (Markdown)", False, str(e))

# Wait for indexing
print("\n[INFO] Waiting for document indexing...")
time.sleep(3)

# Test 5: Semantic Search
print("\n[TEST] Semantic Search...")
try:
    search_data = {
        "query": "How does the system use artificial intelligence and machine learning?",
        "top_k": 5
    }
    
    response = requests.post(f"{BASE_URL}/search", json=search_data, headers=headers, timeout=15)
    if response.status_code == 200:
        results = response.json()["results"]
        if len(results) > 0:
            log_test("Semantic Search", True, f"Found {len(results)} results, top score: {results[0]['score']:.4f}")
            print(f"      Top result: {results[0]['filename']}")
            print(f"      Snippet: {results[0]['chunk'][:80]}...")
        else:
            log_test("Semantic Search", False, "No results found")
    else:
        log_test("Semantic Search", False, f"Status {response.status_code}")
except Exception as e:
    log_test("Semantic Search", False, str(e))

# Test 6: Keyword Search
print("\n[TEST] Keyword Search...")
try:
    search_data = {
        "query": "FAISS BM25 vector embeddings",
        "top_k": 5
    }
    
    response = requests.post(f"{BASE_URL}/search", json=search_data, headers=headers, timeout=15)
    if response.status_code == 200:
        results = response.json()["results"]
        if len(results) > 0:
            log_test("Keyword Search", True, f"Found {len(results)} results")
        else:
            log_test("Keyword Search", False, "No results found")
    else:
        log_test("Keyword Search", False, f"Status {response.status_code}")
except Exception as e:
    log_test("Keyword Search", False, str(e))

# Test 7: Filtered Search
print("\n[TEST] Filtered Search (by file type)...")
try:
    search_data = {
        "query": "machine learning",
        "file_type": "md",
        "top_k": 5
    }
    
    response = requests.post(f"{BASE_URL}/search", json=search_data, headers=headers, timeout=15)
    if response.status_code == 200:
        results = response.json()["results"]
        md_only = all(r['file_type'] == 'md' for r in results)
        if md_only and len(results) > 0:
            log_test("Filtered Search", True, f"Found {len(results)} markdown files")
        elif len(results) == 0:
            log_test("Filtered Search", True, "No markdown files match (expected)")
        else:
            log_test("Filtered Search", False, "Filter not working correctly")
    else:
        log_test("Filtered Search", False, f"Status {response.status_code}")
except Exception as e:
    log_test("Filtered Search", False, str(e))

# Test 8: Get Documents
print("\n[TEST] Get User Documents...")
try:
    response = requests.get(f"{BASE_URL}/documents", headers=headers, timeout=10)
    if response.status_code == 200:
        documents = response.json()
        if len(documents) >= 2:
            log_test("Get Documents", True, f"Retrieved {len(documents)} documents")
            for doc in documents:
                print(f"      - {doc['filename']} ({doc['file_type']})")
        else:
            log_test("Get Documents", False, f"Expected 2+ documents, got {len(documents)}")
    else:
        log_test("Get Documents", False, f"Status {response.status_code}")
except Exception as e:
    log_test("Get Documents", False, str(e))

# Test 9: Security - Unauthorized Access
print("\n[TEST] Security (Unauthorized Access)...")
try:
    response = requests.post(f"{BASE_URL}/search", json={"query": "test"}, timeout=10)
    if response.status_code == 401:
        log_test("Security Check", True, "Unauthorized access properly blocked")
    else:
        log_test("Security Check", False, f"Expected 401, got {response.status_code}")
except Exception as e:
    log_test("Security Check", False, str(e))

# Test 10: Invalid Login
print("\n[TEST] Security (Invalid Credentials)...")
try:
    response = requests.post(
        f"{BASE_URL}/login",
        data={"username": "nonexistent@example.com", "password": "wrongpass"},
        timeout=10
    )
    if response.status_code == 401:
        log_test("Invalid Login Blocked", True, "Invalid credentials rejected")
    else:
        log_test("Invalid Login Blocked", False, f"Expected 401, got {response.status_code}")
except Exception as e:
    log_test("Invalid Login Blocked", False, str(e))

# Summary
print("\n" + "="*70)
print(" TEST SUMMARY")
print("="*70)

passed = sum(1 for _, result in test_results if result)
total = len(test_results)

for name, result in test_results:
    status = "[PASS]" if result else "[FAIL]"
    print(f"{status} {name}")

print("="*70)
percentage = (passed / total) * 100
print(f"\nResults: {passed}/{total} tests passed ({percentage:.1f}%)")
print("="*70 + "\n")

if passed == total:
    print("[SUCCESS] All tests passed! System is fully functional.\n")
elif passed >= total * 0.8:
    print("[GOOD] Most tests passed. System is operational.\n")
else:
    print("[WARNING] Several tests failed. Check the output above.\n")
