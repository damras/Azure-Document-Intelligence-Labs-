# Git Push Guide for DIworkshop Repository

## ✅ Pre-Push Checklist

Before pushing to GitHub, verify:
- [x] `.gitignore` created (prevents .venv and .env from being committed)
- [x] `.env.example` created (template for others)
- [x] Main README.md created at repository root
- [x] Labs/README.md exists (workshop guide)

## 🚀 Step-by-Step Git Push Instructions

### Step 1: Initialize Git Repository (if not already done)

Open PowerShell or Command Prompt in the DIworkshop folder:

```powershell
# Navigate to the repository root
cd W:\Engagements\QNB\DIworkshop

# Initialize git (skip if already initialized)
git init
```

### Step 2: Verify .gitignore is Working

Check what will be committed:

```powershell
# See what files git will track
git status
```

**Important:** You should **NOT** see:
- `.venv/` folder
- `Labs/.env` file
- `__pycache__/` folders

If you see these, verify `.gitignore` is in the root folder.

### Step 3: Add Remote Repository

Replace `<your-repository-url>` with your actual GitHub repository URL:

```powershell
# Add your GitHub repository as remote
git remote add origin <your-repository-url>

# Example:
# git remote add origin https://github.com/yourusername/azure-document-intelligence-workshop.git
```

### Step 4: Stage All Files

```powershell
# Add all files (respecting .gitignore)
git add .

# Verify what will be committed
git status
```

**What you SHOULD see:**
- ✅ README.md
- ✅ .gitignore
- ✅ Labs/README.md
- ✅ Labs/.env.example
- ✅ Labs/requirements.txt
- ✅ All Python scripts (.py files)
- ✅ All data folders with sample files
- ✅ All lab README.md files

**What you should NOT see:**
- ❌ .venv/
- ❌ Labs/.env (your actual credentials)
- ❌ __pycache__/
- ❌ *.pyc files

### Step 5: Create First Commit

```powershell
git commit -m "Initial commit: Azure Document Intelligence Workshop with 4 labs"
```

### Step 6: Push to GitHub

```powershell
# Push to main branch (or master, depending on your default branch)
git push -u origin main

# If your default branch is master, use:
# git push -u origin master

# If you encounter branch name issues, create and push to main:
# git branch -M main
# git push -u origin main
```

### Step 7: Verify on GitHub

1. Go to your GitHub repository URL
2. Check that all files are present
3. **Most Important:** Verify that `.env` file is **NOT** visible
4. Verify that `.venv` folder is **NOT** visible
5. Check that README.md displays nicely

## 🔒 Security Verification

After pushing, double-check:

```powershell
# List what's in your remote repository
git ls-tree -r main --name-only

# Make sure .env is NOT in this list
# Make sure .venv/ is NOT in this list
```

## 📝 What Gets Pushed vs. Ignored

### ✅ Pushed to GitHub (Safe):
```
DIworkshop/
├── README.md                          ✅
├── .gitignore                         ✅
└── Labs/
    ├── README.md                      ✅
    ├── .env.example                   ✅ (template only)
    ├── requirements.txt               ✅
    ├── lab-1-read/
    │   ├── README.md                  ✅
    │   ├── data/                      ✅ (sample files)
    │   ├── read.py                    ✅
    │   ├── searchable_pdf.py          ✅
    │   └── read_batch_demo.py         ✅
    ├── lab-2-layout/
    │   ├── README.md                  ✅
    │   ├── data/                      ✅
    │   └── layout.py                  ✅
    ├── lab-3-general/
    │   ├── README.md                  ✅
    │   ├── data/                      ✅
    │   └── general_document.py        ✅
    └── lab-4-prebuilt-models/
        ├── README.md                  ✅
        ├── 1-bank-statements/         ✅
        ├── 2-invoices/                ✅
        ├── 3-credit-cards/            ✅
        ├── 4-identity-documents/      ✅
        └── 5-receipts/                ✅
```

### ❌ Ignored (NOT pushed - Local only):
```
Labs/
├── .env                               ❌ (contains your Azure credentials)
├── .venv/                             ❌ (virtual environment)
├── __pycache__/                       ❌ (Python cache)
└── lab-1-read/
    └── data/
        └── read_searchable.pdf        ❌ (generated output)
```

## 🆘 Troubleshooting

### Problem: .env file was accidentally committed

If you accidentally committed `.env`:

```powershell
# Remove .env from git tracking (keeps local file)
git rm --cached Labs/.env

# Commit the removal
git commit -m "Remove .env file from repository"

# Push the change
git push origin main
```

### Problem: .venv folder was committed

```powershell
# Remove .venv from git tracking
git rm -r --cached Labs/.venv

# Commit the removal
git commit -m "Remove .venv folder from repository"

# Push the change
git push origin main
```

### Problem: "fatal: remote origin already exists"

```powershell
# Remove existing remote
git remote remove origin

# Add the correct remote
git remote add origin <your-repository-url>
```

### Problem: Branch name mismatch (main vs master)

```powershell
# Rename current branch to main
git branch -M main

# Push to main
git push -u origin main
```

## 📊 Final Checklist

After pushing, verify on GitHub:

- [ ] Repository README.md displays properly
- [ ] Labs/README.md is accessible
- [ ] All 4 lab folders are present
- [ ] All Python scripts are present
- [ ] Sample data files are present
- [ ] `.env` file is **NOT** visible ⚠️
- [ ] `.venv` folder is **NOT** visible ⚠️
- [ ] `.env.example` **IS** visible ✅
- [ ] `.gitignore` **IS** visible ✅

## 🎉 Success!

Your repository is now live on GitHub and ready for others to clone and use!

**What users will do:**
1. Clone your repository
2. Copy `.env.example` to `.env`
3. Fill in their own Azure credentials
4. Create their own virtual environment
5. Install dependencies
6. Start Lab 1

## 📝 Future Updates

To push changes in the future:

```powershell
# Check what changed
git status

# Add changes
git add .

# Commit with descriptive message
git commit -m "Description of changes"

# Push to GitHub
git push origin main
```

## 🔗 Share Your Repository

Once pushed, share your repository URL with others:
```
https://github.com/yourusername/your-repository-name
```

Users can clone it with:
```bash
git clone https://github.com/yourusername/your-repository-name.git
```

---

**Important:** Always verify that sensitive files (.env, credentials) are never committed to GitHub!
