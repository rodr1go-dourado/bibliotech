# Laudo de qualidade: BiblioTech

| Item | Valor |
|---|---|
| Sistema | BiblioTech, versão 1.0 |
| Ambiente de produção | https://bibliotech-c8ps.onrender.com (Render + PostgreSQL) |
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

## 2. Validação com usuários (5 testes simulados, conforme orientação do professor)

| # | Testador | Data | Funcionou | Não funcionou / a corrigir | Não testado |
|---|---|---|---|---|---|
| T1 | Mariana Costa | 17/11/2026 | Cadastro, login, filtro, empréstimo e devolução (notebook) | Busca "codigo" sem acento não achou "Código Limpo" | Área de admin |
| T2 | Rafael Lima | 17/11/2026 | Layout no celular, menu, empréstimo e devolução | Falta mostrar quantos dias faltam para devolver | Feedback com print |
| T3 | Juliana Alves | 17/11/2026 | Busca, bloqueio de duplicidade e de limite | Botão "Pegar emprestado" aparece em livro que o leitor já tem | Bloqueio por atraso |
| T4 | Pedro Henrique Santos | 17/11/2026 | CRUD de livros, gestão, triagem de feedbacks (admin) | Não existe "Esqueci minha senha" | Exclusão de livro com histórico |
| T5 | Camila Rocha | 17/11/2026 | Formulário de teste, mensagens do cadastro, página 404 | Acervo sem paginação (sugestão) | iPhone/Safari |

## 3. Correções feitas a partir dos testes

| # | Problema | Decisão | Evidência |
|---|---|---|---|
| T1 | Busca sensível a acento | **Corrigido**: função `normalizar()` em `controllers/livros.py` + teste `test_t1_busca_ignora_acentos_e_maiusculas` | `evidencias/T1-busca-antes.png` → `T1-busca-depois.png` |
| T2 | Prazo pouco claro | **Corrigido**: propriedade `Emprestimo.prazo_texto` ("Faltam X dias", "Vence hoje", "X dia(s) de atraso") + teste `test_t2_texto_de_prazo` | `evidencias/T2-prazo-antes.png` → `T2-prazo-depois.png` |
| T3 | Botão enganoso | **Corrigido**: aviso "Você já está com este livro…" no lugar do botão + teste `test_t3_detalhe_avisa_livro_ja_emprestado` | `evidencias/T3-detalhe-antes.png` → `T3-detalhe-depois.png` |
| T4 | Recuperação de senha | **Backlog (RF14)**: depende de serviço de e-mail, o mesmo do RF13 | Relato no formulário |
| T5 | Paginação | **Backlog**: o acervo tem 10 títulos; a paginação será criada acima de 50 | Relato no formulário |

## 4. Parecer final

- Problemas registrados: 9 (4 na verificação interna + 5 relatos de usuários)
- Corrigidos: 7 · Backlog: 2 · Abertos críticos: 0
- Testes automatizados: 30, todos aprovados, 90% de cobertura
- Requisitos funcionais implementados: 11 de 14
- **Conclusão:** o sistema atende aos fluxos principais de leitores e administradores e está apto para uso pela biblioteca comunitária, com as melhorias de backlog previstas para a próxima versão.
