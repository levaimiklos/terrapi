#! /usr/bin/env python3

import sys
import datetime
import time
import os
import urllib
import json
import logging
from flask import *
from flask_socketio import SocketIO
from werkzeug.urls import url_parse
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required

from webapp import webapp
from webapp import socketio
from webapp import db
from webapp.models import User
from webapp.forms import LoginForm
# from webapp.forms import RegistrationForm

sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))
import flow as Flow
Flow = Flow.Flow()

@webapp.route("/")
@webapp.route("/index")
@login_required
def index():
    door = Flow.read_door()
    # lamp = Flow.read_lamp()
    lamp = 1
    # heater = Flow.read_heater()
    heater = 1
    # humidifier = Flow.read_humidifier()
    humidifier = 1
    # dehumidifier = Flow.read_dehumidifier()
    dehumidifier = 1
    new_temp_sp_val = Flow.new_temperature_setpoint
    new_humi_sp_val = Flow.new_humidity_setpoint
    battery_percentage = Flow.read_battery_percentage()
    battery_voltage = Flow.read_battery_voltage()

    template_data = {'door' : door,
                     'lamp' : lamp,
                     'heater' : heater,
                     'humidifier' : humidifier,
                     'dehumidifier' : dehumidifier,
                     'new_temp_sp_val' : new_temp_sp_val,
                     'new_humi_sp_val' : new_humi_sp_val,
                     'battery_percentage' : battery_percentage,
                     'battery_voltage' : battery_voltage,
                     'loading' : -1}
    return render_template('index.html', **template_data)

@webapp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@webapp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@socketio.on('change_led')
def change_led(state):
    if state == 'on':
        Flow.set_led(True)
    elif state == 'off':
        Flow.set_led(False)
    else:
        return ('Invalid LED state', 400)

@socketio.on('change_temperature_sp')
def change_temperature_sp(way):
    if way == 'increase':
        Flow.increase_temperature_setpoint(0.5)
    elif way == 'decrease':
        Flow.decrease_temperature_setpoint(0.5)
    else:
        return ('Invalid way of temperature change', 400)
    new_temp_sp_val = Flow.new_temperature_setpoint
    print('new_temp_sp_val: ', new_temp_sp_val)
    socketio.emit('new_temp_sp_val', {'new_temp_sp_val' : new_temp_sp_val})

@socketio.on('change_humidity_sp')
def change_humidity_sp(way):
    if way == 'increase':
        Flow.increase_humidity_setpoint(1)
    elif way == 'decrease':
        Flow.decrease_humidity_setpoint(1)
    else:
        return ('Invalid way of humidity change', 400)
    new_humi_sp_val = Flow.new_humidity_setpoint
    print('new_humi_sp_val: ', new_humi_sp_val)
    socketio.emit('new_humi_sp_val', {'new_humi_sp_val' : new_humi_sp_val})

#internal callback that will called when a new  temp+humi data is available.
def temp_humidity_change(temperature, humidity):
    # if temperature is not None and humidity is not None:
    socketio.emit('temp_humidity_change', {'temperature' : temperature, "humidity" : humidity})
#internal callback that will be called when the door changes state.
def door_change(door):
    socketio.emit('door_change', {'door': door})
#internal callback that will be called when the lamp changes state.
def lamp_change(lamp):
    socketio.emit('lamp_change', {'lamp' : lamp})
#internal callback that will be called when the heater changes state.
def heater_change(heater):
    socketio.emit('heater_change', {'heater' : heater})
#internal callback that will be called when the humidifier changes state.
def humidifier_change(humidifier):
    socketio.emit('humidifier_change', {'humidifier' : humidifier})
#internal callback that will be called when the humidifier changes state.
def dehumidifier_change(dehumidifier):
    socketio.emit('dehumidifier_change', {'dehumidifier' : dehumidifier})
def battery_change(battery_p, battery_v):
    socketio.emit('battery_change', {'battery_p' : battery_p, 'battery_v' : battery_v})


Flow.on_temp_humidity_change(temp_humidity_change)
Flow.on_door_change(door_change)
Flow.on_LAMP_change(lamp_change)
Flow.on_UVB_change(heater_change)
Flow.on_HEATER_change(humidifier_change)
Flow.on_RAIN_change(dehumidifier_change)
Flow.on_BATTERY_change(battery_change)
