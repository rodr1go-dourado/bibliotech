import re

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from app import db
from app.models import RegraNegocioError, Usuario

bp = Blueprint("auth", __name__, url_prefix="/auth")

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@bp.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        confirmacao = request.form.get("confirmacao", "")

        erros = []
        if not nome:
            erros.append("Nome é obrigatório.")
        if not EMAIL_RE.match(email):
            erros.append("E-mail inválido.")
        if senha != confirmacao:
            erros.append("As senhas não conferem.")
        if Usuario.query.filter_by(email=email).first():
            erros.append("Este e-mail já está cadastrado.")

        if not erros:
            usuario = Usuario(nome=nome, email=email)
            try:
                usuario.definir_senha(senha)
            except RegraNegocioError as e:
                erros.append(str(e))

        if erros:
            for erro in erros:
                flash(erro, "erro")
            return render_template("auth/registrar.html", nome=nome, email=email), 400

        db.session.add(usuario)
        db.session.commit()
        flash("Cadastro realizado! Faça login para continuar.", "sucesso")
        return redirect(url_for("auth.login"))

    return render_template("auth/registrar.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario is None or not usuario.verificar_senha(senha):
            flash("E-mail ou senha incorretos.", "erro")
            return render_template("auth/login.html", email=email), 401
        login_user(usuario)
        flash(f"Bem-vindo(a), {usuario.nome}!", "sucesso")
        proxima = request.args.get("next")
        if proxima and proxima.startswith("/") and not proxima.startswith("//"):
            return redirect(proxima)
        return redirect(url_for("main.index"))
    return render_template("auth/login.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu do sistema.", "sucesso")
    return redirect(url_for("main.index"))
