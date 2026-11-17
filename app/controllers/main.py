from flask import Blueprint, render_template
from flask_login import current_user

from app.models import Emprestimo, Livro

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    total_livros = Livro.query.count()
    destaques = Livro.query.order_by(Livro.id.desc()).limit(6).all()
    meus_ativos = []
    if current_user.is_authenticated:
        meus_ativos = current_user.emprestimos_ativos().order_by(Emprestimo.data_prevista).all()
    return render_template("index.html", total_livros=total_livros,
                           destaques=destaques, meus_ativos=meus_ativos)
