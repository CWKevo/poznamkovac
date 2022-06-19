from flask import Blueprint, render_template


HLAVNY_BLUEPRINT = Blueprint('main', __name__)



@HLAVNY_BLUEPRINT.route('/')
def index():
    return render_template('hlavny.html')
