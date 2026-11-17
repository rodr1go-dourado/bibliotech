import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db  # noqa: E402
from app.models import Livro, Usuario  # noqa: E402
from config import TestConfig  # noqa: E402


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        admin = Usuario(nome="Admin", email="admin@teste.com", perfil="admin")
        admin.definir_senha("admin123")
        leitor = Usuario(nome="Leitor", email="leitor@teste.com")
        leitor.definir_senha("leitor123")
        db.session.add_all([admin, leitor])
        db.session.add(Livro(titulo="Dom Casmurro", autor="Machado de Assis", isbn="9788594318602",
                             ano=1899, categoria="Literatura Brasileira",
                             quantidade_total=2, quantidade_disponivel=2))
        db.session.add(Livro(titulo="Código Limpo", autor="Robert C. Martin", isbn="9788576082675",
                             ano=2008, categoria="Tecnologia",
                             quantidade_total=1, quantidade_disponivel=1))
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()
        db.engine.dispose()


@pytest.fixture
def client(app):
    return app.test_client()


def login(client, email, senha):
    return client.post("/auth/login", data={"email": email, "senha": senha}, follow_redirects=True)


@pytest.fixture
def leitor_client(client):
    login(client, "leitor@teste.com", "leitor123")
    return client


@pytest.fixture
def admin_client(client):
    login(client, "admin@teste.com", "admin123")
    return client
