from flask import Flask
from datetime import datetime

def main():
    app = create_app()
    configure_routes(app)
    app.run(debug=True)
def create_app():
    print('create app')
    app = Flask('Lab_one')
    return app

def configure_routes(app):
    print('config route')
    @app.route('/')
    def get_current_time():
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"Current Time: {current_time}"

if __name__ == '__main__':
    main()
