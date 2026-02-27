from flask import Blueprint

maestros_bp  = Blueprint('maestros',__name__,
                         template_folder="maestros_templates")
from . import routes