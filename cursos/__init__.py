from flask import Blueprint

cursos_bp  = Blueprint('cursos',__name__,
                         template_folder="cursos_templates")
from . import routes