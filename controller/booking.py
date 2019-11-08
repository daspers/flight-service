import json
from controller.flight import get_remaining_seat_flight
from controller.passenger import get_num_of_passenger
from model.flight import generate_update_diff_query_by_id
from model.booking import BookingModel, generate_booking_id, generate_add_booking_query, generate_get_booking_query, generate_delete_booking_query
from model.passenger import generate_add_passenger_query, generate_delete_passenger_query


def get_booking(mysql, booking_id):
    cur = mysql.connection.cursor()
    cur.execute(generate_get_booking_query({'booking_id': booking_id}))
    query_result = list(cur.fetchall())
    cur.close()

    if len(query_result) == 0:
        return None
    return query_result[0]


def create_booking(mysql, params):
    params_label = ['flight_id', 'passengers']
    for label in params_label:
        if label not in params:
            return 'Error! Bad request', 400
    flight_id = params['flight_id']
    rem_seat = get_remaining_seat_flight(mysql, flight_id)

    num_of_passengers = len(params['passengers'])
    if rem_seat == -1 or num_of_passengers == 0:
        return 'Error! Invalid value', 400

    if num_of_passengers > rem_seat:
        return 'Book failed, cause of remaining seat less than number of passengers', 401

    cur = mysql.connection.cursor()
    cur.execute(generate_update_diff_query_by_id({
        'remaining_seat' : -num_of_passengers
    }, flight_id))
    # mysql.connection.commit()
    # cur.close()

    booking_id = generate_booking_id()
    # cur = mysql.connection.cursor()
    cur.execute(generate_add_booking_query(booking_id, flight_id))
    for passenger in params['passengers']:
        cur.execute(generate_add_passenger_query(passenger, booking_id))
    mysql.connection.commit()
    cur.close()

    data = {'booking_id': booking_id}
    return json.dumps(data, default=str), 200


def cancel_booking(mysql, params):
    if 'booking_id' not in params:
        return 'Error! Bad request', 400

    booking_id = params['booking_id']
    num_of_passengers = get_num_of_passenger(mysql, booking_id)

    booking = get_booking(mysql, booking_id)
    if booking is None:
        return 'Error! Invalid value', 400

    booking = BookingModel(*list(booking)).get_data()
    flight_id = booking['flight_id']

    cur = mysql.connection.cursor()
    cur.execute(generate_update_diff_query_by_id({
        'remaining_seat' : num_of_passengers
    }, flight_id))

    cur.execute(generate_delete_booking_query({'booking_id': booking_id}))
    cur.execute(generate_delete_passenger_query({'booking_id': booking_id}))
    mysql.connection.commit()
    cur.close()

    return 'Success', 200