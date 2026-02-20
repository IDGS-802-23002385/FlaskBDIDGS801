from wtforms import Form
from wtforms import StringField, IntegerField,PasswordField, RadioField
from wtforms import EmailField
from wtforms import validators

class UserForm2(Form):
    matricula=IntegerField('id',[validators.data_required(message="el campo es requerido"),
                                        validators.number_range(min=1,max=1000,message="el campo es requerido")])
    nombre=StringField('nombre',[validators.data_required(message="el campo es requerido"), 
                                 validators.length(min=3,max=10,message="el campo es requerido")])
    apaterno=StringField('apaterno',[validators.data_required(message="el campo es requerido"),validators.length(min=3,max=10,message="el campo es requerido")])
    correo=EmailField('correo',[validators.data_required(message="el campo es requerido"),validators.length(min=3,max=30,message="el campo es requerido")])
    
