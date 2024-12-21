# Usar a imagem oficial do Python
FROM python:3.12.8-slim

# Copiar o conteúdo do projeto para o contêiner
COPY . /src

# Definir diretório de trabalho
WORKDIR /src

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta que o FastAPI estará escutando
EXPOSE 8000

# Comando para rodar a aplicação com o Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]