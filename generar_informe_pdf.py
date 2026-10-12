"""
Generador del Informe Académico Formal en formato PDF con Renderizado de Fórmulas Matemáticas
Proyecto: Preprocesamiento de Dataset de Imágenes de Concreto
Estudiante: Domingo de Guzman Quispe Mamani
Asignatura: Visión Computacional - UNSAAC
"""

import os
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

BASE_DIR = r"c:\Users\wtfcl\Desktop\VISION COMPUTACIONAL\proyecto_preprocesamiento"
OUTPUT_PDF = os.path.join(BASE_DIR, "Informe_Preprocesamiento_Domingo_Quispe.pdf")
IMG_DIR = os.path.join(BASE_DIR, "reportes_visuales")
FORMULAS_DIR = os.path.join(IMG_DIR, "formulas")


def render_latex_formula(latex_str, fname, fontsize=14, fig_width=6, fig_height=0.9):
    """
    Renderiza una expresión matemática LaTeX con el motor mathtext de matplotlib
    y la guarda como imagen PNG transparente de alta resolución.
    """
    os.makedirs(FORMULAS_DIR, exist_ok=True)
    fpath = os.path.join(FORMULAS_DIR, fname)
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.text(0.5, 0.5, latex_str, fontsize=fontsize, ha='center', va='center', color='#1A365D')
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(fpath, dpi=300, bbox_inches='tight', transparent=True)
    plt.close()
    return fpath


class NumberedCanvas(canvas.Canvas):
    """Canvas de dos pasadas para numerar páginas dinámicamente y agregar encabezado/pie."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Portada limpia

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4A5568"))

        # Encabezado
        self.drawString(54, 750, "UNSAAC — Visión Computacional | Informe Técnico de Preprocesamiento")
        self.drawRightString(558, 750, "Estudiante: Domingo de Guzman Quispe Mamani")
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(54, 744, 558, 744)

        # Pie de página
        self.line(54, 45, 558, 45)
        self.drawString(54, 32, "Proyecto Semestral: Detección y Clasificación de Grietas en Concreto")
        self.drawRightString(558, 32, f"Página {self._pageNumber} de {page_count}")
        self.restoreState()


def build_pdf():
    # 1. Pre-renderizar fórmulas matemáticas como imágenes vectorizadas nítidas
    f1_path = render_latex_formula(
        r'$Y = 0.299 \cdot R + 0.587 \cdot G + 0.114 \cdot B$',
        'formula_luminancia.png', fontsize=13, fig_width=5.5, fig_height=0.6
    )
    f2_path = render_latex_formula(
        r'$g(x, y) = f(x, y) + \eta(x, y)$',
        'formula_ruido.png', fontsize=13, fig_width=4.5, fig_height=0.6
    )
    f3_path = render_latex_formula(
        r'$G(x, y) = \frac{1}{2\pi \sigma^2} \exp\left(-\frac{x^2 + y^2}{2\sigma^2}\right)$',
        'formula_gaussiana.png', fontsize=14, fig_width=5.5, fig_height=0.8
    )
    f4_path = render_latex_formula(
        r'$A \bullet B = (A \oplus B) \ominus B$',
        'formula_cierre.png', fontsize=14, fig_width=4.5, fig_height=0.6
    )

    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CoverTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=24, leading=28,
        textColor=colors.HexColor("#1A365D"), alignment=1
    )
    subtitle_style = ParagraphStyle(
        'CoverSubtitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=13, leading=18,
        textColor=colors.HexColor("#2B6CB0"), alignment=1
    )
    meta_style = ParagraphStyle(
        'CoverMeta', parent=styles['Normal'],
        fontName='Helvetica', fontSize=10, leading=15,
        textColor=colors.HexColor("#2D3748"), alignment=1
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=14.5, leading=18.5,
        textColor=colors.HexColor("#1A365D"), spaceBefore=14, spaceAfter=6, keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Heading2_Custom', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=11, leading=15,
        textColor=colors.HexColor("#2B6CB0"), spaceBefore=10, spaceAfter=4, keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9.5, leading=13.5,
        textColor=colors.HexColor("#2D3748"), spaceAfter=6
    )
    bullet_style = ParagraphStyle(
        'Bullet_Custom', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9.5, leading=13.5,
        textColor=colors.HexColor("#2D3748"), leftIndent=15, spaceAfter=3
    )
    caption_style = ParagraphStyle(
        'Caption_Text', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=8, leading=10,
        textColor=colors.HexColor("#718096"), alignment=1, spaceAfter=8
    )

    def formula_table(img_path, eq_num, w=240, h=30):
        """Crea un bloque centrado para la ecuación con su número de ecuación a la derecha."""
        img = Image(img_path, width=w, height=h)
        num_p = Paragraph(f"<b>({eq_num})</b>", ParagraphStyle('EqNum', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, alignment=2, textColor=colors.HexColor("#4A5568")))
        t = Table([[img, num_p]], colWidths=[440, 50], hAlign='CENTER')
        t.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        return t

    story = []

    # ==========================================
    # 1. PORTADA FORMAL
    # ==========================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("UNIVERSIDAD NACIONAL DE SAN ANTONIO ABAD DEL CUSCO", ParagraphStyle('Inst', parent=title_style, fontSize=13, leading=16, textColor=colors.HexColor("#4A5568"))))
    story.append(Spacer(1, 6))
    story.append(Paragraph("FACULTAD DE INGENIERÍA ELÉCTRICA, ELECTRÓNICA, INFORMÁTICA Y MECÁNICA", ParagraphStyle('Fac', parent=title_style, fontSize=10, leading=13, textColor=colors.HexColor("#718096"))))
    story.append(Paragraph("DEPARTAMENTO ACADÉMICO DE INFORMÁTICA", ParagraphStyle('Dept', parent=title_style, fontSize=9.5, leading=12, textColor=colors.HexColor("#718096"))))
    story.append(Spacer(1, 40))

    story.append(HRFlowable(width="90%", thickness=2.5, color=colors.HexColor("#1A365D"), spaceBefore=0, spaceAfter=20))
    story.append(Paragraph("INFORME TÉCNICO DE PREPROCESAMIENTO DE DATASET", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Detección y Clasificación Automatizada de Fisuras y Grietas en Superficies de Concreto", subtitle_style))
    story.append(HRFlowable(width="90%", thickness=1, color=colors.HexColor("#CBD5E0"), spaceBefore=20, spaceAfter=25))

    story.append(Spacer(1, 30))

    meta_table_data = [
        [Paragraph("<b>Asignatura:</b>", meta_style), Paragraph("Visión Computacional", meta_style)],
        [Paragraph("<b>Docente:</b>", meta_style), Paragraph("Prof. Hans H. Ccacyahuillca Bejar", meta_style)],
        [Paragraph("<b>Estudiante:</b>", meta_style), Paragraph("Domingo de Guzman Quispe Mamani", meta_style)],
        [Paragraph("<b>Modalidad:</b>", meta_style), Paragraph("Individual", meta_style)],
        [Paragraph("<b>Entrega:</b>", meta_style), Paragraph("Fase 1 — Selección y Preprocesamiento de Dataset", meta_style)],
        [Paragraph("<b>Semestre / Fecha:</b>", meta_style), Paragraph("Cusco, Octubre 2026", meta_style)]
    ]
    t_meta = Table(meta_table_data, colWidths=[130, 250], hAlign='CENTER')
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F7FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#E2E8F0")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#EDF2F7")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(t_meta)

    story.append(PageBreak())

    # ==========================================
    # 2. RESUMEN EJECUTIVO
    # ==========================================
    story.append(Paragraph("Resumen Ejecutivo", h1_style))
    story.append(Paragraph(
        "El presente informe documenta el desarrollo y fundamentación matemática de la <b>Fase 1 (Preprocesamiento del Dataset de Imágenes)</b> "
        "para el proyecto semestral de Visión Computacional. Se seleccionó un dataset real e intrínsecamente desafiante: "
        "<i>Concrete Crack Images for Classification</i> (Özgenel & Sorguç). Este dataset contiene fotografías de superficies de concreto divididas "
        "en dos clases: presencia de grietas (<b>Positive</b>) y superficies sanas (<b>Negative</b>).",
        body_style
    ))
    story.append(Paragraph(
        "Debido a que el concreto presenta un fuerte ruido de textura granular de alta frecuencia, bajo contraste tonal y sombras proyectadas, "
        "se diseñó un pipeline de preprocesamiento secuencial basado estrictamente en los fundamentos del curso: "
        "remuestreo geométrico bicúbico, reducción de canal de color, filtrado espacial Gaussiano, ecualización local adaptativa de histograma (CLAHE) "
        "y refinamiento morfológico de cierre (<i>A</i> • <i>B</i>). El código fue modularizado en <code>preprocessor.py</code> y <code>procesar_dataset.py</code>, "
        "generando muestras balanceadas de entrada y salida, además de gráficas de dispersión e histogramas comparativos que sustentan la eficacia de la solución.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # ==========================================
    # 3. MARCO TEÓRICO COMPLETO
    # ==========================================
    story.append(Paragraph("1. Marco Teórico y Fundamentos de Visión Computacional", h1_style))
    story.append(Paragraph(
        "Las técnicas implementadas se sustentan en los conceptos teóricos analizados en las sesiones de clase:",
        body_style
    ))

    story.append(Paragraph("1.1. Representación Digital y Remuestreo Espacial (Interpolación Bicúbica)", h2_style))
    story.append(Paragraph(
        "Una imagen digital continua <i>f(x, y)</i> se convierte al dominio discreto mediante <b>muestreo espacial</b> y <b>cuantificación de amplitud</b>. "
        "Al requerir un tamaño homogéneo para tareas posteriores de clasificación (estándar 224 × 224 píxeles), el mapeo geométrico "
        "<i>(x', y') = T(x, y)</i> requiere determinar la intensidad en coordenadas reales continuas.",
        body_style
    ))
    story.append(Paragraph(
        "A diferencia de la interpolación por vecino más cercano (que introduce artefactos de bloque) o la bilineal (que tiende a suavizar en exceso bordes sutiles), "
        "la <b>interpolación bicúbica</b> considera un vecindario de 4 × 4 (16 píxeles adyacentes) mediante un ajuste polinomial de tercer orden. "
        "Esto garantiza superficies de intensidad derivables y conserva la nitidez y continuidad de las fisuras delgadas.",
        body_style
    ))

    story.append(Paragraph("1.2. Reducción a Escala de Grises y Eliminación de Redundancia Cromática", h2_style))
    story.append(Paragraph(
        "Las imágenes originales se capturan en espacio tridimensional RGB. En la inspección estructural de concreto, el color posee escasa información discriminativa, "
        "pues tanto el cemento como la fisura presentan tonalidades neutras (grises). Conservar los 3 canales multiplica por 3 el costo computacional "
        "sin aportar valor diagnóstico. La transformación al canal de luminancia se realiza según la ponderación perceptual estándar recomendada por ITU-R:",
        body_style
    ))
    story.append(formula_table(f1_path, "1", w=250, h=25))
    story.append(Spacer(1, 4))

    story.append(Paragraph("1.3. Modelos de Ruido y Filtrado Espacial Gaussiano", h2_style))
    story.append(Paragraph(
        "La superficie del concreto está compuesta por agregados minerales, arena y poros microscópicos que se manifiestan como ruido aditivo de alta frecuencia:",
        body_style
    ))
    story.append(formula_table(f2_path, "2", w=160, h=24))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Si se intentase binarizar o detectar bordes directamente sobre la imagen cruda, el detector respondería masivamente a la grava "
        "en lugar de la fisura. Se emplea un <b>filtro Gaussiano</b> discreto 3 × 3, cuya función de ponderación espacial bidimensional es:",
        body_style
    ))
    story.append(formula_table(f3_path, "3", w=220, h=32))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Este filtro atenúa las variaciones locales aleatorias sin difuminar de manera destructiva las líneas continuas de la grieta.",
        body_style
    ))

    story.append(Paragraph("1.4. Análisis de Histogramas y Ecualización Adaptativa (CLAHE)", h2_style))
    story.append(Paragraph(
        "El histograma <i>h(g)</i> representa la distribución empírica de frecuencias de los niveles de gris de la imagen. "
        "En imágenes de concreto, el histograma original muestra un <b>rango dinámico sumamente estrecho</b> (conglomerado en tonos medios de gris entre 110 y 160), "
        "provocando un contraste deficiente entre la grieta (gris oscuro) y el fondo.",
        body_style
    ))
    story.append(Paragraph(
        "La ecualización de histograma tradicional aplica la función de distribución acumulada (CDF) sobre toda la imagen, pero en fondos con iluminación heterogénea "
        "o sombras proyectadas produce una sobreamplificación inaceptable del ruido en zonas lisas. Por ello se recurre a <b>CLAHE</b> (<i>Contrast Limited Adaptive Histogram Equalization</i>):",
        body_style
    ))
    story.append(Paragraph(
        "• <b>División en Bloques:</b> La imagen se divide en cuadrículas rectangulares contextuales (8 × 8 bloques).<br/>"
        "• <b>Límite de Contraste (Clip Limit):</b> Se recorta el pico del histograma local que supere un umbral (en este caso 2.5), y el exceso de píxeles se redistribuye uniformemente.<br/>"
        "• <b>Interpolación Bilineal Inter-bloques:</b> Elimina las discontinuidades artificiales entre las fronteras de los bloques vecinos.",
        bullet_style
    ))

    story.append(Paragraph("1.5. Morfología Matemática y Operación de Cierre", h2_style))
    story.append(Paragraph(
        "La morfología matemática analiza estructuras espaciales a través de la interacción de la imagen <i>A</i> con un conjunto geométrico conocido como <b>Elemento Estructurador (<i>B</i>)</b>. "
        "Las fisuras en concreto con frecuencia sufren interrupciones visuales por polvo o iluminación débil. Para resolverlo, se aplica la operación de <b>Cierre Morfológico</b> (<i>A</i> • <i>B</i>):",
        body_style
    ))
    story.append(formula_table(f4_path, "4", w=190, h=24))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "El cierre consiste en una <b>dilatación</b> <i>A</i> ⊕ <i>B</i> (que expande la región oscura de la fisura y llena huecos pequeños) seguida de una <b>erosión</b> "
        "con el mismo elemento estructurador (que restaura las dimensiones exteriores del objeto). Como resultado, las grietas segmentadas o rotas se reconectan en una trayectoria continua sin engrosar artificialmente la fisura.",
        body_style
    ))

    story.append(PageBreak())

    # ==========================================
    # 4. JUSTIFICACIÓN DEL DATASET
    # ==========================================
    story.append(Paragraph("2. Caracterización del Dataset Seleccionado", h1_style))
    story.append(Paragraph(
        "<b>Dataset Oficial:</b> <i>Concrete Crack Images for Classification</i> (Özgenel & Sorguç, Middle East Technical University / Kaggle).",
        body_style
    ))

    data_summary = [
        [Paragraph("<b>Propiedad</b>", meta_style), Paragraph("<b>Detalle</b>", meta_style)],
        [Paragraph("Tamaño original", body_style), Paragraph("40,000 imágenes RGB (227 × 227 píxeles)", body_style)],
        [Paragraph("Clases", body_style), Paragraph("2 Clases balanceadas: <code>Positive</code> (con grieta) y <code>Negative</code> (sin grieta)", body_style)],
        [Paragraph("Fuente de Descarga", body_style), Paragraph("API automatizada <code>kagglehub</code> (descarga directa sin descompresión manual)", body_style)],
        [Paragraph("Muestra del Proyecto", body_style), Paragraph("500 imágenes seleccionadas (250 Positive + 250 Negative) para optimizar el repositorio", body_style)],
        [Paragraph("Condiciones ambientales", body_style), Paragraph("Estructuras de concreto reales, luz solar directa, sombra, suciedad y porosidad", body_style)]
    ]
    t_data = Table(data_summary, colWidths=[150, 350], hAlign='CENTER')
    t_data.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2B6CB0")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_data)
    story.append(Spacer(1, 10))

    story.append(Paragraph("¿Por qué este dataset es desafiador para el proyecto?", h2_style))
    story.append(Paragraph(
        "A diferencia de datasets elementales de laboratorio (como MNIST, CIFAR o fotos de catálogo en fondo blanco):",
        body_style
    ))
    story.append(Paragraph("• <b>Falsos Positivos por Textura:</b> Los poros del hormigón y agregados rocosos producen discontinuidades tonales idénticas a micro-grietas.", bullet_style))
    story.append(Paragraph("• <b>Bajo Rango Dinámico:</b> No existe una separación bimodal clara en el histograma global, haciendo inviable una umbralización simple directa.", bullet_style))
    story.append(Paragraph("• <b>Gradientes de Luz:</b> Sombras en diagonales o iluminación desbalanceada en esquinas que engañan a operadores puntuales.", bullet_style))

    story.append(Spacer(1, 10))

    # ==========================================
    # 5. ANÁLISIS DE CÓDIGO
    # ==========================================
    story.append(Paragraph("3. Análisis Detallado del Módulo <code>preprocessor.py</code>", h1_style))
    story.append(Paragraph(
        "El archivo <code>preprocessor.py</code> contiene la clase principal <code>ConcreteCrackPreprocessor</code>. "
        "Fue diseñada siguiendo los principios de modularidad, encapsulamiento y reproducibilidad. A continuación se detalla cada método:",
        body_style
    ))

    code_methods = [
        ("1. Constructor: __init__(self, target_size, clahe_clip, clahe_grid, blur_kernel)",
         "Inicializa los hiperparámetros del pipeline. Crea el objeto CLAHE con <code>cv2.createCLAHE</code> pasando el factor de corte (2.5) "
         "y la grilla de bloques (8 × 8). Asimismo, precompila el kernel morfológico rectangular de 3 × 3 con <code>cv2.getStructuringElement</code> "
         "para no recalcularlo en cada imagen."),
        
        ("2. Remuestreo: resize_bicubic(self, img_bgr)",
         "Utiliza <code>cv2.resize(img, (224, 224), interpolation=cv2.INTER_CUBIC)</code>. "
         "Garantiza que todas las imágenes entren con dimensiones estandarizadas a los modelos convolucionales preservando los gradientes finos de las fisuras."),
        
        ("3. Conversión: to_grayscale(self, img_bgr)",
         "Aplica <code>cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)</code>. Pasa de un tensor tridimensional (224, 224, 3) a una matriz bidimensional (224, 224), "
         "eliminando datos de color no correlacionados con la fisura."),
        
        ("4. Reducción de Ruido: reduce_noise(self, img_gray, method='gaussian')",
         "Ejecuta <code>cv2.GaussianBlur(img_gray, (3, 3), sigmaX=0)</code>. Suprime frecuencias espaciales excesivamente altas (granos de arena) "
         "previo a la amplificación de contraste, evitando que CLAHE realce ruido indeseado."),
        
        ("5. Realce de Contraste: enhance_contrast(self, img_gray)",
         "Invoca <code>self.clahe.apply(img_gray)</code>. Redistribuye las frecuencias tonales dentro de cada tesela de 8 × 8 píxeles. "
         "Convierte áreas oscuras de fisuras de bajo contraste en valles de intensidad perfectamente diferenciados del fondo de concreto."),
        
        ("6. Refinamiento Morfológico: morphological_refine(self, img_enhanced)",
         "Aplica <code>cv2.morphologyEx(img_enhanced, cv2.MORPH_CLOSE, kernel)</code>. "
         "Realiza la operación de cierre (<i>A</i> • <i>B</i>). Permite cerrar grietas discontinuas y consolidar la trayectoria lineal del defecto estructural."),
        
        ("7. Normalización: normalize(self, img_processed)",
         "Convierte los valores de escala entera <code>uint8</code> [0, 255] a punto flotante <code>float32</code> normalizado en el rango [0.0, 1.0]. "
         "Paso fundamental para garantizar la estabilidad numérica en gradientes descendentes durante entrenamientos posteriores."),
        
        ("8. Método Maestro: process(self, img_bgr, return_all_steps=False)",
         "Orquesta la ejecución secuencial completa. Cuenta con una bandera <code>return_all_steps=True</code> que devuelve un diccionario con las matrices "
         "de cada etapa intermedia, utilizado para generar los gráficos explicativos.")
    ]

    for title, desc in code_methods:
        story.append(Paragraph(f"<b>{title}</b>", h2_style))
        story.append(Paragraph(desc, body_style))

    story.append(PageBreak())

    # ==========================================
    # 6. ANÁLISIS DE procesar_dataset.py
    # ==========================================
    story.append(Paragraph("4. Análisis Detallado del Script <code>procesar_dataset.py</code>", h1_style))
    story.append(Paragraph(
        "El script <code>procesar_dataset.py</code> es el punto de entrada que ejecuta el procesamiento por lotes sobre las imágenes del disco. "
        "Su lógica se divide en los siguientes bloques:",
        body_style
    ))

    proc_steps = [
        ("1. Detección y Enlace con la Caché de Kaggle",
         "Apunta a la ruta generada por la descarga de <code>kagglehub</code>: "
         "<code>C:\\Users\\...\\.cache\\kagglehub\\datasets\\...\\versions\\1</code>. "
         "Evita duplicar almacenamiento innecesario descargando zip manuales."),
        
        ("2. Gestión de Estructura 'Antes vs. Después'",
         "Crea dos directorios independientes de salida:<br/>"
         "• <code>dataset_muestra_original/</code>: Almacena una copia de respaldo sin modificar de las imágenes evaluadas (el estado 'Antes').<br/>"
         "• <code>dataset_preprocesado/</code>: Guarda las imágenes procesadas por el pipeline en escala de grises de 8 bits (el estado 'Después').<br/>"
         "Ambos preservan las subcarpetas <code>Positive/</code> y <code>Negative/</code> para mantener las etiquetas intactas."),
        
        ("3. Muestreo Balanceado",
         "Toma 250 imágenes aleatorias de la clase <code>Positive</code> y 250 de <code>Negative</code> (total 500 imágenes). "
         "Esto genera un paquete liviano (~30 MB) que cumple los límites de subida de GitHub sin requerir Git LFS."),
        
        ("4. Generación Automática de Reportes Gráficos",
         "En la primera iteración de cada clase, invoca las funciones de <code>generar_reporte_visual.py</code>: "
         "calcula los histogramas de frecuencias con <code>cv2.calcHist</code> y exporta las figuras en formato PNG a alta resolución (300 DPI) "
         "en la carpeta <code>reportes_visuales/</code>.")
    ]

    for title, desc in proc_steps:
        story.append(Paragraph(f"<b>{title}</b>", h2_style))
        story.append(Paragraph(desc, body_style))

    story.append(Spacer(1, 10))

    # ==========================================
    # 7. RESULTADOS Y EVIDENCIA VISUAL
    # ==========================================
    story.append(Paragraph("5. Evidencia Visual y Discusión de Resultados", h1_style))
    story.append(Paragraph(
        "A continuación se presentan las figuras generadas automáticamente por el pipeline durante la ejecución:",
        body_style
    ))

    img_steps_path = os.path.join(IMG_DIR, "desglose_paso_a_paso.png")
    if os.path.exists(img_steps_path):
        story.append(Spacer(1, 5))
        story.append(Image(img_steps_path, width=490, height=105))
        story.append(Paragraph("<b>Figura 1:</b> Desglose secuencial del pipeline: Entrada BGR → Escala de Grises → Filtro Gaussiano 3 × 3 → Realce CLAHE → Cierre Morfológico.", caption_style))

    story.append(Spacer(1, 5))

    img_pos_path = os.path.join(IMG_DIR, "comparativa_positive.png")
    if os.path.exists(img_pos_path):
        story.append(Image(img_pos_path, width=420, height=260))
        story.append(Paragraph("<b>Figura 2:</b> Análisis de la clase Positive (con grieta). Nótese en los paneles inferiores cómo el histograma original (comprimido en gris medio) es expandido uniformemente por CLAHE, diferenciando los valles oscuros de la fisura.", caption_style))

    story.append(PageBreak())

    img_neg_path = os.path.join(IMG_DIR, "comparativa_negative.png")
    if os.path.exists(img_neg_path):
        story.append(Image(img_neg_path, width=420, height=260))
        story.append(Paragraph("<b>Figura 3:</b> Análisis de la clase Negative (superficie sana). El histograma procesado confirma que el algoritmo regulariza la iluminación sin crear falsos bordes de fisura.", caption_style))

    story.append(Spacer(1, 10))

    # ==========================================
    # 8. GUÍA PARA LA EXPOSICIÓN ORAL
    # ==========================================
    story.append(Paragraph("6. Guía de Defensa Oral ante el Docente", h1_style))
    story.append(Paragraph(
        "Al ser una sustentación individual elegida por el docente, es vital responder con precisión conceptual. A continuación se presentan las preguntas típicas y sus respuestas modelo:",
        body_style
    ))

    defense_qa = [
        ("P1: ¿Por qué no utilizaste directamente ecualización de histograma global (cv2.equalizeHist)?",
         "<b>Respuesta:</b> La ecualización global calcula una función acumulativa (CDF) única para toda la imagen. En superficies de concreto con iluminación irregular o sombras diagonales, la ecualización global sobre-satura las zonas claras y amplifica excesivamente el ruido de fondo en áreas lisas. CLAHE divide la imagen en cuadrículas (8 × 8) y limita el contraste (clip limit 2.5), logrando un realce homogéneo y local sin introducir artefactos."),
        
        ("P2: ¿Por qué aplicaste el filtro Gaussiano ANTES de CLAHE y no al revés?",
         "<b>Respuesta:</b> Si se aplica CLAHE primero, el algoritmo tomará los granos de arena y poros como detalles válidos y amplificará su contraste. Al suavizar primero con Gaussiano 3 × 3, se eliminan esas fluctuaciones de alta frecuencia, garantizando que CLAHE concentre su ganancia de contraste exclusivamente en las fronteras reales de la grieta."),
        
        ("P3: ¿Qué ventaja matemática aporta la interpolación bicúbica sobre la bilineal en este caso?",
         "<b>Respuesta:</b> La interpolación bicúbica utiliza polinomios de tercer orden sobre 16 píxeles vecinos, manteniendo derivadas continuas en los bordes. En imágenes de grietas delgadas (que a menudo tienen 1 o 2 píxeles de espesor), la interpolación bilineal difumina el borde y atenúa el gradiente, mientras que la bicúbica retiene el contraste y agudeza estructural."),
        
        ("P4: ¿Por qué realizaste un Cierre morfológico y no una Apertura?",
         "<b>Respuesta:</b> La apertura elimina detalles pequeños aislados (útil contra ruido impulsivo). Sin embargo, las fisuras reales a menudo sufren micro-cortes por polvo o iluminación débil. El cierre (<i>A</i> • <i>B</i> = (<i>A</i> ⊕ <i>B</i>) ⊖ <i>B</i>) primero dilata para conectar esos segmentos discontinuos y luego erosiona para restaurar el ancho original, preservando la continuidad morfológica de la fisura.")
    ]

    for q, a in defense_qa:
        q_box = [
            [Paragraph(f"<b>{q}</b>", ParagraphStyle('QStyle', parent=h2_style, textColor=colors.HexColor("#1A365D")))],
            [Paragraph(a, body_style)]
        ]
        t_box = Table(q_box, colWidths=[500], hAlign='CENTER')
        t_box.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F7FAFC")),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E0")),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(t_box)
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # ==========================================
    # 9. CONCLUSIONES Y REFERENCIAS
    # ==========================================
    story.append(Paragraph("7. Conclusiones", h1_style))
    story.append(Paragraph(
        "1. <b>Cumplimiento de Objetivos:</b> Se seleccionó y preprocesó exitosamente un dataset desafiante de inspección estructural de concreto, "
        "estandarizándolo a dimensiones homogéneas (224 × 224) con valores normalizados listos para futuras fases de aprendizaje computacional.<br/>"
        "2. <b>Sinergia Teórico-Práctica:</b> El pipeline articuló los temas centrales del curso: muestreo geométrico, espacios tonales, "
        "filtrado espacial contra ruido, transformación de histogramas (CLAHE) y operadores morfológicos de conjuntos.<br/>"
        "3. <b>Organización Profesional del Repositorio:</b> Se estructuró una separación estricta entre datos crudos ('Antes') y procesados ('Después'), "
        "con código modular y reproducibilidad garantizada vía <code>requirements.txt</code>.",
        body_style
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("8. Referencias Bibliográficas", h1_style))
    story.append(Paragraph(
        "• Dawson-Howe, K. (2014). <i>A Practical Introduction to Computer Vision with OpenCV</i>. John Wiley & Sons.<br/>"
        "• Özgenel, Ç. F., & Sorguç, A. G. (2018). <i>Performance Comparison of Pretrained Convolutional Neural Networks on Crack Detection in Concrete</i>. ISARC Proceedings.<br/>"
        "• Universidad de Valladolid. (2020). <i>Curso de Visión Artificial Industrial: Morfología Matemática y Operaciones Espaciales</i>.<br/>"
        "• Ccacyahuillca Bejar, H. H. (2026). <i>Material de Cátedra: Visión Computacional</i>. Universidad Nacional de San Antonio Abad del Cusco (UNSAAC).",
        body_style
    ))

    # Compilar documento
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generado exitosamente con formulas renderizadas en: {OUTPUT_PDF}")


if __name__ == "__main__":
    build_pdf()
