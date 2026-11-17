"""CT-12 a CT-17: regras de negócio de empréstimo e devolução."""
from datetime import date, timedelta

from app import db
from app.models import Emprestimo, Livro, Usuario


def _livro(app, titulo):
    with app.app_context():
        return Livro.query.filter_by(titulo=titulo).one().id


def test_ct12_emprestimo_com_sucesso(leitor_client, app):
    livro_id = _livro(app, "Dom Casmurro")
    r = leitor_client.post(f"/emprestimos/solicitar/{livro_id}", follow_redirects=True)
    assert "Empréstimo realizado" in r.get_data(as_text=True)
    with app.app_context():
        livro = db.session.get(Livro, livro_id)
        emp = Emprestimo.query.one()
        assert livro.quantidade_disponivel == 1
        assert emp.data_prevista == date.today() + timedelta(days=14)


def test_ct13_livro_sem_exemplar(leitor_client, admin_client, app):
    livro_id = _livro(app, "Código Limpo")  # só 1 exemplar
    with app.app_context():
        admin = Usuario.query.filter_by(email="admin@teste.com").one()
        Emprestimo.realizar(admin, db.session.get(Livro, livro_id))
    r = leitor_client.post(f"/emprestimos/solicitar/{livro_id}", follow_redirects=True)
    assert "Não há exemplares disponíveis" in r.get_data(as_text=True)


def test_ct14_limite_de_tres_emprestimos(leitor_client, app):
    with app.app_context():
        for i in range(3):
            db.session.add(Livro(titulo=f"Extra {i}", autor="A", quantidade_total=1, quantidade_disponivel=1))
        db.session.commit()
        ids = [l.id for l in Livro.query.filter(Livro.titulo.like("Extra%")).all()]
    for livro_id in ids:
        leitor_client.post(f"/emprestimos/solicitar/{livro_id}")
    r = leitor_client.post(f"/emprestimos/solicitar/{_livro(app, 'Dom Casmurro')}", follow_redirects=True)
    assert "Limite de 3 empréstimos" in r.get_data(as_text=True)


def test_ct15_bloqueio_por_atraso(leitor_client, app):
    livro_id = _livro(app, "Dom Casmurro")
    leitor_client.post(f"/emprestimos/solicitar/{livro_id}")
    with app.app_context():
        emp = Emprestimo.query.one()
        emp.data_prevista = date.today() - timedelta(days=1)
        db.session.commit()
        assert emp.status == "Atrasado"
    r = leitor_client.post(f"/emprestimos/solicitar/{_livro(app, 'Código Limpo')}", follow_redirects=True)
    assert "empréstimo em atraso" in r.get_data(as_text=True)


def test_ct16_devolucao_restaura_estoque(leitor_client, app):
    livro_id = _livro(app, "Dom Casmurro")
    leitor_client.post(f"/emprestimos/solicitar/{livro_id}")
    with app.app_context():
        emp_id = Emprestimo.query.one().id
    r = leitor_client.post(f"/emprestimos/{emp_id}/devolver", follow_redirects=True)
    assert "Devolução" in r.get_data(as_text=True)
    with app.app_context():
        assert db.session.get(Livro, livro_id).quantidade_disponivel == 2
        assert db.session.get(Emprestimo, emp_id).status == "Devolvido"
    r = leitor_client.post(f"/emprestimos/{emp_id}/devolver", follow_redirects=True)
    assert "já foi devolvido" in r.get_data(as_text=True)


def test_ct17_leitor_nao_devolve_emprestimo_de_outro(client, app):
    livro_id = _livro(app, "Dom Casmurro")
    with app.app_context():
        admin = Usuario.query.filter_by(email="admin@teste.com").one()
        emp_id = Emprestimo.realizar(admin, db.session.get(Livro, livro_id)).id
    client.post("/auth/login", data={"email": "leitor@teste.com", "senha": "leitor123"})
    assert client.post(f"/emprestimos/{emp_id}/devolver").status_code == 403


def test_nao_pega_dois_exemplares_do_mesmo_livro(leitor_client, app):
    livro_id = _livro(app, "Dom Casmurro")
    leitor_client.post(f"/emprestimos/solicitar/{livro_id}")
    r = leitor_client.post(f"/emprestimos/solicitar/{livro_id}", follow_redirects=True)
    assert "já está com um exemplar" in r.get_data(as_text=True)


def test_admin_filtra_atrasados(admin_client, app):
    livro_id = _livro(app, "Dom Casmurro")
    admin_client.post(f"/emprestimos/solicitar/{livro_id}")
    assert "Dom Casmurro" not in admin_client.get("/emprestimos/?filtro=atrasados").get_data(as_text=True)
    assert "Dom Casmurro" in admin_client.get("/emprestimos/?filtro=ativos").get_data(as_text=True)
