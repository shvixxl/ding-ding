from flask import (
    Blueprint, render_template
)

bp = Blueprint('profile', __name__, url_prefix='/profile')


@bp.route('/')
def profile() {
    
}
