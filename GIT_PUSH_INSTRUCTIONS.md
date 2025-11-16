# Push to New Git Repository

## Step 1: Initialize Git (if not already done)
```bash
cd "c:\Users\heyia\OneDrive\Desktop\New folder (2)"
git init
```

## Step 2: Add your new remote repository
```bash
git remote add origin YOUR_NEW_REPO_URL
```
Replace `YOUR_NEW_REPO_URL` with your actual GitHub/GitLab repo URL like:
- `https://github.com/yourusername/repo-name.git` or
- `git@github.com:yourusername/repo-name.git`

## Step 3: Add all files
```bash
git add .
```

## Step 4: Commit the files
```bash
git commit -m "Initial commit: ADHD Story Generator with login, games, and AI stories"
```

## Step 5: Push to the new repository
```bash
git branch -M main
git push -u origin main
```

## If you get an error about existing content:
```bash
git push -u origin main --force
```

## One-liner (after adding remote):
```bash
git add . && git commit -m "Initial commit" && git branch -M main && git push -u origin main
```

## To change remote if already set:
```bash
git remote remove origin
git remote add origin YOUR_NEW_REPO_URL
```
