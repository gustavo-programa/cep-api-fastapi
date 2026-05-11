from fastapi import FastAPI, Depends, HTTPException # Ferramentas do FastAPI
from sqlalchemy.orm import Session # Tipo da sessão do banco
from . import models, schemas, services, database # Importa nossos arquivos
from .database import engine, get_db # Importa a conexão

# Comando para criar a tabela no MySQL assim que o servidor ligar
models.Base.metadata.create_all(bind=engine)

# Inicia a aplicação
app = FastAPI(title="API de Consulta de CEP Pro", description="Busca com Cache em MySQL")

# Rota principal de consulta
@app.get("/cep/{cep_input}", response_model=schemas.CEPOut)
async def consultar_cep(cep_input: str, db: Session = Depends(get_db)):
    # 1. LIMPEZA: Tira o traço do CEP digitado
    cep_limpo = cep_input.replace("-", "")
    
    # 2. CACHE: Procura se esse CEP já está no nosso MySQL (evita internet lenta)
    db_cep = db.query(models.CEPRecord).filter(models.CEPRecord.cep == cep_limpo).first()
    
    # Se achou no banco, devolve na hora! Mais rápido que o Cruzeiro no contra-ataque
    if db_cep:
        print(f"DEBUG: Achou {cep_limpo} no banco local!")
        return db_cep

    # 3. INTEGRAÇÃO: Se não achou no banco, vai buscar na API externa
    print(f"DEBUG: {cep_limpo} não está no banco. Buscando no ViaCEP...")
    dados_externos = await services.buscar_cep_externo(cep_limpo)
    
    # Se a API externa falhar ou não achar o CEP, dá erro 404
    if not dados_externos:
        raise HTTPException(status_code=404, detail="CEP não encontrado em lugar nenhum!")

    # 4. PERSISTÊNCIA: Salva o que achou na internet no nosso MySQL para a próxima vez
    novo_registro = models.CEPRecord(
        cep=cep_limpo,
        logradouro=dados_externos.get("logradouro"),
        bairro=dados_externos.get("bairro"),
        cidade=dados_externos.get("localidade"),
        estado=dados_externos.get("uf")
    )
    db.add(novo_registro) # Adiciona na fila
    db.commit() # Salva no HD (MySQL)
    db.refresh(novo_registro) # Atualiza o objeto com o ID gerado
    
    return novo_registro # Devolve os dados para o usuário