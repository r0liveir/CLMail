# CLMail — starter da aula

Este diretório contém o boilerplate do CLMail para que a aula se concentre na
integração com o modelo.

Já estão prontos:

- models e relacionamentos do SQLAlchemy;
- repository e regras iniciais do service;
- criação, população e impressão do banco em memória;
- leitura do e-mail e estrutura da CLI;
- mensagens de exemplo.

Serão implementados durante a aula, diretamente em `src/clmail/main.py`:

1. o contrato `TaskAction`;
2. o prompt;
3. a extração com OpenAI SDK e, depois, com PydanticAI;
4. o roteamento da ação para o service.

O fluxo permanece linear na primeira aplicação: ler o e-mail, chamar o modelo,
obter a ação, abrir a sessão e encaminhar a operação com `match`. Não há helpers
para esconder essas etapas; apenas o boilerplate do banco foi separado.

## Executando

```bash
$ export GROQ_API_KEY="sua-chave-aqui"
$ uv sync
$ uv run clmail src/texts/add_task.txt
```

Antes da implementação feita em aula, o comando termina nos
`NotImplementedError` marcados em `main.py`. Durante a aula, remova cada um ao
adicionar a chamada e o roteamento. A versão completa está no diretório pai.
