from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from sqlalchemy import or_

from app import db
from app.controllers import admin_required
from app.models import Livro

bp = Blueprint("livros", __name__, url_prefix="/livros")


def _int_ou_none(valor):
    try:
        return int(valor) if valor not in (None, "") else None
    except ValueError:
        return -1  # força erro de validação


@bp.route("/")
def listar():
    busca = request.args.get("q", "").strip()
    categoria = request.args.get("categoria", "").strip()
    consulta = Livro.query
    if busca:
        termo = f"%{busca}%"
        consulta = consulta.filter(or_(Livro.titulo.ilike(termo), Livro.autor.ilike(termo)))
    if categoria:
        consulta = consulta.filter_by(categoria=categoria)
    livros = consulta.order_by(Livro.titulo).all()
    categorias = [c[0] for c in db.session.query(Livro.categoria).distinct().order_by(Livro.categoria)]
    return render_template("livros/lista.html", livros=livros, busca=busca,
                           categoria=categoria, categorias=categorias)


@bp.route("/<int:livro_id>")
def detalhe(livro_id):
    livro = db.session.get(Livro, livro_id) or abort(404)
    return render_template("livros/detalhe.html", livro=livro)


@bp.route("/novo", methods=["GET", "POST"])
@admin_required
def novo():
    if request.method == "POST":
        return _salvar(Livro())
    return render_template("livros/form.html", livro=None)


@bp.route("/<int:livro_id>/editar", methods=["GET", "POST"])
@admin_required
def editar(livro_id):
    livro = db.session.get(Livro, livro_id) or abort(404)
    if request.method == "POST":
        return _salvar(livro)
    return render_template("livros/form.html", livro=livro)


def _salvar(livro):
    f = request.form
    titulo, autor = f.get("titulo", "").strip(), f.get("autor", "").strip()
    isbn = f.get("isbn", "").strip().replace("-", "") or None
    ano, quantidade = _int_ou_none(f.get("ano")), _int_ou_none(f.get("quantidade_total"))
    categoria = f.get("categoria", "").strip() or "Geral"

    erros = Livro.validar_dados(titulo, autor, isbn, ano, quantidade)
    if isbn:
        existente = Livro.query.filter_by(isbn=isbn).first()
        if existente and existente.id != livro.id:
            erros.append("Já existe um livro com este ISBN.")
    emprestados = (livro.quantidade_total - livro.quantidade_disponivel) if livro.id else 0
    if quantidade and quantidade < emprestados:
        erros.append(f"Há {emprestados} exemplar(es) emprestado(s); a quantidade não pode ser menor.")

    if erros:
        for erro in erros:
            flash(erro, "erro")
        return render_template("livros/form.html", livro=livro if livro.id else None, dados=f), 400

    livro.titulo, livro.autor, livro.isbn, livro.ano, livro.categoria = titulo, autor, isbn, ano, categoria
    livro.quantidade_total = quantidade
    livro.quantidade_disponivel = quantidade - emprestados
    if not livro.id:
        db.session.add(livro)
    db.session.commit()
    flash("Livro salvo com sucesso.", "sucesso")
    return redirect(url_for("livros.detalhe", livro_id=livro.id))


@bp.route("/<int:livro_id>/excluir", methods=["POST"])
@admin_required
def excluir(livro_id):
    livro = db.session.get(Livro, livro_id) or abort(404)
    if livro.emprestimos.count() > 0:
        flash("Não é possível excluir: o livro possui histórico de empréstimos.", "erro")
        return redirect(url_for("livros.detalhe", livro_id=livro.id))
    db.session.delete(livro)
    db.session.commit()
    flash("Livro excluído.", "sucesso")
    return redirect(url_for("livros.listar"))
