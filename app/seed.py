"""Comandos de linha de comando: `flask --app run seed` popula dados de demonstração."""
import os

import click

from app import db
from app.models import Livro, Usuario

LIVROS = [
    ("Dom Casmurro", "Machado de Assis", "9788594318602", 1899, "Literatura Brasileira", 3),
    ("O Cortiço", "Aluísio Azevedo", "9788594318633", 1890, "Literatura Brasileira", 2),
    ("Vidas Secas", "Graciliano Ramos", "9788501114051", 1938, "Literatura Brasileira", 2),
    ("A Hora da Estrela", "Clarice Lispector", "9788532508126", 1977, "Literatura Brasileira", 1),
    ("Código Limpo", "Robert C. Martin", "9788576082675", 2008, "Tecnologia", 2),
    ("O Programador Pragmático", "Andrew Hunt e David Thomas", "9788577807000", 1999, "Tecnologia", 1),
    ("Engenharia de Software", "Ian Sommerville", "9788543024974", 2018, "Tecnologia", 2),
    ("Sapiens", "Yuval Noah Harari", "9788525432186", 2011, "História", 2),
    ("O Pequeno Príncipe", "Antoine de Saint-Exupéry", "9788595081512", 1943, "Infantojuvenil", 3),
    ("1984", "George Orwell", "9788535914849", 1949, "Ficção", 2),
]


def popular():
    if not Usuario.query.filter_by(email="admin@bibliotech.com").first():
        admin = Usuario(nome="Administrador", email="admin@bibliotech.com", perfil="admin")
        admin.definir_senha(os.environ.get("ADMIN_PASSWORD", "admin123"))
        db.session.add(admin)
    if not Usuario.query.filter_by(email="leitor@bibliotech.com").first():
        leitor = Usuario(nome="Leitor Demo", email="leitor@bibliotech.com")
        leitor.definir_senha("leitor123")
        db.session.add(leitor)
    if Livro.query.count() == 0:
        for titulo, autor, isbn, ano, cat, qtd in LIVROS:
            db.session.add(Livro(titulo=titulo, autor=autor, isbn=isbn, ano=ano, categoria=cat,
                                 quantidade_total=qtd, quantidade_disponivel=qtd))
    db.session.commit()


def register_commands(app):
    @app.cli.command("seed")
    def seed():
        """Cria usuários e livros de demonstração."""
        popular()
        click.echo("Dados de demonstração criados.")
