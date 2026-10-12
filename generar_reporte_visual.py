"""
Generador de Visualizaciones Comparativas e Histogramas
Proyecto: Preprocesamiento de Dataset de Concreto
Estudiante: Domingo de Guzman Quispe Mamani
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from preprocessor import ConcreteCrackPreprocessor


def plot_comparison(original_bgr, preprocessor, save_path, title_label="Grieta de Concreto (Positive)"):
    """
    Genera una figura comparativa de 4 paneles:
    1. Imagen Original
    2. Imagen Preprocesada (Filtrado Gaussiano + CLAHE + Morfología)
    3. Histograma de la imagen original en escala de grises
    4. Histograma de la imagen preprocesada (mostrando la redistribución y ecualización de frecuencias)
    """
    steps = preprocessor.process(original_bgr, return_all_steps=True)
    
    gray_orig = steps["gray"]
    processed = steps["morph"]
    
    # Calcular histogramas
    hist_orig = cv2.calcHist([gray_orig], [0], None, [256], [0, 256])
    hist_proc = cv2.calcHist([processed], [0], None, [256], [0, 256])

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f"Pipeline de Preprocesamiento: {title_label}\nEstudiante: Domingo de Guzman Quispe Mamani - Visión Computacional", fontsize=14, fontweight='bold')

    # Panel 1: Original
    img_rgb = cv2.cvtColor(steps["resized"], cv2.COLOR_BGR2RGB)
    axes[0, 0].imshow(img_rgb)
    axes[0, 0].set_title(f"1. Imagen Original (Bicubic 224x224)\n[Bajo contraste, textura granular]")
    axes[0, 0].axis('off')

    # Panel 2: Preprocesada
    axes[0, 1].imshow(processed, cmap='gray')
    axes[0, 1].set_title(f"2. Resultado Final (Denoise + CLAHE + Morfología)\n[Fisuras destacadas, contraste optimizado]")
    axes[0, 1].axis('off')

    # Panel 3: Histograma Original
    axes[1, 0].plot(hist_orig, color='steelblue', lw=2)
    axes[1, 0].fill_between(range(256), hist_orig.flatten(), color='steelblue', alpha=0.3)
    axes[1, 0].set_title("3. Histograma Original (Rango Dinámico Comprimido)")
    axes[1, 0].set_xlabel("Nivel de Gris (0 - 255)")
    axes[1, 0].set_ylabel("Frecuencia (Píxeles)")
    axes[1, 0].grid(True, linestyle='--', alpha=0.5)
    axes[1, 0].set_xlim([0, 256])

    # Panel 4: Histograma Preprocesado
    axes[1, 1].plot(hist_proc, color='darkgreen', lw=2)
    axes[1, 1].fill_between(range(256), hist_proc.flatten(), color='darkgreen', alpha=0.3)
    axes[1, 1].set_title("4. Histograma tras CLAHE (Rango Dinámico Expandido)")
    axes[1, 1].set_xlabel("Nivel de Gris (0 - 255)")
    axes[1, 1].set_ylabel("Frecuencia (Píxeles)")
    axes[1, 1].grid(True, linestyle='--', alpha=0.5)
    axes[1, 1].set_xlim([0, 256])

    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Gráfica guardada en: {save_path}")


def plot_step_by_step(original_bgr, preprocessor, save_path):
    """
    Muestra la descomposición paso a paso de todas las etapas del pipeline.
    """
    steps = preprocessor.process(original_bgr, return_all_steps=True)

    fig, axes = plt.subplots(1, 5, figsize=(20, 4))
    
    stages = [
        ("Original (Color)", cv2.cvtColor(steps["resized"], cv2.COLOR_BGR2RGB), None),
        ("Paso 1: Grises", steps["gray"], 'gray'),
        ("Paso 2: Denoise Gaussiano", steps["denoised"], 'gray'),
        ("Paso 3: Realce CLAHE", steps["clahe"], 'gray'),
        ("Paso 4: Cierre Morfológico", steps["morph"], 'gray')
    ]

    for idx, (title, img, cmap) in enumerate(stages):
        if cmap:
            axes[idx].imshow(img, cmap=cmap)
        else:
            axes[idx].imshow(img)
        axes[idx].set_title(title, fontsize=11, fontweight='bold')
        axes[idx].axis('off')

    plt.suptitle("Desglose Paso a Paso del Pipeline de Preprocesamiento", fontsize=14, fontweight='bold')
    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Desglose por pasos guardado en: {save_path}")
