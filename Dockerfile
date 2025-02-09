# Usar a imagem oficial do Python
FROM python:3.12.8

# Copiar o conteúdo do projeto para o contêiner
COPY . /app

# Definir diretório de trabalho
WORKDIR /app

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Crie a pasta db, se necessário
RUN mkdir -p /db && touch /db/database.db

# Expor a porta que o FastAPI estará escutando
EXPOSE 8000

# Comando para rodar a aplicação com o Uvicorn
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]