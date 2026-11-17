"""CT-01 a CT-06: cadastro, login e controle de acesso."""
from app.models import Usuario
from tests.conftest import login


def test_ct01_cadastro_valido(client, app):
    r = client.post("/auth/registrar", data={"nome": "Maria", "email": "maria@teste.com",
                                             "senha": "segura123", "confirmacao": "segura123"},
                    follow_redirects=True)
    assert "Cadastro realizado" in r.get_data(as_text=True)
    with app.app_context():
        u = Usuario.query.filter_by(email="maria@teste.com").first()
        assert u is not None and u.perfil == "leitor"
        assert u.senha_hash != "segura123"  # senha nunca em texto puro


def test_ct02_cadastro_email_duplicado(client):
    r = client.post("/auth/registrar", data={"nome": "X", "email": "leitor@teste.com",
                                             "senha": "abcdef", "confirmacao": "abcdef"})
    assert r.status_code == 400
    assert "já está cadastrado" in r.get_data(as_text=True)


def test_ct03_cadastro_senha_curta_e_divergente(client):
    r = client.post("/auth/registrar", data={"nome": "X", "email": "x@teste.com",
                                             "senha": "123", "confirmacao": "999"})
    texto = r.get_data(as_text=True)
    assert r.status_code == 400
    assert "não conferem" in texto


def test_ct04_login_valido_e_invalido(client):
    assert "Bem-vindo(a)" in login(client, "leitor@teste.com", "leitor123").get_data(as_text=True)
    client.get("/auth/logout")
    r = client.post("/auth/login", data={"email": "leitor@teste.com", "senha": "errada"})
    assert r.status_code == 401
    assert "incorretos" in r.get_data(as_text=True)


def test_ct05_rota_protegida_redireciona_para_login(client):
    r = client.get("/emprestimos/meus")
    assert r.status_code == 302
    assert "/auth/login" in r.headers["Location"]


def test_ct06_leitor_nao_acessa_area_admin(leitor_client):
    assert leitor_client.get("/livros/novo").status_code == 403
    assert leitor_client.get("/emprestimos/").status_code == 403
    assert leitor_client.get("/feedback/").status_code == 403


def test_open_redirect_bloqueado(client):
    r = client.post("/auth/login?next=//site-malicioso.com",
                    data={"email": "leitor@teste.com", "senha": "leitor123"})
    assert "site-malicioso" not in r.headers["Location"]
