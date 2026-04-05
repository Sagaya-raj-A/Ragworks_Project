# 🚀 Enterprise Search System - NOW RUNNING

## Current Status

✅ **Backend:** Running on http://localhost:8000  
✅ **Frontend:** Opened in your browser  
✅ **Database:** enterprise_search.db (SQLite)  
✅ **Search Index:** Loaded and ready

---

## What's Open

1. **Backend Server** - FastAPI running on port 8000
2. **Frontend UI** - Login/Signup page opened in your browser

---

## Quick Start Guide

### Step 1: Create an Account
1. You should see the login page in your browser
2. Click the "Sign Up" tab
3. Enter:
   - Username: Your name
   - Email: your.email@example.com
   - Password: Choose a secure password
4. Click "Sign Up"

### Step 2: Login
1. Switch to the "Login" tab
2. Enter your email and password
3. Click "Login"
4. You'll be redirected to the dashboard

### Step 3: Upload Documents
1. On the dashboard, find the "Upload Document" section (left sidebar)
2. Click "Choose File" and select a document:
   - Supported: PDF, DOCX, TXT, Markdown (.md)
3. Optionally add tags (e.g., "report, 2024, finance")
4. Click "Upload"
5. Wait for confirmation

### Step 4: Search Your Documents
1. Use the search bar at the top
2. Type your query (e.g., "machine learning algorithms")
3. Click "Search" or press Enter
4. View results with relevance scores

### Step 5: Use Filters (Optional)
1. In the left sidebar, find "Filters"
2. Select file type (PDF, DOCX, TXT, MD)
3. Enter tags to filter by
4. Search again to see filtered results

---

## Example Searches to Try

Once you've uploaded some documents, try these searches:

### Semantic Search (AI-powered)
- "How does artificial intelligence work?"
- "What are the benefits of machine learning?"
- "Explain neural networks"

### Keyword Search
- "FAISS vector database"
- "BM25 algorithm implementation"
- "JWT authentication security"

### With Filters
- Search: "project report"
- Filter by: File type = PDF
- Filter by: Tags = "2024"

---

## Features Available

### 🔐 Authentication
- ✅ Secure signup with email validation
- ✅ Login with JWT tokens
- ✅ Password hashing (bcrypt)
- ✅ Session management

### 📁 Document Management
- ✅ Upload PDF, DOCX, TXT, Markdown
- ✅ Automatic text extraction
- ✅ Tag-based organization
- ✅ View all your documents

### 🔍 Hybrid Search
- ✅ Semantic search (understands meaning)
- ✅ Keyword search (exact matches)
- ✅ Combined scoring for best results
- ✅ Relevance scores displayed

### 🎯 Filtering
- ✅ Filter by file type
- ✅ Filter by tags
- ✅ Filter by upload date
- ✅ User-specific results

---

## API Endpoints (for developers)

If you want to use the API directly:

### Authentication
```bash
# Signup
POST http://localhost:8000/signup
Body: {"email": "user@example.com", "username": "User", "password": "pass123"}

# Login
POST http://localhost:8000/login
Body: username=user@example.com&password=pass123
```

### Documents
```bash
# Upload (requires auth token)
POST http://localhost:8000/upload
Headers: Authorization: Bearer <token>
Body: multipart/form-data with file and tags

# Search (requires auth token)
POST http://localhost:8000/search
Headers: Authorization: Bearer <token>
Body: {"query": "search term", "file_type": "pdf", "top_k": 10}

# Get Documents (requires auth token)
GET http://localhost:8000/documents
Headers: Authorization: Bearer <token>
```

### API Documentation
Visit: http://localhost:8000/docs (Swagger UI)

---

## Sample Documents to Upload

Create these test files to try the system:

### 1. test_ai.txt
```
Artificial Intelligence and Machine Learning

AI is transforming how we process information. Machine learning
algorithms can learn from data and make predictions. Deep learning
uses neural networks to understand complex patterns.

Key concepts:
- Supervised learning
- Unsupervised learning
- Neural networks
- Natural language processing
```

### 2. project_notes.md
```
# Project Notes

## Overview
This project implements a hybrid search system using:
- FAISS for vector storage
- BM25 for keyword matching
- SentenceTransformers for embeddings

## Features
- Multi-format support
- Real-time indexing
- Semantic search
```

---

## Troubleshooting

### Frontend not loading?
- Check if the browser opened
- Manually open: `frontend/index.html`
- Or navigate to: `file:///C:/New folder/frontend/index.html`

### Can't connect to backend?
- Check if backend is running (should see "Uvicorn running" message)
- Try: http://localhost:8000/docs
- Restart backend: Stop and run `start_backend.bat`

### Upload fails?
- Check file format (PDF, DOCX, TXT, MD only)
- Ensure you're logged in
- Check file size (keep under 10MB)

### Search returns no results?
- Wait a few seconds after upload for indexing
- Try different search terms
- Check if documents were uploaded (view "My Documents")

---

## Stopping the System

### To stop the backend:
1. Go to the terminal running the backend
2. Press `Ctrl+C`
3. Or close the terminal window

### To restart:
```bash
start_backend.bat
```

---

## What's Happening Behind the Scenes

When you upload a document:
1. ✅ File is received by FastAPI
2. ✅ Text is extracted (PDF/DOCX/TXT/MD)
3. ✅ Text is cleaned and chunked
4. ✅ Embeddings are generated (384-dimensional vectors)
5. ✅ Vectors stored in FAISS index
6. ✅ BM25 index updated
7. ✅ Metadata saved to database

When you search:
1. ✅ Query converted to embedding
2. ✅ FAISS finds similar vectors (semantic)
3. ✅ BM25 finds keyword matches
4. ✅ Scores combined (50/50 fusion)
5. ✅ Results filtered by metadata
6. ✅ Top results returned with scores

---

## Performance Tips

### For best search results:
- Use natural language queries
- Be specific but not too narrow
- Try both short and long queries
- Use filters to narrow results

### For faster uploads:
- Keep files under 5MB
- Use TXT or MD for fastest processing
- PDF and DOCX take slightly longer

---

## Next Steps

1. ✅ **Upload your first document**
2. ✅ **Try a search query**
3. ✅ **Experiment with filters**
4. ✅ **Upload more documents**
5. ✅ **Compare search results**

---

## System Information

- **Backend:** FastAPI 0.109.0
- **Database:** SQLite (async)
- **Vector Store:** FAISS 1.7.4
- **Embeddings:** all-MiniLM-L6-v2 (384 dimensions)
- **Search:** Hybrid (BM25 + Dense Vectors)
- **Auth:** JWT tokens (24-hour expiry)

---

## Support Files

- **README.md** - Full documentation
- **QUICKSTART.md** - Quick start guide
- **TEST_REPORT.md** - Test results
- **PROJECT_SUMMARY.md** - System overview

---

**Enjoy your Enterprise Search System!** 🎉

The system is now running and ready to use. Start by creating an account and uploading your first document!
