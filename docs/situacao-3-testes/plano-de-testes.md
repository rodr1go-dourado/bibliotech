# Plano e resultado dos testes (verificação e validação)

A estratégia segue o **Modelo V**:

| Nível | O que valida | Como |
|---|---|---|
| Unitário | Regras dos models (validação de livro, senha, status do empréstimo) | pytest chamando métodos do model |
| Integração | Controller + Model + banco (requisição HTTP completa) | pytest + `app.test_client()` + SQLite em memória |
| Sistema | Fluxos de ponta a ponta no navegador | roteiro manual + capturas de tela |
| Aceitação | O sistema atende o usuário real? | 5 colegas usando o [formulário de teste](formulario-de-teste.md) |

## Casos de teste automatizados

| CT | Requisito | Cenário | Resultado esperado | Arquivo / função | Resultado |
|---|---|---|---|---|---|
| CT01 | RF01, RN09 | Cadastro com dados válidos | Usuário criado como leitor, senha em hash | `test_auth::test_ct01_cadastro_valido` | ✅ Passou |
| CT02 | RF01 | E-mail já cadastrado | HTTP 400 + "já está cadastrado" | `test_auth::test_ct02_cadastro_email_duplicado` | ✅ Passou |
| CT03 | RF01 | Senhas divergentes | HTTP 400 + "não conferem" | `test_auth::test_ct03_cadastro_senha_curta_e_divergente` | ✅ Passou |
| CT04 | RF02 | Login correto e incorreto | Boas-vindas / HTTP 401 | `test_auth::test_ct04_login_valido_e_invalido` | ✅ Passou |
| CT05 | RNF03 | Acessar rota protegida sem login | Redireciona para /auth/login | `test_auth::test_ct05_…` | ✅ Passou |
| CT06 | RNF03 | Leitor acessa área de admin | HTTP 403 | `test_auth::test_ct06_…` | ✅ Passou |
| CT06b | Segurança | `next=//site-externo` no login | Não redireciona para fora | `test_auth::test_open_redirect_bloqueado` | ✅ Passou |
| CT07 | RF03, RF04 | Busca por autor e filtro por categoria | Só os livros correspondentes | `test_livros::test_ct07_…`, `test_ct07b_…` | ✅ Passou |
| CT08 | RF05 | Admin cadastra livro | Livro salvo com estoque = quantidade | `test_livros::test_ct08_…` | ✅ Passou |
| CT09 | RN08 | Campos inválidos | 5 mensagens de validação | `test_livros::test_ct09_…` | ✅ Passou |
| CT10 | RN08 | ISBN duplicado | HTTP 400 | `test_livros::test_ct10_…` | ✅ Passou |
| CT11 | RN06 | Excluir livro com histórico | Bloqueado | `test_livros::test_ct11_…` | ✅ Passou |
| CT11b | RN07 | Reduzir quantidade abaixo do emprestado | HTTP 400 | `test_livros::test_edicao_nao_reduz_…` | ✅ Passou |
| CT11c | RNF04 | Livro inexistente | HTTP 404 | `test_livros::test_livro_inexistente_…` | ✅ Passou |
| CT12 | RF06, RN01 | Empréstimo válido | Estoque −1, prazo = hoje + 14 | `test_emprestimos::test_ct12_…` | ✅ Passou |
| CT13 | RN04 | Livro sem exemplar | Mensagem de indisponível | `test_emprestimos::test_ct13_…` | ✅ Passou |
| CT14 | RN02 | 4º empréstimo simultâneo | "Limite de 3" | `test_emprestimos::test_ct14_…` | ✅ Passou |
| CT15 | RN03 | Leitor com atraso | Bloqueado | `test_emprestimos::test_ct15_…` | ✅ Passou |
| CT16 | RF07 | Devolver e devolver de novo | Estoque +1; 2ª vez bloqueada | `test_emprestimos::test_ct16_…` | ✅ Passou |
| CT17 | RNF03 | Leitor devolve empréstimo de outro | HTTP 403 | `test_emprestimos::test_ct17_…` | ✅ Passou |
| CT17b | RN05 | Mesmo título duas vezes | Bloqueado | `test_emprestimos::test_nao_pega_dois_…` | ✅ Passou |
| CT17c | RF09 | Filtro ativos/atrasados | Lista correta | `test_emprestimos::test_admin_filtra_atrasados` | ✅ Passou |
| CT18 | RF10 | Feedback com print PNG | Salvo com imagem, status Aberto | `test_feedback::test_ct18_…` | ✅ Passou |
| CT19 | RF10 | Feedback vazio / arquivo não imagem | HTTP 400 | `test_feedback::test_ct19_…`, `test_ct19b_…` | ✅ Passou |
| CT20 | RF11 | Admin lista e muda status | Status = Corrigido | `test_feedback::test_ct20_…` | ✅ Passou |

## Execução

```bash
pytest -v --cov=app --cov-report=term-missing
```

**Resultado:** 27 testes, **27 aprovados, 0 falhas**, cobertura de **90%** das linhas do pacote `app`.

| Módulo | Cobertura |
|---|---|
| controllers/emprestimos.py | 100% |
| controllers/main.py | 100% |
| models.py | 99% |
| app/__init__.py | 91% |
| controllers/auth.py | 90% |
| controllers/livros.py | 88% |
| controllers/feedback.py | 83% |
| seed.py | 39% (script de carga inicial, testado manualmente) |
| **Total** | **90%** |

## Testes de sistema (manuais)

| Roteiro | Evidência |
|---|---|
| Cadastro → login → busca → empréstimo → meus empréstimos | `../situacao-2-codificacao/telas/01` a `05` |
| Admin: validação de cadastro de livro | `telas/07-validacao-livro.png` |
| Admin: gestão de empréstimos | `telas/08-gestao-emprestimos.png` |
| Responsividade em tela de 390 px | `telas/09-mobile-acervo.png` |
