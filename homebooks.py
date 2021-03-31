from app import app
from app.models import Book


@app.shell_context_processor
def make_shell_context():
    return {'Book': Book}

