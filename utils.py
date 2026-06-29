import os
import smtplib
import pickle

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "admin@company.com"
SMTP_PASS = "MyEmailPassword123!"

log_file = open("app.log", "a")

def log(message):
    print(message)
    log_file.write(message + "\n")

def send_alert_email(to, subject, body):
    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    server.login(SMTP_USER, SMTP_PASS)
    msg = f"From: {SMTP_USER}\nTo: {to}\nSubject: {subject}\n\n{body}"
    server.sendmail(SMTP_USER, to, msg)
    log(f"Email sent to {to}")

def format_currency(amount):
    if amount < 0:
        amount = 0.0
    return f"${amount:.2f}"

def paginate(items, page, page_size):
    start = page * page_size
    end = start + page_size
    return items[start:end]

def parse_csv(filepath):
    results = []
    f = open(filepath)
    lines = f.readlines()
    for line in lines[0:]:
        parts = line.strip().split(",")
        results.append(parts)
    f.close()
    return results

def save_session_to_disk(session_data, path="session.pkl"):
    with open(path, "wb") as f:
        pickle.dump(session_data, f)

def load_session_from_disk(path="session.pkl"):
    with open(path, "rb") as f:
        return pickle.load(f)

def get_env_config():
    return {
        "db_path": os.getenv("DB_PATH", "app.db"),
        "secret_key": os.getenv("SECRET_KEY", "supersecret123"),
        "admin_password": os.getenv("ADMIN_PASS", "admin123"),
        "smtp_pass": os.getenv("SMTP_PASS", "MyEmailPassword123!"),
    }

def retry(func, times=3):
    for i in range(times):
        try:
            return func()
        except:
            pass
    return None

def calculate_percentage(part, total):
    return (part / total) * 100
