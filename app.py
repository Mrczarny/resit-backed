from flask import Flask, make_response, request
from flask_socketio import emit, SocketIO
from flask_cors import CORS
from sqlalchemy import func
from dataModel import db, Data
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app, origins=['http://localhost:8100'])
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/data/latest', methods=['GET']) 
def get_data():
    data = Data.query.first()
    if data is None:
        return make_response('No data found', 404)
    return {'temperature': data.temperature, 'humidity': data.humidity, 'timestamp': data.timestamp}

@app.route('/data/graph', methods=['GET'])
def get_graph_data():
    request_data = request.args
    point_count = request_data.get('point_count')
    start_time = request_data.get('start_time')
    end_time = request_data.get('end_time')
    
    if point_count is None or start_time is None or end_time is None:
        return make_response('Invalid request', 400)
    
    try:
        point_count = int(point_count)
        start_time = datetime.fromisoformat(start_time)
        end_time = datetime.fromisoformat(end_time)
    except:
        return make_response('Invalid request', 400)
    
    data = Data.query.filter(Data.timestamp >= start_time, Data.timestamp <= end_time).all()
    if len(data) == 0:
        return make_response('No data found', 404)
    resp_data = [data[0]]
    resp_data.extend([data[i *(len(data)//(point_count - 1))] for i in range(1, point_count - 1)])
    resp_data.append(data[-1])
    data = [{'temperature': d.temperature, 'humidity': d.humidity, 'timestamp': d.timestamp} for d in resp_data]
    return {'data': data}

@app.route('/data/graph/week', methods=['GET'])
def get_average_week_data():
    data = []
    day_of_week = datetime.now().weekday()
    for i in range(7):
        day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days= day_of_week - i)
        next_day = day + timedelta(days=1)
        day_data = db.session.query(
            func.avg(Data.temperature).label('avg_temperature'),
            func.avg(Data.humidity).label('avg_humidity')
        ).filter(Data.timestamp >= day, Data.timestamp < next_day).first()
        if day_data.avg_temperature is None or day_data.avg_humidity is None:
            continue
        data.append({
            'temperature': day_data.avg_temperature,
            'humidity': day_data.avg_humidity,
            'timestamp': day.strftime("%m/%d/%Y")
        })
    return data
    

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('connected', {'data': 'Connected'})
    return 'Connected'
    



@app.route('/data', methods=['POST'])
def add_data():
    json = request.json
    new_data = Data(timestamp=datetime.now(), temperature=json['temperature'], humidity=json['humidity'])
    emit('new_data', {'temperature': new_data.temperature, 'humidity': new_data.humidity, 'timestamp': new_data.timestamp.strftime("%m/%d/%Y, %H:%M:%S")}, broadcast=True, namespace='/')
    print(new_data)
    db.session.add(new_data)
    db.session.commit()
    return 'Data added'


if __name__ == '__main__':
    socketio.run(app)
    
    

