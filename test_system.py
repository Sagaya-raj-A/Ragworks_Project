import requests
import json
import time
from pathlib import Path
import sys

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:8000"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name):
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}Testing: {name}{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")

def print_success(message):
    print(f"{Colors.GREEN}[PASS] {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}[FAIL] {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.YELLOW}[INFO] {message}{Colors.END}")

# Test data
test_user = {
    "email": f"test_{int(time.time())}@example.com",
    "username": "Test User",
    "password": "testpass123"
}

token = None
document_id = None

def test_signup():
    print_test("User Signup")
    try:
        response = requests.post(f"{BASE_URL}/signup", json=test_user)
        if response.status_code == 200:
            data = response.json()
            print_success(f"User created: {data['email']}")
            print_info(f"User ID: {data['id']}")
            return True
        else:
            print_error(f"Signup failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Signup error: {str(e)}")
        return False

def test_login():
    print_test("User Login")
    global token
    try:
        response = requests.post(
            f"{BASE_URL}/login",
            data={
                "username": test_user["email"],
                "password": test_user["password"]
            }
        )
        if response.status_code == 200:
            data = response.json()
            token = data["access_token"]
            print_success("Login successful")
            print_info(f"Token: {token[:50]}...")
            return True
        else:
            print_error(f"Login failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Login error: {str(e)}")
        return False

def test_upload_txt():
    print_test("Upload TXT File")
    global document_id
    try:
        # Create a test file
        test_content = """
        Enterprise Search System Documentation
        
        This is a comprehensive guide to using the enterprise search system.
        The system uses artificial intelligence and machine learning to provide
        accurate search results across all your company documents.
        
        Key features include:
        - Hybrid search combining keyword and semantic search
        - Support for multiple file formats
        - Advanced filtering capabilities
        - Real-time indexing
        
        The search engine uses FAISS for vector storage and BM25 for keyword matching.
        """
        
        files = {'file': ('test_document.txt', test_content, 'text/plain')}
        data = {'tags': 'test, documentation, AI'}
        headers = {'Authorization': f'Bearer {token}'}
        
        response = requests.post(
            f"{BASE_URL}/upload",
            files=files,
            data=data,
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            document_id = result["document_id"]
            print_success(f"File uploaded successfully")
            print_info(f"Document ID: {document_id}")
            print_info(f"Message: {result['message']}")
            return True
        else:
            print_error(f"Upload failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Upload error: {str(e)}")
        return False

def test_upload_md():
    print_test("Upload Markdown File")
    try:
        test_content = """
# Machine Learning Guide

## Introduction
Machine learning is a subset of artificial intelligence that enables systems to learn from data.

## Key Concepts
- **Supervised Learning**: Training with labeled data
- **Unsupervised Learning**: Finding patterns in unlabeled data
- **Neural Networks**: Deep learning architectures
- **Natural Language Processing**: Understanding human language

## Applications
Machine learning powers search engines, recommendation systems, and chatbots.
        """
        
        files = {'file': ('ml_guide.md', test_content, 'text/markdown')}
        data = {'tags': 'machine learning, AI, guide'}
        headers = {'Authorization': f'Bearer {token}'}
        
        response = requests.post(
            f"{BASE_URL}/upload",
            files=files,
            data=data,
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            print_success(f"Markdown file uploaded")
            print_info(f"Document ID: {result['document_id']}")
            return True
        else:
            print_error(f"Upload failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Upload error: {str(e)}")
        return False

def test_search_semantic():
    print_test("Semantic Search")
    try:
        # Wait for indexing
        time.sleep(2)
        
        search_data = {
            "query": "artificial intelligence and machine learning",
            "top_k": 5
        }
        headers = {'Authorization': f'Bearer {token}'}
        
        response = requests.post(
            f"{BASE_URL}/search",
            json=search_data,
            headers=headers
        )
        
        if response.status_code == 200:
            results = response.json()["results"]
            print_success(f"Search completed: {len(results)} results found")
            
            for i, result in enumerate(results[:3], 1):
                print_info(f"\nResult {i}:")
                print(f"  File: {result['filename']}")
                print(f"  Score: {result['score']:.4f}")
                print(f"  Snippet: {result['chunk'][:100]}...")
            return True
        else:
            print_error(f"Search failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Search error: {str(e)}")
        return False

def test_search_keyword():
    print_test("Keyword Search")
    try:
        search_data = {
            "query": "FAISS vector storage BM25",
            "top_k": 5
        }
        headers = {'Authorization': f'Bearer {token}'}
        
        response = requests.post(
            f"{BASE_URL}/search",
            json=search_data,
            headers=headers
        )
        
        if response.status_code == 200:
            results = response.json()["results"]
            print_success(f"Keyword search: {len(results)} results found")
            
            for i, result in enumerate(results[:2], 1):
                print_info(f"\nResult {i}:")
                print(f"  File: {result['filename']}")
                print(f"  Score: {result['score']:.4f}")
            return True
        else:
            print_error(f"Search failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Search error: {str(e)}")
        return False

def test_search_with_filters():
    print_test("Search with Filters")
    try:
        search_data = {
            "query": "machine learning",
            "file_type": "md",
            "tags": "AI",
            "top_k": 5
        }
        headers = {'Authorization': f'Bearer {token}'}
        
        response = requests.post(
            f"{BASE_URL}/search",
            json=search_data,
            headers=headers
        )
        
        if response.status_code == 200:
            results = response.json()["results"]
            print_success(f"Filtered search: {len(results)} results found")
            
            for result in results:
                print_info(f"File: {result['filename']} (Type: {result['file_type']}, Tags: {result['tags']})")
            return True
        else:
            print_error(f"Search failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Search error: {str(e)}")
        return False

def test_get_documents():
    print_test("Get User Documents")
    try:
        headers = {'Authorization': f'Bearer {token}'}
        
        response = requests.get(
            f"{BASE_URL}/documents",
            headers=headers
        )
        
        if response.status_code == 200:
            documents = response.json()
            print_success(f"Retrieved {len(documents)} documents")
            
            for doc in documents:
                print_info(f"- {doc['filename']} ({doc['file_type']}) - {doc['upload_date']}")
            return True
        else:
            print_error(f"Get documents failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Get documents error: {str(e)}")
        return False

def test_unauthorized_access():
    print_test("Unauthorized Access (Security Test)")
    try:
        # Try to search without token
        response = requests.post(
            f"{BASE_URL}/search",
            json={"query": "test"}
        )
        
        if response.status_code == 401:
            print_success("Unauthorized access properly blocked")
            return True
        else:
            print_error(f"Security issue: Expected 401, got {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Security test error: {str(e)}")
        return False

def run_all_tests():
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}ENTERPRISE SEARCH SYSTEM - COMPREHENSIVE TESTING{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")
    
    tests = [
        ("Signup", test_signup),
        ("Login", test_login),
        ("Upload TXT", test_upload_txt),
        ("Upload Markdown", test_upload_md),
        ("Semantic Search", test_search_semantic),
        ("Keyword Search", test_search_keyword),
        ("Filtered Search", test_search_with_filters),
        ("Get Documents", test_get_documents),
        ("Security Test", test_unauthorized_access),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"Test '{name}' crashed: {str(e)}")
            results.append((name, False))
    
    # Summary
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}TEST SUMMARY{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = f"{Colors.GREEN}PASS{Colors.END}" if result else f"{Colors.RED}FAIL{Colors.END}"
        print(f"{name:.<40} {status}")
    
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    percentage = (passed / total) * 100
    color = Colors.GREEN if percentage == 100 else Colors.YELLOW if percentage >= 70 else Colors.RED
    print(f"{color}Results: {passed}/{total} tests passed ({percentage:.1f}%){Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    return passed == total

if __name__ == "__main__":
    try:
        # Check if backend is running
        print_info("Checking if backend is running...")
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        print_success("Backend is running!")
        
        # Run tests
        success = run_all_tests()
        
        if success:
            print(f"\n{Colors.GREEN}[SUCCESS] All tests passed! System is fully functional.{Colors.END}\n")
        else:
            print(f"\n{Colors.YELLOW}[WARNING] Some tests failed. Check the output above.{Colors.END}\n")
            
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to backend. Make sure it's running on http://localhost:8000")
        print_info("Run: start_backend.bat")
    except Exception as e:
        print_error(f"Test suite error: {str(e)}")
