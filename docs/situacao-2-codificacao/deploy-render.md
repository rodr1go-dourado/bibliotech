# Publicação: GitHub + Render

## 1. Subir o código no GitHub

1. Crie uma conta em https://github.com (se ainda não tiver).
2. Clique em **New repository** → nome `bibliotech` → **Public** → **Create repository** (sem README, porque o projeto já tem um).
3. No terminal, dentro da pasta do projeto:

```bash
git init
git add .
git commit -m "BiblioTech: versão inicial PIT II"
git branch -M main
git remote add origin https://github.com/rodr1go-dourado/bibliotech.git
git push -u origin main
```

## 2. Publicar no Render (gratuito)

O repositório já tem um `render.yaml` (Blueprint) que cria o site e o banco PostgreSQL de uma vez.

1. Acesse https://render.com e entre com a conta do GitHub.
2. Clique em **New +** → **Blueprint**.
3. Selecione o repositório `bibliotech` → **Connect**.
4. O Render lê o `render.yaml` e mostra os dois recursos: `bibliotech` (Web Service) e `bibliotech-db` (PostgreSQL). Clique em **Apply**.
5. Quando aparecer **Live**, o link fica no topo da página (ex.: `https://bibliotech-xxxx.onrender.com`).
6. Senha do admin: o Blueprint gera uma aleatória. Para ver, abra o serviço → **Environment** → `ADMIN_PASSWORD`. O login é `admin@bibliotech.com`.

> **Observações do plano gratuito:** o site "dorme" depois de 15 min sem acesso, e a primeira abertura leva uns 50 segundos. O PostgreSQL gratuito expira após 30 dias, então faça a entrega antes disso ou recrie o banco.

## Alternativa sem Blueprint

**New +** → **Web Service** → escolha o repositório e configure:

| Campo | Valor |
|---|---|
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `flask --app run seed && gunicorn run:app` |
| Variáveis | `SECRET_KEY` (qualquer texto longo), `ADMIN_PASSWORD`, `DATABASE_URL` (Internal URL de um PostgreSQL criado em **New +** → **PostgreSQL**) |
