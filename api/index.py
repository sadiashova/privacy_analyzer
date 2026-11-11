"""
Vercel serverless entrypoint for Privacy Policy Analyzer.
Exposes 'app', 'application', and 'handler' from app.py.
"""
from app import app, application, handler

__all__ = ["app", "application", "handler"]
