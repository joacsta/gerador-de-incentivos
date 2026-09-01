
CREATE TABLE programa_incentivo (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    dt_inicio DATE NOT NULL, -- YYYY-MM-DD
    dt_fim DATE NOT NULL,    -- YYYY-MM-DD
    ativo INT NOT NULL DEFAULT 1,
    criado_em DATETIME2 NOT NULL DEFAULT GETDATE(),
    atualizado_em DATETIME2
);

CREATE TABLE regra_apuracao (
    id INT IDENTITY(1,1) PRIMARY KEY,
    programa_id INT NOT NULL,
    nome VARCHAR(255) NOT NULL,
    criterio VARCHAR(MAX) NOT NULL, -- JSON/texto longo
    peso FLOAT,
    ativo INT NOT NULL DEFAULT 1,
    criado_em DATETIME2 NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (programa_id) REFERENCES programa_incentivo(id)
);

CREATE TABLE template_sql (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    conteudo VARCHAR(MAX) NOT NULL, -- Conteúdos longos de SQL
    versao INT NOT NULL DEFAULT 1,
    ativo INT NOT NULL DEFAULT 1,
    criado_em DATETIME2 NOT NULL DEFAULT GETDATE()
);

CREATE TABLE parametro_programa (
    id INT IDENTITY(1,1) PRIMARY KEY,
    programa_id INT NOT NULL,
    chave VARCHAR(100) NOT NULL,
    valor VARCHAR(MAX),
    tipo VARCHAR(50), -- string, int, date, bool
    FOREIGN KEY (programa_id) REFERENCES programa_incentivo(id),
    CONSTRAINT UQ_programa_chave UNIQUE (programa_id, chave)
);

CREATE TABLE execucao_apuracao (
    id INT IDENTITY(1,1) PRIMARY KEY,
    programa_id INT NOT NULL,
    template_id INT NOT NULL,
    ambiente VARCHAR(50) NOT NULL, -- stage/producao
    status VARCHAR(50) NOT NULL,   -- pendente/executando/sucesso/erro
    script_gerado VARCHAR(MAX),
    iniciado_em DATETIME2 NOT NULL DEFAULT GETDATE(),
    finalizado_em DATETIME2,
    mensagem_erro VARCHAR(MAX),
    FOREIGN KEY (programa_id) REFERENCES programa_incentivo(id),
    FOREIGN KEY (template_id) REFERENCES template_sql(id)
);

CREATE TABLE resultado_apuracao (
    id INT IDENTITY(1,1) PRIMARY KEY,
    execucao_id INT NOT NULL,
    entidade_ref VARCHAR(100) NOT NULL,   -- vendedor, loja, etc
    chave_entidade VARCHAR(100) NOT NULL,
    valor_apurado FLOAT NOT NULL,
    observacao VARCHAR(MAX),
    criado_em DATETIME2 NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (execucao_id) REFERENCES execucao_apuracao(id)
);

-- Criação dos Índices
CREATE INDEX ix_regra_programa_id ON regra_apuracao(programa_id);
CREATE INDEX ix_param_programa_id ON parametro_programa(programa_id);
CREATE INDEX ix_exec_programa_id ON execucao_apuracao(programa_id);
CREATE INDEX ix_exec_status ON execucao_apuracao(status);
CREATE INDEX ix_result_execucao_id ON resultado_apuracao(execucao_id);
