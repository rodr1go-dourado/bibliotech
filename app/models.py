"""Camada MODEL do padrão MVC: entidades persistidas e regras de negócio."""
from datetime import date, datetime, timedelta, timezone

from flask import current_app
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class RegraNegocioError(Exception):
    """Violação de regra de negócio (mensagem exibida ao usuário)."""


class Usuario(UserMixin, db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    senha_hash = db.Column(db.String(256), nullable=False)
    perfil = db.Column(db.String(10), nullable=False, default="leitor")  # leitor | admin
    criado_em = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    emprestimos = db.relationship("Emprestimo", back_populates="usuario", lazy="dynamic")

    __table_args__ = (db.CheckConstraint("perfil IN ('leitor', 'admin')", name="ck_usuario_perfil"),)

    def definir_senha(self, senha):
        if not senha or len(senha) < 6:
            raise RegraNegocioError("A senha deve ter pelo menos 6 caracteres.")
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    @property
    def is_admin(self):
        return self.perfil == "admin"

    def emprestimos_ativos(self):
        return self.emprestimos.filter(Emprestimo.data_devolucao.is_(None))

    def tem_atraso(self):
        return self.emprestimos_ativos().filter(Emprestimo.data_prevista < date.today()).count() > 0


class Livro(db.Model):
    __tablename__ = "livro"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(150), nullable=False)
    isbn = db.Column(db.String(13), unique=True)
    ano = db.Column(db.Integer)
    categoria = db.Column(db.String(50), nullable=False, default="Geral")
    quantidade_total = db.Column(db.Integer, nullable=False, default=1)
    quantidade_disponivel = db.Column(db.Integer, nullable=False, default=1)

    emprestimos = db.relationship("Emprestimo", back_populates="livro", lazy="dynamic")

    __table_args__ = (
        db.CheckConstraint("quantidade_total >= 0", name="ck_livro_qtd_total"),
        db.CheckConstraint("quantidade_disponivel >= 0", name="ck_livro_qtd_disp"),
        db.CheckConstraint("quantidade_disponivel <= quantidade_total", name="ck_livro_qtd_limite"),
    )

    @property
    def disponivel(self):
        return self.quantidade_disponivel > 0

    @staticmethod
    def validar_dados(titulo, autor, isbn, ano, quantidade):
        erros = []
        if not titulo or not titulo.strip():
            erros.append("Título é obrigatório.")
        if not autor or not autor.strip():
            erros.append("Autor é obrigatório.")
        if isbn and (not isbn.isdigit() or len(isbn) not in (10, 13)):
            erros.append("ISBN deve ter 10 ou 13 dígitos numéricos.")
        if ano is not None and (ano < 1450 or ano > date.today().year):
            erros.append("Ano de publicação inválido.")
        if quantidade is None or quantidade < 1:
            erros.append("Quantidade deve ser no mínimo 1.")
        return erros


class Emprestimo(db.Model):
    __tablename__ = "emprestimo"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False, index=True)
    livro_id = db.Column(db.Integer, db.ForeignKey("livro.id"), nullable=False, index=True)
    data_emprestimo = db.Column(db.Date, nullable=False, default=date.today)
    data_prevista = db.Column(db.Date, nullable=False)
    data_devolucao = db.Column(db.Date)

    usuario = db.relationship("Usuario", back_populates="emprestimos")
    livro = db.relationship("Livro", back_populates="emprestimos")

    @property
    def ativo(self):
        return self.data_devolucao is None

    @property
    def atrasado(self):
        return self.ativo and self.data_prevista < date.today()

    @property
    def status(self):
        if not self.ativo:
            return "Devolvido"
        return "Atrasado" if self.atrasado else "Em andamento"

    @classmethod
    def realizar(cls, usuario, livro):
        """Regras: livro disponível, sem atraso, limite de empréstimos ativos, sem duplicidade."""
        limite = current_app.config["LIMITE_EMPRESTIMOS_ATIVOS"]
        if not livro.disponivel:
            raise RegraNegocioError("Não há exemplares disponíveis deste livro.")
        if usuario.tem_atraso():
            raise RegraNegocioError("Você possui empréstimo em atraso. Devolva-o antes de pegar outro livro.")
        if usuario.emprestimos_ativos().count() >= limite:
            raise RegraNegocioError(f"Limite de {limite} empréstimos ativos atingido.")
        if usuario.emprestimos_ativos().filter(cls.livro_id == livro.id).count() > 0:
            raise RegraNegocioError("Você já está com um exemplar deste livro.")

        prazo = current_app.config["PRAZO_EMPRESTIMO_DIAS"]
        emp = cls(usuario=usuario, livro=livro, data_emprestimo=date.today(),
                  data_prevista=date.today() + timedelta(days=prazo))
        livro.quantidade_disponivel -= 1
        db.session.add(emp)
        db.session.commit()
        return emp

    def devolver(self):
        if not self.ativo:
            raise RegraNegocioError("Este empréstimo já foi devolvido.")
        self.data_devolucao = date.today()
        self.livro.quantidade_disponivel += 1
        db.session.commit()


class Feedback(db.Model):
    """Formulário de teste usado pelos colegas (Situação 3): bugs, sugestões e prints."""
    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    nome_testador = db.Column(db.String(100), nullable=False)
    data_teste = db.Column(db.Date, nullable=False, default=date.today)
    funcionou = db.Column(db.Text)
    nao_funcionou = db.Column(db.Text)
    nao_testado = db.Column(db.Text)
    sugestoes = db.Column(db.Text)
    print_tela = db.Column(db.LargeBinary)
    print_mimetype = db.Column(db.String(50))
    status = db.Column(db.String(20), nullable=False, default="Aberto")  # Aberto | Corrigido | Descartado
    criado_em = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
