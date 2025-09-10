"""
WSGI entry point for deployment platforms that require it.
This file provides a WSGI wrapper around the FastAPI ASGI application.
"""

from main import app

# For platforms that absolutely require WSGI, we can use this
# But the recommended approach is to use ASGI with uvicorn workers
application = app
