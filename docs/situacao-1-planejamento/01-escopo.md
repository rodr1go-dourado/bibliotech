# 1. Escopo revisado (Kaizen)

## 1.1 Problema

Bibliotecas comunitárias (associações de bairro, escolas, igrejas, ONGs) costumam controlar empréstimos em cadernos ou planilhas. Por isso:

- o leitor não sabe se um livro está disponível sem ir até o local;
- os prazos de devolução se perdem e os atrasos não são cobrados;
- o responsável não tem visão rápida de quais livros estão fora e com quem.

## 1.2 Solução

O **BiblioTech** é uma aplicação web responsiva que centraliza o acervo e os empréstimos. Funciona no computador e no celular, sem instalar nada.

## 1.3 Atores

| Ator | Descrição |
|---|---|
| Visitante | Qualquer pessoa sem login. Consulta o acervo e pode enviar relatório de teste. |
| Leitor | Usuário cadastrado. Pega livros emprestados, devolve e acompanha seus prazos. |
| Administrador | Responsável pela biblioteca. Mantém o acervo, acompanha empréstimos e triagem de feedbacks. |

## 1.4 Requisitos funcionais

| ID | Requisito | Prioridade | Status |
|---|---|---|---|
| RF01 | Cadastrar leitor (nome, e-mail, senha) | Alta | Implementado |
| RF02 | Autenticar usuário (login/logout) | Alta | Implementado |
| RF03 | Consultar acervo com busca por título/autor | Alta | Implementado |
| RF04 | Filtrar acervo por categoria | Média | Implementado |
| RF05 | Cadastrar, editar e excluir livros (admin) | Alta | Implementado |
| RF06 | Realizar empréstimo de livro disponível | Alta | Implementado |
| RF07 | Registrar devolução | Alta | Implementado |
| RF08 | Listar meus empréstimos com status (em andamento / atrasado / devolvido) | Alta | Implementado |
| RF09 | Painel de empréstimos ativos e atrasados (admin) | Média | Implementado |
| RF10 | Formulário de relato de testes com print de tela | Média | Implementado (novo no PIT II) |
| RF11 | Triagem de feedbacks (Aberto / Corrigido / Descartado) | Baixa | Implementado (novo no PIT II) |
| RF12 | Reserva de livro indisponível (fila de espera) | Baixa | Backlog |
| RF13 | Envio de e-mail lembrando a devolução | Baixa | Backlog |
| RF14 | Recuperação de senha por e-mail | Média | Backlog (veio do teste T4) |

## 1.5 Regras de negócio

| ID | Regra |
|---|---|
| RN01 | O prazo de empréstimo é de 14 dias corridos. |
| RN02 | Cada leitor pode ter no máximo 3 empréstimos ativos. |
| RN03 | Leitor com empréstimo atrasado não pode pegar novo livro até devolver. |
| RN04 | Só é possível emprestar livro com exemplar disponível. |
| RN05 | O leitor não pode pegar dois exemplares do mesmo título ao mesmo tempo. |
| RN06 | Livro com histórico de empréstimos não pode ser excluído. |
| RN07 | A quantidade total de exemplares não pode ficar menor que a quantidade emprestada. |
| RN08 | ISBN, quando informado, tem 10 ou 13 dígitos e é único. |
| RN09 | Senhas têm no mínimo 6 caracteres e são armazenadas apenas como hash. |

## 1.6 Requisitos não funcionais

| ID | Requisito |
|---|---|
| RNF01 | Interface responsiva (desktop e celular, a partir de 360 px). |
| RNF02 | Senhas com hash (scrypt via Werkzeug); nenhuma senha em texto puro. |
| RNF03 | Controle de acesso por perfil: rotas de admin retornam 403 para leitores. |
| RNF04 | Erros tratados com páginas amigáveis (403, 404, 413, 500). |
| RNF05 | SGBD popular e de fácil manutenção (PostgreSQL). |
| RNF06 | Cobertura de testes automatizados acima de 80%. |
| RNF07 | Código versionado no GitHub e implantado em nuvem (Render). |

## 1.7 O que mudou em relação ao PIT I

| Antes (PIT I) | Agora (PIT II) | Motivo |
|---|---|---|
| Sem regra de atraso | RN03 bloqueia novos empréstimos | Sugestão de colegas: sem isso, ninguém devolve no prazo |
| Limite de empréstimos não definido | RN02 = 3 livros | Evita que um leitor "esvazie" o acervo |
| Exclusão livre de livros | RN06 impede excluir livro com histórico | Preserva a integridade referencial |
| Sem canal de feedback | RF10/RF11: formulário de teste com print | Exigência da Situação 3 e melhoria contínua |
| Quantidade única por livro | `quantidade_total` + `quantidade_disponivel` | Bibliotecas têm vários exemplares do mesmo título |
