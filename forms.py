from wtforms import Form
from wtforms import StringField, IntegerField,PasswordField, RadioField
from wtforms import EmailField
from wtforms import validators

class UserForm2(Form):
    matricula=IntegerField('id',[validators.data_required(message="el campo es requerido"),
                                        validators.number_range(min=1,max=1000,message="el campo es requerido")])
    nombre=StringField('nombre',[validators.data_required(message="el campo es requerido"), 
                                 validators.length(min=3,max=10,message="el campo es requerido")])
    apellidos=StringField('apellidos',[validators.data_required(message="el campo es requerido"),validators.length(min=3,max=50,message="el campo es requerido")])
    correo=EmailField('correo',[validators.data_required(message="el campo es requerido"),validators.length(min=3,max=30,message="el campo es requerido")])
    telefono=StringField('telefono',[validators.data_required(message="el campo es requerido"),validators.length(min=10,max=50,message="el campo es requerido")])

class maestroForm(Form):
    id=IntegerField('id',[validators.data_required(message="el campo es requerido"),
                                        validators.number_range(min=1,max=1000,message="el campo es requerido")])
    nombre=StringField('nombre',[validators.data_required(message="el campo es requerido"), 
                                 validators.length(min=3,max=10,message="el campo es requerido")])
    apellidos=StringField('apellidos',[validators.data_required(message="el campo es requerido"),validators.length(min=3,max=50,message="el campo es requerido")])
    especialidad=StringField('especialidad',[validators.data_required(message="el campo es requerido"),validators.length(min=3,max=20,message="el campo es requerido")])
    email=EmailField('email',[validators.data_required(message="el campo es requerido"),validators.length(min=3,max=30,message="el campo es requerido")])
    
