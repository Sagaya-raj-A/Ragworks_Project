import requests
import json
import time

BASE_URL = "http://localhost:8000"

print("\n" + "="*60)
print("ENTERPRISE SEARCH SYSTEM - TESTING")
print("="*60)

# Test data
test_user = {
    "email": f"test_{int(time.time())}@example.com",
    "username": "Test User",
    "password": "testpass123"
}

token = None
results = []

def test(name, func):
    print(f"\n[TEST] {name}")
    try:
        success = func()
        status = "PASS" if success else "FAIL"
        print(f"[{status}] {name}")
        results.append((name, success))
        return success
    except Exception as e:
        print(f"[ERROR] {name}: {str(e)}")
        results.append((name, False))
        return False

def test_backend():
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        print("[INFO] Backend is running")
        return True
    except:
        print("[ERROR] Backend not running")
        return False

def test_signup():
    global test_user
    response = requests.post(f"{BASE_URL}/signup", json=test_user)
    if response.status_code == 200:
        data = response.json()
        print(f"[INFO] User created: {data['email']}")
        return True
    print(f"[ERROR] Signup failed: {response.status_code}")
    return False

def test_login():
    global token
    response = requests.post(
        f"{BASE_URL}/login",
        data={"username": test_user["email"], "password": test_user["password"]}
    )
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"[INFO] Token received")
        return True
    print(f"[ERROR] Login failed")
    return False

def test_upload():
    content = """Enterprise Search System
    
    This system uses artificial intelligence and machine learning
    for hybrid search combining BM25 and dense vector retrieval.
    Features include FAISS vector storage and semantic search."""
    
    files = {'file': ('test.txt', content, 'text/plain')}
    data = {'tags': 'test, AI'}
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.post(f"{BASE_URL}/upload", files=files, data=data, headers=headers)
    if response.status_code == 200:
        doc_id = response.json()["document_id"]
        print(f"[INFO] Document uploaded: ID {doc_id}")
        return True
    print(f"[ERROR] Upload failed")
    return False

def test_search():
    time.sleep(2)  # Wait for indexing
    
    search_data = {"query": "artificial intelligence machine learning", "top_k": 5}
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.post(f"{BASE_URL}/search", json=search_data, headers=headers)
    if response.status_code == 200:
        results_data = response.json()["results"]
        print(f"[INFO] Found {len(results_data)} results")
        if results_data:
            print(f"[INFO] Top result score: {results_data[0]['score']:.4f}")
        return len(results_data) > 0
    print(f"[ERROR] Search failed")
    return False

def test_documents():
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f"{BASE_URL}/documents", headers=headers)
    if response.status_code == 200:
        docs = response.json()
        print(f"[INFO] Retrieved {len(docs)} documents")
        return len(docs) > 0
    print(f"[ERROR] Get documents failed")
    return False

def test_security():
    response = requests.post(f"{BASE_URL}/search", json={"query": "test"})
    if response.status_code == 401:
        print("[INFO] Unauthorized access blocked")
        return True
    print("[ERROR] Security issue")
    return False

# Run tests
if not test_backend():
    print("\n[FATAL] Backend not running. Start it with: start_backend.bat")
    exit(1)

test("User Signup", test_signup)
test("User Login", test_login)
test("File Upload", test_upload)
test("Search Query", test_search)
test("Get Documents", test_documents)
test("Security Check", test_security)

# Summary
print("\n" + "="*60)
print("TEST SUMMARY")
print("="*60)

passed = sum(1 for _, r in results if r)
total = len(results)

for name, result in results:
    status = "PASS" if result else "FAIL"
    print(f"{name:.<40} [{status}]")

print("="*60)
percentage = (passed / total) * 100
print(f"Results: {passed}/{total} tests passed ({percentage:.1f}%)")
print("="*60 + "\n")

if passed == total:
    print("[SUCCESS] All tests passed! System is fully functional.\n")
else:
    print("[WARNING] Some tests failed.\n")
