import json
from flask import Flask, request
from flask_mysqldb import MySQL


from controller.flight import get_flights
from controller.booking import create_booking, cancel_booking


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config['MYSQL_HOST'] = 'localhost'
    # app.config['MYSQL_PORT'] = 3306
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'root'
    app.config['MYSQL_DB'] = 'flight_service'

    mysql = MySQL(app)

    app.config.from_mapping(
        SECRET_KEY='dev',
        threaded=True
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # a simple page that says hello
    @app.route('/airline/flight', methods=['GET'])
    def get_flights_handler():
        try:
            return get_flights(mysql, request.args), 200
        except:
            return 'Internal Server Error', 500

    @app.route('/airline/flight/book', methods=['POST'])
    def make_booking_handler():
        try:
            body = request.form if len(request.form) > 0 else json.loads(request.get_data())
            return create_booking(mysql, body)
        except:
            return 'Internal Server Error', 500

    @app.route('/airline/flight/book/cancel', methods=['POST'])
    def cancel_booking_handler():
        try:
            body = request.form if len(request.form) > 0 else json.loads(request.get_data())
            return cancel_booking(mysql, body)
        except:
            return 'Internal Server Error', 500

    return app


app = create_app()
app.run(
    port=5000,
    threaded=True,
    debug=False
)