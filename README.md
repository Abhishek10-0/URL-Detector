# 🛡️ URL Security Scanner

A full-stack web application that analyzes URLs for malicious patterns and security threats. Detects SQL Injection, XSS, Command Injection, Path Traversal, and 8+ other attack types.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![React](https://img.shields.io/badge/React-18.3-61DAFB.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
  - [Clone from GitHub](#-clone-from-github)
  - [Backend Setup](#-backend-setup)
  - [Frontend Setup](#-frontend-setup)
- [How to Run](#-how-to-run)
- [API Documentation](#-api-documentation)
- [Usage Examples](#-usage-examples)
- [Detection Capabilities](#-detection-capabilities)
- [Screenshots](#-screenshots)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

✅ **Real-time URL Analysis** - Instant security scanning  
✅ **Multi-threat Detection** - Detects 8+ attack types  
✅ **Risk Scoring** - 0-100 risk score calculation  
✅ **Detailed Reporting** - Evidence-based threat breakdown  
✅ **Smart Whitelisting** - Avoids false positives for legitimate URLs  
✅ **Modern UI** - Beautiful gradient design with Tailwind CSS  
✅ **REST API** - Easy integration with other applications  
✅ **Fast Performance** - Analysis completed in <1 second  

---

## 🛠️ Tech Stack

### Backend
- **Python 3.8+** - Core language
- **Flask 3.0.0** - Web framework
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **React 18.3** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Lucide React** - Icons

---

## 📁 Project Structure

```
url-detector/
├── backend/
│   ├── app.py              # Flask REST API server
│   ├── detector.py         # URL detection engine
│   └── requirements.txt    # Python dependencies
│
└── frontend/
    ├── src/
    │   ├── App.jsx                    # Main React component
    │   ├── main.jsx                   # React entry point
    │   ├── index.css                  # Global styles
    │   └── components/
    │       └── URLScanner.jsx         # Scanner component
    ├── public/
    ├── index.html                     # HTML template
    ├── package.json                   # npm dependencies
    ├── vite.config.js                 # Vite configuration
    ├── tailwind.config.js             # Tailwind configuration
    └── postcss.config.js              # PostCSS configuration
```

---

## 🚀 Installation

### 📥 Clone from GitHub

```bash
# Clone the repository
git clone https://github.com/your-username/url-detector.git

# Navigate to project directory
cd url-detector
```

---

### 🐍 Backend Setup

#### 1️⃣ Navigate to backend directory
```bash
cd backend
```

#### 2️⃣ Create virtual environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3️⃣ Install Python dependencies
```bash
pip install -r requirements.txt
```

**requirements.txt includes:**
- Flask==3.0.0
- flask-cors==4.0.0
- Werkzeug==3.0.1

#### 4️⃣ Verify installation
```bash
python app.py
```

You should see:
```
🚀 URL Detector API Starting...
📡 Server running on http://localhost:5000
```

---

### ⚛️ Frontend Setup

#### 1️⃣ Open new terminal and navigate to frontend
```bash
cd frontend
```

#### 2️⃣ Install Node.js dependencies
```bash
npm install
```

This will install:
- React 18.3
- Vite
- Tailwind CSS
- Lucide React (icons)
- All dev dependencies

#### 3️⃣ Verify installation
```bash
npm run dev
```

You should see:
```
VITE v5.4.2  ready in 500 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

---

## ▶️ How to Run

### Method 1: Two Terminal Windows (Recommended)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate     # Windows: venv\Scripts\activate
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Method 2: Background Process (Linux/Mac)

```bash
# Start backend in background
cd backend && source venv/bin/activate && python app.py &

# Start frontend
cd frontend && npm run dev
```

### ✅ Access the Application

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:5000
- **API Health Check:** http://localhost:5000/api/health

---

## 📚 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1️⃣ Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "URL Detector API",
  "version": "1.0"
}
```

---

#### 2️⃣ Analyze URL
```http
POST /api/analyze
Content-Type: application/json
```

**Request Body:**
```json
{
  "url": "https://example.com/login?id=1' OR '1'='1"
}
```

**Response:**
```json
{
  "success": true,
  "url": "https://example.com/login?id=1' OR '1'='1",
  "decoded_url": "https://example.com/login?id=1' or '1'='1",
  "verdict": "MALICIOUS",
  "verdict_color": "red",
  "risk_score": 75,
  "threats_detected": ["SQL_INJECTION"],
  "reasons": [
    {
      "category": "SQL Injection",
      "severity": "critical",
      "description": "SQL comparison logic",
      "evidence": "' or '1'='1"
    }
  ],
  "metadata": {
    "url_length": 45,
    "encoding_layers": 0,
    "entropy": 3.82,
    "is_https": true,
    "has_ip": false,
    "domain": "example.com"
  }
}
```

---

#### 3️⃣ Batch Analyze (Bonus)
```http
POST /api/batch-analyze
Content-Type: application/json
```

**Request Body:**
```json
{
  "urls": [
    "https://google.com",
    "https://site.com/login?id=1' OR '1'='1"
  ]
}
```

---

## 🎯 Usage Examples

### Safe URLs ✅
```
https://google.com
https://github.com/user/repo
https://open.spotify.com/track/abc?si=xyz
http://localhost:8080/api
http://192.168.1.1/admin
```

### Malicious URLs ⚠️
```
https://site.com/login?id=1' OR '1'='1
https://site.com/search?q=<script>alert(1)</script>
https://site.com/file?path=../../etc/passwd
https://site.com/ping?host=8.8.8.8;cat /etc/passwd
https://evil.com/redirect?url=javascript:alert(1)
```

---

## 🔍 Detection Capabilities

### Attack Types Detected

| Attack Type | Patterns | Severity |
|------------|----------|----------|
| **SQL Injection** | 40+ patterns | Critical |
| **XSS (Cross-Site Scripting)** | 15+ patterns | Critical |
| **Command Injection** | 10+ patterns | Critical |
| **Path Traversal** | 8+ patterns | Critical |
| **LDAP Injection** | 6+ patterns | High |
| **XML/XXE Injection** | 8+ patterns | Critical |
| **SSRF** | 10+ patterns | High |
| **NoSQL Injection** | 7+ patterns | High |
| **Template Injection** | 11+ patterns | High |
| **Prototype Pollution** | 4+ patterns | Critical |
| **CRLF Injection** | 6+ patterns | Critical |
| **Log Injection** | 5+ patterns | Medium |

### Verdict Categories

| Verdict | Risk Score | Color | Description |
|---------|------------|-------|-------------|
| 🟢 **CLEAN** | 0 | Green | No threats detected |
| 🔵 **LOW RISK** | 1-14 | Blue | Minor suspicious patterns |
| 🟡 **WARNING** | 15-39 | Yellow | Moderate concerns |
| 🟠 **SUSPICIOUS** | 40-69 | Orange | Highly suspicious |
| 🔴 **MALICIOUS** | 70-100 | Red | Definitely dangerous |

---

## 📸 Screenshots

### Clean URL Result
```
🟢 CLEAN | Risk Score: 0/100
✅ No security issues detected
```

### Malicious URL Result
```
🔴 MALICIOUS | Risk Score: 85/100
⚠️ Threats Detected: SQL_INJECTION, XSS
📋 3 Critical Issues Found
```

<!-- ---

## 🐛 Troubleshooting

### Backend Issues

**Problem:** Port 5000 already in use
```python
# Solution: Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)

# Update frontend URLScanner.jsx
fetch('http://localhost:5001/api/analyze', ...)
```

**Problem:** Module not found errors
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt
```

**Problem:** CORS errors
```bash
# Solution: Install flask-cors
pip install flask-cors
```

--- -->
<!-- 
### Frontend Issues

**Problem:** Cannot connect to backend
```
Solution: 
1. Ensure backend is running on port 5000
2. Check browser console for errors
3. Verify CORS is enabled in app.py
```

**Problem:** Tailwind CSS not working
```bash
# Solution: Reinstall Tailwind
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

**Problem:** Build errors
```bash
# Solution: Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
``` -->

<!-- ---

## 🔒 Security Notes

⚠️ **This tool is for educational and security testing purposes only**

- Use on URLs you own or have permission to test
- Do not use for malicious purposes
- Not a replacement for professional security audits
- False negatives/positives may occur

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@your-username](https://github.com/your-username)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- Flask documentation
- React & Vite teams
- Tailwind CSS
- Security research community

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Open an [Issue](https://github.com/your-username/url-detector/issues)
3. Contact via email

---

## 🗺️ Roadmap

- [ ] Add more attack pattern detection
- [ ] Implement rate limiting
- [ ] Add user authentication
- [ ] Create browser extension
- [ ] Add URL history tracking
- [ ] Export reports as PDF
- [ ] Multi-language support

--- -->

**⭐ If you find this project useful, please give it a star!**

**Made with ❤️ for cybersecurity education**