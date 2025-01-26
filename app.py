from flask import Flask, request
from dataModel import db, Data
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/data', methods=['POST'])
def add_data():
    json = request.json
    new_data = Data(timestamp=datetime.now(), temperature=json['temperature'], humidity=json['humidity'])
    print(new_data)
    db.session.add(new_data)
    db.session.commit()
    return 'Data added'


if __name__ == '__main__':
    app.run()
    

