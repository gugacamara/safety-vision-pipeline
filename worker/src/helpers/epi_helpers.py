
"""
Helper class para verificação de EPIs (Equipamentos de Proteção Individual)
na detecção de pessoas usando caixas delimitadoras (bboxes).
"""
class EpiHelper:

  @staticmethod
  def verifyPersons(detections: list, epi_list: list) -> list:
    """
    Para cada pessoa detectada, verifica se ela está usando todos os EPIs da lista.
    Considera 'no-helmet' e 'no-vest' como ausência do EPI correspondente.
    Args:
        detections (list): Lista de detecções do YOLO.
        epi_list (list): Lista de EPIs a serem verificados (ex: ["helmet", "vest"]).
    Returns:
        list: Lista de dicionários, um para cada pessoa, indicando quais EPIs ela está usando e se está com todos.
    """
    if not isinstance(detections, list) or not detections:
        return []

    persons = [d for d in detections if d.get("name") == "person"]
    epis_map = {epi: [d for d in detections if d.get("name") == epi] for epi in epi_list}
    no_epi_map = {f"no-{epi}": [d for d in detections if d.get("name") == f"no-{epi}"] for epi in epi_list}

    result = []
    for p in persons:
        p_bbox = [p["box"]["x1"], p["box"]["y1"], p["box"]["x2"], p["box"]["y2"]]
        person_result = {"person_bbox": p_bbox}
        equipped_person = True

        for epi in epi_list: # A cada pessoa, verifica cada ocorrência do EPI e no-EPI
            epi_bboxes = [
                [e["box"]["x1"], e["box"]["y1"], e["box"]["x2"], e["box"]["y2"]]
                for e in epis_map[epi]
            ]
            no_epi_bboxes = [
                [e["box"]["x1"], e["box"]["y1"], e["box"]["x2"], e["box"]["y2"]]
                for e in no_epi_map.get(f"no-{epi}", [])
            ]
            # Se houver "no-epi" sobrepondo, considera como ausência do EPI
            if EpiHelper.isEpiPresent(p_bbox, no_epi_bboxes):
                has_epi = False
            else:
                has_epi = EpiHelper.isEpiPresent(p_bbox, epi_bboxes)
            person_result[epi] = has_epi
            
            if not has_epi:
                equipped_person = False

        person_result["complete"] = equipped_person
        result.append(person_result)

    return result

  @staticmethod
  def isEpiPresent(person_bbox: list, epi_bboxes: list) -> bool:
    """
    Verifica se algum EPI está sobreposto à pessoa (pela bbox).
    Args:
        person_bbox (list): Caixa delimitadora da pessoa.
        epi_bboxes (list): Lista de caixas dos EPIs.
    Returns:
        bool: True se o EPI está sobreposto, False caso contrário.
    """
    for epi_bbox in epi_bboxes:
        if EpiHelper.bboxesOverlap(person_bbox, epi_bbox):
            return True
    return False

  @staticmethod
  def bboxesOverlap(bbox1: list, bbox2: list) -> bool:
    """
    Verifica se duas caixas delimitadoras (bboxes) se sobrepõem.
    Args:
        bbox1 (list): [x1_min, y1_min, x1_max, y1_max]
        bbox2 (list): [x2_min, y2_min, x2_max, y2_max]
    Returns:
        bool: True se as caixas se sobrepõem, False caso contrário.
    """
    x1_min, y1_min, x1_max, y1_max = bbox1
    x2_min, y2_min, x2_max, y2_max = bbox2
    return not ((x1_max < x2_min or x2_max < x1_min) or (y1_max < y2_min or y2_max < y1_min)) # se apenas uma das condições for verdadeira, não há sobreposição