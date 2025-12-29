# 🦺 Safety Vision Pipeline

> **Pipeline de Visão Computacional para Detecção de EPIs em Imagens**
> *Reconheça automaticamente o uso de capacetes e outros EPIs em fotos de trabalhadores.*

![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Backend-FastAPI-blue)
![Angular](https://img.shields.io/badge/Frontend-Angular_17+-red)
![Docker](https://img.shields.io/badge/Infra-Docker-2496ED)
![YOLOv8](https://img.shields.io/badge/YOLO-v8n-green)

## 📖 Sobre o Projeto

O **Safety Vision Pipeline** é uma aplicação full-stack para detecção automática de Equipamentos de Proteção Individual (EPIs) em imagens, com foco em capacetes de segurança. O sistema permite o upload de fotos, processa as imagens com um modelo YOLOv8 treinado especificamente para o contexto de segurança do trabalho, e retorna em tempo real o status de cada pessoa detectada.

### 🚀 Principais Funcionalidades

*   **Detecção de EPIs**: Identifica automaticamente capacetes, coletes e outros EPIs em fotos.
*   **Feedback em Tempo Real**: Interface Angular com status dinâmico do processamento.
*   **Arquitetura Modular**: Backend FastAPI, worker YOLOv8, frontend Angular, comunicação via Redis.
*   **Containerização**: Orquestração completa via Docker Compose, com suporte a GPU.
*   **Fine-tuning YOLOv8n**: Modelo YOLOv8n treinado com dataset customizado de capacetes ([Roboflow Worker Safety Dataset](https://app.roboflow.com/gugadev/worker-safety-i1ivk/overview)).

---

## 🛠️ Tecnologias Utilizadas

### Backend & Worker
*   **Python 3.11+**
*   **FastAPI**: API REST para upload e status.
*   **Ultralytics YOLOv8n**: Detecção de objetos (fine-tuning para EPIs).
*   **Redis**: Fila de tarefas e status.
*   **Pytest**: Testes automatizados.

### Frontend
*   **Angular (v17+)**: SPA moderna para upload e visualização.
*   **Signals**: Estado reativo.
*   **CSS Customizado**: Interface amigável.

### Infraestrutura
*   **Docker & Docker Compose**: Orquestração dos serviços.
*   **NVIDIA Container Toolkit**: Suporte a GPU (opcional).

---

## ⚙️ Pré-requisitos

*   [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/install/)
*   *(Opcional)* Drivers NVIDIA e NVIDIA Container Toolkit para aceleração por GPU

---

## 🚀 Como Executar

### 1. Clone o Repositório
```bash
git clone https://github.com/seu-usuario/safety-vision-pipeline.git
cd safety-vision-pipeline
```

### 2. Ajuste as Configurações (se necessário)
- Edite variáveis de ambiente em arquivos `.env` ou diretamente nos arquivos de configuração.

### 3. Inicie os Containers
```bash
docker compose up -d --build
```

### 4. Acesse a Aplicação
*   **Frontend**: [http://localhost:4200](http://localhost:4200)
*   **API Docs (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧠 Fine-tuning do YOLOv8n

O modelo YOLOv8n foi treinado (fine-tuning) com um dataset customizado de imagens de trabalhadores usando e não usando capacetes de segurança, disponível no [Roboflow Worker Safety Dataset](https://app.roboflow.com/gugadev/worker-safety-i1ivk/overview). O dataset inclui anotações para as classes:
- `helmet`
- `no-helmet`
- `person`
- `vest`
- `no-vest`

O treinamento foi realizado para garantir alta precisão na detecção de EPIs em ambientes industriais e de construção.

---

## 📂 Estrutura do Projeto

```
safety-vision-pipeline/
├── api/                 # Backend FastAPI
├── app/                 # Frontend Angular
├── worker/              # Worker YOLOv8 (detecção)
│   ├── src/
│   │   ├── helpers/     # Lógica de verificação de EPIs
│   │   ├── train/       # Scripts de treinamento YOLO
│   │   └── ...
│   └── best.pt          # Modelo YOLOv8n treinado
├── docker-compose.yml   # Orquestração dos serviços
└── README.md
```

---

## 🔮 Melhorias Futuras

*   [ ] Suporte a vídeo e streaming em tempo real
*   [ ] Detecção de outros EPIs (luvas, óculos, etc.)

---

## 📝 Licença

Este projeto está sob a licença MIT. Sinta-se à vontade para contribuir!

---
Desenvolvido por **[Gustavo Camara]** 🚀
[LinkedIn](https://linkedin.com/in/seu-linkedin) | [GitHub](https://github.com/seu-github)
