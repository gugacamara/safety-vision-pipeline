import redis
import json
from ultralytics import YOLO
from config import REDIS_HOST, REDIS_PORT
from helpers.epi_helpers import EpiHelper
from utils.logger_utils import get_logger

logger = get_logger("worker")
logger.info("Worker iniciado e aguardando tarefas...")
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
model = YOLO("best.pt")

while True:
    try:
        _, task = redis_client.brpop("file_queue")
        data = json.loads(task)
        ticket_id = data["ticket_id"]
        file_path = data["file_path"]

        logger.info(f"Nova tarefa recebida: ticket_id={ticket_id}, file_path={file_path}")
        redis_client.set(
            f"status:{ticket_id}", 
            json.dumps({
                "code": 100, 
                "status": "em processamento", 
                "final": False
            })
        )
        # Processamento YOLO
        try:
            results = model(file_path)
            detections = json.loads(results[0].to_json())
            epis_list = ['helmet']  # Elementos a serem verificados
            persons = EpiHelper.verifyPersons(detections, epis_list)
            logger.info(f"Processamento concluído: ticket_id={ticket_id}")
            if not persons:
                logger.warning(f"Nenhuma pessoa detectada na imagem: ticket_id={ticket_id} dados={detections} persons={persons}")
            if any(not p.get('complete', False) for p in persons):
                logger.warning(f"Pelo menos uma pessoa sem todos os EPIs para ticket_id={ticket_id}: {persons}")

            redis_client.set(
                f"status:{ticket_id}",
                json.dumps({
                    "code": 200,
                    "status": "concluido",
                    "final": True,
                    "result": persons
                })
            )
            logger.debug(f"Resultado salvo no Redis para ticket_id={ticket_id}")
        except Exception as e:
            redis_client.set(
                f"status:{ticket_id}",
                json.dumps({
                    "code": 500,
                    "status": "erro no processamento",
                    "final": True,
                    "error": str(e)
                })
            )
            logger.error(f"Erro ao processar imagem {file_path}: {str(e)}")
            continue
    except Exception as e:
        logger.error(f"Erro geral no worker: {str(e)}")
        continue