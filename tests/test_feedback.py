"""CT-18 a CT-20: formulário de teste usado pelos colegas (Situação 3)."""
import io

from app.models import Feedback

PNG_1PX = (b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00"
           b"\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18\xd8N\x00\x00"
           b"\x00\x00IEND\xaeB`\x82")


def test_ct18_envio_de_feedback_com_print(client, app):
    r = client.post("/feedback/novo", data={
        "nome_testador": "Colega 1", "data_teste": "2026-11-20",
        "funcionou": "Cadastro e login", "nao_funcionou": "Botão X",
        "print_tela": (io.BytesIO(PNG_1PX), "erro.png", "image/png"),
    }, content_type="multipart/form-data", follow_redirects=True)
    assert "Obrigado" in r.get_data(as_text=True)
    with app.app_context():
        fb = Feedback.query.one()
        assert fb.print_tela == PNG_1PX and fb.status == "Aberto"


def test_ct19_feedback_vazio_rejeitado(client):
    r = client.post("/feedback/novo", data={"nome_testador": "Colega"})
    assert r.status_code == 400
    assert "pelo menos um" in r.get_data(as_text=True)


def test_ct19b_arquivo_que_nao_e_imagem(client):
    r = client.post("/feedback/novo", data={
        "nome_testador": "Colega", "funcionou": "ok",
        "print_tela": (io.BytesIO(b"texto"), "x.txt", "text/plain"),
    }, content_type="multipart/form-data")
    assert r.status_code == 400


def test_ct20_admin_lista_e_atualiza_status(admin_client, app):
    admin_client.post("/feedback/novo", data={"nome_testador": "Colega 2", "sugestoes": "Modo escuro"})
    with app.app_context():
        fb_id = Feedback.query.one().id
    assert "Colega 2" in admin_client.get("/feedback/").get_data(as_text=True)
    admin_client.post(f"/feedback/{fb_id}/status", data={"status": "Corrigido"})
    with app.app_context():
        assert Feedback.query.one().status == "Corrigido"
