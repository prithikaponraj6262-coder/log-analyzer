from flask import Flask, render_template, request
from collections import defaultdict
import os

app = Flask(__name__)

def analyze_logs(file):
    failed_attempts = defaultdict(int)

    for line in file:
        if "FAILED LOGIN" in line:
            ip = line.split("from ")[1].strip()
            failed_attempts[ip] += 1

    results = []
    for ip, count in failed_attempts.items():
        if count >= 3:
            results.append(f"🚨 ALERT: Brute force attack from {ip} ({count} attempts)")
        else:
            results.append(f"⚠ Warning: Failed attempts from {ip} ({count} attempts)")

    return results


@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    if request.method == "POST":
        file = request.files["logfile"]
        lines = file.read().decode("utf-8").split("\n")
        results = analyze_logs(lines)

    return render_template("index.html", results=results)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)