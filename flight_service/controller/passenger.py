from ..model.passenger import generate_passenger_count_query


def get_num_of_passenger(mysql, booking_id):
    cur = mysql.connection.cursor()
    cur.execute(generate_passenger_count_query(booking_id))
    query_result = list(cur.fetchall())
    cur.close()

    return query_result[0][0]
