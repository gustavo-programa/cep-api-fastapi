import httpx # Biblioteca moderna para fazer requisições HTTP (tipo um navegador via código)

# Função assíncrona para buscar o CEP na internet
async def buscar_cep_externo(cep: str):
    # Remove qualquer traço ou ponto que o usuário tenha digitado
    cep_limpo = cep.replace("-", "").replace(".", "")
    
    # URL da API pública do ViaCEP
    url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
    
    # Abre um cliente de conexão temporário
    async with httpx.AsyncClient() as client:
        response = await client.get(url) # Faz a chamada na URL
        
        # Se o site externo responder erro, retornamos "Nada"
        if response.status_code != 200:
            return None
        
        dados = response.json() # Transforma a resposta em um dicionário Python
        
        # O ViaCEP retorna {"erro": true} se o CEP não existir
        if "erro" in dados:
            return None
            
        return dados # Retorna os dados crus da internet