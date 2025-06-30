import base64
import re
from typing import Any, Union

from i2j.objects import ImageData, ImageJson

async def images2jsonList(images:list[ImageData])->list[ImageJson]:
    """
    Convert a list of images to a JSON-compatible format.
    Each image is represented as a dictionary with filename, content_type, and base64 encoded content.
    """
    images_data = []
    for image in images:
        image_bytes = await image.read()
        image_b64 = base64.b64encode(image_bytes).decode('utf-8')
        images_data.append({
            "filename": image.filename,
            "content_type": image.content_type,
            "base64": image_b64
        })
    return images_data

    """
    Allow path such as:
    "path/to/element"
    "path/to/"array[index]"
    "path/to/element[field=value]" <-- value with no ""
    "path/to/element/array[index]/key"
    "path/to/element/array[field=value]/key"
    "path/to/key[index]/key[field=value]/key" <-- value with no ""
    """
def insert_at_path(
    data: dict[str, Any],
    path: str,
    images_data: list[dict[str, Union[str, list[dict[str, str]]]]],
    mode: str
) -> dict[str, Any]:
    parts = [p for p in path.strip("/").split("/") if p]
    current = data
    parent = None
    last_key = None

    for i, part in enumerate(parts):
        parent = current
        last_key = part

        # Match: key[index]
        if match := re.match(r"(\w+)\[(\d+)\]", part):
            key, index = match.groups()
            index = int(index)
            current = current[key][index]

        # Match: key[field=value]
        elif match := re.match(r"(\w+)\[(\w+)=([^\]]+)\]", part):
            key, field, value = match.groups()
            array = current[key]
            found = next((el for el in array if str(el.get(field)) == value), None)
            if found is None:
                raise KeyError(f"No element in {key} with {field}={value}")
            current = found

        else:
            if part in current:
                current = current[part]
            else:
                raise KeyError(f"Key '{part}' not found in JSON")
    # Ora 'current' è l'elemento dove vogliamo inserire le immagini   
    if isinstance(current, list):
        # Se siamo su un array, aggiungiamo un nuovo elemento
        if mode == "add":
            current.append({"images": images_data})
        else:
            raise ValueError("Cannot update an array directly. Use a specific index or filter.")
    elif isinstance(current, dict):
        # Se siamo su un oggetto, aggiorniamo/sostituiamo "images"
        if mode == "add":
            if "images" not in current:
                current["images"] = []
            current["images"].extend(images_data)
        elif mode == "update":
            current["images"] = images_data
        else:
            raise ValueError(f"Invalid mode: {mode}")
    else:
        raise TypeError("Target element is not suitable for image insertion.")

    return data
