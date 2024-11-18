<div align="center">

# Chappy CLI

<img src="/images/chappy_icon.png" width="200" height="200" alt="Chappy CLI Banner" />

### Supercharge Your Browser Automation Deployment 🚀

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.x-brightgreen.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/docker-required-blue.svg)](https://www.docker.com/)

</div>

## ✨ Overview

Chappy is your all-in-one CLI companion for setting up and deploying browser-based automation testing infrastructure to the cloud. Say goodbye to complex configurations and hello to streamlined deployments for Selenium, Playwright, or Puppeteer projects! 

## 🎯 Key Features

- 🔄 Quick project initialization
- 🐳 Automated Docker environment setup
- ☁️ One-command cloud deployments
- 🛠️ Multi-framework support
- 📊 Real-time logging

## 🚦 Prerequisites

Before you begin, ensure you have these tools installed:

- 🐍 Python 3.x
- 🐳 Docker
- 📦 Node.js (for Playwright projects)
- ☁️ AWS CLI (for AWS deployments)
- 🌐 Azure CLI (for Azure deployments)
- 🏗️ AWS CDK (for AWS deployments)
- 🌍 Google Cloud SDK (for GCP deployments)

## 💻 Installation

```bash
pip install chappy
```

## 🚀 Quick Start

### 1️⃣ Initialize a New Project

```bash
chappy init
```

This interactive wizard will guide you through:
- 📝 Project naming
- 🔧 Framework selection (Selenium/Playwright/Puppeteer)
- ☁️ Cloud provider choice (AWS/Azure/GCP)
- 📁 Project scaffolding

### 2️⃣ Build Your Project

```bash
chappy build
```

Automates:
- 🐳 Docker image creation
- 📦 Dependencies installation
- 🌐 Browser setup

### 3️⃣ Local Development

```bash
chappy run
```

Features:
- 📂 Volume mounting
- 🔌 Port 3000 exposed
- 📊 Live logs

### 4️⃣ Cloud Deployment

```bash
chappy deploy
```

## 📁 Project Structure

```
your_project_name/
├── 📄 config.json         # Project configuration
├── 🐳 Dockerfile         # Docker configuration
└── 📦 [Framework files]
```

## ⚙️ Configuration Options

The `config.json` manages your project settings:

```json
{
  "project_name": "your-project",
  "framework": "playwright",
  "cloud_provider": "aws",
  "config": {
    "region": "us-west-2"
  }
}
```

## 🛠️ Command Reference

| Command | Description |
|---------|-------------|
| `chappy version` | 📊 Show version info |
| `chappy init` | 🆕 Start new project |
| `chappy build` | 🏗️ Build environment |
| `chappy run` | 🏃 Local development |
| `chappy deploy` | 🚀 Cloud deployment |

## 🔧 Troubleshooting

### Common Issues & Solutions

#### 🐳 Docker Problems
```bash
# Verify Docker installation
docker --version

# Check Docker daemon
sudo systemctl status docker
```

#### 🏗️ Build Failures
- Ensure Docker daemon is running
- Verify Dockerfile exists
- Check permissions

#### ☁️ Deployment Issues
- Verify cloud credentials
- Check resource limits
- Review IAM permissions

## 🤝 Contributing

We love contributions! Thank you for considering contributing to Chappy CLI!

### Code of Conduct

Our project adheres to a Code of Conduct that we expect all participants to follow.

### How to Contribute

1. 🍴 Fork the repository
2. 🌿 Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. 💻 Make your changes
4. ✅ Ensure tests pass (`pytest`)
5. 📝 Update documentation as needed
6. 🔍 Run linting (`flake8`)
7. 📦 Commit your changes (`git commit -m 'Add some AmazingFeature'`)
8. 🚀 Push to the branch (`git push origin feature/AmazingFeature`)
9. 🎯 Open a Pull Request

### Development Setup

1. Clone your fork:
```bash
git clone https://github.com/your-username/chappy.git
cd chappy
```

2. Set up development environment:
```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate  # Unix
venv\Scripts\activate     # Windows

# Install development dependencies
pip install -e ".[dev]"
```

3. Run tests:
```bash
pytest
```

### Pull Request Guidelines

- 📝 Include a clear description of the changes
- ✅ Add tests for new features
- 📚 Update documentation as needed
- 🔍 Ensure all tests pass
- 🎯 Keep PRs focused on a single feature/fix

### Reporting Issues

🐛 Found a bug? Have a suggestion? Please open an issue!

When reporting bugs:
1. Check existing issues first
2. Include your environment details
3. Provide steps to reproduce
4. Include expected vs actual behavior

## 📄 License

MIT License

Copyright (c) 2024 Chappy CLI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---
<div align="center">
Made with ❤️ by the Chappy Team
</div>
