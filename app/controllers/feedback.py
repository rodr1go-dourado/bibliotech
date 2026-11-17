from datetime import date

from flask import Blueprint, Response, abort, flash, redirect, render_template, request, url_for

from app import db
from app.controllers import admin_required
from app.models import Feedback

bp = Blueprint("feedback", __name__, url_prefix="/feedback")

TIPOS_PERMITIDOS = {"image/png", "image/jpeg", "image/gif", "image/webp"}
STATUS_VALIDOS = ("Aberto", "Corrigido", "Descartado")


@bp.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        f = request.form
        nome = f.get("nome_testador", "").strip()
        if not nome:
            flash("Informe seu nome.", "erro")
            return render_template("feedback/form.html", dados=f), 400
        if not any(f.get(c, "").strip() for c in ("funcionou", "nao_funcionou", "nao_testado", "sugestoes")):
            flash("Preencha pelo menos um dos campos de avaliação.", "erro")
            return render_template("feedback/form.html", dados=f), 400

        try:
            data_teste = date.fromisoformat(f.get("data_teste")) if f.get("data_teste") else date.today()
        except ValueError:
            data_teste = date.today()

        fb = Feedback(nome_testador=nome, data_teste=data_teste,
                      funcionou=f.get("funcionou", "").strip(),
                      nao_funcionou=f.get("nao_funcionou", "").strip(),
                      nao_testado=f.get("nao_testado", "").strip(),
                      sugestoes=f.get("sugestoes", "").strip())

        arquivo = request.files.get("print_tela")
        if arquivo and arquivo.filename:
            if arquivo.mimetype not in TIPOS_PERMITIDOS:
                flash("O print deve ser uma imagem (PNG, JPG, GIF ou WEBP).", "erro")
                return render_template("feedback/form.html", dados=f), 400
            fb.print_tela = arquivo.read()
            fb.print_mimetype = arquivo.mimetype

        db.session.add(fb)
        db.session.commit()
        flash("Obrigado! Seu relatório de teste foi enviado.", "sucesso")
        return redirect(url_for("main.index"))
    return render_template("feedback/form.html", dados={"data_teste": date.today().isoformat()})


@bp.route("/")
@admin_required
def listar():
    feedbacks = Feedback.query.order_by(Feedback.criado_em.desc()).all()
    return render_template("feedback/lista.html", feedbacks=feedbacks, status_validos=STATUS_VALIDOS)


@bp.route("/<int:fb_id>/print")
@admin_required
def print_tela(fb_id):
    fb = db.session.get(Feedback, fb_id) or abort(404)
    if not fb.print_tela:
        abort(404)
    return Response(fb.print_tela, mimetype=fb.print_mimetype)


@bp.route("/<int:fb_id>/status", methods=["POST"])
@admin_required
def alterar_status(fb_id):
    fb = db.session.get(Feedback, fb_id) or abort(404)
    status = request.form.get("status")
    if status not in STATUS_VALIDOS:
        abort(400)
    fb.status = status
    db.session.commit()
    flash("Status atualizado.", "sucesso")
    return redirect(url_for("feedback.listar"))
