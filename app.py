from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import gevent
from flask.ext.socketio import SocketIO, emit
import pygal
from flask_wtf import Form
from wtforms import StringField
import random


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app

app = create_app()
app.config['SECRET_KEY'] = 'secret123'
#app.debug = True
socketio = SocketIO(app)

class MyForm(Form):
    emit_name = StringField('emit_name')
    emit_broadcast = StringField('emit_broadcast')


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


@socketio.on('random_nr', namespace='/test')
def gen_random_nr():
    while True:
        emit(
            'crap_data',
            {'data': random.randint(0, 1000000)},
            namespace='/test')
        gevent.sleep(1)


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('connected')


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
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
    socketio.run(app)
