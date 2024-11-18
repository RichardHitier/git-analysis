from flask import Flask


def create_app():
    """App factory method
    takes environment variable as arg to choose between configuration:
    production, development, testing or default

    @return: running app
    """
    app = Flask(__name__)

    # Initialize blueprints
    from web.main import bp as main_bp

    app.register_blueprint(main_bp)
    
    app.logger.info(
        "#+-#+-#+-#+-#+-#+-#+-#+-#+-#+- CREATE APP -+#-+#-+#-+#-+#-+#-+#-+#-+#-+#"
    )

    return app
