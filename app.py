import re
from wtforms.validators import email
from flask import Flask, render_template
from flask import request
from flask import flash
from flask import redirect, url_for
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
from maestros import maestros_bp
from cursos import cursos_bp
from flask_migrate import Migrate

from models import db
from models import Alumnos
import forms

app = Flask(__name__)
app.config.from_object(	DevelopmentConfig)
app.register_blueprint(maestros_bp)
app.register_blueprint(cursos_bp)
db.init_app(app)
csrf=CSRFProtect()
migrate=Migrate(app,db)

@app.errorhandler(404)
def notFound(e):
	return render_template("404.html"),404

@app.route("/", methods=['GET','POST'])
@app.route("/index")
def index():
	create_form=forms.UserForm2(request.form)
	#tem=Alumnos.query('select * from alumnos')
	alumno= Alumnos.query.all()
	return render_template("index.html", form=create_form,alumno=alumno)

@app.route("/alumnos")
def alumnosLista():
	create_form=forms.UserForm2(request.form)
	#tem=Alumnos.query('select * from alumnos')
	alumno= Alumnos.query.all()
	return render_template("alumnosIndex.html", form=create_form,alumno=alumno)

@app.route("/alumnos/agregar", methods=['GET','POST'])
def alumnos():
	create_form=forms.UserForm2(request.form)
	if request.method=="POST":
		alum=Alumnos(nombre=create_form.nombre.data,
			   apellidos=create_form.apellidos.data,
			   email=create_form.correo.data,
			   telefono=create_form.telefono.data)
		db.session.add(alum)
		db.session.commit()
		return redirect("alumnos")
	return render_template("alumnos.html",form=create_form)

@app.route("/modificar", methods=['GET','POST'])
def modificar():
	create_form=forms.UserForm2(request.form)
	nombre=""
	apellidos=""
	email=""
	telefono=""
	id=0
	if request.method=="GET":
		id=request.args.get('id')
		alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
		nombre=alum1.nombre
		apellidos=alum1.apellidos
		email=alum1.email
		telefono=alum1.telefono
		create_form.nombre.data = nombre
		create_form.apellidos.data = apellidos
		create_form.correo.data = email
		create_form.telefono.data = telefono
	if request.method=="POST":
		id= request.form.get('id')
		alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
		alum1.id=id
		alum1.nombre=str.rstrip(create_form.nombre.data)
		alum1.apellidos=str.rstrip(create_form.apellidos.data)
		alum1.email=str.rstrip(create_form.correo.data)
		alum1.telefono=str.rstrip(create_form.telefono.data)
		db.session.add(alum1)
		db.session.commit()
		return redirect("alumnos")
	return render_template("modificar.html",form=create_form,id=id)

@app.route("/eliminar", methods=['GET','POST'])
def eliminar():
	create_form=forms.UserForm2(request.form)
	nombre=""
	apellidos=""
	email=""
	id=0
	telefono=""
	if request.method=="GET":
		id=request.args.get('id')
		alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
		nombre=alum1.nombre
		apellidos=alum1.apellidos
		email=alum1.email
		telefono=alum1.telefono
		create_form.nombre.data = nombre
		create_form.apellidos.data = apellidos
		create_form.correo.data = email
		create_form.telefono.data = telefono
	if request.method=="POST":
		id= request.form.get('id')
		alum1=Alumnos.query.get(id)
		alum1.id=id
		db.session.delete(alum1)
		db.session.commit()
		return redirect("alumnos")
	return render_template("eliminar.html",form=create_form,id=id)

@app.route("/detalles", methods=["GET","POST"])
def detalles():
	create_form=forms.UserForm2(request.form)
	nombre=""
	apellidos=""
	email=""
	telefono=""
	cursos=""
	if request.method=="GET":
		id=request.args.get('id')
		alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
		nombre=alum1.nombre
		apellidos=alum1.apellidos
		email=alum1.email
		telefono=alum1.telefono
		cursos=alum1.cursos
	return render_template("detalles.html",nombre=nombre,apellidos=apellidos,email=email,telefono=telefono,cursos=cursos)

if __name__ == '__main__':
	csrf.init_app(app)
	with app.app_context():
		db.create_all()
	app.run()
