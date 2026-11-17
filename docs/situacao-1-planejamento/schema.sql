-- BiblioTech: projeto físico (PostgreSQL)
-- Gerado a partir dos models SQLAlchemy (app/models.py)

CREATE TABLE feedback (
	id SERIAL NOT NULL, 
	nome_testador VARCHAR(100) NOT NULL, 
	data_teste DATE NOT NULL, 
	funcionou TEXT, 
	nao_funcionou TEXT, 
	nao_testado TEXT, 
	sugestoes TEXT, 
	print_tela BYTEA, 
	print_mimetype VARCHAR(50), 
	status VARCHAR(20) NOT NULL, 
	criado_em TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id)
);


CREATE TABLE livro (
	id SERIAL NOT NULL, 
	titulo VARCHAR(200) NOT NULL, 
	autor VARCHAR(150) NOT NULL, 
	isbn VARCHAR(13), 
	ano INTEGER, 
	categoria VARCHAR(50) NOT NULL, 
	quantidade_total INTEGER NOT NULL, 
	quantidade_disponivel INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT ck_livro_qtd_total CHECK (quantidade_total >= 0), 
	CONSTRAINT ck_livro_qtd_disp CHECK (quantidade_disponivel >= 0), 
	CONSTRAINT ck_livro_qtd_limite CHECK (quantidade_disponivel <= quantidade_total), 
	UNIQUE (isbn)
);


CREATE TABLE usuario (
	id SERIAL NOT NULL, 
	nome VARCHAR(100) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	senha_hash VARCHAR(256) NOT NULL, 
	perfil VARCHAR(10) NOT NULL, 
	criado_em TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT ck_usuario_perfil CHECK (perfil IN ('leitor', 'admin'))
);

CREATE UNIQUE INDEX ix_usuario_email ON usuario (email);

CREATE TABLE emprestimo (
	id SERIAL NOT NULL, 
	usuario_id INTEGER NOT NULL, 
	livro_id INTEGER NOT NULL, 
	data_emprestimo DATE NOT NULL, 
	data_prevista DATE NOT NULL, 
	data_devolucao DATE, 
	PRIMARY KEY (id), 
	FOREIGN KEY(usuario_id) REFERENCES usuario (id), 
	FOREIGN KEY(livro_id) REFERENCES livro (id)
);

CREATE INDEX ix_emprestimo_livro_id ON emprestimo (livro_id);
CREATE INDEX ix_emprestimo_usuario_id ON emprestimo (usuario_id);

