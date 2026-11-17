from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.controllers import admin_required
from app.models import Emprestimo, Livro, RegraNegocioError

bp = Blueprint("emprestimos", __name__, url_prefix="/emprestimos")


@bp.route("/meus")
@login_required
def meus():
    emprestimos = current_user.emprestimos.order_by(Emprestimo.data_emprestimo.desc()).all()
    return render_template("emprestimos/lista.html", emprestimos=emprestimos, titulo="Meus empréstimos")


@bp.route("/")
@admin_required
def todos():
    filtro = request.args.get("filtro", "ativos")
    consulta = Emprestimo.query
    if filtro == "ativos":
        consulta = consulta.filter(Emprestimo.data_devolucao.is_(None))
    elif filtro == "atrasados":
        from datetime import date
        consulta = consulta.filter(Emprestimo.data_devolucao.is_(None), Emprestimo.data_prevista < date.today())
    emprestimos = consulta.order_by(Emprestimo.data_prevista).all()
    return render_template("emprestimos/lista.html", emprestimos=emprestimos,
                           titulo="Gestão de empréstimos", admin=True, filtro=filtro)


@bp.route("/solicitar/<int:livro_id>", methods=["POST"])
@login_required
def solicitar(livro_id):
    livro = db.session.get(Livro, livro_id) or abort(404)
    try:
        emp = Emprestimo.realizar(current_user, livro)
        flash(f"Empréstimo realizado! Devolva até {emp.data_prevista.strftime('%d/%m/%Y')}.", "sucesso")
    except RegraNegocioError as e:
        flash(str(e), "erro")
    return redirect(url_for("livros.detalhe", livro_id=livro.id))


@bp.route("/<int:emp_id>/devolver", methods=["POST"])
@login_required
def devolver(emp_id):
    emp = db.session.get(Emprestimo, emp_id) or abort(404)
    if emp.usuario_id != current_user.id and not current_user.is_admin:
        abort(403)
    try:
        emp.devolver()
        flash(f"Devolução de \"{emp.livro.titulo}\" registrada.", "sucesso")
    except RegraNegocioError as e:
        flash(str(e), "erro")
    destino = "emprestimos.todos" if current_user.is_admin and emp.usuario_id != current_user.id else "emprestimos.meus"
    return redirect(url_for(destino))
