
from fastapi import FastAPI, UploadFile, File, HTTPException
from services.file_service import saveUploadedFile, enqueueFile, getStatus

app = FastAPI()


@app.post("/upload")
async def uploadFile(file: UploadFile = File(...)):
    """
    Recebe uma imagem via upload, salva no disco, gera um ticket único,
    enfileira para processamento e retorna o ticket ao usuário.
    Args:
        file (UploadFile): Arquivo enviado via upload.
    Returns:
        dict: Contém o 'file_id' (ticket) e o nome do arquivo.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Arquivo enviado não é uma imagem.")
    
    try:
        file_id, file_path = saveUploadedFile(file)
        enqueueFile(file_id, file_path)
        return {"file_id": file_id, "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar arquivo: {str(e)}")


@app.get("/status/{file_id}")
def checkStatus(file_id: str):
    """
    Consulta o status do processamento de uma imagem pelo ticket.
    Args:
        file_id (str): ID único do arquivo.
    Returns:
        dict: Contém o 'file_id' e o 'status' atual do processamento.
    """
    status = getStatus(file_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Status não encontrado para o ID fornecido.")
    return {"file_id": file_id, "status": status}