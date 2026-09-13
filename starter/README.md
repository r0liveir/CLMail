# CLMail — skeleton starter

Skeleton directory with ready boilerplate code for CLMail.

What's provided:
- models, tables and relations with SQLAlchemy
- initial repository and service layers
- database config, seed and print rules
- reading email through CLI usage
- Example messages

Also, one `add_task` service function is already provided.

What's missing (mainly on `main.py` and `service.py`):
- Contract `TaskAction`
- Model instructions
- OpenAI config
- Routing from action to service

## Executing

```bash
$ export GROQ_API_KEY="sua-chave-aqui"
$ uv sync
$ uv run clmail src/texts/add_task.txt
```

Current code does not work as is. Fill in the gaps.
