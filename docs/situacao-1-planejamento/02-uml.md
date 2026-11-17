# 2. Modelagem UML

> Os diagramas estão em [Mermaid](https://mermaid.js.org/), que o GitHub desenha automaticamente ao abrir este arquivo.

## 2.1 Diagrama de casos de uso

```mermaid
flowchart LR
    V([Visitante])
    L([Leitor])
    A([Administrador])

    subgraph BiblioTech
        UC1((Consultar acervo))
        UC2((Cadastrar-se))
        UC3((Fazer login))
        UC4((Pegar livro emprestado))
        UC5((Devolver livro))
        UC6((Ver meus empréstimos))
        UC7((Manter livros))
        UC8((Acompanhar empréstimos))
        UC9((Enviar relatório de teste))
        UC10((Triar feedbacks))
    end

    V --- UC1
    V --- UC2
    V --- UC9
    L --- UC3
    L --- UC4
    L --- UC5
    L --- UC6
    A --- UC7
    A --- UC8
    A --- UC10
    A --- UC5
    L -. herda .-> V
    A -. herda .-> L
    UC4 -. include .-> UC3
```

## 2.2 Caso de uso expandido: UC4 Pegar livro emprestado

| Campo | Descrição |
|---|---|
| Ator | Leitor |
| Pré-condição | Leitor autenticado |
| Pós-condição | Empréstimo criado com data prevista = hoje + 14 dias; estoque decrementado |
| **Fluxo principal** | 1. Leitor abre o detalhe do livro. 2. Clica em "Pegar emprestado". 3. Sistema valida RN02, RN03, RN04 e RN05. 4. Sistema registra o empréstimo e diminui a quantidade disponível. 5. Sistema exibe "Empréstimo realizado! Devolva até dd/mm/aaaa". |
| FA1: sem exemplar | Em 3, se não há exemplar: exibe "Não há exemplares disponíveis deste livro." |
| FA2: atraso | Em 3, se o leitor tem atraso: exibe "Você possui empréstimo em atraso…" |
| FA3: limite | Em 3, se já tem 3 ativos: exibe "Limite de 3 empréstimos ativos atingido." |
| FA4: duplicidade | Em 3, se já está com o título: exibe "Você já está com um exemplar deste livro." |

## 2.3 Diagrama de classes (persistência)

```mermaid
classDiagram
    class Usuario {
        +int id
        +str nome
        +str email
        -str senha_hash
        +str perfil
        +datetime criado_em
        +definir_senha(senha)
        +verificar_senha(senha) bool
        +is_admin() bool
        +emprestimos_ativos()
        +tem_atraso() bool
    }
    class Livro {
        +int id
        +str titulo
        +str autor
        +str isbn
        +int ano
        +str categoria
        +int quantidade_total
        +int quantidade_disponivel
        +disponivel() bool
        +validar_dados()$ list
    }
    class Emprestimo {
        +int id
        +date data_emprestimo
        +date data_prevista
        +date data_devolucao
        +ativo() bool
        +atrasado() bool
        +status() str
        +realizar(usuario, livro)$ Emprestimo
        +devolver()
    }
    class Feedback {
        +int id
        +str nome_testador
        +date data_teste
        +str funcionou
        +str nao_funcionou
        +str nao_testado
        +str sugestoes
        +bytes print_tela
        +str status
    }
    Usuario "1" --> "0..*" Emprestimo : realiza
    Livro "1" --> "0..*" Emprestimo : é emprestado em
```

## 2.4 Diagrama de sequência: realizar empréstimo (MVC)

```mermaid
sequenceDiagram
    actor L as Leitor
    participant V as View (detalhe.html)
    participant C as Controller (emprestimos.solicitar)
    participant M as Model (Emprestimo)
    participant DB as PostgreSQL

    L->>V: clica "Pegar emprestado"
    V->>C: POST /emprestimos/solicitar/{id}
    C->>DB: busca Livro
    C->>M: Emprestimo.realizar(usuario, livro)
    M->>DB: conta empréstimos ativos / atrasados
    alt regra violada
        M-->>C: RegraNegocioError(msg)
        C-->>V: flash(msg, "erro") + redirect
    else tudo ok
        M->>DB: INSERT emprestimo; UPDATE livro
        M-->>C: Emprestimo
        C-->>V: flash("Empréstimo realizado…") + redirect
    end
    V-->>L: mensagem na tela
```

## 2.5 Diagrama de atividades: devolução

```mermaid
flowchart TD
    I([Início]) --> A[Leitor ou admin abre lista de empréstimos]
    A --> B[Clica em Devolver]
    B --> C{Confirma?}
    C -- Não --> A
    C -- Sim --> D{Usuário é dono ou admin?}
    D -- Não --> E[403 Acesso negado] --> F([Fim])
    D -- Sim --> G{Empréstimo ativo?}
    G -- Não --> H[Mensagem: já devolvido] --> F
    G -- Sim --> J[Registra data_devolucao = hoje]
    J --> K[quantidade_disponivel + 1]
    K --> L[Mensagem de sucesso] --> F
```
