# Django Calculator App --- GitHub Workflow Documentation

This README documents the **journey of pushing the Django Calculator
project to GitHub**.\
It starts from when the project was complete locally, and covers every
step, question, and solution along the way.

------------------------------------------------------------------------

## Step 1 --- Verify Git installation

I asked:

> **"should I come out of venv?"**

Answer: **Yes.**\
Deactivate the virtual environment first so you're just using system
tools (not the venv):

``` powershell
deactivate
```

Then check Git:

``` powershell
git --version
```

✅ Output:

    git version 2.50.1.windows.1

------------------------------------------------------------------------

## Step 2 --- Configure Git identity

I wasn't sure if I already set it up, so I asked:

> **"i think i did this but i don't remember what name and email i
> gave"**

Solution: run:

``` powershell
git config --global user.name
git config --global user.email
```

✅ Output showed:

    dolleena
    mleenashu@gmail.com

So my identity was already configured.

------------------------------------------------------------------------

## Step 3 --- Initialize Git repo

I asked:

> **"inside the django calc?"**

Answer: **Yes.**\
Run `git init` inside the project root
(`C:\Users\Me\projects\django-calc`), where `manage.py` lives.

``` powershell
git init
git status
```

✅ Output:

    Initialized empty Git repository in C:/Users/Me/projects/django-calc/.git/
    On branch master

    No commits yet

    Untracked files:
      calcsite/
      calculator/
      db.sqlite3
      manage.py

------------------------------------------------------------------------

## Step 4 --- Create `.gitignore`

Created `.gitignore` in project root:

``` gitignore
# Python
__pycache__/
*.py[cod]

# Django database
*.sqlite3

# Virtual environment
.venv/

# Logs
*.log

# VS Code
.vscode/

# Static files
/staticfiles/
```

This ensures unnecessary files (like `db.sqlite3` and `.venv`) aren't
tracked.

------------------------------------------------------------------------

## Step 5 --- First commit

Stage and commit all project files:

``` powershell
git add .
git commit -m "Initial commit: Django calculator app"
```

✅ Output:

    [master (root-commit) 50111d6] Initial commit: Django calculator app
     20 files changed, 1123 insertions(+)
     create mode 100644 .gitignore
     create mode 100644 calcsite/__init__.py
     create mode 100644 calcsite/settings.py
     ...
     create mode 100644 manage.py

------------------------------------------------------------------------

## Step 6 --- Create GitHub repo

On GitHub: - Created a new repo named **django-calc** - Left it empty
(no README, no .gitignore, no license)

------------------------------------------------------------------------

## Step 7 --- Add remote

I asked:

> **"how to check my origin?"**

Solution: run:

``` powershell
git remote -v
```

Initially there was no origin, so I added one:

``` powershell
git remote add origin https://github.com/dolleena/django-calc.git
git remote -v
```

✅ Output:

    origin  https://github.com/dolleena/django-calc.git (fetch)
    origin  https://github.com/dolleena/django-calc.git (push)

------------------------------------------------------------------------

## Step 8 --- Push code

I asked:

> **"we should push in main or master branch?"**

Answer: GitHub defaults to `main`. Local repo started on `master`.\
So I renamed `master` → `main` and pushed:

``` powershell
git branch -M main
git push -u origin main
```

✅ This uploaded all files to GitHub.

------------------------------------------------------------------------

## Step 9 --- Verify

On GitHub, I now see: - All project files - README.md - Django app
structure

------------------------------------------------------------------------

## Step 10 --- What about `db.sqlite3`?

I asked:

> **"what is db.sqlite3? why we did not copy it in git?"**

Answer: - `db.sqlite3` is the **local SQLite database** created by
Django.\
- It contains **data** (your test calculations, superuser account).\
- We don't commit it because: - It changes constantly - Everyone should
generate their own DB locally with:
`powershell     python manage.py migrate` - Instead, we commit: -
`models.py` → schema definition - `migrations/` → instructions to create
schema

So the DB can always be recreated, but personal/test data is not shared.

------------------------------------------------------------------------

## Step 11 --- Updating in the future

To save new changes:

``` powershell
git add .
git commit -m "Describe what you changed"
git push
```

That's it 🎉

------------------------------------------------------------------------

# Final Notes

-   Project repo:
    **[django-calc](https://github.com/dolleena/django-calc)**\
-   Includes:
    -   Full Django calculator app
    -   Delete feature
    -   Admin integration
    -   README with step-by-step setup
-   This README documents the **exact GitHub workflow and Q&A** during
    setup.

------------------------------------------------------------------------
