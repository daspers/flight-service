import string, random


create_booking_query = 'INSERT INTO `booking` (`booking_id`, `flight_id`) VALUES ("{}", "{}")'
get_booking_query = 'SELECT `booking_id`, `flight_id` FROM `booking`'
delete_booking_query = 'DELETE FROM `booking` WHERE '


class BookingModel:
    def __init__(self, *args):
        labels = ['booking_id', 'flight_id']

        self.data = {}
        for i in range(len(args)):
            self.data[labels[i]] = args[i]

    def get_data(self):
        return self.data

def randomStringDigits(stringLength=16):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits

    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

def generate_booking_id():
    return randomStringDigits()


def generate_add_booking_query(booking_id, flight_id):
    return create_booking_query.format(booking_id, flight_id)


def generate_get_booking_query(params):
    param_applied = False
    query_condition = ''
    for key, val in params.items():
        if param_applied:
            query_condition += ' AND '
        else:
            query_condition += ' WHERE '
            param_applied = True
        query_condition += '{}="{}"'.format(str(key), val)
    query = get_booking_query + query_condition
    print(query)
    return query


def generate_delete_booking_query(params):
    param_applied = False
    query_condition = ''
    for key, val in params.items():
        if param_applied:
            query_condition += ' AND '
        param_applied = True
        query_condition += '{}="{}"'.format(str(key), val)
    query = delete_booking_query + query_condition
    print(query)
    return query
