import json
import os
import sys
from typing import Optional

# If running within a Streamlit process, seamlessly run the Streamlit interface
try:
    import streamlit as st
    if st.runtime.exists():
        import streamlit_app
        streamlit_app.main()
        sys.exit(0)
except Exception:
    pass

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, Response
from starlette.routing import Route

from analyzer.pipeline import analyze_policy

CATEGORY_META = {
    "collection": {"icon": "📥", "title": "Personal Data Collected"},
    "purpose": {"icon": "🎯", "title": "Processing Purpose"},
    "sharing": {"icon": "🤝", "title": "Third-Party Sharing"},
    "tracking": {"icon": "🍪", "title": "Tracking & Cookies"},
    "retention": {"icon": "⏳", "title": "Data Retention Duration"},
    "security": {"icon": "🔒", "title": "Security & Encryption"},
    "rights": {"icon": "⚖️", "title": "User Rights & Choices"},
}

SAMPLE_EN = (
    "Example Privacy Policy:\n\n"
    "We collect your email address, full name, phone number, and device location to provide and improve our service.\n"
    "We share personal information with trusted advertising partners and analytics providers for marketing purposes.\n"
    "We utilize cookies, pixels, and tracking beacons to personalize content and track usage activity.\n"
    "We retain your data for as long as your account remains active or up to five years after termination.\n"
    "All communications and data are encrypted using industry-standard TLS and stored securely.\n"
    "You have the right to access, rectify, or request deletion of your information at any time."
)

SAMPLE_DA = (
    "Eksempel på Privatlivspolitik:\n\n"
    "Vi indsamler dit navn, e-mailadresse, telefonnummer og placering for at levere og forbedre vores tjenester.\n"
    "Vi deler dine oplysninger med vores betroede tredjeparts partnere og annoncører.\n"
    "Vi anvender cookies og sporing for at analysere brugernes adfærd.\n"
    "Vi opbevarer dine personoplysninger i op til fem år.\n"
    "Vi beskytter dine data med sikker kryptering og adgangskontrol.\n"
    "Du har ret til indsigt samt ret til at få dine oplysninger slettet."
)

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Privacy Policy Inspector 🛡️</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #090d16;
      --card-bg: #111827;
      --card-border: rgba(255, 255, 255, 0.08);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --primary: #2563eb;
      --primary-hover: #1d4ed8;
      --accent-green: #10b981;
      --accent-green-bg: rgba(16, 185, 129, 0.16);
      --accent-amber: #f59e0b;
      --accent-amber-bg: rgba(245, 158, 11, 0.16);
      --accent-red: #ef4444;
      --accent-red-bg: rgba(239, 68, 68, 0.16);
    }
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    body {
      background: var(--bg);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }
    .layout-wrapper {
      display: flex;
      flex: 1;
      width: 100%;
      max-width: 1400px;
      margin: 0 auto;
    }
    /* Sidebar */
    .sidebar {
      width: 310px;
      padding: 32px 24px;
      border-right: 1px solid var(--card-border);
      background: rgba(17, 24, 39, 0.7);
      display: flex;
      flex-direction: column;
      gap: 24px;
    }
    .sidebar h2 {
      font-size: 1.25rem;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .sidebar-subtitle {
      font-size: 0.85rem;
      color: var(--text-muted);
      margin-top: 4px;
    }
    .divider {
      height: 1px;
      background: var(--card-border);
    }
    .scoring-weights {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--card-border);
      border-radius: 8px;
      padding: 14px 16px;
      font-size: 0.88rem;
    }
    .scoring-weights ul {
      list-style: none;
      margin-top: 8px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .scoring-weights code {
      background: rgba(255, 255, 255, 0.08);
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 0.82rem;
      color: #93c5fd;
    }
    .tier-list {
      margin-top: 10px;
      font-size: 0.82rem;
      display: flex;
      flex-direction: column;
      gap: 4px;
      color: var(--text-muted);
    }
    .sidebar-footer {
      margin-top: auto;
      font-size: 0.8rem;
      color: var(--text-muted);
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid var(--card-border);
      padding: 10px 12px;
      border-radius: 6px;
    }

    /* Main Content */
    .main-content {
      flex: 1;
      padding: 36px 40px;
      overflow-y: auto;
    }
    .hero-header h1 {
      font-size: 2rem;
      font-weight: 700;
      letter-spacing: -0.5px;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .hero-header p {
      color: var(--text-muted);
      margin-top: 6px;
      font-size: 1.02rem;
    }

    /* Tabs */
    .tabs-nav {
      display: flex;
      gap: 12px;
      margin-top: 28px;
      border-bottom: 1px solid var(--card-border);
      padding-bottom: 12px;
    }
    .tab-btn {
      background: none;
      border: none;
      color: var(--text-muted);
      font-size: 0.95rem;
      font-weight: 600;
      padding: 8px 16px;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .tab-btn:hover {
      color: var(--text-main);
      background: rgba(255, 255, 255, 0.05);
    }
    .tab-btn.active {
      color: #fff;
      background: rgba(37, 99, 235, 0.2);
      border: 1px solid rgba(37, 99, 235, 0.4);
    }

    /* Tab Panes */
    .tab-content {
      margin-top: 20px;
    }
    .tab-pane {
      display: none;
    }
    .tab-pane.active {
      display: block;
    }
    .input-grid {
      display: grid;
      grid-template-columns: 1fr 280px;
      gap: 20px;
    }
    textarea {
      width: 100%;
      height: 220px;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--card-border);
      border-radius: 8px;
      padding: 14px;
      color: var(--text-main);
      font-size: 0.95rem;
      resize: vertical;
      line-height: 1.5;
    }
    textarea:focus, input[type="text"]:focus {
      outline: none;
      border-color: var(--primary);
      box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.3);
    }
    input[type="text"] {
      width: 100%;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--card-border);
      border-radius: 8px;
      padding: 14px;
      color: var(--text-main);
      font-size: 0.95rem;
    }
    .presets-card {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--card-border);
      border-radius: 8px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .presets-card h4 {
      font-size: 0.88rem;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .btn-preset {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--card-border);
      color: var(--text-main);
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 0.88rem;
      cursor: pointer;
      text-align: left;
      transition: all 0.15s ease;
    }
    .btn-preset:hover {
      background: rgba(255, 255, 255, 0.1);
      border-color: rgba(255, 255, 255, 0.2);
    }
    .btn-primary {
      background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
      color: #fff;
      border: none;
      padding: 12px 24px;
      font-size: 1rem;
      font-weight: 600;
      border-radius: 8px;
      cursor: pointer;
      margin-top: 14px;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      box-shadow: 0 4px 14px rgba(37, 99, 235, 0.25);
      transition: all 0.2s ease;
    }
    .btn-primary:hover {
      background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
      transform: translateY(-1px);
      box-shadow: 0 6px 18px rgba(37, 99, 235, 0.4);
    }
    .btn-primary:disabled {
      opacity: 0.6;
      cursor: not-allowed;
      transform: none;
    }

    /* Alerts */
    .alert-error {
      background: var(--accent-red-bg);
      border: 1px solid rgba(239, 68, 68, 0.3);
      color: #fca5a5;
      padding: 14px 16px;
      border-radius: 8px;
      margin-top: 20px;
      display: none;
      align-items: center;
      justify-content: space-between;
      font-size: 0.95rem;
    }

    /* Loading Spinner */
    .spinner-wrap {
      display: none;
      align-items: center;
      gap: 12px;
      margin-top: 24px;
      color: var(--text-muted);
      font-size: 0.95rem;
    }
    .spinner {
      width: 24px;
      height: 24px;
      border: 3px solid rgba(255, 255, 255, 0.15);
      border-top-color: var(--primary);
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }
    @keyframes spin {
      to { transform: rotate(360deg); }
    }

    /* Results Dashboard */
    .dashboard-wrap {
      display: none;
      margin-top: 36px;
      border-top: 1px solid var(--card-border);
      padding-top: 32px;
    }
    .dashboard-title {
      font-size: 1.45rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 24px;
    }
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
    }
    .metric-card {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 12px;
      padding: 18px 20px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
      transition: transform 0.15s ease;
    }
    .metric-card:hover {
      transform: translateY(-2px);
    }
    .metric-label {
      font-size: 0.82rem;
      color: var(--text-muted);
      margin-bottom: 6px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .metric-value {
      font-size: 1.55rem;
      font-weight: 700;
    }
    .badge-pill {
      display: inline-block;
      padding: 4px 14px;
      border-radius: 20px;
      font-weight: 600;
      font-size: 0.88rem;
      letter-spacing: 0.5px;
    }
    .badge-low {
      background: var(--accent-green-bg);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.4);
    }
    .badge-medium {
      background: var(--accent-amber-bg);
      color: #fbbf24;
      border: 1px solid rgba(245, 158, 11, 0.4);
    }
    .badge-high {
      background: var(--accent-red-bg);
      color: #f87171;
      border: 1px solid rgba(239, 68, 68, 0.4);
    }

    /* Risk Progress Bar */
    .progress-bar-container {
      width: 100%;
      height: 10px;
      background: rgba(255, 255, 255, 0.08);
      border-radius: 5px;
      margin: 28px 0;
      overflow: hidden;
    }
    .progress-bar-fill {
      height: 100%;
      width: 0%;
      border-radius: 5px;
      transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* 2-Column Split */
    .results-split {
      display: grid;
      grid-template-columns: 1fr 2fr;
      gap: 28px;
    }
    .column-title {
      font-size: 1.15rem;
      font-weight: 700;
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .factor-pill-danger {
      background: rgba(239, 68, 68, 0.12);
      border: 1px solid rgba(239, 68, 68, 0.3);
      color: #f87171;
      padding: 8px 12px;
      border-radius: 8px;
      margin-bottom: 10px;
      font-size: 0.92rem;
    }
    .factor-pill-safe {
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid rgba(16, 185, 129, 0.3);
      color: #34d399;
      padding: 8px 12px;
      border-radius: 8px;
      margin-bottom: 10px;
      font-size: 0.92rem;
    }
    .btn-export {
      margin-top: 18px;
      width: 100%;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--card-border);
      color: var(--text-main);
      padding: 10px 16px;
      border-radius: 8px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: all 0.2s ease;
    }
    .btn-export:hover {
      background: rgba(255, 255, 255, 0.12);
      border-color: rgba(255, 255, 255, 0.25);
    }

    /* Category Boxes */
    .category-box {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-left: 4px solid #3b82f6;
      border-radius: 8px;
      padding: 14px 16px;
      margin-bottom: 14px;
    }
    .category-box.present {
      border-left-color: #10b981;
    }
    .category-box.absent {
      border-left-color: #64748b;
      opacity: 0.75;
    }
    .category-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
    }
    .category-snippet {
      font-size: 0.93rem;
      font-style: italic;
      color: #cbd5e1;
      line-height: 1.45;
    }
    .expander-toggle {
      background: none;
      border: none;
      color: #60a5fa;
      font-size: 0.85rem;
      cursor: pointer;
      margin-top: 8px;
      padding: 0;
      display: inline-block;
    }
    .expander-toggle:hover {
      text-decoration: underline;
    }
    .all-sentences {
      display: none;
      margin-top: 8px;
      padding-top: 8px;
      border-top: 1px dashed rgba(255, 255, 255, 0.1);
      font-size: 0.88rem;
      color: #e2e8f0;
    }
    .all-sentences ol {
      padding-left: 20px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    @media (max-width: 960px) {
      .layout-wrapper {
        flex-direction: column;
      }
      .sidebar {
        width: 100%;
        border-right: none;
        border-bottom: 1px solid var(--card-border);
      }
      .input-grid, .results-split {
        grid-template-columns: 1fr;
      }
      .kpi-grid {
        grid-template-columns: repeat(2, 1fr);
      }
    }
  </style>
</head>
<body>
  <div class="layout-wrapper">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div>
        <h2>🛡️ Privacy Inspector</h2>
        <p class="sidebar-subtitle">Automated Transparency & Risk Analysis Engine</p>
      </div>
      <div class="divider"></div>

      <div class="scoring-weights">
        <strong>📊 Risk Scoring Weights</strong>
        <ul>
          <li>Data Sharing: <code>+3 pts</code></li>
          <li>≥ 3 Personal Data Types: <code>+3 pts</code></li>
          <li>Tracking / Cookies: <code>+2 pts</code></li>
          <li>User Rights Granted: <code>-1 pt</code></li>
        </ul>
        <div class="tier-list">
          <div>🟢 <strong>Low Risk:</strong> ≤ 3</div>
          <div>🟡 <strong>Medium Risk:</strong> 4 – 7</div>
          <div>🔴 <strong>High Risk:</strong> ≥ 8</div>
        </div>
      </div>

      <div class="divider"></div>
      <div>
        <strong style="font-size: 0.9rem;">🌐 Supported Languages</strong>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 6px;">
          • English (<code>EN</code>)<br>
          • Danish (<code>DA</code>)
        </p>
      </div>

      <div class="sidebar-footer">
        🔒 <strong>Client-Side Privacy:</strong> Analyzed text is processed in memory and never stored externally.
      </div>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
      <div class="hero-header">
        <h1>🛡️ Privacy Policy Analyzer</h1>
        <p>Perform automated transparency audits, inspect third-party tracking, and calculate compliance risk scores in seconds.</p>
      </div>

      <!-- Tabs Navigation -->
      <div class="tabs-nav">
        <button class="tab-btn active" onclick="switchTab('text')">📄 Paste Policy Text</button>
        <button class="tab-btn" onclick="switchTab('url')">🌐 Analyze from Web URL</button>
      </div>

      <!-- Tab 1: Paste Text -->
      <div class="tab-content">
        <div id="tab-text" class="tab-pane active">
          <div class="input-grid">
            <div>
              <textarea id="policy-text" placeholder="Paste privacy policy text here (minimum 50 characters)..."></textarea>
              <button class="btn-primary" id="btn-analyze-text" onclick="analyzeText()">
                🔍 Analyze Pasted Text
              </button>
            </div>
            <div class="presets-card">
              <h4>Sample Presets</h4>
              <button class="btn-preset" onclick="fillSample('en')">🇺🇸 English Example</button>
              <button class="btn-preset" onclick="fillSample('da')">🇩🇰 Danish Example</button>
              <button class="btn-preset" onclick="clearText()">🗑️ Clear Text</button>
            </div>
          </div>
        </div>

        <!-- Tab 2: URL -->
        <div id="tab-url" class="tab-pane">
          <div class="input-grid">
            <div>
              <input type="text" id="policy-url" placeholder="https://example.com/privacy" />
              <button class="btn-primary" id="btn-analyze-url" onclick="analyzeUrl()">
                🌐 Fetch & Analyze URL
              </button>
            </div>
            <div class="presets-card">
              <h4>Example Links</h4>
              <button class="btn-preset" onclick="fillUrl('https://www.linkedin.com/legal/privacy-policy')">🔗 LinkedIn Policy</button>
              <button class="btn-preset" onclick="fillUrl('https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement')">🔗 GitHub Privacy</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Error Alert -->
      <div class="alert-error" id="error-box">
        <span id="error-message">Error message</span>
        <button onclick="dismissError()" style="background:none; border:none; color:inherit; font-weight:bold; cursor:pointer;">✕</button>
      </div>

      <!-- Spinner -->
      <div class="spinner-wrap" id="loading-spinner">
        <div class="spinner"></div>
        <span>Analyzing disclosures, tracking markers, and privacy risks...</span>
      </div>

      <!-- Results Dashboard -->
      <section class="dashboard-wrap" id="results-dashboard">
        <h2 class="dashboard-title">📊 Analysis Dashboard</h2>

        <div class="kpi-grid">
          <div class="metric-card">
            <div class="metric-label">RISK TIER</div>
            <div id="kpi-tier" class="badge-pill badge-medium">⚠️ MEDIUM RISK</div>
          </div>
          <div class="metric-card">
            <div class="metric-label">RISK SCORE</div>
            <div class="metric-value"><span id="kpi-score">0</span> <span style="font-size: 0.85rem; font-weight: 400; color: #94a3b8;">/ 10</span></div>
          </div>
          <div class="metric-card">
            <div class="metric-label">DETECTED LANGUAGE</div>
            <div id="kpi-lang" class="metric-value" style="font-size: 1.3rem;">🌐 English (EN)</div>
          </div>
          <div class="metric-card">
            <div class="metric-label">DISCLOSURES FOUND</div>
            <div id="kpi-disclosures" class="metric-value" style="font-size: 1.3rem;">0 of 7 topics</div>
          </div>
        </div>

        <div class="progress-bar-container">
          <div class="progress-bar-fill" id="progress-bar"></div>
        </div>

        <div class="results-split">
          <!-- Left: Risk Factors -->
          <div>
            <h3 class="column-title">⚠️ Risk Factors Identified</h3>
            <div id="factors-container"></div>
            <button class="btn-export" onclick="exportReport()">
              📥 Export Report (Markdown)
            </button>
          </div>

          <!-- Right: Category Disclosures -->
          <div>
            <h3 class="column-title">🔍 Category-by-Category Findings</h3>
            <div id="categories-container"></div>
          </div>
        </div>
      </section>
    </main>
  </div>

  <script>
    const SAMPLE_EN = `Example Privacy Policy:\\n\\nWe collect your email address, full name, phone number, and device location to provide and improve our service.\\nWe share personal information with trusted advertising partners and analytics providers for marketing purposes.\\nWe utilize cookies, pixels, and tracking beacons to personalize content and track usage activity.\\nWe retain your data for as long as your account remains active or up to five years after termination.\\nAll communications and data are encrypted using industry-standard TLS and stored securely.\\nYou have the right to access, rectify, or request deletion of your information at any time.`;

    const SAMPLE_DA = `Eksempel på Privatlivspolitik:\\n\\nVi indsamler dit navn, e-mailadresse, telefonnummer og placering for at levere og forbedre vores tjenester.\\nVi deler dine oplysninger med vores betroede tredjeparts partnere og annoncører.\\nVi anvender cookies og sporing for at analysere brugernes adfærd.\\nVi opbevarer dine personoplysninger i op til fem år.\\nVi beskytter dine data med sikker kryptering og adgangskontrol.\\nDu har ret til indsigt samt ret til at få dine oplysninger slettet.`;

    const CATEGORY_META = {
      "collection": {"icon": "📥", "title": "Personal Data Collected"},
      "purpose": {"icon": "🎯", "title": "Processing Purpose"},
      "sharing": {"icon": "🤝", "title": "Third-Party Sharing"},
      "tracking": {"icon": "🍪", "title": "Tracking & Cookies"},
      "retention": {"icon": "⏳", "title": "Data Retention Duration"},
      "security": {"icon": "🔒", "title": "Security & Encryption"},
      "rights": {"icon": "⚖️", "title": "User Rights & Choices"}
    };

    let latestResult = null;

    function switchTab(tab) {
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));
      if (tab === 'text') {
        document.querySelector('.tab-btn:nth-child(1)').classList.add('active');
        document.getElementById('tab-text').classList.add('active');
      } else {
        document.querySelector('.tab-btn:nth-child(2)').classList.add('active');
        document.getElementById('tab-url').classList.add('active');
      }
    }

    function fillSample(lang) {
      document.getElementById('policy-text').value = (lang === 'en') ? SAMPLE_EN : SAMPLE_DA;
    }
    function clearText() {
      document.getElementById('policy-text').value = '';
    }
    function fillUrl(url) {
      document.getElementById('policy-url').value = url;
    }
    function showError(msg) {
      const el = document.getElementById('error-box');
      document.getElementById('error-message').textContent = msg;
      el.style.display = 'flex';
    }
    function dismissError() {
      document.getElementById('error-box').style.display = 'none';
    }

    async function analyzeText() {
      const text = document.getElementById('policy-text').value.trim();
      if (!text) {
        showError("Please paste some privacy policy text first.");
        return;
      }
      runAnalysis({ text });
    }

    async function analyzeUrl() {
      let url = document.getElementById('policy-url').value.trim();
      if (!url) {
        showError("Please enter a valid web URL.");
        return;
      }
      if (!url.startsWith('http://') && !url.startsWith('https://')) {
        url = 'https://' + url;
      }
      runAnalysis({ url });
    }

    async function runAnalysis(payload) {
      dismissError();
      document.getElementById('loading-spinner').style.display = 'flex';
      document.getElementById('btn-analyze-text').disabled = true;
      document.getElementById('btn-analyze-url').disabled = true;

      try {
        const response = await fetch('/api/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await response.json();
        if (!response.ok || !data.success) {
          throw new Error(data.error || 'Failed to analyze policy.');
        }
        latestResult = data.data;
        renderDashboard(latestResult);
      } catch (err) {
        showError(err.message || 'An unexpected error occurred.');
      } finally {
        document.getElementById('loading-spinner').style.display = 'none';
        document.getElementById('btn-analyze-text').disabled = false;
        document.getElementById('btn-analyze-url').disabled = false;
      }
    }

    function renderDashboard(res) {
      const dashboard = document.getElementById('results-dashboard');
      dashboard.style.display = 'block';

      const risk = res.risk;
      const level = risk.level;
      const score = risk.score;
      const lang = res.language;
      const findings = res.findings;

      // Tier KPI
      const tierEl = document.getElementById('kpi-tier');
      tierEl.className = 'badge-pill';
      if (level === 'Low') {
        tierEl.classList.add('badge-low');
        tierEl.textContent = '🛡️ LOW RISK';
      } else if (level === 'Medium') {
        tierEl.classList.add('badge-medium');
        tierEl.textContent = '⚠️ MEDIUM RISK';
      } else {
        tierEl.classList.add('badge-high');
        tierEl.textContent = '🚨 HIGH RISK';
      }

      // Score KPI
      document.getElementById('kpi-score').textContent = score;

      // Lang KPI
      const langLabel = (lang === 'en') ? '🌐 English (EN)' : ((lang === 'da') ? '🌐 Danish (DA)' : `🌐 ${lang.toUpperCase()}`);
      document.getElementById('kpi-lang').textContent = langLabel;

      // Disclosures Found KPI
      let foundCount = 0;
      for (const k in findings) {
        if (findings[k] && findings[k].length > 0) foundCount++;
      }
      document.getElementById('kpi-disclosures').innerHTML = `${foundCount} of ${Object.keys(findings).length} <span style="font-size: 0.85rem; font-weight: 400; color: #94a3b8;">topics</span>`;

      // Progress Bar
      const fillEl = document.getElementById('progress-bar');
      const pct = Math.min(Math.max((score / 10.0) * 100, 10), 100);
      fillEl.style.width = pct + '%';
      if (level === 'Low') fillEl.style.background = '#10b981';
      else if (level === 'Medium') fillEl.style.background = '#f59e0b';
      else fillEl.style.background = '#ef4444';

      // Left Column: Risk Factors
      const factorsContainer = document.getElementById('factors-container');
      factorsContainer.innerHTML = '';
      if (risk.factors && risk.factors.length > 0) {
        risk.factors.forEach(([pts, reason]) => {
          const isDanger = pts.startsWith('+');
          const pill = document.createElement('div');
          pill.className = isDanger ? 'factor-pill-danger' : 'factor-pill-safe';
          pill.innerHTML = `<strong>${isDanger ? '🔺' : '🔻'} ${pts} pts</strong> — ${escapeHtml(reason)}`;
          factorsContainer.appendChild(pill);
        });
      } else {
        const clean = document.createElement('div');
        clean.className = 'factor-pill-safe';
        clean.innerHTML = `✅ <strong>Clean Assessment</strong> — No elevated risk factors identified.`;
        factorsContainer.appendChild(clean);
      }

      // Right Column: Categories
      const categoriesContainer = document.getElementById('categories-container');
      categoriesContainer.innerHTML = '';
      for (const catKey in CATEGORY_META) {
        const meta = CATEGORY_META[catKey];
        const sList = findings[catKey] || [];
        const box = document.createElement('div');

        if (sList.length > 0) {
          box.className = 'category-box present';
          const firstSnippet = sList[0].slice(0, 260) + (sList[0].length > 260 ? '...' : '');
          let expanderHtml = '';
          if (sList.length > 1) {
            const listItems = sList.map((s, idx) => `<li>${escapeHtml(s)}</li>`).join('');
            expanderHtml = `
              <button class="expander-toggle" onclick="toggleExpander(this)">View all ${sList.length} extracted disclosures ▾</button>
              <div class="all-sentences"><ol>${listItems}</ol></div>
            `;
          }
          box.innerHTML = `
            <div class="category-header">
              <strong>${meta.icon} ${meta.title}</strong>
              <span style="color: #10b981; font-weight: 600; font-size: 0.88rem;">● ${sList.length} sentence(s)</span>
            </div>
            <div class="category-snippet">"${escapeHtml(firstSnippet)}"</div>
            ${expanderHtml}
          `;
        } else {
          box.className = 'category-box absent';
          box.innerHTML = `
            <div class="category-header">
              <strong>${meta.icon} ${meta.title}</strong>
              <span style="color: #64748b; font-size: 0.85rem;">Not clearly mentioned</span>
            </div>
          `;
        }
        categoriesContainer.appendChild(box);
      }

      dashboard.scrollIntoView({ behavior: 'smooth' });
    }

    function toggleExpander(btn) {
      const details = btn.nextElementSibling;
      if (details.style.display === 'block') {
        details.style.display = 'none';
        btn.textContent = btn.textContent.replace('▴', '▾');
      } else {
        details.style.display = 'block';
        btn.textContent = btn.textContent.replace('▾', '▴');
      }
    }

    function exportReport() {
      if (!latestResult) return;
      const res = latestResult;
      const md = [
        '# Privacy Policy Inspection Report\\n',
        `**Risk Level:** ${res.risk.level} (Score: ${res.risk.score})`,
        `**Detected Language:** ${res.language}\\n`,
        '## Risk Factors'
      ];
      (res.risk.factors || []).forEach(([pts, reason]) => {
        md.push(`- **${pts}**: ${reason}`);
      });
      md.push('\\n## Category Disclosures');
      for (const catKey in CATEGORY_META) {
        const meta = CATEGORY_META[catKey];
        const sList = (res.findings && res.findings[catKey]) || [];
        md.push(`### ${meta.title}`);
        if (sList.length > 0) {
          sList.forEach(s => md.push(`> ${s}\\n`));
        } else {
          md.push('*Not clearly mentioned.*\\n');
        }
      }
      const content = md.join('\\n');
      const blob = new Blob([content], { type: 'text/markdown;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'privacy_policy_report.md';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    }

    function escapeHtml(str) {
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }
  </script>
</body>
</html>
"""


async def handle_index(request: Request) -> Response:
    return HTMLResponse(HTML_PAGE)


async def handle_analyze(request: Request) -> Response:
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"success": False, "error": "Invalid JSON body"}, status_code=400)

    text: Optional[str] = body.get("text")
    url: Optional[str] = body.get("url")

    if not text and not url:
        return JSONResponse(
            {"success": False, "error": "Please provide either policy 'text' or 'url'."},
            status_code=400,
        )

    try:
        result = analyze_policy(text=text, url=url)
        return JSONResponse({"success": True, "data": result})
    except ValueError as val_err:
        return JSONResponse({"success": False, "error": str(val_err)}, status_code=400)
    except Exception as exc:
        return JSONResponse(
            {"success": False, "error": f"Analysis failed: {str(exc)}"},
            status_code=500,
        )


async def handle_health(request: Request) -> Response:
    return JSONResponse({"status": "ok", "app": "Privacy Policy Analyzer"})


routes = [
    Route("/", endpoint=handle_index, methods=["GET"]),
    Route("/analyze", endpoint=handle_analyze, methods=["POST"]),
    Route("/api/analyze", endpoint=handle_analyze, methods=["POST"]),
    Route("/api/health", endpoint=handle_health, methods=["GET"]),
]

# Top-level ASGI application instance for Vercel and ASGI runners
app = Starlette(debug=False, routes=routes)
application = app  # Alias for WSGI/ASGI conventions
handler = app      # Alias for Vercel handler conventions

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
