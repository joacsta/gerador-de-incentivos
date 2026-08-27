PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS programa_incentivo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    dt_inicio TEXT NOT NULL, -- YYYY-MM-DD
    dt_fim TEXT NOT NULL,    -- YYYY-MM-DD
    ativo INTEGER NOT NULL DEFAULT 1,
    criado_em TEXT NOT NULL DEFAULT (datetime('now')),
    atualizado_em TEXT
);

CREATE TABLE IF NOT EXISTS regra_apuracao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    programa_id INTEGER NOT NULL,
    nome TEXT NOT NULL,
    criterio TEXT NOT NULL, -- JSON/texto
    peso REAL,
    ativo INTEGER NOT NULL DEFAULT 1,
    criado_em TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (programa_id) REFERENCES programa_incentivo(id)
);

CREATE TABLE IF NOT EXISTS template_sql (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    conteudo TEXT NOT NULL,
    versao INTEGER NOT NULL DEFAULT 1,
    ativo INTEGER NOT NULL DEFAULT 1,
    criado_em TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS parametro_programa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    programa_id INTEGER NOT NULL,
    chave TEXT NOT NULL,
    valor TEXT,
    tipo TEXT, -- string, int, date, bool
    FOREIGN KEY (programa_id) REFERENCES programa_incentivo(id),
    UNIQUE (programa_id, chave)
);

CREATE TABLE IF NOT EXISTS execucao_apuracao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    programa_id INTEGER NOT NULL,
    template_id INTEGER NOT NULL,
    ambiente TEXT NOT NULL, -- stage/producao
    status TEXT NOT NULL,   -- pendente/executando/sucesso/erro
    script_gerado TEXT,
    iniciado_em TEXT NOT NULL DEFAULT (datetime('now')),
    finalizado_em TEXT,
    mensagem_erro TEXT,
    FOREIGN KEY (programa_id) REFERENCES programa_incentivo(id),
    FOREIGN KEY (template_id) REFERENCES template_sql(id)
);

CREATE TABLE IF NOT EXISTS resultado_apuracao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    execucao_id INTEGER NOT NULL,
    entidade_ref TEXT NOT NULL,   -- vendedor, loja, etc
    chave_entidade TEXT NOT NULL,
    valor_apurado REAL NOT NULL,
    observacao TEXT,
    criado_em TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (execucao_id) REFERENCES execucao_apuracao(id)
);

CREATE INDEX IF NOT EXISTS ix_regra_programa_id ON regra_apuracao(programa_id);
CREATE INDEX IF NOT EXISTS ix_param_programa_id ON parametro_programa(programa_id);
CREATE INDEX IF NOT EXISTS ix_exec_programa_id ON execucao_apuracao(programa_id);
CREATE INDEX IF NOT EXISTS ix_exec_status ON execucao_apuracao(status);
CREATE INDEX IF NOT EXISTS ix_result_execucao_id ON resultado_apuracao(execucao_id);
