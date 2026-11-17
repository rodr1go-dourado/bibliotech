"""CT-07 a CT-11: acervo (consulta e manutenção pelo administrador)."""
from app import db
from app.models import Livro


def test_ct07_listagem_publica_e_busca(client):
    r = client.get("/livros/?q=machado")
    texto = r.get_data(as_text=True)
    assert r.status_code == 200
    assert "Dom Casmurro" in texto and "Código Limpo" not in texto


def test_ct07b_filtro_por_categoria(client):
    texto = client.get("/livros/?categoria=Tecnologia").get_data(as_text=True)
    assert "Código Limpo" in texto and "Dom Casmurro" not in texto


def test_ct08_admin_cadastra_livro(admin_client, app):
    r = admin_client.post("/livros/novo", data={"titulo": "Vidas Secas", "autor": "Graciliano Ramos",
                                                "isbn": "9788501114051", "ano": "1938",
                                                "categoria": "Literatura Brasileira",
                                                "quantidade_total": "2"}, follow_redirects=True)
    assert "Livro salvo" in r.get_data(as_text=True)
    with app.app_context():
        livro = Livro.query.filter_by(isbn="9788501114051").one()
        assert livro.quantidade_disponivel == 2


def test_ct09_validacao_dos_campos(admin_client):
    r = admin_client.post("/livros/novo", data={"titulo": "", "autor": "", "isbn": "123",
                                                "ano": "3000", "quantidade_total": "0"})
    texto = r.get_data(as_text=True)
    assert r.status_code == 400
    for msg in ("Título é obrigatório", "Autor é obrigatório", "ISBN deve ter",
                "Ano de publicação inválido", "Quantidade deve ser"):
        assert msg in texto


def test_ct10_isbn_duplicado(admin_client):
    r = admin_client.post("/livros/novo", data={"titulo": "Outro", "autor": "Alguém",
                                                "isbn": "9788594318602", "quantidade_total": "1"})
    assert r.status_code == 400
    assert "Já existe um livro com este ISBN" in r.get_data(as_text=True)


def test_ct11_nao_exclui_livro_com_historico(admin_client, app):
    with app.app_context():
        livro_id = Livro.query.filter_by(titulo="Dom Casmurro").one().id
    admin_client.post(f"/emprestimos/solicitar/{livro_id}")
    r = admin_client.post(f"/livros/{livro_id}/excluir", follow_redirects=True)
    assert "histórico de empréstimos" in r.get_data(as_text=True)
    with app.app_context():
        assert db.session.get(Livro, livro_id) is not None


def test_edicao_nao_reduz_abaixo_do_emprestado(admin_client, app):
    with app.app_context():
        livro_id = Livro.query.filter_by(titulo="Dom Casmurro").one().id
    admin_client.post(f"/emprestimos/solicitar/{livro_id}")
    admin_client.post(f"/emprestimos/solicitar/{livro_id}")  # 2ª tentativa barrada (duplicidade)
    r = admin_client.post(f"/livros/{livro_id}/editar",
                          data={"titulo": "Dom Casmurro", "autor": "Machado de Assis",
                                "quantidade_total": "0"})
    assert r.status_code == 400


def test_livro_inexistente_retorna_404(client):
    assert client.get("/livros/9999").status_code == 404
