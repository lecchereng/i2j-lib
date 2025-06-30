import asyncio
import json

from i2j.objects import ImageData
from i2j.utils import images_2_json_list, insert_at_path

# Funzione principale per eseguire lo script
async def main():
# 1. Carica JSON da file
    with open("example.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # 2. Carica immagini locali
    image_paths = ["img1.jpg", "img2.jpg"]
    image_objects = [ImageData(p) for p in image_paths]

    # 3. Converte le immagini in base64
    images_json = await images_2_json_list(image_objects)

    # 4. Inserisci immagini nel JSON
    updated_data = insert_at_path(data, "root/elements[name=anotherExample]/children[1]", images_json, mode="add")

    # 5. Stampa o salva il risultato
    print(json.dumps(updated_data, indent=2))

    # Facoltativo: salva su file
    with open("example_modified.json", "w", encoding="utf-8") as f_out:
        json.dump(updated_data, f_out, indent=2, ensure_ascii=False)

# Esecuzione asincrona
if __name__ == "__main__":
    asyncio.run(main())