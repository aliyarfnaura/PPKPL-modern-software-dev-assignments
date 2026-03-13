# Week 6 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **Aliya Raffa Naura Ayu** \
SUNet ID: **N/A** \
Citations: **Semgrep documentation, Warp AI assistant**

This assignment took me about **1.5 hours** hours to do. 


## Brief findings overview 
> A static security scan was performed using Semgrep on the Week 6 application, which includes a FastAPI backend and a JavaScript frontend. The scan analyzed 19 files and applied hundreds of security rules.

The initial scan detected six security findings, including:

- Insecure CORS configuration
- SQL injection risk in a SQLAlchemy query
- Cross-site scripting (XSS) in the frontend
- Use of unsafe functions such as eval
- Use of subprocess with shell=True
- Dynamic URL usage with urllib

For this assignment, three vulnerabilities were selected and remediated using the Warp AI coding assistant. After applying the fixes and running Semgrep again, the number of findings was reduced.

## Fix #1
a. File and line(s)
> backend/app/main.py, line 24

b. Rule/category Semgrep flagged
> python.fastapi.security.wildcard-cors.wildcard-cors

c. Brief risk description
> The application allowed all origins using the wildcard "*". This configuration is insecure because it allows any website to access the API, which may expose the application to unauthorized cross-origin requests.

d. Your change (short code diff or explanation, AI coding tool usage)
> Before:

allow_origins=["*"]

After:

allow_origins=[
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

Warp AI was used to analyze the Semgrep result and suggest restricting the allowed origins instead of using a wildcard.

e. Why this mitigates the issue
> Restricting CORS origins ensures that only trusted local clients can access the API, preventing arbitrary external websites from interacting with the backend.

## Fix #2
a. File and line(s)
> backend/app/routers/notes.py, lines 71–78

b. Rule/category Semgrep flagged
> python.sqlalchemy.security.audit.avoid-sqlalchemy-text

c. Brief risk description
> The SQL query used string interpolation with an f-string that directly inserted user input into the query. This creates a risk of SQL injection, where malicious users could manipulate the database query.

d. Your change (short code diff or explanation, AI coding tool usage)
> Before:

sql = text(
        f"""
        SELECT id, title, content, created_at, updated_at
        FROM notes
        WHERE title LIKE '%{q}%' OR content LIKE '%{q}%'
        ORDER BY created_at DESC
        LIMIT 50
        """
    )
    rows = db.execute(sql).all()



After:

sql = text(
        """
        SELECT id, title, content, created_at, updated_at
        FROM notes
        WHERE title LIKE '%' || :q || '%' OR content LIKE '%' || :q || '%'
        ORDER BY created_at DESC
        LIMIT 50
        """
    )
    rows = db.execute(sql, {"q": q}).all()

Warp AI suggested converting the query to use parameterized SQLAlchemy bind variables.

e. Why this mitigates the issue
> Parameterized queries separate user input from the SQL command, ensuring that user data is treated as a parameter rather than executable SQL code. This prevents SQL injection attacks.

## Fix #3
a. File and line(s)
> frontend/app.js, line 14

b. Rule/category Semgrep flagged
> javascript.browser.security.insecure-document-method.insecure-document-method

c. Brief risk description
> User-controlled data was inserted into the DOM using innerHTML. If a malicious user provides HTML or JavaScript code as input, the browser may execute it, resulting in a cross-site scripting (XSS) vulnerability.

d. Your change (short code diff or explanation, AI coding tool usage)
> Before:

li.innerHTML = `<strong>${n.title}</strong>: ${n.content}`;

After:

const strong = document.createElement('strong');
    strong.textContent = n.title;
    li.appendChild(strong);
    li.appendChild(document.createTextNode(': ' + n.content));

Warp AI suggested replacing innerHTML with safe DOM element creation and textContent.

e. Why this mitigates the issue
> Using textContent and safe DOM manipulation ensures that user input is treated as plain text rather than executable HTML. This prevents the browser from executing injected scripts.