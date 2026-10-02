from flask import Flask, render_template, request, redirect, url_for, flash
from database import init_db, add_complaint, get_complaints, update_status, get_stats

app = Flask(__name__)
app.secret_key = "autoreSolve-demo-secret"

init_db()

def classify_problem(description):
    text = description.lower()
    rules = {
        "Plumbing": ["water", "leak", "pipe", "tap", "toilet", "drain"],
        "Electrical": ["electric", "light", "fan", "switch", "power", "socket", "wire"],
        "IT Support": ["wifi", "wi-fi", "internet", "network", "computer", "printer", "login"],
        "Cleaning": ["dirty", "clean", "garbage", "waste", "dust", "washroom"],
        "Maintenance": ["chair", "desk", "door", "window", "broken", "repair", "furniture"],
    }
    for category, keywords in rules.items():
        if any(word in text for word in keywords):
            return category
    return "General Maintenance"

def calculate_priority(description):
    text = description.lower()
    critical = ["fire", "gas leak", "smoke", "shock", "danger", "flood"]
    high = ["heavy leak", "major", "urgent", "not working", "broken"]
    if any(word in text for word in critical):
        return "Critical"
    if any(word in text for word in high):
        return "High"
    if len(text) > 80:
        return "Medium"
    return "Low"

def team_for(category):
    return {
        "Plumbing": "Plumbing Team",
        "Electrical": "Electrical Team",
        "IT Support": "IT Support Team",
        "Cleaning": "Housekeeping Team",
        "Maintenance": "Maintenance Team",
        "General Maintenance": "Facilities Team",
    }.get(category, "Facilities Team")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        location = request.form.get("location", "").strip()
        description = request.form.get("description", "").strip()

        if not name or not location or not description:
            flash("Please complete all fields.", "error")
            return redirect(url_for("index"))

        category = classify_problem(description)
        priority = calculate_priority(description)
        team = team_for(category)
        status = "Escalated" if priority == "Critical" else "Pending"

        complaint_id = add_complaint(
            name, location, description, category, priority, team, status
        )
        return redirect(url_for("result", complaint_id=complaint_id))

    return render_template("index.html")

@app.route("/result/<int:complaint_id>")
def result(complaint_id):
    complaints = [c for c in get_complaints() if c["id"] == complaint_id]
    if not complaints:
        return "Complaint not found", 404
    return render_template("result.html", complaint=complaints[0])

@app.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        complaints=get_complaints(),
        stats=get_stats()
    )

@app.route("/status/<int:complaint_id>/<status>")
def change_status(complaint_id, status):
    allowed = {"Pending", "In Progress", "Resolved", "Escalated"}
    if status in allowed:
        update_status(complaint_id, status)
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)
