# Ajay Rathnavel Karunan – Portfolio (Flask, multi-page)

Routes: `/`, `/about`, `/skills`, `/education`, `/projects`, `/experience`, `/achievements`, `/contact` (GET page, POST form). Shared layout: `templates/base.html`.

## Install & run
```
cd ajay-portfolio
python -m venv venv
venv\Scripts\activate          # Windows   (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
python app.py                  # open http://127.0.0.1:5000
```
## Resume & photo
- Resume: replace `static/documents/resume.pdf` (keep the filename).
- Photo (optional): add `static/images/profile.png`. If absent, a typographic "AR" monogram is shown automatically.

## Contact form email (optional)
Without SMTP settings, valid messages are saved to `messages.jsonl` (not emailed). To email them, set env vars:
`SMTP_HOST=smtp.gmail.com  SMTP_PORT=587  SMTP_USER=you@gmail.com  SMTP_PASSWORD=<Gmail App Password>  CONTACT_TO=ajayrathnavelkarunan08@gmail.com`
(Gmail needs 2-Step Verification + an App Password.)

## Test checklist
Nav links scroll smoothly · mobile menu opens (narrow window) · "Download Resume" downloads the PDF · all project/social links open · submit empty form (errors show) · submit valid form (success + `messages.jsonl`) · visit `/xyz` for the 404 page.

## Deploy on Render
1. Push the folder to a GitHub repo.
2. Render → New → Web Service → connect the repo.
3. Build command: `pip install -r requirements.txt` · Start command: `gunicorn app:app`
4. Add the SMTP env vars above under Environment. Note: Render's free disk is ephemeral, so `messages.jsonl` won't persist – use SMTP in production.
