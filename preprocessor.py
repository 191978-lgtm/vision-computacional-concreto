"""
Módulo de Preprocesamiento de Imágenes de Concreto
Proyecto: Detección y Clasificación de Grietas en Superficies de Concreto
Estudiante: Domingo de Guzman Quispe Mamani
Curso: Visión Computacional - UNSAAC
"""

import cv2
import numpy as np


class ConcreteCrackPreprocessor:
    def __init__(self, target_size=(224, 224), clahe_clip=2.5, clahe_grid=(8, 8), blur_kernel=(3, 3)):
        """
        Inicializa los parámetros del pipeline de preprocesamiento.
        
        Args:
            target_size (tuple): Tamaño al que se redimensionará la imagen (W, H).
            clahe_clip (float): Límite de contraste para el algoritmo CLAHE.
            clahe_grid (tuple): Tamaño de la rejilla para la ecualización local adaptativa.
            blur_kernel (tuple): Tamaño del kernel Gaussiano para reducción de ruido.
        """
        self.target_size = target_size
        self.clahe_clip = clahe_clip
        self.clahe_grid = clahe_grid
        self.blur_kernel = blur_kernel
        self.clahe = cv2.createCLAHE(clipLimit=self.clahe_clip, tileGridSize=self.clahe_grid)
        self.morph_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    def resize_bicubic(self, img_bgr):
        """Paso 1: Remuestreo con interpolación bicúbica para máxima conservación de textura."""
        return cv2.resize(img_bgr, self.target_size, interpolation=cv2.INTER_CUBIC)

    def to_grayscale(self, img_bgr):
        """Paso 2: Conversión a escala de grises (eliminación de redundancia cromática)."""
        return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    def reduce_noise(self, img_gray, method="gaussian"):
        """
        Paso 3: Reducción de ruido de textura de alta frecuencia.
        Opciones: 'gaussian' o 'bilateral' (preserva bordes mientras suaviza textura).
        """
        if method == "bilateral":
            return cv2.bilateralFilter(img_gray, d=5, sigmaColor=50, sigmaSpace=50)
        else:
            return cv2.GaussianBlur(img_gray, self.blur_kernel, sigmaX=0)

    def enhance_contrast(self, img_gray):
        """
        Paso 4: Realce adaptativo de contraste local (CLAHE).
        Evita sobreamplificar el ruido mientras expande el rango dinámico de la fisura.
        """
        return self.clahe.apply(img_gray)

    def morphological_refine(self, img_enhanced):
        """
        Paso 5: Operación morfológica para conectar micro-segmentos de la fisura.
        Un cierre morfológico (Dilatación seguida de Erosión) une fisuras interrumpidas.
        """
        # Cierre morfológico: A • B = (A ⊕ B) ⊖ B
        # En escala de grises, para destacar valles oscuros de fisuras se puede usar blackhat o cierre
        closed = cv2.morphologyEx(img_enhanced, cv2.MORPH_CLOSE, self.morph_kernel)
        return closed

    def normalize(self, img_processed):
        """Paso 6: Normalización numérica flotante [0.0, 1.0] para entrenamiento o extracción."""
        return (img_processed.astype(np.float32) / 255.0)

    def process(self, img_bgr, return_all_steps=False):
        """
        Ejecuta el pipeline completo sobre una imagen de entrada.
        """
        step1_resized = self.resize_bicubic(img_bgr)
        step2_gray = self.to_grayscale(step1_resized)
        step3_denoised = self.reduce_noise(step2_gray, method="gaussian")
        step4_enhanced = self.enhance_contrast(step3_denoised)
        step5_morph = self.morphological_refine(step4_enhanced)
        step6_normalized = self.normalize(step5_morph)

        if return_all_steps:
            return {
                "original": img_bgr,
                "resized": step1_resized,
                "gray": step2_gray,
                "denoised": step3_denoised,
                "clahe": step4_enhanced,
                "morph": step5_morph,
                "normalized": step6_normalized
            }
        
        return step5_morph
