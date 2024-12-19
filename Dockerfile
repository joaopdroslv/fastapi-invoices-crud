# Usar a imagem oficial do Python
FROM python:3.12.8-slim

# Copiar o conteúdo do projeto para o contêiner
COPY . /invoices

# Definir diretório de trabalho
WORKDIR /invoices

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta que o FastAPI estará escutando
EXPOSE 8000

# Comando para rodar a aplicação com o Uvicorn
CMD ["uvicorn", "invoices.main:app", "--host", "0.0.0.0", "--port", "8000"]