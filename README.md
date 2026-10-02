# AutoResolve – Smart Complaint Classification & Escalation System

AutoResolve is a Flask-based prototype for handling facility complaints. A user submits a problem, and the application classifies it, calculates a priority, assigns a responsible team, and escalates critical issues.

## Problem
Facility complaints in colleges, hostels, offices, and apartments can be difficult to classify, route, prioritize, and track manually.

## Solution
AutoResolve provides a simple workflow:

**Report → Classify → Prioritize → Assign → Escalate → Track**

## Features
- Complaint submission
- Rule-based category detection
- Priority calculation
- Automatic team assignment
- Critical-issue escalation
- SQLite persistence
- Admin dashboard
- Status updates
- Automated tests

## Technology
- Python
- Flask
- SQLite
- HTML/CSS
- Pytest

## Run locally

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

## Example
Complaint:

> Water is leaking heavily from the bathroom pipe.

Expected processing:

- Category: Plumbing
- Priority: High
- Team: Plumbing Team
- Status: Pending

A critical complaint containing terms such as fire, gas leak, smoke, shock, danger, or flood is automatically marked as Escalated.

## Testing

```bash
pytest
```

