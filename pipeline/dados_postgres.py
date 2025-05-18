import requests
from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from time import sleep
import os
from dotenv import load_dotenv


load_dotenv()

# Configurações do banco de dados
DATABASE_URL = os.getenv('DB_URL')
# Criação do engine e sessão
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

#Definir modelo dos dos dados
class CryptoPrice(Base):
    __tablename__ = 'crypto_prices'
    id = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(Float)
    cripto = Column(String(10))
    moeda = Column(String(10))
    timestamp = Column(DateTime)
# Criação da tabela
Base.metadata.create_all(engine)
# Função para extrair dados da API
def extrair_dados():
    # URL da API
    url = "https://api.coinbase.com/v2/prices/spot"
    # Fazendo a requisição GET
    response = requests.get(url)
    return response.json()
# Função para transformar os dados
def tratar_dados_cripto(dados_json):
    valor = float(dados_json['data']['amount'])
    cripto = dados_json['data']['base']
    moeda = dados_json['data']['currency']
    dados_tratados = CryptoPrice (
        valor=valor,
        cripto=cripto,
        moeda=moeda,
        timestamp=datetime.now()
    )
    return dados_tratados
def salvar_dados_sqlalqemy(dados):
    with Session() as session:
        session.add(dados)
        session.commit()
        print("Dados inseridos com sucesso!")
# Função principal
def main():
    while True:
        # Chamando a função para extrair os dados
        dados_json = extrair_dados()
        dados_tratados = tratar_dados_cripto(dados_json)
        #salvar dados no banco
        salvar_dados_sqlalqemy(dados_tratados)
        sleep(1 * 60)  # Espera 1 minuto antes de fazer a próxima requisição
       
if __name__ == "__main__":
    main()