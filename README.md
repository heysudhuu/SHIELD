# 🛡️ SHIELD // CORE
### Personal Security Console

A modern cybersecurity toolkit built in Python that provides essential security utilities through an intuitive desktop interface.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Security](https://img.shields.io/badge/Security-Toolkit-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📸 Preview

### Main Dashboard

<img src="screenshots/dashboard.png" width="900">

---

## 🚀 Features

### 🔐 Cryptographically Secure Password Generator
Generate strong passwords using Python's `secrets` module.

**Features**
- Custom password length
- Uppercase letters
- Lowercase letters
- Numeric digits
- Special characters
- Copy-to-clipboard support
- Password strength scoring

---

### 🛡️ Password Strength Analyzer

Analyze password security and receive detailed feedback.

Checks include:

- Password length
- Character diversity
- Complexity score
- Common weakness detection
- Security recommendations

---

### 🌐 Port Scanner (Educational)

Educational port scanning utility for learning networking concepts.

**Capabilities**

- Scan common TCP ports
- Detect open ports
- Service identification
- Learning-focused implementation

> ⚠️ Intended for educational and authorized environments only.

---

### 📡 Network Scanner (Educational)

Simulates and demonstrates local network discovery techniques.

**Features**

- Host discovery simulation
- Device identification
- MAC address mapping
- Security advisory reporting
- Network visualization concepts

> ⚠️ Educational use only.

---

### 🔍 File Hash Integrity Checker

Verify file integrity using cryptographic hash functions.

Supported algorithms:

- MD5
- SHA1
- SHA256
- SHA512

Use cases:

- File verification
- Integrity monitoring
- Security auditing

---

### 📊 History & Reports

Track previous operations and maintain logs.

Features include:

- Scan history
- Generated reports
- JSON-based storage
- Activity tracking

---

### 🌙 Modern UI

Built with a cybersecurity-inspired interface.

- Dark Mode
- Responsive Layout
- Sidebar Navigation
- Modern Security Dashboard Design
- Neon Cyber Theme

---

## 🏗️ Project Structure

```text
CyberToolkit/
│
├── modules/
│   ├── password_generator.py
│   ├── password_checker.py
│   ├── port_scanner.py
│   ├── network_scanner.py
│   └── hash_checker.py
│
├── reports/
│
├── scan_history.json
├── requirements.txt
├── main.py
│
└── README.md
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/heysudhuu/SHIELD.git

cd shield-core
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

**Windows**

```bash
.venv\Scripts\activate
```

**Linux/macOS**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Application

```bash
python main.py
```

---

## 🧰 Technologies Used

- Python
- Tkinter / CustomTkinter
- Secrets Module
- Hashlib
- Socket Programming
- JSON Storage
- Threading

---

## 🎯 Learning Objectives

This project was created to explore:

- Cybersecurity fundamentals
- Password security
- Cryptographic hashing
- Network discovery concepts
- Port scanning techniques
- GUI application development
- Secure coding practices

---

## 🔒 Security Notice

This project is intended strictly for:

✅ Education  
✅ Learning  
✅ Personal Security Awareness  
✅ Authorized Testing Environments

Do not use any scanning functionality against systems or networks without proper authorization.

---

## 📈 Future Improvements

- [ ] Real-time network monitoring
- [ ] Vulnerability assessment module
- [ ] Password breach checking
- [ ] Export reports to PDF
- [ ] Multi-theme support
- [ ] User authentication system
- [ ] Dashboard analytics

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Sudhanshu**

Cybersecurity Enthusiast • Computer Science Engineer

> "Security is not a product, but a process."
