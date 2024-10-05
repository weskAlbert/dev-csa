from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import and register the blueprint
    from .routes import bp
    app.register_blueprint(bp)

    return app
