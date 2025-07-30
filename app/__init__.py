from flask import Flask
from .routes import init_routes

app = Flask(__name__)
app.secret_key = 'supersecretkey'

init_routes(app)
