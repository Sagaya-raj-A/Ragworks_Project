# 🔍 Enterprise Search System

AI-powered internal document search system with hybrid retrieval combining semantic and keyword search.

![Status](https://img.shields.io/badge/status-production--ready-brightgreen)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688)
![Tests](https://img.shields.io/badge/tests-11%2F11%20passing-success)

## 🎯 Overview

A complete enterprise search solution that allows users to upload documents and search across them using advanced AI retrieval techniques. Think "Google for your company" - but better, with semantic understanding.

### ✨ Key Features

- 🔐 **Secure Authentication** - JWT-based login/signup with bcrypt password hashing
- 📁 **Multi-Format Support** - PDF, DOCX, TXT, and Markdown files
- 🤖 **Hybrid Search** - Combines BM25 (keyword) + Dense Vector Search (semantic)
- 🎯 **High Accuracy** - 78.64% relevance score on semantic queries
- 🏷️ **Smart Filtering** - Filter by file type, tags, upload date, and user
- ⚡ **Fast Performance** - Sub-second search queries
- 🔒 **Data Security** - User-specific document isolation

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- ~500MB disk space (for ML models)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Sagaya-raj/Ragwork_Project.git
cd Ragwork_Project

# 2. Run setup
setup.bat

# 3. Start backend
start_backend.bat

# 4. Open frontend
start_frontend.bat
```

That's it! The system is now running.

## 📖 Usage

1. **Sign Up** - Create your account
2. **Upload Documents** - Drag and drop PDF, DOCX, TXT, or MD files
3. **Search** - Use natural language queries
4. **Filter** - Narrow results by file type or tags

### Example Searches

```
"How does machine learning work?"
"FAISS vector database implementation"
"What are the security measures?"
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Frontend (HTML/JS/CSS)          │
│    Modern UI with Bootstrap 5           │
└──────────────┬──────────────────────────┘
               │ REST API
┌──────────────▼──────────────────────────┐
│         FastAPI Backend                  │
│  • JWT Authentication                    │
│  • Document Processing                   │
│  • Hybrid Search Engine                  │
└──────┬───────────────────┬───────────────┘
       │                   │
┌──────▼────────┐   ┌──────▼──────────────┐
│  SQLite DB    │   │  Search Engine      │
│  • Users      │   │  • FAISS (vectors)  │
│  • Documents  │   │  • BM25 (keywords)  │
└───────────────┘   │  • Embeddings       │
                    └─────────────────────┘
```

## 🔬 Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Async ORM for database operations
- **FAISS** - Facebook AI Similarity Search for vector storage
- **SentenceTransformers** - Generate semantic embeddings (all-MiniLM-L6-v2)
- **BM25** - Probabilistic ranking for keyword search
- **JWT** - Secure token-based authentication
- **bcrypt** - Password hashing

### Frontend
- **HTML5/CSS3/JavaScript**
- **Bootstrap 5** - Responsive UI framework
- **Fetch API** - RESTful API communication

### Search Algorithm
- **Hybrid Retrieval**: 50% semantic + 50% keyword matching
- **Vector Dimension**: 384 (optimized for speed and accuracy)
- **Indexing**: Real-time with ~3s latency
- **Ranking**: Score fusion with metadata filtering

## 📊 Performance

| Metric | Value |
|--------|-------|
| Search Query Time | < 1s |
| Document Upload | < 2s |
| Indexing Time | ~3s |
| Semantic Accuracy | 78.64% |
| Test Pass Rate | 100% (11/11) |

## 🧪 Testing

Comprehensive test suite included:

```bash
python test_final.py
```

**Test Coverage:**
- ✅ Authentication (signup, login, security)
- ✅ File upload (TXT, Markdown, PDF, DOCX)
- ✅ Semantic search
- ✅ Keyword search
- ✅ Filtered search
- ✅ Document retrieval
- ✅ Security validation

## 📁 Project Structure

```
enterprise-search/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── auth.py              # JWT authentication
│   ├── database.py          # Database setup
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── document_processor.py # Text extraction
│   └── search_engine.py     # Hybrid search
├── frontend/
│   ├── index.html           # Login/Signup
│   ├── dashboard.html       # Main interface
│   ├── styles.css           # Custom styling
│   ├── auth.js              # Auth logic
│   └── dashboard.js         # Dashboard logic
├── requirements.txt         # Dependencies
├── setup.bat               # Setup script
└── README.md               # Documentation
```

## 🔒 Security Features

- **Password Hashing**: bcrypt with salt
- **JWT Tokens**: 24-hour expiration
- **User Isolation**: Document access by user_id
- **SQL Injection Prevention**: SQLAlchemy ORM
- **CORS Configuration**: Controlled origins
- **Input Validation**: Pydantic schemas

## 🎯 Use Cases

- **Internal Knowledge Base** - Search company documentation
- **Research Papers** - Find relevant academic papers
- **Legal Documents** - Search contracts and agreements
- **Technical Documentation** - Find API docs and guides
- **Meeting Notes** - Search across team notes
- **Project Files** - Locate project-related documents

## 📈 Roadmap

- [ ] RAG (Retrieval-Augmented Generation) for answer generation
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Collaborative features
- [ ] Document versioning
- [ ] Cloud deployment guides

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Sagayaraj A**
- GitHub: [@Sagaya-raj](https://github.com/Sagaya-raj)

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- Facebook Research for FAISS
- Sentence-Transformers for embeddings
- The open-source community

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the documentation in `README.md`
- Review `QUICKSTART.md` for setup help

---

**⭐ Star this repo if you find it useful!**

Built with ❤️ using Python, FastAPI, and AI
