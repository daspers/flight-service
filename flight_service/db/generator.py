import pandas as pd
import random
import string

def randomStringDigits(stringLength=8):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_uppercase + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

df = pd.read_csv('airport.csv')
n = len(df)
for i in range(10):
    for j in range(12):
        x = random.randint(0, n-1)
        y = random.randint(0, n-1)
        while y == x:
            y = random.randint(0, n-1)

        print('INSERT INTO `flight` (`flight_id`,`origin_airport`, `destination_airport`, `departure_date`, `arrival_date`, `price`, `remaining_seat`) VALUES (', 
        '"' + randomStringDigits() + '",',
        '"' + df['code'][x] + '",',
        '"' + df['code'][y] + '",',
        'DATE_ADD(NOW(), interval ', i*1440+480,' minute),',
        'DATE_ADD(NOW(), interval ',i*1440+480+random.randint(30, 240),' minute),',
        random.randint(1000, 1000000),',',
        random.randint(1, 200),');',
        sep='')