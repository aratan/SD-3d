import cv2
import numpy as np
import yaml
import os

def generar_plano_cad(imagen_url):
    try:
        # Cargar configuración
        with open("config.yaml", "r") as file:
            config = yaml.safe_load(file)

        # Cargar la imagen
        img = cv2.imread(imagen_url)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Configuración de parámetros
        opencv_config = config['opencv']
        threshold1 = opencv_config['canny_threshold1']
        threshold2 = opencv_config['canny_threshold2']
        hough_threshold = opencv_config['hough_threshold']
        min_line_length = opencv_config['min_line_length']
        max_line_gap = opencv_config['max_line_gap']
        cad_output_path = config['output_paths']['cad_path']

        # Detección de bordes
        edges = cv2.Canny(gray, threshold1, threshold2)

        # Detección de líneas
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, hough_threshold, 
                                minLineLength=min_line_length, maxLineGap=max_line_gap)

        # Crear imagen en blanco para el plano CAD
        plano = np.ones((img.shape[0], img.shape[1], 3), dtype=np.uint8) * 255

        # Dibujar líneas detectadas
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(plano, (x1, y1), (x2, y2), (0, 0, 0), 2)

        # Guardar el plano
        cv2.imwrite(cad_output_path, plano)
        return cad_output_path
    except Exception as e:
        print(f"Error al generar el plano CAD: {e}")
        return None