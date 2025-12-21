
class EpiHelper:

  @staticmethod
  def verifyPersons(detections: list, epi_list: list) -> list:
    """
    Para cada pessoa detectada, verifica se ela está usando todos os EPIs da lista.
    Args:
        detections (list): Lista de detecções do YOLO.
        epi_list (list): Lista de EPIs a serem verificados (ex: ["helmet", "mask"]).
    Returns:
        list: Lista de dicionários, um para cada pessoa, indicando quais EPIs ela está usando e se está com todos.
    """
    if not isinstance(detections, list) or not detections:
        return []

    persons = [d for d in detections if d.get("class") == "person"]
    # Cria um dicionário: {"helmet": [...], "mask": [...], ...}
    epis_detected = {epi: [d for d in detections if d.get("class") == epi] for epi in epi_list}

    result = []
    for p in persons:
        p_bbox = p["bbox"]
        person_result = {"person_bbox": p_bbox}
        equipped_person = True
        for epi in epi_list:
            has_epi = EpiHelper.isEpiPresent(p_bbox, [e["bbox"] for e in epis_detected[epi]])
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
    return not (x1_max < x2_min or x2_max < x1_min or y1_max < y2_min or y2_max < y1_min)