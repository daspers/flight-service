create_passenger_query = 'INSERT INTO `passenger` (`name`, `identification`, `booking_id`) VALUES ("{}", "{}", "{}")'
passenger_count_query = 'SELECT COUNT(*) FROM `passenger` WHERE `booking_id`="{}"'
delete_passenger_query = 'DELETE FROM `passenger` WHERE'


def generate_add_passenger_query(passenger, booking_id):
    return create_passenger_query.format(passenger['name'], passenger['identification'], booking_id)


def generate_passenger_count_query(booking_id):
    return passenger_count_query.format(booking_id)


def generate_delete_passenger_query(params):
    param_applied = False
    query_condition = ''
    for key, val in params.items():
        if param_applied:
            query_condition += ' AND '
        param_applied = True
        query_condition += '`{}`="{}"'.format(key,val)
    query = delete_passenger_query + query_condition
    print(query)
    return query
