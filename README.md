# Anotador de Vídeo para YOLO

Este repositório contém ferramentas para anotação de vídeos e preparação de datasets para treinamento de modelos YOLO.

## Ferramentas Disponíveis

### 1. Anotador de Vídeo (`label-simulate.py`)

Ferramenta para extrair e anotar frames de vídeos, criando datasets compatíveis com o formato YOLO.

**Funcionalidades:**
- Extração de frames de vídeo
- Interface gráfica para marcação de bounding boxes
- Classificação de objetos (classes 0-5)
- Normalização automática de coordenadas para o formato YOLO
- Controle de velocidade de reprodução
- Navegação entre frames

**Atalhos de Teclado:**
- `q` - Sair do programa
- `n` - Limpar todas as bounding boxes
- `Del` - Limpar todas as bounding boxes
- `s` - Salvar o frame atual com as anotações
- `0-5` - Definir a classe do objeto marcado
- `+` - Aumentar velocidade de reprodução
- `-` - Diminuir velocidade de reprodução
- `a` - Retroceder 5 segundos (150 frames)
- `d` - Avançar 5 segundos (150 frames)

### 2. Organizador de Dataset (`estrutura-yolo.py`)

Ferramenta para organizar as imagens e anotações no formato adequado para treinamento YOLO, separando automaticamente os conjuntos de treino e validação.

**Funcionalidades:**
- Criação automática da estrutura de diretórios para YOLO
- Divisão aleatória entre conjuntos de treino e validação (80/20 por padrão)
- Movimentação de arquivos para os diretórios correspondentes

## Como Usar

### Anotador de Vídeo

1. Configure o caminho do vídeo de entrada e diretórios de saída em `label-simulate.py`:
   ```python
   video_path = "/caminho/para/seu/video.avi"
   output_images = "dataset/images"
   output_labels = "dataset/labels"
   ```

2. Execute o script:
   ```bash
   python label-simulate.py
   ```

3. Use o mouse para desenhar bounding boxes nos objetos
4. Pressione 0-5 para classificar o objeto
5. Pressione 's' para salvar o frame e as anotações
6. Use 'a' e 'd' para navegar pelo vídeo

### Organizador de Dataset

1. Configure os caminhos dos diretórios em `estrutura-yolo.py`:
   ```python
   images_folder = "/caminho/para/dataset/images"
   labels_folder = "/caminho/para/dataset/labels"
   output_folder = "/caminho/para/treino/dataset"
   ```

2. Execute o script:
   ```bash
   python estrutura-yolo.py
   ```

## Estrutura do Dataset Resultante

```
dataset/
├── images/
│   ├── train/
│   └── val/
└── labels/
    ├── train/
    └── val/
```

## Requisitos

- Python 3.6+
- OpenCV (`pip install opencv-python`)
- Os pacotes padrão do Python: os, time, shutil, random
