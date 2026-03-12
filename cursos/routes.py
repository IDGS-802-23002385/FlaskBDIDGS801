import re

from wtforms.validators import email

from models import Alumnos, Curso, Maestros, db
from flask import Flask, render_template
from flask import request
from flask import redirect, url_for
import forms
from . import cursos_bp

from flask import flash

@cursos_bp.route("/cursos",methods=['GET','POST'])
def maestros():
    create_form=forms.maestroForm(request.form)
    curso= Curso.query.all()
    return render_template("cursosIndex.html", form=create_form,curso=curso)

@cursos_bp.route("/curso/agregar",methods=['GET','POST'])
def registrar():
    create_form=forms.cursoForm(request.form)
    mae= Maestros.query.all()
    if request.method=="POST":
        # Verificar si se seleccionó un maestro
        maestro_id = request.form.get("maestro_id")
        if not maestro_id:
            flash('Debes seleccionar un maestro para el curso', 'error')
            return render_template("cursosAgregar.html",form=create_form,mae=mae)
            
        curso=Curso(nombre=create_form.nombre.data,
			   descripcion=create_form.descripcion.data,
               maestro_id=maestro_id
               )
        db.session.add(curso)
        db.session.commit()
        return redirect("/cursos")
    return render_template("cursosAgregar.html",form=create_form,mae=mae)

@cursos_bp.route("/cursos/eliminar", methods=['GET','POST'])
def eliminar():
	create_form=forms.cursoForm(request.form)
	nombre=""
	descripcion=""
	id=0
	maestro=""
	if request.method=="GET":
		id=request.args.get('id')
		curso1=db.session.query(Curso).filter(Curso.id==id).first()
		nombre=curso1.nombre
		descripcion=curso1.descripcion
		create_form.nombre.data = nombre
		create_form.descripcion.data = descripcion
		create_form.id_maestro.data = curso1.maestro_id
		maestro=db.session.query(Maestros).filter(Maestros.id==curso1.maestro_id).first()
	if request.method=="POST":
		id= request.form.get('id')
		curso1=Curso.query.get(id)
		curso1.id=id
		db.session.delete(curso1)
		db.session.commit()
		return redirect("/cursos")
	return render_template("cursosEliminar.html",form=create_form,id=id,maestro=maestro,mae= Maestros.query.all())

@cursos_bp.route("/cursos/modificar", methods=['GET','POST'])
def modificar():
	create_form=forms.cursoForm(request.form)
	nombre=""
	descripcion=""
	id=0
	maestro=""
	if request.method=="GET":
		id=request.args.get('id')
		curso1=db.session.query(Curso).filter(Curso.id==id).first()
		nombre=curso1.nombre
		descripcion=curso1.descripcion
		create_form.nombre.data = nombre
		create_form.descripcion.data = descripcion
		create_form.id_maestro.data = curso1.maestro_id
		maestro=db.session.query(Maestros).filter(Maestros.id==curso1.maestro_id).first()
	if request.method=="POST":
		id= request.form.get('id')
		# Verificar si se seleccionó un maestro
		maestro_id = request.form.get("maestro_id")
		if not maestro_id:
			flash('Debes seleccionar un maestro para el curso', 'error')
			return redirect(f"/cursos/modificar?id={id}")
			
		curso1=db.session.query(Curso).filter(Curso.id==id).first()
		curso1.id=id
		curso1.nombre=str.rstrip(create_form.nombre.data)
		curso1.descripcion=str.rstrip(create_form.descripcion.data)
		curso1.id_maestro=maestro_id
		db.session.add(curso1)
		db.session.commit()
		return redirect("/cursos")
	return render_template("cursosModificar.html",form=create_form,id=id,maestro=maestro,mae= Maestros.query.all())

@cursos_bp.route("/cursos/detalles", methods=["GET","POST"])
def detalles():
	create_form=forms.cursoForm(request.form)
	id=0
	nombre=""
	descripcion=""
	maestro=""
	alum=""
	if request.method=="GET":
		id=request.args.get('id')
		curso1=db.session.query(Curso).filter(Curso.id==id).first()
		alum=curso1.alumnos
		nombre=curso1.nombre
		descripcion=curso1.descripcion
		maestro=curso1.maestro
	return render_template("cursosDetalles.html",nombre=nombre,descripcion=descripcion,maestro=maestro,all=alum,id=id)

@cursos_bp.route("/cursos/inscripcion", methods=["GET","POST"])
def inscripcion():
    create_form = forms.cursoForm(request.form)
    nombre = ""
    descripcion = ""
    maestro = ""
    alu = []
    id = request.args.get('id')
    if request.method == "GET":
        curso1 = db.session.query(Curso).filter(Curso.id == id).first()
        if curso1:
            nombre = curso1.nombre
            descripcion = curso1.descripcion
            maestro = curso1.maestro
            create_form.nombre.data = nombre
            create_form.descripcion.data = descripcion
            alu = Alumnos.query.all()
        else:
            flash('Curso no encontrado', 'error')
            return redirect("/cursos")
    if request.method == "POST":
        alumno_id = request.form.get("alumno_id")
        if not alumno_id:
            flash('Debes seleccionar un alumno para inscribir', 'warning')
            return redirect(f"/cursos/inscripcion?id={id}")
        curso1 = db.session.query(Curso).filter(Curso.id == id).first()
        alumno1 = db.session.query(Alumnos).filter(Alumnos.id == alumno_id).first()
        if alumno1 in curso1.alumnos:
            flash(f'El alumno {alumno1.nombre} {alumno1.apellidos} ya está inscrito en este curso.', 'info')
            return redirect(f"/cursos/inscripcion?id={id}")
        curso1.alumnos.append(alumno1)
        db.session.commit()
        return redirect("/cursos")
    return render_template("inscripcion.html", form=create_form, maestro=maestro, alu=alu, id=id)

@cursos_bp.route('/cursos/expulsar')
def expulsar():
    id_curso = request.args.get('id')
    id_alumno = request.args.get('id_alumno')
    if not id_curso or not id_alumno:
        flash("Faltan parámetros para procesar la expulsión.", "error")
        return redirect("/cursos")
    curso = Curso.query.get(id_curso)
    alumno = Alumnos.query.get(id_alumno)
    curso.alumnos.remove(alumno)
    db.session.commit()
    return redirect("/cursos")