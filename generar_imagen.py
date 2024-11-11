import torch
from diffusers import StableDiffusionPipeline
import yaml
import os

def generar_imagen_casa(prompt):
    try:
        # Verificar si el archivo config.yaml existe
        if not os.path.exists("config.yaml"):
            print("Error: El archivo config.yaml no se encuentra.")
            return None

        # Cargar configuración desde archivo YAML
        with open("config.yaml", "r") as file:
            config = yaml.safe_load(file)
            print(f"Configuración cargada: {config}")

        # Verificar si 'stable_diffusion' está en la configuración
        if 'stable_diffusion' not in config:
            print("Error: La sección 'stable_diffusion' falta en config.yaml.")
            return None

        sd_config = config['stable_diffusion']
        model_id = sd_config.get('model_id')
        output_dir = sd_config.get('output_dir')

        if not model_id or not output_dir:
            print("Error: 'model_id' o 'output_dir' faltan en la sección 'stable_diffusion' de config.yaml.")
            return None

        # Procesar el modelo de difusión
        pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
        pipe = pipe.to("cuda")
        
        # Generar la imagen
        image = pipe(prompt).images[0]
        
        # Crear el directorio de salida si no existe
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Guardar la imagen generada
        output_path = os.path.join(output_dir, "casa_generada.png")
        image.save(output_path)
        print(f"Imagen generada y guardada en: {output_path}")
        return output_path

    except Exception as e:
        print(f"Error al generar la imagen de la casa: {e}")
        return None