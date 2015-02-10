from flask_wtf import Form
from wtforms import StringField

class MyForm(Form):
    emit_name = StringField('emit_name')
    emit_broadcast = StringField('emit_broadcast')