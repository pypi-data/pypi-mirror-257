from flask import Flask
import datetime


def build_app():
    print("In build_app")
    app = Flask(__name__)

    @app.route('/')
    def retrieve_local_time():
        local_time = str(datetime.datetime.now().strftime("%I:%M %p"))
        return f"Local time is: {local_time}"

    return app


def main():
    print("Building Flask App...")
    flask_app = build_app()
    print("Starting Flask")
    flask_app.run(host='localhost', port=8080, debug=True)
    print("Flask Started")


if __name__ == '__main__':
    main()
