"""Vercel serverless entry point for the existing Django application."""

from odin_ta_junior.wsgi import application

app = application
