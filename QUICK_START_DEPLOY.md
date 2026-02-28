# SafeMask - Quick Start & Deploy Guide

## FASTEST PATH TO PyPI

Follow these 7 simple steps to deploy SafeMask to PyPI:

### 1. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

### 2. Clone Repository
```bash
git clone https://github.com/amalsp220/safemask.git
cd safemask
```

### 3. Generate All Files
```bash
python complete_build.py
```

### 4. Install Dependencies
```bash
pip install -e \".[dev]\"
```

### 5. Create PyPI Account
Visit https://pypi.org/account/register/ and create an account

### 6. Build Package
```bash
python -m build
```

### 7. Publish to PyPI
```bash
python -m twine upload dist/*
```

Enter your PyPI credentials when prompted.

## Done!

Your SafeMask package is now published on PyPI:
https://pypi.org/project/safemask/

Install it with: `pip install safemask`
