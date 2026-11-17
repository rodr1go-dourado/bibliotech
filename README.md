# 📚 BiblioTech

**Autor:** [@rodr1go-dourado](https://github.com/rodr1go-dourado)  
**Repositório:** https://github.com/rodr1go-dourado/bibliotech  
**Sistema online:** _em breve_

Sistema web de empréstimo de livros para bibliotecas comunitárias, desenvolvido no **Projeto Integrador Transdisciplinar em Engenharia de Software II**.

O leitor consulta o acervo, pega livros emprestados e acompanha seus prazos. O administrador cadastra livros, acompanha empréstimos ativos e atrasados e registra devoluções.

| Item | Tecnologia |
|---|---|
| Back-end | Python 3.12+ · Flask 3 (padrão **MVC**) |
| Front-end | HTML5, CSS3 (responsivo), JavaScript, templates Jinja2 |
| Banco de dados | PostgreSQL (produção) · SQLite (desenvolvimento/testes) · ORM SQLAlchemy |
| Autenticação | Flask-Login + senhas com hash (Werkzeug/scrypt) |
| Testes | pytest + pytest-cov (27 casos, ~90% de cobertura) |
| Hospedagem | Render (Web Service + PostgreSQL) |
| Modo de codificação | Tradicional |

## Funcionalidades

- Cadastro e login de leitores; perfis **leitor** e **admin**
- Acervo com busca por título/autor e filtro por categoria
- CRUD de livros (admin) com validação de ISBN, ano e quantidade
- Empréstimo com regras de negócio:
  - prazo de **14 dias**
  - no máximo **3 empréstimos ativos** por leitor
  - bloqueio de novos empréstimos para quem tem livro **em atraso**
  - um exemplar do mesmo título por leitor
- Devolução com atualização automática do estoque
- Painel de gestão (ativos / atrasados / todos)
- **Formulário de teste** (`/feedback/novo`) para os testadores relatarem o que funcionou, o que falhou e anexarem print da tela, com painel de triagem para o admin

## Arquitetura MVC

```
bibliotech/
├── app/
│   ├── models.py          ← MODEL: entidades + regras de negócio
│   ├── controllers/       ← CONTROLLER: rotas (Blueprints)
│   │   ├── auth.py  livros.py  emprestimos.py  feedback.py  main.py
│   ├── templates/         ← VIEW: páginas Jinja2
│   └── static/css/
├── tests/                 ← testes automatizados (pytest)
├── docs/                  ← documentação por situação-problema
│   ├── situacao-1-planejamento/
│   ├── situacao-2-codificacao/
│   └── situacao-3-testes/
├── config.py  run.py  requirements.txt  render.yaml
```

## Como rodar localmente

```bash
git clone https://github.com/rodr1go-dourado/bibliotech.git
cd bibliotech
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
flask --app run seed             # cria usuários e livros de demonstração
flask --app run run --debug      # http://127.0.0.1:5000
```

Usuários de demonstração:

| Perfil | E-mail | Senha |
|---|---|---|
| Admin | admin@bibliotech.com | admin123 (ou valor de `ADMIN_PASSWORD`) |
| Leitor | leitor@bibliotech.com | leitor123 |

## Testes

```bash
pytest -v --cov=app --cov-report=term-missing
```

## Deploy

Ver [docs/situacao-2-codificacao/deploy-render.md](docs/situacao-2-codificacao/deploy-render.md).

## Documentação

- [Escopo revisado](docs/situacao-1-planejamento/01-escopo.md)
- [Modelagem UML](docs/situacao-1-planejamento/02-uml.md)
- [IHC e protótipo](docs/situacao-1-planejamento/03-ihc.md)
- [Banco de dados: conceitual, lógico, físico e dicionário](docs/situacao-1-planejamento/04-banco-de-dados.md)
- [Manual de uso](docs/situacao-2-codificacao/manual-de-uso.md)
- [Plano e resultado dos testes](docs/situacao-3-testes/plano-de-testes.md)
- [Formulário de teste (colegas)](docs/situacao-3-testes/formulario-de-teste.md)
- [Laudo de qualidade](docs/situacao-3-testes/laudo-de-qualidade.md)
- [Roteiro dos vídeos](docs/situacao-3-testes/roteiro-videos.md)
