import os, re, json, smtplib, datetime
from email.message import EmailMessage
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
BASE = os.path.dirname(os.path.abspath(__file__))
EMAIL = "ajayrathnavelkarunan08@gmail.com"

PROFILE = {
    "name": "Ajay Rathnavel Karunan", "email": EMAIL, "phone": "+91 7448703397",
    "location": "Coimbatore, Tamil Nadu, India",
    "github": "https://github.com/ajayrathnavelkarunan",
    "linkedin": "https://www.linkedin.com/in/ajay-rathnavel-karunan-804097364",
}
SKILLS = [
    ("Frontend", ["HTML", "CSS", "Bootstrap", "JavaScript", "React.js"]),
    ("Backend", ["Python", "Node.js"]),
    ("Database", ["SQLite"]),
    ("Computer Science", ["Computer Networks", "Data Structures and Algorithms"]),
    ("Data Analytics", ["Power BI", "Tableau", "Data Cleaning", "Data Visualization"]),
    ("Other", ["Data Science", "Generative AI"]),
]
PROJECTS = [
    {"title": "TN CivicIntel", "sub": "AI-Powered Grievance Platform",
     "desc": "An AI-powered grievance platform for Ariyalur District that lets citizens generate professional complaints for 10+ departments, including water and electricity.",
     "points": ["AI-assisted complaint drafting", "Structured complaint generation", "Citizen-friendly interface", "Responsive website"],
     "tech": ["HTML", "CSS", "Bootstrap", "AI Drafting Logic"],
     "url": "https://tn-civicintel-greivance-system.streamlit.app/", "cta": "Live Project"},
    {"title": "Heart Disease Risk Prediction", "sub": "Data Science Notebook",
     "desc": "A Python-based data science project exploring demographic, physiological and behavioural factors associated with cardiovascular disease.",
     "points": [], "tech": ["Python"],
     "url": "https://colab.research.google.com/drive/1MwlHzlwBlbtnIpMokt-r_u5TywsABC-L?usp=sharing", "cta": "Open Notebook"},
    {"title": "Personal Portfolio Website", "sub": "Responsive Website",
     "desc": "A responsive portfolio website built with HTML, CSS and Bootstrap to showcase professional information, skills and projects.",
     "points": [], "tech": ["HTML", "CSS", "Bootstrap"],
     "url": "https://ajaiiportfolio.ccbp.tech/", "cta": "View Portfolio"},
]

PAGES = ["about", "skills", "education", "projects", "experience", "achievements"]

def ctx():
    has_photo = os.path.exists(os.path.join(BASE, "static", "images", "profile.png"))
    return dict(p=PROFILE, skills=SKILLS, projects=PROJECTS, has_photo=has_photo)

@app.route("/")
def index():
    return render_template("index.html", **ctx())

def _page(name):
    return lambda: render_template(f"{name}.html", **ctx())

for _n in PAGES:  # /about, /skills, /education, /projects, /experience, /achievements
    app.add_url_rule(f"/{_n}", _n, _page(_n))

def validate(f):
    errors = {}
    name, email, msg = f.get("name", "").strip(), f.get("email", "").strip(), f.get("message", "").strip()
    if not 2 <= len(name) <= 80: errors["name"] = "Please enter your name (2-80 characters)."
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]{2,}", email) or len(email) > 120: errors["email"] = "Please enter a valid email address."
    if not 10 <= len(msg) <= 1500: errors["message"] = "Message must be 10-1500 characters."
    return errors, name, email, msg

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html", **ctx())
    if request.form.get("website"):  # honeypot field: bots fill it, humans don't see it
        return jsonify(ok=True, message="Thanks!")
    errors, name, email, msg = validate(request.form)
    if errors:
        return jsonify(ok=False, errors=errors), 400
    host, user, pwd = os.getenv("SMTP_HOST"), os.getenv("SMTP_USER"), os.getenv("SMTP_PASSWORD")
    if host and user and pwd:
        try:
            m = EmailMessage()
            m["Subject"], m["From"], m["To"], m["Reply-To"] = f"Portfolio message from {name}", user, os.getenv("CONTACT_TO", EMAIL), email
            m.set_content(f"Name: {name}\nEmail: {email}\n\n{msg}")
            with smtplib.SMTP(host, int(os.getenv("SMTP_PORT", 587)), timeout=15) as s:
                s.starttls(); s.login(user, pwd); s.send_message(m)
            return jsonify(ok=True, message="Message sent. I'll get back to you soon!")
        except Exception as e:
            app.logger.error("SMTP failed: %s", e)
            return jsonify(ok=False, errors={"form": "Could not send email right now. Please email me directly."}), 502
    # No SMTP configured: store the message locally instead of pretending it was emailed.
    with open(os.path.join(BASE, "messages.jsonl"), "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"t": datetime.datetime.utcnow().isoformat(), "name": name, "email": email, "message": msg}) + "\n")
    return jsonify(ok=True, message="Message received and saved. Thank you!")

@app.errorhandler(404)
def not_found(_):
    return render_template("404.html", p=PROFILE), 404

if __name__ == "__main__":
    app.run(debug=True)
