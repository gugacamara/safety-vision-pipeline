import os
import redis
import json
from ultralytics import YOLO
from config import REDIS_HOST, REDIS_PORT
from helpers.epi_helpers import EpiHelper
from utils.logger_utils import get_logger

logger = get_logger("worker")
logger.info("Worker iniciado e aguardando tarefas...")
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
model = YOLO("yolov8n.pt")


while True:
    try:
        _, task = redis_client.brpop("file_queue")
        data = json.loads(task)
        ticket_id = data["ticket_id"]
        file_path = data["file_path"]

        logger.info(f"Nova tarefa recebida: ticket_id={ticket_id}, file_path={file_path}")
        redis_client.set(f"status:{ticket_id}", "processando")
        # Processamento YOLO
        try:
            results = model(file_path)
            detections = json.loads(results[0].tojson())
            epis_list = ['helmet', 'mask']  # Elementos a serem verificados
            persons = EpiHelper.verifyPersons(detections, epis_list)
            logger.info(f"Processamento concluído: ticket_id={ticket_id}")
            if not persons:
                logger.warning(f"Nenhuma pessoa detectada na imagem: ticket_id={ticket_id}")
            if any(not p.get('complete', False) for p in persons):
                logger.warning(f"Pelo menos uma pessoa sem todos os EPIs para ticket_id={ticket_id}: {persons}")
        except Exception as e:
            redis_client.set(f"status:{ticket_id}", "erro no processamento")
            redis_client.set(f"result:{ticket_id}", str(e))
            logger.error(f"Erro ao processar imagem {file_path}: {str(e)}")
            continue

        # Salva o resultado do processamento no Redis
        redis_client.set(f"result:{ticket_id}", persons)
        redis_client.set(f"status:{ticket_id}", "concluido")
        logger.debug(f"Resultado salvo no Redis para ticket_id={ticket_id}")
    except Exception as e:
        logger.error(f"Erro geral no worker: {str(e)}")
        continue