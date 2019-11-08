import datetime, json
from model.flight import FlightModel, generate_search_query, generate_search_by_id_query

def get_flights(mysql, params):
    cur = mysql.connection.cursor()
    cur.execute(generate_search_query(params))
    query_result = list(cur.fetchall())
    cur.close()

    result = []
    for query_tuple in query_result:
        result.append(FlightModel(*list(query_tuple)).get_data())

    data = {'flights' : result}
    return json.dumps(data, default=str)

def get_remaining_seat_flight(mysql, flight_id):
    cur = mysql.connection.cursor()
    cur.execute(generate_search_by_id_query(flight_id))
    query_result = list(cur.fetchall())
    cur.close()
    if len(query_result) == 0:
        return -1
    return FlightModel(*query_result[0]).get_data()['remaining_seat']

def get_flight_by_id(mysql, flight_id):
    cur = mysql.connection.cursor()
    cur.execute(generate_search_by_id_query(flight_id))
    query_result = list(cur.fetchall())
    cur.close()

    if len(query_result) == 0:
        return "Not found", 404

    result = FlightModel(*list(query_result[0])).get_data()
    data = {'flight': result}

    return json.dumps(data, default=str), 200