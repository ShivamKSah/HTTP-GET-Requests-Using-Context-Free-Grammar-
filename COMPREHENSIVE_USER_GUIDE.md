# 📚 **CFG QODER - Complete User Guide**

## 🎯 **Table of Contents**
1. [Introduction](#introduction)
2. [Quick Start Guide](#quick-start-guide)
3. [Core Features Overview](#core-features-overview)
4. [Step-by-Step Tutorials](#step-by-step-tutorials)
5. [Advanced Usage](#advanced-usage)
6. [API Reference](#api-reference)
7. [Educational Modules](#educational-modules)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)

---

## 🌟 **Introduction**

Welcome to CFG QODER - the most comprehensive educational platform for learning **Formal Language Automata Theory** through **real-world HTTP protocol analysis**. This guide will take you from beginner to advanced user with practical examples and hands-on tutorials.

### **What is CFG QODER?**
CFG QODER is a unique educational and professional tool that:
- ✅ **Validates HTTP requests** using Context-Free Grammar (CFG) rules
- ✅ **Demonstrates formal automata** (NFA, DFA, PDA) in practice
- ✅ **Integrates computer networks** with formal language theory
- ✅ **Provides NLP capabilities** for text analysis and processing
- ✅ **Offers interactive visualizations** for learning complex concepts

### **Who Should Use This Guide?**
- 🎓 **Computer Science Students** learning formal language theory
- 👨‍💻 **Web Developers** needing HTTP protocol validation
- 🔬 **Researchers** studying formal verification methods
- 👩‍🏫 **Educators** teaching automata theory and networking
- 🏢 **Professional Developers** building protocol compliance tools

---

## 🚀 **Quick Start Guide**

### **Prerequisites**
- **Python 3.10+** installed on your system
- **Node.js 18+** for frontend development
- **Git** for version control (optional)
- **Basic understanding** of HTTP protocols (helpful but not required)

### **Installation Steps**

#### **Step 1: Download the Project**
```bash
# Option A: Clone from repository (if available)
git clone https://github.com/your-repo/cfg-qoder.git
cd cfg-qoder

# Option B: Download and extract ZIP file
# Download from your source and extract to desired directory
```

#### **Step 2: Backend Setup**
```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Start the backend server
python app.py
```

✅ **Backend should now be running at**: `http://localhost:5000`

#### **Step 3: Frontend Setup**
```bash
# Open new terminal and navigate to frontend
cd frontend

# Install Node.js dependencies
npm install

# Start the development server
npm run dev
```

✅ **Frontend should now be accessible at**: `http://localhost:5174`

#### **Step 4: Verify Installation**
1. Open your browser to `http://localhost:5174`
2. You should see the CFG QODER welcome page
3. Try validating a simple request: `GET / HTTP/1.1`
4. If you see a green "Valid" result, everything is working! 🎉

---

## 🎯 **Core Features Overview**

### **1. HTTP Request Validation** 
**Purpose**: Validate HTTP GET requests using formal CFG rules
**Use Cases**: 
- Learning HTTP syntax structure
- Debugging malformed requests
- Educational demonstrations of CFG parsing

**Example**:
```
✅ Valid: GET /index.html HTTP/1.1
❌ Invalid: POST /index.html HTTP/1.1 (wrong method)
❌ Invalid: GET invalid_path HTTP/1.1 (malformed path)
```

### **2. Interactive Parse Tree Visualization**
**Purpose**: Visualize how CFG rules break down HTTP requests
**Educational Value**: 
- Understand CFG derivation steps
- See grammatical structure visually
- Learn formal language parsing

### **3. Advanced Automata Engines**
- **🔄 NFA Engine**: Nondeterministic pattern matching with Thompson's Construction
- **⚡ DFA Engine**: Deterministic pattern matching with Subset Construction  
- **🔍 Regex Matcher**: Compare NFA, DFA, and Python regex performance

### **4. Natural Language Processing**
- **📝 Text Summarization**: 6 different algorithms (TF-IDF, TextRank, LSA, etc.)
- **🤖 Query Processing**: Intelligent question answering about CFG and networking
- **📊 Document Classification**: Categorize technical documents automatically

### **5. Network Protocol Analysis**
- **🌐 TCP State Modeling**: Visualize TCP connection lifecycle
- **📦 Packet Analysis**: Analyze HTTP packet structure and flow
- **✅ Protocol Compliance**: Verify RFC compliance automatically

---

## 📖 **Step-by-Step Tutorials**

### **Tutorial 1: Basic HTTP Request Validation**

#### **Objective**: Learn to validate HTTP requests and understand CFG rules

#### **Step 1: Access the Validator**
1. Open CFG QODER in your browser (`http://localhost:5174`)
2. Click on "**Validator**" in the navigation menu
3. You'll see the main validation interface

#### **Step 2: Try Valid Requests**
Enter these valid HTTP requests one by one:

```http
GET / HTTP/1.1
```
**Expected Result**: ✅ Valid with parse tree showing grammatical breakdown

```http
GET /index.html HTTP/1.0
```
**Expected Result**: ✅ Valid - demonstrates different HTTP version support

```http
GET /api/users/123 HTTP/2.0
```
**Expected Result**: ✅ Valid - shows complex path handling

#### **Step 3: Try Invalid Requests**
Now try these invalid requests to see error handling:

```http
POST /index.html HTTP/1.1
```
**Expected Result**: ❌ Invalid - "Only GET method supported"

```http
GET invalid_path HTTP/1.1
```
**Expected Result**: ❌ Invalid - "Invalid URI format"

```http
GET /index.html HTTP/3.0
```
**Expected Result**: ❌ Invalid - "Unsupported HTTP version"

#### **Step 4: Analyze Parse Trees**
For valid requests:
1. Look at the **parse tree visualization** on the right
2. Notice how the request is broken down into components:
   - `RequestLine` → Root of the parse tree
   - `GET` → HTTP method terminal
   - `RequestTarget` → URI structure
   - `HTTPVersion` → Version identifier

#### **What You Learned**:
- ✅ Basic HTTP request syntax rules
- ✅ How CFG parsing breaks down requests
- ✅ Common validation errors and their causes
- ✅ Parse tree structure and visualization

---

### **Tutorial 2: Understanding Formal Automata**

#### **Objective**: Learn how NFA and DFA engines work with practical examples

#### **Step 1: Access Automata Tools**
1. Navigate to "**Advanced**" → "**Automata Engines**"
2. You'll see three tabs: **NFA**, **DFA**, and **Regex Comparison**

#### **Step 2: NFA Pattern Matching**
1. Click the **NFA** tab
2. Enter pattern: `GET`
3. Enter test text: `GET`
4. Click "**Match Pattern**"

**Expected Result**: 
- ✅ Match successful
- View **execution trace** showing NFA state transitions
- See **epsilon closures** and nondeterministic behavior

#### **Step 3: DFA Pattern Matching**
1. Click the **DFA** tab  
2. Use same pattern: `GET`
3. Enter test text: `GET`
4. Click "**Convert & Match**"

**Expected Result**:
- ✅ Match successful  
- View **DFA construction** from NFA using Subset Construction
- Compare **performance metrics** with NFA

#### **Step 4: Performance Comparison**
1. Click **Regex Comparison** tab
2. Pattern: `^GET\s+/.*\s+HTTP/[12]\.[01]$`
3. Text: `GET /index.html HTTP/1.1`
4. Click "**Compare All Methods**"

**Performance Results**:
```
NFA:    ~0.001s (educational, shows steps)
DFA:    ~0.0005s (optimized, deterministic)  
Python: ~0.0001s (native, highly optimized)
```

#### **What You Learned**:
- ✅ NFA vs DFA differences in practice
- ✅ Thompson's Construction algorithm
- ✅ Subset Construction for NFA→DFA conversion
- ✅ Performance trade-offs between different approaches
- ✅ Real-world applications of formal automata

---

### **Tutorial 3: Natural Language Processing Features**

#### **Objective**: Use NLP capabilities for text analysis and query processing

#### **Step 1: Text Summarization**
1. Navigate to "**NLP**" → "**Text Summarization**"
2. Paste this sample text:
```
The Hypertext Transfer Protocol (HTTP) is an application-layer protocol 
for distributed, collaborative, hypermedia information systems. HTTP is 
the foundation of data communication for the World Wide Web. HTTP functions 
as a request-response protocol in the client-server computing model. A web 
browser, for example, may be the client and an application running on a 
computer hosting a website may be the server.
```
3. Select **TF-IDF** method
4. Set summary length to **2 sentences**
5. Click "**Generate Summary**"

**Expected Result**:
```
HTTP is an application-layer protocol for distributed, collaborative, 
hypermedia information systems. HTTP functions as a request-response 
protocol in the client-server computing model.
```

#### **Step 2: Try Different Algorithms**
Compare results with different summarization methods:
- **TextRank**: Graph-based ranking
- **LSA**: Latent Semantic Analysis  
- **Luhn**: Frequency-based approach

#### **Step 3: Intelligent Query Processing**
1. Navigate to "**NLP**" → "**Query Processing**"
2. Ask: `"What is a context-free grammar?"`
3. Click "**Process Query**"

**Expected Response**:
```
A context-free grammar (CFG) is a formal grammar used to describe 
the syntax of programming languages and protocols. In CFG QODER, 
we use CFG rules to validate HTTP request structure by defining 
production rules that specify valid request components.
```

#### **Step 4: Document Classification**
1. Navigate to "**NLP**" → "**Document Classification**"
2. Enter technical text:
```
This API endpoint accepts POST requests with JSON payload containing 
user authentication credentials. The response includes access tokens 
and user profile information.
```
3. Select **Ensemble** method
4. Click "**Classify**"

**Expected Result**:
```
Category: API Documentation
Confidence: 92%
Method: Ensemble (Rule-based + Naive Bayes)
```

#### **What You Learned**:
- ✅ Multiple text summarization algorithms
- ✅ Intelligent query processing for educational content
- ✅ Automatic document classification
- ✅ NLP integration with CFG and networking concepts

---

### **Tutorial 4: Network Protocol Analysis**

#### **Objective**: Understand network protocol integration with formal methods

#### **Step 1: TCP State Machine**
1. Navigate to "**Networks**" → "**Protocol Analysis**"
2. Click "**TCP State Simulation**"
3. Watch the **interactive TCP state diagram**
4. Click "**Simulate Connection**"

**State Transitions**:
```
CLOSED → LISTEN → SYN_RCVD → ESTABLISHED → 
FIN_WAIT_1 → FIN_WAIT_2 → TIME_WAIT → CLOSED
```

#### **Step 2: HTTP Packet Analysis**
1. Click "**Packet Analysis**" tab
2. Enter HTTP request: `GET /api/data HTTP/1.1`
3. Click "**Analyze Packet Structure**"

**Analysis Results**:
```
Application Layer: HTTP/1.1 Request
Transport Layer: TCP (Port 80/443)
Network Layer: IP (Source → Destination)
Data Link Layer: Ethernet Frame
Physical Layer: Bit transmission
```

#### **Step 3: Protocol Compliance Check**
1. Click "**Compliance Checker**" tab
2. Enter full HTTP request with headers:
```
GET /api/users HTTP/1.1
Host: example.com
User-Agent: CFG-QODER/1.0
Accept: application/json
```
3. Click "**Verify Compliance**"

**Compliance Results**:
```
✅ RFC 7230 HTTP/1.1 Compliance: PASS
✅ Required Headers Present: PASS  
✅ Header Format Valid: PASS
✅ Method-URI Consistency: PASS
Overall Score: 100%
```

#### **What You Learned**:
- ✅ TCP protocol state management
- ✅ HTTP packet structure analysis
- ✅ Multi-layer network protocol stack
- ✅ RFC compliance verification
- ✅ Integration of formal methods with networking

---

## 🔧 **Advanced Usage**

### **Batch Request Validation**
For processing multiple requests efficiently:

```bash
# Using the API directly
curl -X POST http://localhost:5000/api/validate/batch \
  -H "Content-Type: application/json" \
  -d '{
    "requests": [
      "GET / HTTP/1.1",
      "GET /index.html HTTP/1.0", 
      "POST /invalid HTTP/1.1"
    ]
  }'
```

### **Custom Configuration**
Create `config.yaml` for custom settings:

```yaml
environment: development
api:
  host: localhost
  port: 5000
  debug: true
logging:
  level: INFO
  enable_file: true
nlp:
  enable_summarization: true
  max_text_length: 50000
automata:
  enable_nfa: true
  enable_dfa: true
  performance_monitoring: true
```

### **Performance Optimization**
For production deployments:

1. **Enable Caching**:
```python
# In config.yaml
performance:
  enable_caching: true
  cache_timeout: 300
```

2. **Configure Rate Limiting**:
```python
security:
  enable_rate_limiting: true
  rate_limit_default: "1000/hour"
```

3. **Production Logging**:
```python
logging:
  level: WARNING
  enable_console: false
  enable_file: true
```

---

## 📡 **API Reference**

### **Base URL**
- **Development**: `http://localhost:5000/api`
- **Production**: Configure via environment variables

### **Authentication**
Currently no authentication required. Sessions tracked automatically.

### **Core Endpoints**

#### **Validation**
```http
POST /api/validate
Content-Type: application/json

{
  "request_line": "GET /index.html HTTP/1.1"
}
```

**Response**:
```json
{
  "is_valid": true,
  "request_line": "GET /index.html HTTP/1.1", 
  "tokens": ["GET", " ", "/index.html", " ", "HTTP/1.1"],
  "parse_trees": [...],
  "errors": [],
  "timestamp": "2024-01-20T15:30:00Z"
}
```

#### **Grammar Information**
```http
GET /api/grammar
```

**Response**:
```json
{
  "rules": [
    {
      "lhs": "RequestLine",
      "rhs": "GET SP RequestTarget SP HTTPVersion", 
      "rule": "RequestLine → GET SP RequestTarget SP HTTPVersion"
    }
  ],
  "description": "Context-Free Grammar for HTTP GET Request Validation"
}
```

#### **Analytics**
```http
GET /api/analytics?days=7
```

**Response**:
```json
{
  "total_requests": 1250,
  "valid_requests": 1100,
  "invalid_requests": 150,
  "success_rate": 88.0,
  "avg_response_time": 0.045
}
```

### **NLP Endpoints**

#### **Text Summarization**
```http
POST /api/v2/summarization/summarize
Content-Type: application/json

{
  "text": "Long text to summarize...",
  "method": "tf_idf",
  "summary_length": 3
}
```

#### **Query Processing**
```http
POST /api/v2/query/process
Content-Type: application/json

{
  "query": "What is a context-free grammar?"
}
```

#### **Document Classification**  
```http
POST /api/v2/classification/classify
Content-Type: application/json

{
  "text": "Document text to classify...",
  "method": "ensemble"
}
```

---

## 🎓 **Educational Modules**

### **Learning Path 1: Formal Language Theory Basics**

#### **Module 1: Introduction to CFG**
- **Objective**: Understand Context-Free Grammar fundamentals
- **Activities**: 
  1. Explore grammar rules in the Grammar page
  2. Validate simple HTTP requests
  3. Analyze parse trees step-by-step
- **Duration**: 30 minutes

#### **Module 2: Automata Theory**  
- **Objective**: Learn NFA and DFA concepts through HTTP parsing
- **Activities**:
  1. Build NFA for HTTP method recognition
  2. Convert NFA to DFA using Subset Construction
  3. Compare performance and complexity
- **Duration**: 45 minutes

#### **Module 3: Pattern Matching**
- **Objective**: Apply regex theory to real-world protocols  
- **Activities**:
  1. Design regex patterns for URI validation
  2. Compare different matching algorithms
  3. Analyze time/space complexity trade-offs
- **Duration**: 60 minutes

### **Learning Path 2: Computer Networks Integration**

#### **Module 1: Protocol Stack Analysis**
- **Objective**: Understand multi-layer network protocols
- **Activities**:
  1. Trace HTTP packets through protocol layers
  2. Analyze TCP state transitions
  3. Verify protocol compliance
- **Duration**: 45 minutes

#### **Module 2: Formal Verification**
- **Objective**: Apply formal methods to network protocols
- **Activities**:
  1. Model HTTP state machine formally
  2. Verify protocol properties
  3. Detect compliance violations
- **Duration**: 60 minutes

### **Assessment Exercises**

#### **Exercise 1: CFG Design Challenge**
**Task**: Design CFG rules for a new HTTP method `PATCH`
**Requirements**:
1. Define production rules
2. Test with valid/invalid examples  
3. Generate parse trees
**Expected Time**: 20 minutes

#### **Exercise 2: Automata Construction**
**Task**: Build NFA for email address validation
**Requirements**:
1. Design state diagram
2. Implement using Thompson's Construction
3. Convert to DFA and compare performance
**Expected Time**: 30 minutes

#### **Exercise 3: Protocol Analysis**
**Task**: Analyze WebSocket upgrade request
**Requirements**:
1. Identify protocol violations
2. Suggest formal grammar improvements
3. Implement compliance checker
**Expected Time**: 45 minutes

---

## 🔧 **Troubleshooting**

### **Common Issues and Solutions**

#### **Issue 1: Backend Server Won't Start**
**Symptoms**: 
- Error: `ModuleNotFoundError: No module named 'flask'`
- Server fails to start on port 5000

**Solutions**:
```bash
# Solution A: Install missing dependencies
pip install -r requirements.txt

# Solution B: Check Python version
python --version  # Should be 3.10+

# Solution C: Use virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

#### **Issue 2: Frontend Build Errors**
**Symptoms**:
- Error: `Cannot resolve dependency`
- Vite build failures

**Solutions**:
```bash
# Solution A: Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Solution B: Check Node.js version  
node --version  # Should be 18+

# Solution C: Use different package manager
npm install -g yarn
yarn install
yarn dev
```

#### **Issue 3: API Connection Errors**
**Symptoms**:
- Frontend can't connect to backend
- CORS errors in browser console

**Solutions**:
1. **Verify both servers are running**:
   - Backend: `http://localhost:5000/api/health`
   - Frontend: `http://localhost:5174`

2. **Check CORS configuration**:
```python
# In backend/app.py, ensure CORS is enabled:
from flask_cors import CORS
CORS(app, supports_credentials=True)
```

3. **Verify API base URL**:
```typescript
// In frontend/src/utils/api.ts
const api = axios.create({
  baseURL: 'http://localhost:5000/api',  // Correct URL
  timeout: 10000,
  withCredentials: true
});
```

#### **Issue 4: Parse Tree Not Displaying**
**Symptoms**:
- Validation works but no