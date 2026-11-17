# Laudo de qualidade: BiblioTech

| Item | Valor |
|---|---|
| Sistema | BiblioTech, versão 1.0 |
| Ambiente de produção | https://SEU-APP.onrender.com (Render + PostgreSQL) |
| Responsável | NOME DO ALUNO |
| Período de testes | DD/MM/AAAA a DD/MM/AAAA |

## 1. Verificação interna (desenvolvedor)

### 1.1 Testes automatizados
- 27 casos de teste (unitários e de integração), **27 aprovados / 0 falhas**
- Cobertura de linhas: **90%**
- Detalhamento: [plano-de-testes.md](plano-de-testes.md)

### 1.2 Defeitos encontrados e corrigidos durante o desenvolvimento

| # | Defeito | Severidade | Evidência | Correção |
|---|---|---|---|---|
| D1 | Risco de *open redirect*: o parâmetro `next` do login aceitava `//site-externo` | Alta (segurança) | Teste `test_open_redirect_bloqueado` | Aceita apenas caminhos internos (começando com `/` e sem `//`) |
| D2 | Variável `d` (dados do formulário) definida fora do bloco Jinja, com risco de não ser enxergada dentro de `{% block content %}`, o que faria o formulário perder o que o usuário digitou ao dar erro de validação | Média | Revisão dos templates `livros/form.html` e `feedback/form.html` | `{% set %}` movido para dentro do bloco; o formulário agora mantém os valores após erro (ver `telas/07-validacao-livro.png`) |
| D3 | Uso de `datetime.utcnow()`, que está obsoleto no Python 3.12+ e gerava 57 avisos na suíte de testes | Baixa | Saída do `pytest` | Trocado por `datetime.now(timezone.utc)` |
| D4 | Conexões SQLite não eram fechadas entre testes (`ResourceWarning`) | Baixa | Saída do `pytest` | `db.engine.dispose()` no teardown da fixture |

## 2. Validação com usuários (5 colegas)

> Preencher com os relatos **reais** recebidos pelo formulário (`/feedback`). Cada linha deve ter o print correspondente na pasta `evidencias/`.

| # | Testador | Data | Funcionou | Não funcionou / a corrigir | Não testado | Evidência |
|---|---|---|---|---|---|---|
| 1 | | | | | | `evidencias/t1.png` |
| 2 | | | | | | `evidencias/t2.png` |
| 3 | | | | | | `evidencias/t3.png` |
| 4 | | | | | | `evidencias/t4.png` |
| 5 | | | | | | `evidencias/t5.png` |

## 3. Correções feitas a partir dos testes

| # | Problema relatado (por quem) | Decisão (corrigir / descartar e por quê) | Commit / evidência do antes e depois |
|---|---|---|---|
| | | | |

## 4. Parecer final

- Requisitos funcionais implementados: 11 de 13 (RF12 e RF13 ficaram no backlog)
- Defeitos abertos: __
- Defeitos corrigidos: __
- **Conclusão:** _ex.: "O sistema está apto para uso em produção pela biblioteca comunitária, com as ressalvas…"_
