# Roteiros dos vídeos

Grave com OBS Studio, Loom ou a gravação de tela do Windows (`Win + G`) e suba no YouTube como **Não listado**.

---

## Vídeo 1: solução em funcionamento (mínimo de 5 min, narrado)

| Tempo | Tela | O que falar |
|---|---|---|
| 0:00 – 0:30 | Página inicial | "Oi, eu sou [nome], RGM [número]. Este é o BiblioTech, um sistema web de empréstimo de livros para bibliotecas comunitárias, feito no PIT II." |
| 0:30 – 1:15 | GitHub (README) | "O código está no GitHub. O back-end é Python com Flask, seguindo MVC: models têm as regras, controllers as rotas e templates as telas. O banco é PostgreSQL no Render." Mostre as pastas `app/models.py`, `controllers/`, `templates/` e `docs/`. |
| 1:15 – 1:45 | Cadastro | Crie uma conta. Mostre a mensagem de erro com senhas diferentes e depois cadastre certo. |
| 1:45 – 2:15 | Acervo | Busque "Machado", filtre por "Tecnologia". "As etiquetas mostram quantos exemplares estão livres." |
| 2:15 – 3:15 | Empréstimo | Pegue "Dom Casmurro" e leia a data de devolução. Tente pegar de novo e mostre a mensagem. Pegue mais 2 livros e tente o 4º: "Limite de 3 empréstimos". |
| 3:15 – 3:45 | Meus empréstimos | Mostre os status e devolva um livro. |
| 3:45 – 4:30 | Login admin | Cadastre um livro com ISBN "123" e mostre a validação. Corrija e salve. Mostre a Gestão (abas Ativos / Atrasados). |
| 4:30 – 5:00 | Formulário de teste | "Esse é o formulário que os colegas usaram para relatar bugs com print." Mostre a tela de Feedbacks. |
| 5:00 – 5:40 | Terminal | Rode `pytest -v --cov=app`. "São 30 testes automatizados, todos passando, com 90% de cobertura." |
| 5:40 – 6:00 | Celular / DevTools | Mostre a versão mobile e encerre: "Obrigado!" |

---

## Vídeo 2: solução atualizada (até 5 min)

| Tempo | O que mostrar / falar |
|---|---|
| 0:00 – 0:20 | "Neste vídeo mostro as mudanças feitas a partir dos testes com 5 colegas." |
| 0:20 – 1:00 | Abra a tela **Feedbacks** e passe pelos 5 relatos. "Recebi X relatos de erro e Y sugestões." |
| 1:00 – 4:00 | Para cada correção (2 ou 3 principais): leia o relato → mostre **antes** (print do colega) → mostre **depois** no sistema → mude o status para *Corrigido*. |
| 4:00 – 4:30 | O que foi descartado e por quê (ex.: "fila de reserva ficou no backlog por ser fora do escopo"). |
| 4:30 – 5:00 | Rode `pytest` de novo mostrando que tudo continua passando e mostre o commit das correções no GitHub. |
