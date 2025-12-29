import uuid
import os
import redis
import json
from config import REDIS_HOST, REDIS_PORT, DATA_DIR

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

def saveUploadedFile(file):
    """
    Salva o arquivo enviado no disco e retorna o caminho e o id.
    Args:
        file: Arquivo enviado via upload.
    Returns:
        tuple: (file_id, file_path)
    """
    file_id = str(uuid.uuid4())
    file_path = os.path.join(DATA_DIR, f"{file_id}_{file.filename}")
    with open(file_path, "wb") as f:
        content = file.file.read()
        f.write(content)
    return file_id, file_path

def enqueueFile(file_id, file_path):
    """
    Enfileira o arquivo para processamento e define status inicial.
    Args:
        file_id (str): ID único do arquivo.
        file_path (str): Caminho do arquivo salvo.
    Returns:
        None
    """
    json_str = json.dumps({ "ticket_id": file_id, "file_path": file_path })
    redis_client.lpush("file_queue", json_str)
    redis_client.set(
        f"status:{file_id}",
        json.dumps({
            "code": 102, 
            "status": "aguardando processamento", 
            "final": False
        })
    )


def getStatus(file_id):
    """
    Consulta o status do processamento pelo id.
    Args:
        file_id (str): ID único do arquivo.
    Returns:
        str or None: Status do processamento ou None se não encontrado.
    """
    status = redis_client.get(f"status:{file_id}")
    if status is None:
        return None
    return status.decode("utf-8")
