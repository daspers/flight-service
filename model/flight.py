import datetime


class FlightModel:
    def __init__(self, *args):
        labels = ['flight_id', 'departure_date', 'arrival_date', 'price', 'remaining_seat',
            'origin_code', 'origin_airport', 'destination_code', 'destination_airport']

        self.data = {}
        for i in range(len(args)):
            self.data[labels[i]] = args[i]

    def get_data(self):
        return self.data


flight_query = "SELECT `flight_id`, `departure_date`, `arrival_date`, `price`, `remaining_seat`, `orig`.`code`, `orig`.`name`, `dest`.`code`, `dest`.`name`  \
    FROM `flight` \
        INNER JOIN `airport` AS `orig` ON `flight`.`origin_airport` = `orig`.`code` \
            INNER JOIN `airport` AS `dest` ON `flight`.`destination_airport` = `dest`.`code`"


flight_update_query = 'UPDATE `flight` SET {} WHERE {}'


def generate_search_query(params):
    query = flight_query
    initial_date_format = '%d-%m-%Y'
    mysql_date_format = '%Y%m%d'

    param_applied = False
    if 'origin_city' in params:
        if param_applied:
            query += ' AND '
        else:
            query += ' WHERE '
            param_applied = True
        val = params['origin_city'].lower()
        query += 'LOWER(`orig`.`location`) LIKE "%'+val+'%"'
    if 'destination_city' in params:
        if param_applied:
            query += ' AND '
        else:
            query += ' WHERE '
            param_applied = True
        val = params['destination_city'].lower()
        query += 'LOWER(`dest`.`location`) LIKE "%'+val+'%"'
    if 'start_date' in params:
        if param_applied:
            query += ' AND '
        else:
            query += ' WHERE '
            param_applied = True
        val = datetime.datetime.strptime(params['start_date'], initial_date_format).strftime(mysql_date_format)
        query += 'DATE(`departure_date`)>='+val
    if 'end_date' in params:
        if param_applied:
            query += ' AND '
        else:
            query += ' WHERE '
            param_applied = True
        val = datetime.datetime.strptime(params['end_date'], initial_date_format).strftime(mysql_date_format)
        query += 'DATE(`departure_date`)<='+val
    return query


def generate_search_by_id_query(flight_id):
    query = flight_query + ' WHERE `flight_id`="{}"'.format(flight_id)
    return query

def generate_update_diff_query_by_id(update_param, flight_id):
    update_string = ''
    separator = False
    for key, val in update_param.items():
        if separator:
            update_string += ', '
        if val >= 0:
            update_string += "`{}`=`{}`+{}".format(key, key, val)
        else:
            update_string += "`{}`=`{}`-{}".format(key, key, -val)
        separator = True

    query = flight_update_query.format(update_string, '`flight_id`="{}"'.format(flight_id))
    return query