from flask import Flask
import datetime

def create_app():
    print("In create app")
    app = Flask(__name__)

    @app.route('/')
    def get_current_time():
        current_time = datetime.datetime.now().strftime("%m/%d/%Y  %H:%M:%S")
        return f"Current Time: {current_time}"

    return app

def main():
    print("Creating Flask App")
    flask_app = create_app()
    print("Starting Flask")
    flask_app.run(debug=True, port=5001)
    print("Flask started")

if __name__ == '__main__':
    main()
#Finshed