from flask import Flask
import json
app = Flask(__name__)

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'root'
# app.config['MYSQL_DB'] = 'MyDB'

@app.route('/', methods=['GET'])
def index():
    res = {
        'a' : 1,
        'b' : 2,
    }
    return json.dumps(res)

if __name__ == "__main__":
    app.run()