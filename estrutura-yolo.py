import os
import shutil
import random

# Definir caminhos das pastas (MODIFIQUE CONFORME NECESSÁRIO)
images_folder = "/home/bruno/testando/dataset/images"  # Pasta com imagens
labels_folder = "/home/bruno/testando/dataset/labels"   # Pasta com .txt

output_folder = "/home/bruno/testando/treino/dataset"  # Onde o dataset será salvo

# Criar estrutura de diretórios
os.makedirs(f"{output_folder}/images/train", exist_ok=True)
os.makedirs(f"{output_folder}/images/val", exist_ok=True)
os.makedirs(f"{output_folder}/labels/train", exist_ok=True)
os.makedirs(f"{output_folder}/labels/val", exist_ok=True)

# Listar todas as imagens
image_files = [f for f in os.listdir(images_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

# Embaralhar as imagens para aleatorizar a separação
random.shuffle(image_files)

# Definir proporção de treino e validação
train_ratio = 0.8
train_size = int(len(image_files) * train_ratio)

train_images = image_files[:train_size]
val_images = image_files[train_size:]

# Função para mover arquivos
def move_files(image_list, split):
    for image_name in image_list:
        # Caminho original da imagem
        src_img = os.path.join(images_folder, image_name)
        # Caminho original da label correspondente
        txt_name = os.path.splitext(image_name)[0] + ".txt"
        src_txt = os.path.join(labels_folder, txt_name)

        # Caminhos de destino
        dst_img = os.path.join(output_folder, f"images/{split}", image_name)
        dst_txt = os.path.join(output_folder, f"labels/{split}", txt_name)

        # Mover arquivos se existirem
        if os.path.exists(src_img):
            shutil.move(src_img, dst_img)
        if os.path.exists(src_txt):
            shutil.move(src_txt, dst_txt)

# Mover arquivos para treino e validação
move_files(train_images, "train")
move_files(val_images, "val")

print("✅ Dataset organizado com sucesso!")
