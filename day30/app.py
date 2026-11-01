
from collections import Counter
from datetime import datetime
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import re

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2 MB limit

LOG_PATTERN = re.compile(
    r'(?P<ip>\S+)\s+\S+\s+\S+\s+'
    r'\[(?P<time>[^\]]+)\]\s+'
    r'"(?P<method>[A-Z]+)\s+(?P<endpoint>\S+)(?:\s+[^"]*)?"\s+'
    r'(?P<status>\d{3})\s+(?P<size>\S+)'
)

SAMPLE_LOG = """192.168.1.10 - - [19/Oct/2026:10:00:00 +0530] "GET / HTTP/1.1" 200 1200
192.168.1.11 - - [19/Oct/2026:10:01:00 +0530] "GET /products HTTP/1.1" 200 2400
192.168.1.10 - - [19/Oct/2026:10:02:00 +0530] "POST /login HTTP/1.1" 401 500
192.168.1.12 - - [19/Oct/2026:10:03:00 +0530] "GET /products HTTP/1.1" 200 2400
192.168.1.10 - - [19/Oct/2026:10:04:00 +0530] "GET /missing HTTP/1.1" 404 300
192.168.1.11 - - [19/Oct/2026:10:05:00 +0530] "GET / HTTP/1.1" 200 1200
192.168.1.13 - - [19/Oct/2026:10:06:00 +0530] "GET /admin HTTP/1.1" 500 100
192.168.1.10 - - [19/Oct/2026:10:07:00 +0530] "GET /products HTTP/1.1" 200 2400
"""


def analyze_log(text):
    """Parse log entries and calculate request statistics."""
    ip_counts = Counter()
    endpoint_counts = Counter()
    status_counts = Counter()
    method_counts = Counter()

    total_requests = 0
    error_count = 0
    malformed_count = 0
    parsed_entries = []

    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        match = LOG_PATTERN.match(line)

        if not match:
            malformed_count += 1
            continue

        entry = match.groupdict()

        ip = entry["ip"]
        endpoint = entry["endpoint"]
        method = entry["method"]
        status = int(entry["status"])

        total_requests += 1
        ip_counts[ip] += 1
        endpoint_counts[endpoint] += 1
        status_counts[str(status)] += 1
        method_counts[method] += 1

        if status >= 400:
            error_count += 1

        parsed_entries.append({
            "ip": ip,
            "endpoint": endpoint,
            "method": method,
            "status": status,
            "time": entry["time"]
        })

    return {
        "total_requests": total_requests,
        "error_count": error_count,
        "success_count": sum(
            count for code, count in status_counts.items()
            if 200 <= int(code) < 400
        ),
        "malformed_count": malformed_count,
        "top_ips": ip_counts.most_common(5),
        "top_endpoints": endpoint_counts.most_common(5),
        "status_counts": sorted(
            status_counts.items(),
            key=lambda item: int(item[0])
        ),
        "method_counts": method_counts.most_common(),
        "entries": parsed_entries[:100]
    }


@app.route("/", methods=["GET", "POST"])
def index():
    report = None
    error = None
    filename = None

    if request.method == "POST":
        uploaded_file = request.files.get("logfile")
        action = request.form.get("action", "upload")

        if action == "sample":
            report = analyze_log(SAMPLE_LOG)
            filename = "sample_access.log"

        elif not uploaded_file or not uploaded_file.filename:
            error = "Please choose a log file to upload."

        elif not uploaded_file.filename.lower().endswith(
            (".log", ".txt")
        ):
            error = "Please upload a .log or .txt file."

        else:
            filename = secure_filename(uploaded_file.filename)

            try:
                content = uploaded_file.read()
                text = content.decode("utf-8", errors="replace")
                report = analyze_log(text)

                if report["total_requests"] == 0:
                    error = (
                        "No valid access-log entries were found. "
                        "Check that the file uses the supported format."
                    )
                    report = None

            except Exception:
                error = "The file could not be processed."

    return render_template(
        "index.html",
        report=report,
        error=error,
        filename=filename
    )


@app.errorhandler(413)
def file_too_large(error):
    return render_template(
        "index.html",
        report=None,
        error="File is too large. Maximum upload size is 2 MB.",
        filename=None
    ), 413


if __name__ == "__main__":
    app.run(debug=True)
