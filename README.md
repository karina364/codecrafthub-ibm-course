# CodeCraftHub REST API (Flask)

CodeCraftHub is a beginner-friendly REST API project built with **Python Flask**. It helps you learn how CRUD APIs work by managing a list of courses.

The API stores data in a local JSON file (`courses.json`) instead of a database, so you can focus on the core API concepts first.

## 1) Project Overview

This project is a simple course management API with full CRUD operations:

- **Create** a new course
- **Read** all courses or one course by ID
- **Update** a course by ID
- **Delete** a course by ID

Each course includes:

- `id` (auto-generated)
- `name`
- `description`
- `target_date` (format: `YYYY-MM-DD`)
- `status` (`Not Started`, `In Progress`, `Completed`)
- `created_at` (auto-generated timestamp)

## 2) Features

- Built with Flask and REST-style endpoints
- JSON file storage (`courses.json`)
- Auto-creation of `courses.json` if missing
- Auto-generated incremental IDs (starting at 1)
- Input validation for required fields
- Validation for status values
- Validation for date format (`YYYY-MM-DD`)
- Consistent JSON error responses
- Beginner-friendly code comments in `app.py`

## 3) Installation (Step-by-Step)

### Prerequisites

- Python 3.10+ installed
- `pip` installed
- A terminal (PowerShell on Windows is fine)

### Step 1: Open the project folder

```powershell
cd c:\Users\DELL\code\repos\codecrafthub
```

### Step 2: (Recommended) Create a virtual environment

```powershell
python -m venv .venv
```

### Step 3: Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run this once in PowerShell as administrator:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activation again.

### Step 4: Install Flask

```powershell
pip install flask
```

### Step 5: Verify installation

```powershell
python -c "import flask; print(flask.__version__)"
```

## 4) How to Run the Application

From the project folder:

```powershell
python app.py
```

You should see Flask start on:

- `http://127.0.0.1:5000`

The app will automatically create `courses.json` if it does not already exist.

## 5) API Endpoints Documentation (with Examples)

Base URL:

- `http://127.0.0.1:5000`

### Course Object Example

```json
{
  "id": 1,
  "name": "Python Basics",
  "description": "Learn variables, loops, and functions",
  "target_date": "2026-06-15",
  "status": "Not Started",
  "created_at": "2026-05-30T10:30:00.000000Z"
}
```

### 5.1 Create Course

- **Method:** `POST`
- **Endpoint:** `/api/courses`
- **Body:** JSON required

Example:

```powershell
curl.exe -i -X POST "http://127.0.0.1:5000/api/courses" -H "Content-Type: application/json" -d "{\"name\":\"Python Basics\",\"description\":\"Learn variables, loops, and functions\",\"target_date\":\"2026-06-15\",\"status\":\"Not Started\"}"
```

Expected success:

- Status: `201 Created`
- Returns the created course JSON

### 5.2 Get All Courses

- **Method:** `GET`
- **Endpoint:** `/api/courses`

Example:

```powershell
curl.exe -i -X GET "http://127.0.0.1:5000/api/courses"
```

Expected success:

- Status: `200 OK`
- Returns JSON array of courses

### 5.3 Get One Course by ID

- **Method:** `GET`
- **Endpoint:** `/api/courses/<id>`

Example:

```powershell
curl.exe -i -X GET "http://127.0.0.1:5000/api/courses/1"
```

Expected success:

- Status: `200 OK`
- Returns one course object

### 5.4 Update Course

- **Method:** `PUT`
- **Endpoint:** `/api/courses/<id>`
- **Body:** Full JSON required

Example:

```powershell
curl.exe -i -X PUT "http://127.0.0.1:5000/api/courses/1" -H "Content-Type: application/json" -d "{\"name\":\"Python Basics - Updated\",\"description\":\"Learn Python with mini projects\",\"target_date\":\"2026-07-01\",\"status\":\"In Progress\"}"
```

Expected success:

- Status: `200 OK`
- Returns updated course object

### 5.5 Delete Course

- **Method:** `DELETE`
- **Endpoint:** `/api/courses/<id>`

Example:

```powershell
curl.exe -i -X DELETE "http://127.0.0.1:5000/api/courses/1"
```

Expected success:

- Status: `200 OK`
- Response:

```json
{
  "message": "Course deleted successfully."
}
```

## 6) Testing Instructions

This section gives a simple manual test flow for beginners.

### Recommended test order

1. Create a course (`POST`)
2. Get all courses (`GET /api/courses`)
3. Get one course (`GET /api/courses/1`)
4. Update course (`PUT /api/courses/1`)
5. Delete course (`DELETE /api/courses/1`)
6. Test error cases

### Error test cases

#### A) Missing required fields

```powershell
curl.exe -i -X POST "http://127.0.0.1:5000/api/courses" -H "Content-Type: application/json" -d "{\"name\":\"Only Name\"}"
```

Expected:

- Status: `400 Bad Request`
- Example error:

```json
{
  "error": "Missing required fields: description, target_date, status"
}
```

#### B) Invalid status

```powershell
curl.exe -i -X POST "http://127.0.0.1:5000/api/courses" -H "Content-Type: application/json" -d "{\"name\":\"Status Test\",\"description\":\"Invalid status\",\"target_date\":\"2026-06-20\",\"status\":\"Done\"}"
```

Expected:

- Status: `400 Bad Request`
- Example error:

```json
{
  "error": "Invalid status value. Must be one of: Not Started, In Progress, Completed"
}
```

#### C) Invalid date format

```powershell
curl.exe -i -X POST "http://127.0.0.1:5000/api/courses" -H "Content-Type: application/json" -d "{\"name\":\"Date Test\",\"description\":\"Wrong date format\",\"target_date\":\"20-06-2026\",\"status\":\"Not Started\"}"
```

Expected:

- Status: `400 Bad Request`
- Example error:

```json
{
  "error": "Invalid target_date. Use YYYY-MM-DD format."
}
```

#### D) Course not found

```powershell
curl.exe -i -X GET "http://127.0.0.1:5000/api/courses/999"
```

Expected:

- Status: `404 Not Found`
- Example error:

```json
{
  "error": "Course not found."
}
```

## 7) Troubleshooting Common Issues

### Issue: `ModuleNotFoundError: No module named 'flask'`

Cause: Flask is not installed in your current environment.

Fix:

```powershell
pip install flask
```

If using virtual environment, make sure it is activated first.

### Issue: Port already in use (`Address already in use`)

Cause: Another app is already using port `5000`.

Fix options:

- Stop the app using port `5000`
- Or run Flask on another port by editing `app.run(debug=True)` to:

```python
app.run(debug=True, port=5001)
```

### Issue: `courses.json` has invalid JSON

Cause: File was manually edited and broken.

Fix:

1. Open `courses.json`
2. Replace contents with:

```json
[]
```

3. Save and rerun the app

### Issue: PowerShell blocks virtual environment activation

Fix:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

## 8) Project Structure Explanation

```text
codecrafthub/
├── app.py
├── courses.json   (created automatically after first run)
└── README.md
```

- `app.py`
  - Main Flask application
  - Defines all API routes and validation
  - Handles reading/writing course data

- `courses.json`
  - Local data store for courses
  - Auto-created if missing

- `README.md`
  - Beginner guide for setup, usage, and testing

## Next Learning Steps

Once you understand this project, try these upgrades:

- Add pagination for `GET /api/courses`
- Add search/filter by status
- Add automated tests with `pytest`
- Replace JSON file storage with SQLite or PostgreSQL
- Build a frontend to consume this API
