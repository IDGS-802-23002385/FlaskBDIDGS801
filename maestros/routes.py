from models import Maestros, db
from flask import Flask, render_template
from flask import request
from flask import redirect, url_for
import forms
from . import maestros_bp

@maestros_bp.route("/maestros",methods=['GET','POST'])
def maestros():
    create_form=forms.maestroForm(request.form)
    maestro= Maestros.query.all()
    return render_template("maestrosIndex.html", form=create_form,maestro=maestro)

@maestros_bp.route("/maestros/agregar",methods=['GET','POST'])
def registrar():
    create_form=forms.maestroForm(request.form)
    if request.method=="POST":
        maest=Maestros(nombre=create_form.nombre.data,
			   apellidos=create_form.apellidos.data,
               especialidad=create_form.especialidad.data,
			   email=create_form.email.data,
               )
        db.session.add(maest)
        db.session.commit()
        return redirect(url_for("maestros.maestros"))
    return render_template("maestrosAgregar.html",form=create_form)


@maestros_bp.route("/maestros/eliminar", methods=['GET','POST'])
def eliminar():
	create_form=forms.maestroForm(request.form)
	nombre=""
	apellidos=""
	email=""
	id=0
	especialidad=""
	if request.method=="GET":
		id=request.args.get('id')
		maest1=db.session.query(Maestros).filter(Maestros.id==id).first()
		nombre=maest1.nombre
		apellidos=maest1.apellidos
		email=maest1.email
		especialidad=maest1.especialidad
		create_form.nombre.data = nombre
		create_form.apellidos.data = apellidos
		create_form.email.data = email
		create_form.especialidad.data = especialidad
	if request.method=="POST":
		id= request.form.get('id')
		maest1=Maestros.query.get(id)
		maest1.id=id
		db.session.delete(maest1)
		db.session.commit()
		return redirect(url_for("maestros.maestros"))
	return render_template("maestrosEliminar.html",form=create_form,id=id)

@maestros_bp.route("/maestros/modificar", methods=['GET','POST'])
def modificar():
	create_form=forms.maestroForm(request.form)
	nombre=""
	apellidos=""
	email=""
	especialidad=""
	id=0
	if request.method=="GET":
		id=request.args.get('id')
		maestr1=db.session.query(Maestros).filter(Maestros.id==id).first()
		nombre=maestr1.nombre
		apellidos=maestr1.apellidos
		email=maestr1.email
		especialidad=maestr1.especialidad
		create_form.nombre.data = nombre
		create_form.apellidos.data = apellidos
		create_form.email.data = email
		create_form.especialidad.data = especialidad
	if request.method=="POST":
		id= request.form.get('id')
		maestr1=db.session.query(Maestros).filter(Maestros.id==id).first()
		maestr1.id=id
		maestr1.nombre=str.rstrip(create_form.nombre.data)
		maestr1.apellidos=str.rstrip(create_form.apellidos.data)
		maestr1.email=str.rstrip(create_form.email.data)
		maestr1.especialidad=str.rstrip(create_form.especialidad.data)
		db.session.add(maestr1)
		db.session.commit()
		return redirect(url_for("maestros.maestros"))
	return render_template("maestrosModificar.html",form=create_form,id=id)

@maestros_bp.route("/maestro/detalles", methods=["GET","POST"])
def detalles():
	create_form=forms.maestroForm(request.form)
	nombre=""
	apellidos=""
	email=""
	especialidad=""
	if request.method=="GET":
		id=request.args.get('id')
		maestro=db.session.query(Maestros).filter(Maestros.id==id).first()
		nombre=maestro.nombre
		apellidos=maestro.apellidos
		email=maestro.email
		especialidad=maestro.especialidad
	return render_template("maestroDetalles.html",nombre=nombre,apellidos=apellidos,email=email,especialidad=especialidad)
