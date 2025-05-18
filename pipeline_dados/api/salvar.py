from pipeline_dados.api.dados_postgres import extrair_dados, tratar_dados_cripto, salvar_dados_sqlalqemy

def handler(request):
    try:
        dados_json = extrair_dados()  # Adicione indentação aqui
        dados_tratados = tratar_dados_cripto(dados_json)
        salvar_dados_sqlalqemy(dados_tratados)
        return {
            "statusCode": 200,
            "body": "Dados salvos com sucesso!"
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error ao salvar dados: {str(e)}"  # Corrigi a formatação aqui
        }