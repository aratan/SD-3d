import os
import yaml
from generar_imagen import generar_imagen_casa
from generar_plano import generar_plano_cad
from generar_modelo import procesar_imagen, generar_modelo_3d

def cargar_configuracion():
    try:
        with open("config.yaml", "r") as file:
            config = yaml.safe_load(file)
        print(f"Configuración cargada: {config}")
        return config
    except FileNotFoundError:
        print("Error: El archivo config.yaml no se encuentra.")
        return None
    except yaml.YAMLError as e:
        print(f"Error al leer el archivo config.yaml: {e}")
        return None

def main():
    config = cargar_configuracion()
    if not config:
        return

    prompt = "Una casa de cristal moderna de dos pisos con grandes ventanales, en planos"
    
    # Generar la imagen de la casa
    imagen_path = generar_imagen_casa(prompt)
    
    if imagen_path:
        # Generar el plano CAD
        plano_path = generar_plano_cad(imagen_path)
        
        if plano_path:
            print(f"El plano CAD se ha guardado en: {plano_path}")
            
            # Procesar la imagen para obtener las líneas
            lines = procesar_imagen(plano_path)

            # Generar el modelo 3D a partir de las líneas detectadas
            if lines is not None:
                modelo_path = generar_modelo_3d(lines)
                if modelo_path:
                    print(f"El modelo 3D se ha guardado en: {modelo_path}")
                else:
                    print("No se pudo generar el modelo 3D.")
            else:
                print("No se pudieron detectar líneas en la imagen.")
        else:
            print("No se pudo generar el plano CAD.")
    else:
        print("No se pudo generar la imagen de la casa.")

if __name__ == "__main__":
    main()