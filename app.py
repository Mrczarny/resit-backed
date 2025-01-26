from flask import Flask
from dataModel import db, Data

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
    db.session.add(Data(timestamp='2020-01-01 00:00:00', temperature=25.0, humidity=50.0))
    db.session.commit()
    return 'Data added'


if __name__ == '__main__':
    app.run()
