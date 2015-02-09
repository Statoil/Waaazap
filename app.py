from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import gevent
from flask.ext.socketio import SocketIO, emit
import pygal
from flask_wtf import Form
from wtforms import StringField
import os
import random
import logging
from flask.ext.restful import Resource, Api
from sets import Set
import redis
from backend import HappyBackend

approved_statuses = Set(["happy", "good", "flat", "sad"])
devices = {
    "test1": {
        "happy": 0,
        "good": 0,
        "flat": 0,
        "sad": 0
    }
}


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app

app = create_app()
app.config['SECRET_KEY'] = 'secret123'
app.debug = 'DEBUG' in os.environ
app.debug = True

api = Api(app)
socketio = SocketIO(app)

REDIS_URL = os.environ['REDISCLOUD_URL']
REDIS_CHAN = 'happymeter'

redis = redis.from_url(REDIS_URL)

"""
POST: /happymeter/test1
{'signal': 'sad',
'timestamp': '<timestamp>'
}
"""

happies = HappyBackend(redis, REDIS_CHAN)
happies.start()

class HappyMeter(Resource):
    def get(self):
        return {
            'devices': devices.keys()
        }

    def get(self, device_id):
        print("Getting data for device id: {}".format(device_id))
        if not devices.has_key(device_id):
            return {
                'status': 'error',
                'msg': "No device with id: {}".format(device_id)
            }
        return devices.get(device_id)

    def post(self, device_id):
        print("Posting new data for device id: {}".format(device_id))
        json_data = request.get_json()
        print("debug: {}".format(json_data))
        data = json_data.get("data")
        if not data:
            return {'status': 'error', 'msg': 'Badly shaped body'}, 400

        if not data.get('signal'):
            return {'status': 'error', 'msg': 'Bad input signal'}, 400
        elif not data.get('timestamp'):
            return {'status': 'error', 'msg': 'Bad input timestamp'}, 400

        device_data = redis.get(device_id)
        # device = devices.get(device_id)
        print("First Redis get: device_data -> {}".format(device_data))

        if not device_data:
            print("Could not find device_data, constructing the basics")
            device_data = {
                "happy": 0,
                "good": 0,
                "flat": 0,
                "sad": 0
            }
            # redis.set(device_id, device_body)
            # return {'status': 'error', 'msg': 'No device found'}, 400

        # Update the data
        print("device_data: {}".format(device_data))
        device_data[data.get('signal')] += 1
        redis.set(device_id, {device_id: device_data})
        redis.publish(REDIS_CHAN, {device_id: device_data})

        return {
            'status': 'ok',
            'msg': 'Updated signal',
            'signal': data.get('signal'),
            'value': device_data.get(data.get('signal'))
        }


class MyForm(Form):
    emit_name = StringField('emit_name')
    emit_broadcast = StringField('emit_broadcast')

api.add_resource(HappyMeter, '/happymeter/<string:device_id>')


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/testws')
def testws():
    return render_template('testws.html', form=MyForm())


@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']})


@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)


@socketio.on('happymeter', namespace='/test')
def ws_happymeter():
    emit('happymeter', {'data': message})


@socketio.on('random_nr', namespace='/test')
def gen_random_nr():
    print("Generating an infinite random int loop")
    while True:
        rand_int = random.randint(0, 1000000)
        emit(
            'crap_data',
            {'data': rand_int},
            namespace='/test')
        gevent.sleep(1)


@socketio.on('connect', namespace='/test')
def test_connect():
    print("Client connected: {}".format(request.namespace))
    happies.register(request.namespace)
    emit('connected')


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    happies.unregister(request.namespace)
    print("Client disconnected")


@app.route('/line_chart')
def line_chart():
    line_chart = pygal.StackedLine(
        fill=True,
        interpolate='cubic',
        style=pygal.style.LightColorizedStyle)
    line_chart.title = 'Browser usage evolution (in %)'
    line_chart.x_labels = map(str, range(2002, 2013))
    line_chart.add(
        'Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add(
        'Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
    line_chart.add(
        'IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add(
        'Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
    chart = line_chart.render(is_unicode=True)
    return render_template('chart.html', chart=chart)


if __name__ == "__main__":
    socketio.run(app, debug=True)
