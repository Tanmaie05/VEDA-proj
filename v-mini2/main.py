
import os
from functools import wraps

from flask import (
    Flask,
    request,
    redirect,
    url_for,
    render_template_string,
    flash,
    session,
)
from werkzeug.security import generate_password_hash, check_password_hash

from data import services, programs, inquiries, service_requests
from storage import initialize_storage, save_data


app = Flask(__name__)

# Set VEDA_SECRET_KEY as an environment variable before deployment.
app.secret_key = os.environ.get(
    "VEDA_SECRET_KEY",
    "change-this-development-secret-before-deployment",
)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("HTTPS_ENABLED") == "1",
    PERMANENT_SESSION_LIFETIME=1800,
)

# Demo login defaults. Configure these environment variables for your own account.
ADMIN_USERNAME = os.environ.get("VEDA_ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("VEDA_ADMIN_PASSWORD", "Veda@123")
ADMIN_PASSWORD_HASH = generate_password_hash(ADMIN_PASSWORD)


COLLECTIONS = {
    "services": {
        "title": "Services",
        "singular": "Service",
        "fields": ["name", "category", "price"],
        "labels": ["Service Name", "Category", "Price (₹)"],
        "statuses": ["Active", "Inactive"],
    },
    "programs": {
        "title": "Programs",
        "singular": "Program",
        "fields": ["name", "duration", "category"],
        "labels": ["Program Name", "Duration", "Category"],
        "statuses": ["Open", "Closed"],
    },
    "inquiries": {
        "title": "Customer Inquiries",
        "singular": "Inquiry",
        "fields": ["customer", "subject", "message"],
        "labels": ["Customer Name", "Subject", "Message"],
        "statuses": ["New", "In Progress", "Resolved"],
    },
    "service_requests": {
        "title": "Service Requests",
        "singular": "Service Request",
        "fields": ["customer", "service", "description"],
        "labels": ["Customer Name", "Service", "Description"],
        "statuses": ["Open", "In Progress", "Resolved", "Closed"],
    },
}


# ---------------------------------------------------------
# Login page
# ---------------------------------------------------------

LOGIN_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign In | Veda Technology</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap"
          rel="stylesheet">

    <style>
        :root {
            --blue: #2563eb;
            --blue-dark: #1d4ed8;
            --ink: #172033;
            --muted: #7b879b;
            --border: #e5eaf2;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            min-height: 100vh;
            font-family: "DM Sans", Arial, sans-serif;
            color: var(--ink);
            background: #f5f7fb;
            display: grid;
            place-items: center;
            padding: 24px;
        }

        .login-layout {
            width: 100%;
            max-width: 1000px;
            min-height: 590px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            overflow: hidden;
            background: white;
            border: 1px solid var(--border);
            border-radius: 22px;
            box-shadow: 0 25px 80px rgba(30, 55, 100, 0.10);
        }

        .brand-panel {
            position: relative;
            overflow: hidden;
            padding: 45px;
            background: linear-gradient(145deg, #1d4ed8, #2563eb 55%, #60a5fa);
            color: white;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .brand-panel::before,
        .brand-panel::after {
            content: "";
            position: absolute;
            border: 1px solid rgba(255,255,255,.16);
            border-radius: 50%;
            pointer-events: none;
        }

        .brand-panel::before {
            width: 370px;
            height: 370px;
            right: -160px;
            top: 90px;
        }

        .brand-panel::after {
            width: 270px;
            height: 270px;
            right: -110px;
            top: 140px;
        }

        .brand,
        .brand-message,
        .brand-footer {
            position: relative;
            z-index: 1;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .brand-logo {
            display: grid;
            place-items: center;
            width: 46px;
            height: 46px;
            border-radius: 13px;
            color: #1d4ed8;
            background: white;
            font: 800 22px "Manrope", sans-serif;
        }

        .brand-name {
            font: 800 17px "Manrope", sans-serif;
        }

        .brand-subtitle {
            font-size: 10px;
            letter-spacing: 1.4px;
            text-transform: uppercase;
            opacity: .78;
            margin-top: 3px;
        }

        .brand-message {
            max-width: 365px;
            padding: 30px 0;
        }

        .eyebrow {
            display: inline-block;
            padding: 7px 11px;
            border: 1px solid rgba(255,255,255,.25);
            border-radius: 30px;
            background: rgba(255,255,255,.10);
            font-size: 10px;
            letter-spacing: 1.3px;
            text-transform: uppercase;
            font-weight: 700;
        }

        .brand-message h1 {
            margin-top: 24px;
            font: 800 clamp(28px, 4vw, 40px)/1.2 "Manrope", sans-serif;
            letter-spacing: -1.4px;
        }

        .brand-message p {
            margin-top: 16px;
            color: rgba(255,255,255,.83);
            font-size: 13px;
            line-height: 1.9;
        }

        .feature-list {
            margin-top: 28px;
            display: grid;
            gap: 14px;
        }

        .feature {
            display: flex;
            gap: 10px;
            align-items: center;
            font-size: 12px;
            color: rgba(255,255,255,.93);
        }

        .check {
            display: grid;
            place-items: center;
            width: 22px;
            height: 22px;
            border-radius: 50%;
            background: rgba(255,255,255,.17);
            font-size: 12px;
        }

        .brand-footer {
            font-size: 10px;
            color: rgba(255,255,255,.68);
        }

        .form-panel {
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 48px clamp(25px, 5vw, 58px);
        }

        .form-eyebrow {
            color: var(--blue);
            text-transform: uppercase;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 1.6px;
        }

        .form-panel h2 {
            margin-top: 10px;
            font: 800 29px "Manrope", sans-serif;
            letter-spacing: -1px;
        }

        .form-intro {
            color: var(--muted);
            font-size: 12px;
            line-height: 1.8;
            margin-top: 8px;
            margin-bottom: 29px;
        }

        .flash {
            margin-bottom: 17px;
            padding: 11px 13px;
            border-radius: 8px;
            font-size: 12px;
            color: #b91c1c;
            background: #fef2f2;
            border: 1px solid #fecaca;
        }

        .flash.success {
            color: #166534;
            background: #f0fdf4;
            border-color: #bbf7d0;
        }

        .field {
            margin-bottom: 18px;
        }

        .field label {
            display: block;
            margin-bottom: 8px;
            font-size: 11px;
            font-weight: 700;
            color: #455168;
        }

        .field input {
            width: 100%;
            padding: 13px 14px;
            border: 1px solid #dfe5ef;
            border-radius: 9px;
            outline: none;
            background: #fff;
            color: var(--ink);
            font-size: 12px;
            transition: .2s;
        }

        .field input:focus {
            border-color: #60a5fa;
            box-shadow: 0 0 0 3px rgba(37,99,235,.09);
        }

        .password-wrap {
            position: relative;
        }

        .password-wrap input {
            padding-right: 65px;
        }

        .show-password {
            position: absolute;
            top: 50%;
            right: 12px;
            transform: translateY(-50%);
            border: 0;
            background: none;
            color: var(--blue);
            font-size: 11px;
            font-weight: 700;
            cursor: pointer;
        }

        .submit-btn {
            width: 100%;
            margin-top: 6px;
            padding: 13px;
            border: 0;
            border-radius: 9px;
            background: var(--blue);
            color: white;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            transition: .2s;
        }

        .submit-btn:hover {
            background: var(--blue-dark);
            transform: translateY(-1px);
        }

        .security-note {
            display: flex;
            gap: 9px;
            align-items: flex-start;
            margin-top: 23px;
            padding: 13px;
            border: 1px solid var(--border);
            border-radius: 9px;
            background: #fafcff;
            color: var(--muted);
            font-size: 10px;
            line-height: 1.7;
        }

        .security-note strong {
            color: #455168;
        }

        .copyright {
            margin-top: 30px;
            color: #a0a8b7;
            text-align: center;
            font-size: 10px;
        }

        @media (max-width: 700px) {
            .login-layout {
                max-width: 430px;
                min-height: auto;
                grid-template-columns: 1fr;
            }

            .brand-panel {
                padding: 25px;
            }

            .brand-message {
                padding: 28px 0 10px;
            }

            .brand-message h1 {
                font-size: 28px;
                margin-top: 15px;
            }

            .brand-message p {
                margin-top: 10px;
            }

            .feature-list {
                display: none;
            }

            .brand-footer {
                margin-top: 15px;
            }

            .form-panel {
                padding: 32px 25px;
            }

            .form-panel h2 {
                font-size: 25px;
            }
        }
    </style>
</head>

<body>
    <main class="login-layout">
        <section class="brand-panel">
            <a class="brand" href="{{ url_for('login') }}">
                <div class="brand-logo">V</div>
                <div>
                    <div class="brand-name">Veda Technology</div>
                    <div class="brand-subtitle">Business Suite</div>
                </div>
            </a>

            <div class="brand-message">
                <span class="eyebrow">Business Management Platform</span>
                <h1>Everything your business needs, in one place.</h1>
                <p>
                    A centralized workspace for managing services,
                    programs, customer inquiries and service requests.
                </p>

                <div class="feature-list">
                    <div class="feature">
                        <span class="check">✓</span>
                        Organized business records
                    </div>
                    <div class="feature">
                        <span class="check">✓</span>
                        Simple status management
                    </div>
                    <div class="feature">
                        <span class="check">✓</span>
                        Secure, authenticated access
                    </div>
                </div>
            </div>

            <div class="brand-footer">
                © <span id="login-year"></span> Veda Technology
            </div>
        </section>

        <section class="form-panel">
            <div class="form-eyebrow">Welcome back</div>
            <h2>Sign in to your account</h2>
            <p class="form-intro">
                Enter your administrator credentials to access your dashboard.
            </p>

            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="flash {% if category == 'success' %}success{% endif %}">
                            {{ message }}
                        </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}

            <form method="POST" action="{{ url_for('login') }}">
                <div class="field">
                    <label for="username">Username</label>
                    <input
                        id="username"
                        name="username"
                        type="text"
                        placeholder="Enter your username"
                        autocomplete="username"
                        required
                        autofocus>
                </div>

                <div class="field">
                    <label for="password">Password</label>
                    <div class="password-wrap">
                        <input
                            id="password"
                            name="password"
                            type="password"
                            placeholder="Enter your password"
                            autocomplete="current-password"
                            required>
                        <button
                            type="button"
                            class="show-password"
                            onclick="togglePassword()">
                            Show
                        </button>
                    </div>
                </div>

                <button class="submit-btn" type="submit">
                    Sign In &nbsp; →
                </button>
            </form>

            <div class="security-note">
                <span>🔒</span>
                <div>
                    <strong>Protected workspace</strong><br>
                    Your dashboard requires an authenticated session.
                    Sign out when you finish.
                </div>
            </div>

            <div class="copyright">
                Veda Technology · Business &amp; Service Management System
            </div>
        </section>
    </main>

    <script>
        document.getElementById("login-year").textContent =
            new Date().getFullYear();

        function togglePassword() {
            const input = document.getElementById("password");
            const button = document.querySelector(".show-password");
            const hidden = input.type === "password";

            input.type = hidden ? "text" : "password";
            button.textContent = hidden ? "Hide" : "Show";
        }
    </script>
</body>
</html>
"""


# ---------------------------------------------------------
# Dashboard template
# ---------------------------------------------------------

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Veda Technology | Business Management</title>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap"
          rel="stylesheet">

    <style>
        :root {
            --primary: #2563eb;
            --primary-dark: #1d4ed8;
            --primary-light: #eff6ff;
            --background: #f5f7fb;
            --surface: #ffffff;
            --text: #172033;
            --muted: #788399;
            --border: #e7ebf2;
            --success: #15803d;
            --danger: #dc2626;
            --shadow: 0 5px 22px rgba(23, 32, 51, .035);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        html {
            scroll-behavior: smooth;
            scroll-padding-top: 95px;
        }

        body {
            font-family: "DM Sans", Arial, sans-serif;
            background: var(--background);
            color: var(--text);
            font-size: 14px;
            line-height: 1.6;
        }

        button, input, select, textarea {
            font: inherit;
        }

        a {
            color: inherit;
            text-decoration: none;
        }

        .sidebar {
            position: fixed;
            inset: 0 auto 0 0;
            width: 252px;
            background: white;
            border-right: 1px solid var(--border);
            padding: 27px 17px;
            display: flex;
            flex-direction: column;
            z-index: 100;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 0 10px 27px;
            border-bottom: 1px solid var(--border);
        }

        .brand-logo {
            height: 43px;
            width: 43px;
            border-radius: 13px;
            background: linear-gradient(145deg, #3b82f6, #1d4ed8);
            display: grid;
            place-items: center;
            color: white;
            font: 800 20px "Manrope", sans-serif;
            box-shadow: 0 5px 13px rgba(37,99,235,.23);
        }

        .brand-name {
            font: 800 16px "Manrope", sans-serif;
            letter-spacing: -.5px;
        }

        .brand-caption {
            font-size: 10px;
            color: var(--muted);
            letter-spacing: 1.15px;
            text-transform: uppercase;
            font-weight: 700;
        }

        .nav-label {
            padding: 25px 12px 10px;
            color: #9aa3b4;
            text-transform: uppercase;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 1.3px;
        }

        .nav-links {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        .nav-link {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 11px 13px;
            border-radius: 9px;
            color: #69758b;
            font-size: 13px;
            font-weight: 600;
            transition: .2s;
        }

        .nav-link:hover {
            background: #f5f8ff;
            color: var(--primary);
        }

        .nav-link.active {
            background: var(--primary-light);
            color: var(--primary);
            font-weight: 700;
        }

        .nav-icon {
            width: 23px;
            text-align: center;
            font-size: 17px;
        }

        .sidebar-bottom {
            margin-top: auto;
            padding: 17px 8px 0;
            border-top: 1px solid var(--border);
        }

        .admin-card {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .admin-avatar {
            width: 38px;
            height: 38px;
            border-radius: 50%;
            background: #dbeafe;
            color: #1d4ed8;
            display: grid;
            place-items: center;
            font-weight: 800;
        }

        .admin-name {
            font-size: 12px;
            font-weight: 700;
        }

        .admin-role {
            color: var(--muted);
            font-size: 11px;
        }

        .main-content {
            margin-left: 252px;
            min-height: 100vh;
        }

        .topbar {
            min-height: 75px;
            background: rgba(255,255,255,.97);
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 15px;
            padding: 12px 35px;
            position: sticky;
            top: 0;
            z-index: 50;
        }

        .breadcrumb {
            color: var(--muted);
            font-size: 12px;
        }

        .breadcrumb strong {
            color: var(--text);
        }

        .topbar-right {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .live-status {
            display: flex;
            align-items: center;
            gap: 7px;
            padding: 7px 11px;
            border: 1px solid var(--border);
            border-radius: 8px;
            color: #475569;
            font-size: 11px;
            font-weight: 600;
            background: white;
        }

        .live-dot {
            height: 7px;
            width: 7px;
            border-radius: 50%;
            background: #22c55e;
        }

        .logout-btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 7px;
            padding: 9px 12px;
            border: 1px solid #dbeafe;
            border-radius: 8px;
            color: var(--primary);
            background: #eff6ff;
            font-size: 11px;
            font-weight: 700;
            cursor: pointer;
        }

        .logout-btn:hover {
            background: #dbeafe;
        }

        .page-content {
            max-width: 1600px;
            margin: 0 auto;
            padding: 31px 35px 45px;
        }

        .welcome-row {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 20px;
            margin-bottom: 27px;
        }

        .eyebrow {
            color: var(--primary);
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            margin-bottom: 7px;
        }

        h1, h2, h3 {
            font-family: "Manrope", "DM Sans", Arial, sans-serif;
        }

        h1 {
            font-size: clamp(25px, 3vw, 32px);
            line-height: 1.25;
            font-weight: 800;
            letter-spacing: -1.2px;
        }

        .welcome-description {
            margin-top: 8px;
            color: var(--muted);
            font-size: 13px;
        }

        .date-chip {
            padding: 10px 13px;
            background: white;
            border: 1px solid var(--border);
            border-radius: 9px;
            font-size: 12px;
            font-weight: 600;
            color: #566177;
            white-space: nowrap;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0,1fr));
            gap: 17px;
            margin-bottom: 27px;
        }

        .stat-card {
            background: white;
            border: 1px solid var(--border);
            border-radius: 13px;
            padding: 21px;
            box-shadow: var(--shadow);
            min-width: 0;
        }

        .stat-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            margin-bottom: 19px;
        }

        .stat-label {
            color: #737f93;
            font-size: 12px;
            font-weight: 600;
        }

        .stat-icon {
            height: 39px;
            width: 39px;
            border-radius: 11px;
            display: grid;
            place-items: center;
            font-size: 18px;
        }

        .icon-blue { color: #2563eb; background: #eff6ff; }
        .icon-purple { color: #7c3aed; background: #f3e8ff; }
        .icon-orange { color: #c2410c; background: #fff7ed; }
        .icon-green { color: #15803d; background: #dcfce7; }

        .stat-value {
            font: 800 31px/1.2 "Manrope", sans-serif;
            letter-spacing: -1px;
        }

        .stat-footer {
            margin-top: 10px;
            color: var(--muted);
            font-size: 11px;
        }

        .stat-accent {
            color: var(--primary);
            font-weight: 700;
        }

        .overview-panel {
            background: white;
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 24px;
            margin-bottom: 29px;
            box-shadow: var(--shadow);
        }

        .section-heading {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 15px;
            margin-bottom: 20px;
        }

        .section-heading h2 {
            font-size: 17px;
            font-weight: 800;
        }

        .section-subtitle {
            color: var(--muted);
            font-size: 12px;
            margin-top: 4px;
        }

        .overview-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0,1fr));
            gap: 13px;
        }

        .overview-item {
            border: 1px solid var(--border);
            background: #fcfdff;
            border-radius: 10px;
            padding: 16px;
            transition: .2s;
        }

        .overview-item:hover {
            border-color: #bfdbfe;
            background: #f8fbff;
            transform: translateY(-2px);
        }

        .overview-item-icon {
            font-size: 19px;
            margin-bottom: 11px;
        }

        .overview-item h3 {
            font-size: 12px;
            font-weight: 800;
        }

        .overview-item p {
            color: var(--muted);
            font-size: 11px;
            margin-top: 4px;
        }

        .overview-arrow {
            display: inline-block;
            color: var(--primary);
            font-weight: 700;
            font-size: 11px;
            margin-top: 12px;
        }

        .collection-section {
            margin-top: 30px;
            scroll-margin-top: 95px;
        }

        .collection-heading {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            margin-bottom: 16px;
        }

        .collection-title-group {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .collection-icon {
            width: 43px;
            height: 43px;
            border-radius: 12px;
            display: grid;
            place-items: center;
            background: var(--primary-light);
            color: var(--primary);
            font-size: 19px;
        }

        .collection-heading h2 {
            font-size: 17px;
            font-weight: 800;
        }

        .collection-heading p {
            font-size: 11px;
            color: var(--muted);
            margin-top: 3px;
        }

        .record-count {
            padding: 6px 10px;
            border-radius: 7px;
            background: white;
            border: 1px solid var(--border);
            color: #667085;
            font-size: 11px;
            font-weight: 700;
            white-space: nowrap;
        }

        .collection-layout {
            display: grid;
            grid-template-columns: minmax(240px,.72fr) minmax(0,1.8fr);
            align-items: start;
            gap: 17px;
        }

        .panel {
            min-width: 0;
            background: white;
            border: 1px solid var(--border);
            border-radius: 12px;
            box-shadow: var(--shadow);
            overflow: hidden;
        }

        .panel-header {
            padding: 18px 19px;
            border-bottom: 1px solid var(--border);
        }

        .panel-header h3 {
            font-size: 13px;
            font-weight: 800;
        }

        .panel-header p {
            margin-top: 3px;
            color: var(--muted);
            font-size: 11px;
        }

        .form-body {
            padding: 19px;
        }

        .form-group {
            margin-bottom: 15px;
        }

        .form-group label {
            display: block;
            margin-bottom: 7px;
            font-size: 11px;
            font-weight: 700;
            color: #455168;
        }

        .form-control {
            width: 100%;
            min-width: 0;
            padding: 10px 11px;
            border: 1px solid #dfe5ef;
            border-radius: 8px;
            background: white;
            color: var(--text);
            outline: none;
            font-size: 12px;
        }

        .form-control:focus {
            border-color: #60a5fa;
            box-shadow: 0 0 0 3px rgba(37,99,235,.09);
        }

        .form-control::placeholder {
            color: #a2aabb;
        }

        textarea.form-control {
            resize: vertical;
            min-height: 84px;
        }

        .btn {
            display: inline-flex;
            justify-content: center;
            align-items: center;
            gap: 7px;
            border: 1px solid transparent;
            border-radius: 8px;
            padding: 9px 13px;
            cursor: pointer;
            font-size: 11px;
            font-weight: 700;
            transition: .2s;
            text-align: center;
        }

        .btn-primary {
            color: white;
            background: var(--primary);
            border-color: var(--primary);
        }

        .btn-primary:hover {
            background: var(--primary-dark);
        }

        .btn-block {
            width: 100%;
            padding: 11px;
        }

        .btn-danger {
            background: white;
            color: var(--danger);
            border-color: #fecaca;
        }

        .btn-danger:hover {
            background: #fef2f2;
        }

        .mini-btn {
            padding: 7px 9px;
            font-size: 10px;
            white-space: nowrap;
        }

        .table-toolbar {
            padding: 14px 17px;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
        }

        .table-toolbar-title {
            font-size: 12px;
            font-weight: 800;
        }

        .table-toolbar-note {
            color: var(--muted);
            font-size: 10px;
            margin-top: 2px;
        }

        .search-box {
            width: 155px;
            max-width: 45%;
            border: 1px solid var(--border);
            border-radius: 7px;
            padding: 8px 10px;
            outline: none;
            font-size: 11px;
        }

        .search-box:focus {
            border-color: #93c5fd;
        }

        .table-scroll {
            width: 100%;
            overflow-x: auto;
        }

        table {
            border-collapse: collapse;
            width: 100%;
            min-width: 570px;
        }

        thead {
            background: #f8fafc;
        }

        th {
            padding: 12px 14px;
            text-align: left;
            white-space: nowrap;
            color: #8791a3;
            font-size: 10px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: .45px;
            border-bottom: 1px solid var(--border);
        }

        td {
            padding: 13px 14px;
            border-bottom: 1px solid #edf0f5;
            color: #536077;
            font-size: 11px;
            vertical-align: middle;
            max-width: 230px;
            overflow-wrap: anywhere;
        }

        tbody tr:last-child td {
            border-bottom: none;
        }

        tbody tr:hover {
            background: #fbfdff;
        }

        .record-id {
            color: #9aa3b4;
            font-size: 10px;
            font-weight: 700;
        }

        .primary-cell {
            color: #263248;
            font-weight: 700;
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            border-radius: 6px;
            padding: 5px 8px;
            font-size: 10px;
            font-weight: 700;
            white-space: nowrap;
            background: #f1f5f9;
            color: #475569;
        }

        .status-badge::before {
            content: "";
            width: 5px;
            height: 5px;
            border-radius: 50%;
            background: currentColor;
        }

        .status-active, .status-resolved {
            background: #dcfce7;
            color: #15803d;
        }

        .status-new {
            background: #ede9fe;
            color: #6d28d9;
        }

        .status-in-progress {
            background: #ffedd5;
            color: #c2410c;
        }

        .status-open {
            background: #fef3c7;
            color: #92400e;
        }

        .status-closed {
            background: #f1f5f9;
            color: #64748b;
        }

        .status-inactive {
            background: #fee2e2;
            color: #b91c1c;
        }

        .status-select {
            width: 115px;
            max-width: 100%;
            padding: 7px 6px;
            border: 1px solid var(--border);
            border-radius: 6px;
            background: white;
            color: #526077;
            font-size: 10px;
            outline: none;
        }

        .status-form {
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .actions-cell {
            white-space: nowrap;
        }

        .empty-state {
            padding: 35px 15px;
            text-align: center;
            color: var(--muted);
        }

        .empty-icon {
            font-size: 25px;
            margin-bottom: 7px;
        }

        .empty-state strong {
            display: block;
            color: #536077;
            font-size: 12px;
            margin-bottom: 3px;
        }

        .empty-state p {
            font-size: 11px;
        }

        .flash-container {
            margin-bottom: 20px;
        }

        .flash-message {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 12px;
            padding: 12px 15px;
            border: 1px solid #bfdbfe;
            border-radius: 9px;
            background: #eff6ff;
            color: #1d4ed8;
            font-size: 12px;
            margin-bottom: 8px;
        }

        .flash-message.error {
            border-color: #fecaca;
            background: #fef2f2;
            color: #b91c1c;
        }

        .flash-close {
            border: 0;
            background: transparent;
            color: inherit;
            cursor: pointer;
            font-size: 17px;
            line-height: 1;
        }

        .footer {
            margin-top: 39px;
            padding-top: 19px;
            border-top: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 15px;
            color: #98a1b1;
            font-size: 10px;
        }

        .footer strong {
            color: #64748b;
        }

        .back-top {
            color: var(--primary);
            font-weight: 700;
        }

        @media (max-width: 1200px) {
            .sidebar { width: 220px; }
            .main-content { margin-left: 220px; }
            .page-content { padding-left: 24px; padding-right: 24px; }
            .topbar { padding-left: 24px; padding-right: 24px; }
            .stats-grid { grid-template-columns: repeat(2,minmax(0,1fr)); }
            .overview-grid { grid-template-columns: repeat(2,minmax(0,1fr)); }
            .collection-layout {
                grid-template-columns: minmax(220px,.75fr) minmax(0,1.5fr);
            }
        }

        @media (max-width: 850px) {
            .sidebar {
                width: 100%;
                height: auto;
                position: sticky;
                top: 0;
                padding: 12px 16px;
                border-right: none;
                border-bottom: 1px solid var(--border);
            }

            .brand { padding: 0 3px 12px; border-bottom: none; }
            .brand-logo { width: 37px; height: 37px; font-size: 17px; }
            .brand-name { font-size: 15px; }
            .brand-caption { font-size: 9px; }
            .nav-label, .sidebar-bottom { display: none; }

            .nav-links {
                flex-direction: row;
                overflow-x: auto;
                padding-top: 9px;
                gap: 5px;
            }

            .nav-link {
                padding: 8px 10px;
                white-space: nowrap;
                font-size: 11px;
            }

            .nav-icon { font-size: 14px; width: auto; }
            .main-content { margin-left: 0; }
            .topbar { position: static; min-height: 57px; padding: 12px 20px; }
            .page-content { padding: 24px 20px 35px; }
            .collection-layout { grid-template-columns: 1fr; }
            .form-body {
                display: grid;
                grid-template-columns: repeat(2,minmax(0,1fr));
                gap: 0 13px;
            }
            .form-body .btn-block { grid-column: 1 / -1; }
        }

        @media (max-width: 540px) {
            .topbar { padding: 12px 14px; }
            .page-content { padding: 22px 13px 28px; }
            .welcome-row { flex-direction: column; gap: 13px; }
            h1 { font-size: 26px; }
            .stats-grid { gap: 10px; }
            .stat-card { padding: 14px; }
            .stat-top { margin-bottom: 13px; align-items: flex-start; }
            .stat-label { font-size: 10px; }
            .stat-icon { height: 31px; width: 31px; font-size: 15px; }
            .stat-value { font-size: 26px; }
            .stat-footer { font-size: 10px; }
            .overview-panel { padding: 16px; }
            .overview-grid { gap: 9px; }
            .overview-item { padding: 12px; }
            .collection-heading h2 { font-size: 15px; }
            .collection-icon { width: 37px; height: 37px; }
            .form-body { grid-template-columns: 1fr; }
            .form-body .btn-block { grid-column: auto; }
            .topbar-right { gap: 6px; }
            .live-status { padding: 6px 7px; font-size: 10px; }
            .logout-btn { padding: 7px 8px; font-size: 10px; }
            .footer { flex-direction: column; align-items: flex-start; }
        }
    </style>
</head>

<body id="top">
<div class="app-layout">

    <aside class="sidebar">
        <a class="brand" href="#dashboard">
            <div class="brand-logo">V</div>
            <div>
                <div class="brand-name">Veda Technology</div>
                <div class="brand-caption">Business Suite</div>
            </div>
        </a>

        <div class="nav-label">Workspace</div>

        <nav class="nav-links">
            <a class="nav-link active" href="#dashboard">
                <span class="nav-icon">▦</span> Dashboard
            </a>
            <a class="nav-link" href="#services">
                <span class="nav-icon">◇</span> Services
            </a>
            <a class="nav-link" href="#programs">
                <span class="nav-icon">▤</span> Programs
            </a>
            <a class="nav-link" href="#inquiries">
                <span class="nav-icon">✉</span> Inquiries
            </a>
            <a class="nav-link" href="#service_requests">
                <span class="nav-icon">↗</span> Service Requests
            </a>
        </nav>

        <div class="nav-label">System</div>
        <nav class="nav-links">
            <a class="nav-link" href="#dashboard">
                <span class="nav-icon">⚙</span> Management Overview
            </a>
        </nav>

        <div class="sidebar-bottom">
            <div class="admin-card">
                <div class="admin-avatar">VT</div>
                <div>
                    <div class="admin-name">{{ session.get('username', 'Admin') }}</div>
                    <div class="admin-role">Signed-in Administrator</div>
                </div>
            </div>
        </div>
    </aside>

    <main class="main-content">
        <header class="topbar">
            <div class="breadcrumb">
                Workspace <span style="padding: 0 7px;">/</span>
                <strong>Dashboard</strong>
            </div>

            <div class="topbar-right">
                <div class="live-status">
                    <span class="live-dot"></span>
                    System Online
                </div>

                <form method="POST" action="{{ url_for('logout') }}">
                    <button class="logout-btn" type="submit">
                        ⇥ Logout
                    </button>
                </form>
            </div>
        </header>

        <div class="page-content">

            <section id="dashboard">
                <div class="welcome-row">
                    <div>
                        <div class="eyebrow">Business Management Platform</div>
                        <h1>Dashboard Overview</h1>
                        <p class="welcome-description">
                            Welcome back, {{ session.get('username', 'Admin') }}.
                            Manage your services, programs and customer activity.
                        </p>
                    </div>

                    <div class="date-chip">
                        ▦ &nbsp; <span id="current-date">Management Console</span>
                    </div>
                </div>

                {% with messages = get_flashed_messages(with_categories=true) %}
                    {% if messages %}
                        <div class="flash-container">
                            {% for category, message in messages %}
                                <div class="flash-message {% if category == 'error' %}error{% endif %}">
                                    <span>{{ message }}</span>
                                    <button type="button"
                                            class="flash-close"
                                            aria-label="Dismiss notification"
                                            onclick="this.parentElement.remove()">
                                        &times;
                                    </button>
                                </div>
                            {% endfor %}
                        </div>
                    {% endif %}
                {% endwith %}

                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-top">
                            <div class="stat-label">Total Services</div>
                            <div class="stat-icon icon-blue">◇</div>
                        </div>
                        <div class="stat-value">{{ services|length }}</div>
                        <div class="stat-footer">
                            <span class="stat-accent">Services</span>
                            in your catalogue
                        </div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-top">
                            <div class="stat-label">Total Programs</div>
                            <div class="stat-icon icon-purple">▤</div>
                        </div>
                        <div class="stat-value">{{ programs|length }}</div>
                        <div class="stat-footer">
                            <span class="stat-accent">Programs</span>
                            available to manage
                        </div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-top">
                            <div class="stat-label">Customer Inquiries</div>
                            <div class="stat-icon icon-orange">✉</div>
                        </div>
                        <div class="stat-value">{{ inquiries|length }}</div>
                        <div class="stat-footer">
                            <span class="stat-accent">Inquiries</span>
                            recorded in the system
                        </div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-top">
                            <div class="stat-label">Open Requests</div>
                            <div class="stat-icon icon-green">↗</div>
                        </div>
                        <div class="stat-value">{{ open_requests }}</div>
                        <div class="stat-footer">
                            <span class="stat-accent">Requests</span>
                            requiring attention
                        </div>
                    </div>
                </div>
            </section>

            <section class="overview-panel">
                <div class="section-heading">
                    <div>
                        <h2>Quick Access</h2>
                        <p class="section-subtitle">
                            Navigate directly to the workspace you need.
                        </p>
                    </div>
                </div>

                <div class="overview-grid">
                    <a class="overview-item" href="#services">
                        <div class="overview-item-icon">◇</div>
                        <h3>Service Catalogue</h3>
                        <p>Manage service details and pricing.</p>
                        <span class="overview-arrow">View services →</span>
                    </a>

                    <a class="overview-item" href="#programs">
                        <div class="overview-item-icon">▤</div>
                        <h3>Programs</h3>
                        <p>Organize program information.</p>
                        <span class="overview-arrow">View programs →</span>
                    </a>

                    <a class="overview-item" href="#inquiries">
                        <div class="overview-item-icon">✉</div>
                        <h3>Customer Inquiries</h3>
                        <p>Review and update inquiry status.</p>
                        <span class="overview-arrow">View inquiries →</span>
                    </a>

                    <a class="overview-item" href="#service_requests">
                        <div class="overview-item-icon">↗</div>
                        <h3>Service Requests</h3>
                        <p>Track customer service requests.</p>
                        <span class="overview-arrow">View requests →</span>
                    </a>
                </div>
            </section>

            {% for key, config in collections.items() %}
                {% set records = data[key] %}

                <section class="collection-section" id="{{ key }}">
                    <div class="collection-heading">
                        <div class="collection-title-group">
                            <div class="collection-icon">
                                {% if key == 'services' %}◇
                                {% elif key == 'programs' %}▤
                                {% elif key == 'inquiries' %}✉
                                {% else %}↗
                                {% endif %}
                            </div>
                            <div>
                                <h2>{{ config.title }}</h2>
                                <p>Manage and maintain your {{ config.title|lower }} records.</p>
                            </div>
                        </div>

                        <div class="record-count">
                            {{ records|length }} record{% if records|length != 1 %}s{% endif %}
                        </div>
                    </div>

                    <div class="collection-layout">
                        <div class="panel">
                            <div class="panel-header">
                                <h3>＋ Add {{ config.singular }}</h3>
                                <p>Enter the details to create a new record.</p>
                            </div>

                            <form class="form-body"
                                  method="POST"
                                  action="{{ url_for('add_record', collection=key) }}">

                                {% for field in config.fields %}
                                    <div class="form-group">
                                        <label for="{{ key }}_{{ field }}">
                                            {{ config.labels[loop.index0] }}
                                        </label>

                                        {% if field == 'message' or field == 'description' %}
                                            <textarea
                                                class="form-control"
                                                id="{{ key }}_{{ field }}"
                                                name="{{ field }}"
                                                placeholder="Enter {{ config.labels[loop.index0]|lower }}"
                                                required></textarea>
                                        {% elif field == 'price' %}
                                            <input
                                                class="form-control"
                                                id="{{ key }}_{{ field }}"
                                                type="number"
                                                name="{{ field }}"
                                                min="0"
                                                step="0.01"
                                                placeholder="0.00"
                                                required>
                                        {% else %}
                                            <input
                                                class="form-control"
                                                id="{{ key }}_{{ field }}"
                                                type="text"
                                                name="{{ field }}"
                                                placeholder="Enter {{ config.labels[loop.index0]|lower }}"
                                                required>
                                        {% endif %}
                                    </div>
                                {% endfor %}

                                <button type="submit" class="btn btn-primary btn-block">
                                    ＋ Add {{ config.singular }}
                                </button>
                            </form>
                        </div>

                        <div class="panel">
                            <div class="table-toolbar">
                                <div>
                                    <div class="table-toolbar-title">
                                        {{ config.title }} Directory
                                    </div>
                                    <div class="table-toolbar-note">
                                        Search records or manage existing entries.
                                    </div>
                                </div>

                                <input
                                    type="search"
                                    class="search-box"
                                    placeholder="⌕ Search..."
                                    aria-label="Search {{ config.title }}"
                                    oninput="filterTable(this, '{{ key }}_table')">
                            </div>

                            <div class="table-scroll">
                                <table id="{{ key }}_table">
                                    <thead>
                                        <tr>
                                            <th>ID</th>
                                            {% for label in config.labels %}
                                                <th>{{ label }}</th>
                                            {% endfor %}
                                            <th>Status</th>
                                            <th>Update</th>
                                            <th>Action</th>
                                        </tr>
                                    </thead>

                                    <tbody>
                                        {% for record in records %}
                                            <tr>
                                                <td>
                                                    <span class="record-id">#{{ record.id }}</span>
                                                </td>

                                                {% for field in config.fields %}
                                                    <td>
                                                        {% if field == 'price' %}
                                                            <span class="primary-cell">
                                                                ₹{{ "%.2f"|format(record[field]|float) }}
                                                            </span>
                                                        {% else %}
                                                            <span {% if loop.first %}class="primary-cell"{% endif %}>
                                                                {{ record[field] }}
                                                            </span>
                                                        {% endif %}
                                                    </td>
                                                {% endfor %}

                                                <td>
                                                    <span class="status-badge status-{{ record.status|lower|replace(' ', '-') }}">
                                                        {{ record.status }}
                                                    </span>
                                                </td>

                                                <td>
                                                    <form class="status-form"
                                                          method="POST"
                                                          action="{{ url_for('update_status', collection=key, record_id=record.id) }}">
                                                        <select class="status-select"
                                                                name="status"
                                                                aria-label="Choose status">
                                                            {% for status in config.statuses %}
                                                                <option value="{{ status }}"
                                                                    {% if record.status == status %}selected{% endif %}>
                                                                    {{ status }}
                                                                </option>
                                                            {% endfor %}
                                                        </select>
                                                        <button class="btn btn-primary mini-btn" type="submit">
                                                            Save
                                                        </button>
                                                    </form>
                                                </td>

                                                <td class="actions-cell">
                                                    <form method="POST"
                                                          action="{{ url_for('delete_record', collection=key, record_id=record.id) }}"
                                                          onsubmit="return confirm('Delete this record permanently?');">
                                                        <button type="submit" class="btn btn-danger mini-btn">
                                                            Delete
                                                        </button>
                                                    </form>
                                                </td>
                                            </tr>
                                        {% else %}
                                            <tr>
                                                <td colspan="{{ config.fields|length + 4 }}">
                                                    <div class="empty-state">
                                                        <div class="empty-icon">▤</div>
                                                        <strong>No records yet</strong>
                                                        <p>
                                                            Add your first {{ config.singular|lower }}
                                                            using the form.
                                                        </p>
                                                    </div>
                                                </td>
                                            </tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </section>
            {% endfor %}

            <footer class="footer">
                <div>
                    © <span id="current-year"></span>
                    <strong>Veda Technology</strong>.
                    Business &amp; Service Management System.
                </div>
                <a class="back-top" href="#top">Back to top ↑</a>
            </footer>

        </div>
    </main>
</div>

<script>
    const now = new Date();

    document.getElementById("current-date").textContent =
        now.toLocaleDateString("en-IN", {
            day: "2-digit",
            month: "short",
            year: "numeric"
        });

    document.getElementById("current-year").textContent =
        now.getFullYear();

    function filterTable(input, tableId) {
        const query = input.value.toLowerCase().trim();
        const table = document.getElementById(tableId);

        if (!table) return;

        table.querySelectorAll("tbody tr").forEach(function (row) {
            row.style.display =
                row.textContent.toLowerCase().includes(query) ? "" : "none";
        });
    }

    const navLinks = document.querySelectorAll(".nav-link");

    function updateActiveLink() {
        const hash = window.location.hash || "#dashboard";

        navLinks.forEach(function (link) {
            link.classList.toggle(
                "active",
                link.getAttribute("href") === hash
            );
        });
    }

    window.addEventListener("hashchange", updateActiveLink);
    updateActiveLink();
</script>
</body>
</html>
"""


# ---------------------------------------------------------
# Authentication helpers
# ---------------------------------------------------------

def login_required(view_function):
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if "username" not in session:
            flash("Please sign in to access the dashboard.", "error")
            return redirect(url_for("login"))

        return view_function(*args, **kwargs)

    return wrapped_view


# ---------------------------------------------------------
# Login and logout routes
# ---------------------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        valid_username = (
            username == ADMIN_USERNAME
            and username != ""
        )

        valid_password = check_password_hash(
            ADMIN_PASSWORD_HASH,
            password,
        )

        if valid_username and valid_password:
            session.clear()
            session["username"] = username
            session.permanent = True

            flash("Welcome back! You have signed in successfully.", "success")

            return redirect(url_for("home"))

        flash("Invalid username or password. Please try again.", "error")

    return render_template_string(LOGIN_PAGE)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You have been signed out successfully.", "success")
    return redirect(url_for("login"))


# ---------------------------------------------------------
# Dashboard
# ---------------------------------------------------------

@app.route("/")
@login_required
def home():
    return render_template_string(
        PAGE,
        collections=COLLECTIONS,
        data={
            "services": services,
            "programs": programs,
            "inquiries": inquiries,
            "service_requests": service_requests,
        },
        services=services,
        programs=programs,
        inquiries=inquiries,
        service_requests=service_requests,
        open_requests=sum(
            1 for record in service_requests
            if record.get("status") == "Open"
        ),
    )


# ---------------------------------------------------------
# Add a record
# ---------------------------------------------------------

@app.route("/add/<collection>", methods=["POST"])
@login_required
def add_record(collection):
    if collection not in COLLECTIONS:
        flash("Invalid collection selected.", "error")
        return redirect(url_for("home"))

    config = COLLECTIONS[collection]

    target = {
        "services": services,
        "programs": programs,
        "inquiries": inquiries,
        "service_requests": service_requests,
    }[collection]

    record = {}

    for index, field in enumerate(config["fields"]):
        value = request.form.get(field, "").strip()

        if not value:
            flash(f"{config['labels'][index]} is required.", "error")
            return redirect(url_for("home") + f"#{collection}")

        record[field] = value

    if collection == "services":
        try:
            price = float(record["price"])

            if price < 0:
                raise ValueError

            record["price"] = round(price, 2)

        except (ValueError, TypeError):
            flash("Enter a valid, non-negative service price.", "error")
            return redirect(url_for("home") + "#services")

    if collection in ("services", "programs"):
        name = record["name"].casefold()

        if any(
            str(existing.get("name", "")).casefold() == name
            for existing in target
        ):
            flash(
                f"A {config['singular'].lower()} with that name already exists.",
                "error",
            )
            return redirect(url_for("home") + f"#{collection}")

    next_id = max(
        (int(item.get("id", 0)) for item in target),
        default=0,
    ) + 1

    record["id"] = next_id

    record["status"] = {
        "services": "Active",
        "programs": "Open",
        "inquiries": "New",
        "service_requests": "Open",
    }[collection]

    if collection == "service_requests":
        record["priority"] = "Medium"

    target.append(record)
    save_data(collection)

    flash(f"{config['singular']} added successfully.", "success")
    return redirect(url_for("home") + f"#{collection}")


# ---------------------------------------------------------
# Update record status
# ---------------------------------------------------------

@app.route("/update/<collection>/<int:record_id>", methods=["POST"])
@login_required
def update_status(collection, record_id):
    if collection not in COLLECTIONS:
        flash("Invalid collection selected.", "error")
        return redirect(url_for("home"))

    config = COLLECTIONS[collection]

    target = {
        "services": services,
        "programs": programs,
        "inquiries": inquiries,
        "service_requests": service_requests,
    }[collection]

    record = next(
        (
            item for item in target
            if int(item.get("id", -1)) == record_id
        ),
        None,
    )

    if record is None:
        flash("The selected record could not be found.", "error")
        return redirect(url_for("home") + f"#{collection}")

    new_status = request.form.get("status", "").strip()

    if new_status not in config["statuses"]:
        flash("Invalid status selected.", "error")
        return redirect(url_for("home") + f"#{collection}")

    record["status"] = new_status
    save_data(collection)

    flash("Record status updated successfully.", "success")
    return redirect(url_for("home") + f"#{collection}")


# ---------------------------------------------------------
# Delete a record
# ---------------------------------------------------------

@app.route("/delete/<collection>/<int:record_id>", methods=["POST"])
@login_required
def delete_record(collection, record_id):
    if collection not in COLLECTIONS:
        flash("Invalid collection selected.", "error")
        return redirect(url_for("home"))

    target = {
        "services": services,
        "programs": programs,
        "inquiries": inquiries,
        "service_requests": service_requests,
    }[collection]

    record = next(
        (
            item for item in target
            if int(item.get("id", -1)) == record_id
        ),
        None,
    )

    if record is None:
        flash("The selected record could not be found.", "error")
        return redirect(url_for("home") + f"#{collection}")

    target.remove(record)
    save_data(collection)

    flash("Record deleted successfully.", "success")
    return redirect(url_for("home") + f"#{collection}")


# ---------------------------------------------------------
# Run application
# ---------------------------------------------------------

if __name__ == "__main__":
    initialize_storage()
    app.run(debug=True)
