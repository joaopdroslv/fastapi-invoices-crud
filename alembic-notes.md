### Criar uma migração (revision) com Alembic

1. **Fazer as alterações necessárias nos models**:

- Se um novo model for criado ou houver alterações em um modelo existente, atualize a definição dos models no código.
- Se um novo model for criado, **lembre-se de importá-lo no arquivo `alembic/env.py`**, para que o Alembic consiga detectar e gerar a migração corretamente.

2. **Gerar uma migração**:

- Execute o comando abaixo para gerar a migração:
  ```bash
  alembic revision --autogenerate -m 'MIGRATION_NAME'
  ```
  Este comando vai:
  - Comparar o estado atual do banco de dados com as modificações nos models.
  - Gerar um arquivo de migração que contém as alterações necessárias para sincronizar o banco com os models.
  - O nome da migração (MIGRATION_NAME) deve ser descritivo sobre o que foi alterado (ex.: `add_user_table`, `update_invoice_schema`).

3. **Revisar a migração gerada**:

- O Alembic tenta gerar as migrações automaticamente, mas é sempre bom revisar o arquivo gerado na pasta `migrations/versions/` para garantir que ele está correto. Às vezes, a detecção automática pode não ser perfeita.

4. **Aplicar a migração**:

- Para atualizar o banco de dados para a versão mais recente, execute o comando:
  ```bash
  alembic upgrade head
  ```
  Isso aplica a migração mais recente ao banco de dados.

5. **Rollback (Desfazer migração)**:

- Caso você precise reverter a migração, pode usar o comando:
  ```bash
  alembic downgrade -1
  ```
  Ou para reverter um número específico de migrações:
  ```bash
  alembic downgrade <número_de_versão>
  ```

---

### Comandos úteis:

- **Gerar uma nova migração:**

```bash
alembic revision --autogenerate -m 'MIGRATION_NAME'
```
