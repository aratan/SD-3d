import cv2
import numpy as np
import trimesh
import yaml
import os

def procesar_imagen(imagen_url):
    try:
        # Cargar configuración
        with open("config.yaml", "r") as file:
            config = yaml.safe_load(file)

        # Cargar la imagen
        img = cv2.imread(imagen_url)
        if img is None:
            print("No se pudo cargar la imagen.")
            return None
        
        # Convertir a escala de grises
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Aplicar un filtro para suavizar la imagen
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Configuración de parámetros
        opencv_config = config['opencv']
        threshold1 = opencv_config['canny_threshold1']
        threshold2 = opencv_config['canny_threshold2']
        hough_threshold = opencv_config['hough_threshold']
        min_line_length = opencv_config['min_line_length']
        max_line_gap = opencv_config['max_line_gap']

        # Detectar bordes
        edges = cv2.Canny(blurred, threshold1, threshold2)

        # Detectar líneas con Hough Transform
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, hough_threshold, minLineLength=min_line_length, maxLineGap=max_line_gap)
        return lines

    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
        return None

def generar_modelo_3d(lines, height=10):
    try:
        # Cargar configuración
        with open("config.yaml", "r") as file:
            config = yaml.safe_load(file)

        vertices = []
        faces = []

        if lines is None:
            return None

        # Encontrar los límites del plano
        min_x, min_y = float('inf'), float('inf')
        max_x, max_y = float('-inf'), float('-inf')

        for line in lines:
            x1, y1, x2, y2 = line[0]
            min_x = min(min_x, x1, x2)
            min_y = min(min_y, y1, y2)
            max_x = max(max_x, x1, x2)
            max_y = max(max_y, y1, y2)

        # Calcular el centro del plano
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2

        for line in lines:
            x1, y1, x2, y2 = line[0]

            # Crear puntos de la base y la parte superior
            base_v1 = [x1, y1, 0]
            base_v2 = [x2, y2, 0]
            top_v1 = [x1, y1, height]
            top_v2 = [x2, y2, height]

            # Añadir los vértices originales
            idx = len(vertices)
            vertices.extend([base_v1, base_v2, top_v1, top_v2])

            # Crear las caras del modelo 3D (extrusión)
            faces.append([idx, idx + 1, idx + 2])
            faces.append([idx + 1, idx + 3, idx + 2])

            # Aplicar simetría
            sym_x1 = 2 * center_x - x1
            sym_x2 = 2 * center_x - x2

            # Crear puntos simétricos
            sym_base_v1 = [sym_x1, y1, 0]
            sym_base_v2 = [sym_x2, y2, 0]
            sym_top_v1 = [sym_x1, y1, height]
            sym_top_v2 = [sym_x2, y2, height]

            # Añadir los vértices simétricos
            idx = len(vertices)
            vertices.extend([sym_base_v1, sym_base_v2, sym_top_v1, sym_top_v2])

            # Crear las caras simétricas
            faces.append([idx, idx + 1, idx + 2])
            faces.append([idx + 1, idx + 3, idx + 2])

        # Crear el objeto 3D con trimesh
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

        # Guardar el modelo en un archivo .obj
        output_path = config['output_paths']['obj_path']
        mesh.export(output_path)
        print(f"Modelo 3D guardado en: {output_path}")
        return output_path

    except Exception as e:
        print(f"Error al generar el modelo 3D: {e}")
        return None
