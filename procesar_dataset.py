"""
Script Principal de Procesamiento y Muestreo del Dataset
Proyecto: Preprocesamiento de Dataset de Concreto
Estudiante: Domingo de Guzman Quispe Mamani
Curso: Visión Computacional - UNSAAC
"""

import os
import shutil
import glob
import cv2
from preprocessor import ConcreteCrackPreprocessor
from generar_reporte_visual import plot_comparison, plot_step_by_step

# Ruta de la caché descargada por kagglehub
CACHE_DIR = r"C:\Users\wtfcl\.cache\kagglehub\datasets\arnavr10880\concrete-crack-images-for-classification\versions\1"
BASE_PROJECT_DIR = r"c:\Users\wtfcl\Desktop\VISION COMPUTACIONAL\proyecto_preprocesamiento"

OUTPUT_RAW_SAMPLE = os.path.join(BASE_PROJECT_DIR, "dataset_muestra_original")
OUTPUT_PROCESSED = os.path.join(BASE_PROJECT_DIR, "dataset_preprocesado")
OUTPUT_REPORT_DIR = os.path.join(BASE_PROJECT_DIR, "reportes_visuales")

# Parámetros del muestreo: cantidad por clase para el repositorio (ligero y representativo)
SAMPLE_PER_CLASS = 250  # 250 Positive + 250 Negative = 500 imágenes perfectas para git

def run():
    print("=" * 60)
    print("INICIANDO PREPROCESAMIENTO DEL DATASET DE CONCRETO")
    print("Estudiante: Domingo de Guzman Quispe Mamani")
    print("=" * 60)

    preprocessor = ConcreteCrackPreprocessor(
        target_size=(224, 224),
        clahe_clip=2.5,
        clahe_grid=(8, 8),
        blur_kernel=(3, 3)
    )

    classes = ["Positive", "Negative"]

    for cls in classes:
        src_cls_dir = os.path.join(CACHE_DIR, cls)
        dest_raw_dir = os.path.join(OUTPUT_RAW_SAMPLE, cls)
        dest_proc_dir = os.path.join(OUTPUT_PROCESSED, cls)

        os.makedirs(dest_raw_dir, exist_ok=True)
        os.makedirs(dest_proc_dir, exist_ok=True)

        # Buscar imágenes jpg/png
        all_images = glob.glob(os.path.join(src_cls_dir, "*.*"))
        print(f"\nClase '{cls}': Encontradas {len(all_images)} imágenes en caché.")

        sample_images = all_images[:SAMPLE_PER_CLASS]
        print(f"-> Muestreando y procesando {len(sample_images)} imágenes para la clase '{cls}'...")

        for idx, img_path in enumerate(sample_images):
            fname = os.path.basename(img_path)
            
            # 1. Copiar muestra original
            dest_raw_file = os.path.join(dest_raw_dir, fname)
            if not os.path.exists(dest_raw_file):
                shutil.copy2(img_path, dest_raw_file)

            # 2. Cargar y preprocesar con OpenCV
            img_bgr = cv2.imread(img_path)
            if img_bgr is None:
                continue

            processed_img = preprocessor.process(img_bgr)

            # 3. Guardar imagen preprocesada (formato 8-bit gray [0, 255])
            dest_proc_file = os.path.join(dest_proc_dir, fname)
            cv2.imwrite(dest_proc_file, processed_img)

            # 4. Generar reportes gráficos comparativos en los primeros ejemplos
            if idx == 0:
                rep_path = os.path.join(OUTPUT_REPORT_DIR, f"comparativa_{cls.lower()}.png")
                plot_comparison(img_bgr, preprocessor, rep_path, title_label=f"Clase: {cls}")
                
                if cls == "Positive":
                    rep_steps_path = os.path.join(OUTPUT_REPORT_DIR, "desglose_paso_a_paso.png")
                    plot_step_by_step(img_bgr, preprocessor, rep_steps_path)

    print("\n" + "=" * 60)
    print("PROCESO COMPLETADO EXITOSAMENTE")
    print(f"1. Muestra Original: {OUTPUT_RAW_SAMPLE}")
    print(f"2. Dataset Preprocesado: {OUTPUT_PROCESSED}")
    print(f"3. Gráficas para Exposición: {OUTPUT_REPORT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    run()
