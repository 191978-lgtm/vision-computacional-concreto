"""
Generador de Diapositivas Académicas Formales en Formato PDF (Apaisado / 16:9 - Landscape)
Proyecto: Preprocesamiento de Dataset de Concreto
Estudiante: Domingo de Guzman Quispe Mamani
Asignatura: Visión Computacional - UNSAAC
"""

import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

BASE_DIR = r"c:\Users\wtfcl\Desktop\VISION COMPUTACIONAL\proyecto_preprocesamiento"
OUTPUT_PDF = os.path.join(BASE_DIR, "Diapositivas_Preprocesamiento_Domingo_Quispe.pdf")
IMG_DIR = os.path.join(BASE_DIR, "reportes_visuales")
FORMULAS_DIR = os.path.join(IMG_DIR, "formulas")

PAGE_WIDTH, PAGE_HEIGHT = landscape(letter)  # 792 x 612 puntos


class SlideCanvas(canvas.Canvas):
    """Canvas formal para diapositivas con encabezado superior institucional, línea y pie con número de diapositiva."""
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
            self.draw_slide_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_slide_decorations(self, total_pages):
        # La diapositiva 1 es la carátula principal
        if self._pageNumber == 1:
            # Borde decorativo exterior formal
            self.saveState()
            self.setStrokeColor(colors.HexColor("#1E3A8A"))
            self.setLineWidth(3)
            self.rect(25, 25, PAGE_WIDTH - 50, PAGE_HEIGHT - 50)
            self.setStrokeColor(colors.HexColor("#3B82F6"))
            self.setLineWidth(0.8)
            self.rect(29, 29, PAGE_WIDTH - 58, PAGE_HEIGHT - 58)
            self.restoreState()
            return

        self.saveState()
        # Franja superior institucional
        self.setFillColor(colors.HexColor("#1E3A8A"))
        self.rect(36, PAGE_HEIGHT - 38, PAGE_WIDTH - 72, 3, fill=1, stroke=0)

        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1E3A8A"))
        self.drawString(36, PAGE_HEIGHT - 30, "UNSAAC • VISIÓN COMPUTACIONAL")

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(PAGE_WIDTH - 36, PAGE_HEIGHT - 30, "PROYECTO SEMESTRAL — FASE 1: PREPROCESAMIENTO")

        # Pie de diapositiva
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.6)
        self.line(36, 32, PAGE_WIDTH - 36, 32)

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(36, 20, "Estudiante: Domingo de Guzman Quispe Mamani | Docente: Prof. Hans H. Ccacyahuillca Bejar")
        self.drawRightString(PAGE_WIDTH - 36, 20, f"Diapositiva {self._pageNumber} de {total_pages}")
        self.restoreState()


def build_slides_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=landscape(letter),
        leftMargin=36,
        rightMargin=36,
        topMargin=48,
        bottomMargin=38
    )

    styles = getSampleStyleSheet()

    # Estilos Tipográficos Formales
    s_tag = ParagraphStyle(
        'SlideTag', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8, leading=10,
        textColor=colors.HexColor("#2563EB"), textTransform='uppercase', spaceAfter=2
    )

    s_title = ParagraphStyle(
        'SlideTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=18, leading=22,
        textColor=colors.HexColor("#0F172A"), spaceAfter=12
    )

    s_card_title = ParagraphStyle(
        'CardTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=11, leading=14,
        textColor=colors.HexColor("#1E3A8A"), spaceAfter=6
    )

    s_body = ParagraphStyle(
        'SlideBody', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=13.5,
        textColor=colors.HexColor("#334155"), spaceAfter=5
    )

    s_bullet = ParagraphStyle(
        'SlideBullet', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.8, leading=13,
        textColor=colors.HexColor("#334155"), leftIndent=12, spaceAfter=4
    )

    s_code = ParagraphStyle(
        'SlideCode', parent=styles['Normal'],
        fontName='Courier', fontSize=7.8, leading=10.5,
        textColor=colors.HexColor("#0F172A")
    )

    s_caption = ParagraphStyle(
        'SlideCaption', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=7.5, leading=9.5,
        textColor=colors.HexColor("#64748B"), alignment=1, spaceBefore=4
    )

    story = []

    # ==============================================================
    # DIAPOSITIVA 1: CARÁTULA FORMAL
    # ==============================================================
    story.append(Spacer(1, 40))
    p_inst = Paragraph("UNIVERSIDAD NACIONAL DE SAN ANTONIO ABAD DEL CUSCO", ParagraphStyle('InstCover', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=colors.HexColor("#1E3A8A"), alignment=1))
    p_fac = Paragraph("FACULTAD DE INGENIERÍA ELÉCTRICA, ELECTRÓNICA, INFORMÁTICA Y MECÁNICA • DEPARTAMENTO DE INFORMÁTICA", ParagraphStyle('FacCover', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor("#64748B"), alignment=1))
    story.append(p_inst)
    story.append(Spacer(1, 4))
    story.append(p_fac)
    story.append(Spacer(1, 25))

    p_proj = Paragraph("PROYECTO SEMESTRAL DE VISIÓN COMPUTACIONAL — FASE 1", ParagraphStyle('SubTag', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.5, leading=12, textColor=colors.HexColor("#2563EB"), alignment=1))
    p_main_title = Paragraph("Detección y Clasificación Automatizada de Grietas<br/>en Superficies de Concreto", ParagraphStyle('MainTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=24, leading=29, textColor=colors.HexColor("#0F172A"), alignment=1))
    p_desc = Paragraph("Diseño, Fundamentación Matemática y Pipeline de Preprocesamiento de Imágenes", ParagraphStyle('DescCover', parent=styles['Normal'], fontName='Helvetica', fontSize=11, leading=15, textColor=colors.HexColor("#475569"), alignment=1))

    story.append(p_proj)
    story.append(Spacer(1, 6))
    story.append(p_main_title)
    story.append(Spacer(1, 6))
    story.append(p_desc)
    story.append(Spacer(1, 35))

    meta_data = [
        [Paragraph("<b>Estudiante:</b>", s_body), Paragraph("Domingo de Guzman Quispe Mamani", s_body),
         Paragraph("<b>Docente:</b>", s_body), Paragraph("Prof. Hans H. Ccacyahuillca Bejar", s_body)],
        [Paragraph("<b>Asignatura:</b>", s_body), Paragraph("Visión Computacional", s_body),
         Paragraph("<b>Dataset:</b>", s_body), Paragraph("Concrete Crack Images (Özgenel & Sorguç)", s_body)],
        [Paragraph("<b>Modalidad:</b>", s_body), Paragraph("Individual", s_body),
         Paragraph("<b>Sede y Fecha:</b>", s_body), Paragraph("Cusco, Octubre 2026", s_body)]
    ]
    t_cover_meta = Table(meta_data, colWidths=[90, 240, 80, 250], hAlign='CENTER')
    t_cover_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(t_cover_meta)
    story.append(PageBreak())

    # ==============================================================
    # DIAPOSITIVA 2: POR QUÉ ES UN DATASET DESAFIADOR
    # ==============================================================
    story.append(Paragraph("CONTEXTO Y SELECCIÓN", s_tag))
    story.append(Paragraph("¿Por qué es un Dataset Altamente Desafiador?", s_title))

    col1 = [
        Paragraph("Desafíos en Entornos Reales de Construcción", s_card_title),
        Paragraph("• <b>Ruido de Textura de Alta Frecuencia:</b> La rugosidad natural del cemento, partículas de arena y poros generan variaciones lumínicas que se confunden fácilmente con micro-fisuras.", s_bullet),
        Paragraph("• <b>Bajo Contraste Tonal (Histograma Estrecho):</b> El interior de una grieta (gris oscuro) y la pared circundante (gris medio) tienen diferencias mínimas de intensidad.", s_bullet),
        Paragraph("• <b>Iluminación Heterogénea:</b> Sombras proyectadas, desgaste superficial y luz solar que impiden una umbralización global directa.", s_bullet),
        Paragraph("• <b>Discontinuidad Estructural:</b> Pequeñas impurezas o polvo interrumpen visualmente las grietas reales.", s_bullet)
    ]
    col2 = [
        Paragraph("Estructura de Clases y Muestreo", s_card_title),
        Paragraph("• <b>Origen:</b> <i>Concrete Crack Images for Classification</i> (Özgenel & Sorguç).", s_bullet),
        Paragraph("• <b>Clase Positive (Con Grieta):</b> 20,000 imágenes con defectos estructurales.", s_bullet),
        Paragraph("• <b>Clase Negative (Sin Grieta):</b> 20,000 imágenes de concreto sano.", s_bullet),
        Paragraph("• <b>Muestra Balanceada:</b> 500 imágenes seleccionadas (250 Positive + 250 Negative) procesadas para mantener el repositorio ágil, ligero y reproducible.", s_bullet),
        Paragraph("• <b>Entornos Reales:</b> A diferencia de MNIST o fotos en fondo blanco plano, este dataset exige un tratamiento digital robusto.", s_bullet)
    ]

    t_s2 = Table([[col1, col2]], colWidths=[350, 350], hAlign='CENTER')
    t_s2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor("#F8FAFC")),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_s2)
    story.append(PageBreak())

    # ==============================================================
    # DIAPOSITIVA 3: ARQUITECTURA GENERAL DEL PIPELINE
    # ==============================================================
    story.append(Paragraph("ARQUITECTURA DEL SISTEMA", s_tag))
    story.append(Paragraph("El Pipeline de Preprocesamiento Completo", s_title))

    img_pasos_file = os.path.join(IMG_DIR, "desglose_paso_a_paso.png")
    if os.path.exists(img_pasos_file):
        story.append(Image(img_pasos_file, width=700, height=135))
        story.append(Paragraph("Figura 1: Evolución visual de una grieta a lo largo de las etapas del pipeline implementado en <code>preprocessor.py</code>", s_caption))

    story.append(Spacer(1, 10))

    grid_pipeline = [
        [Paragraph("<b>1. Bicubic Resize</b><br/>Estandarización a 224×224 preservando bordes finos mediante ajuste polinomial.", s_body),
         Paragraph("<b>2. Grayscale</b><br/>Eliminación de redundancia cromática (ahorro del 66% de volumen de datos).", s_body),
         Paragraph("<b>3. Gaussian Denoise</b><br/>Filtro espacial 3×3 para atenuar la textura granular de la arena antes de CLAHE.", s_body)],
        [Paragraph("<b>4. Realce CLAHE</b><br/>Ecualización adaptativa local 8×8 con límite de corte de 2.5 para resaltar la grieta.", s_body),
         Paragraph("<b>5. Cierre Morfológico</b><br/>Operación (A ⊕ B) ⊖ B para conectar micro-segmentos discontinuos de la fisura.", s_body),
         Paragraph("<b>6. Normalización</b><br/>Escalado numérico flotante [0.0, 1.0] para estabilidad en modelos futuros.", s_body)]
    ]
    t_pipe_grid = Table(grid_pipeline, colWidths=[233, 233, 234], hAlign='CENTER')
    t_pipe_grid.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_pipe_grid)
    story.append(PageBreak())

    # ==============================================================
    # DIAPOSITIVA 4: ETAPAS 1 Y 2 (INTERPOLACIÓN Y ESCALA DE GRISES)
    # ==============================================================
    story.append(Paragraph("ETAPAS 1 Y 2 DEL PIPELINE", s_tag))
    story.append(Paragraph("Remuestreo Bicúbico y Reducción a Escala de Grises", s_title))

    col_e1 = [
        Paragraph("1.1. Interpolación Bicúbica (cv2.INTER_CUBIC)", s_card_title),
        Paragraph("• Las imágenes originales miden <b>227 × 227</b> y se estandarizan a <b>224 × 224</b>.", s_bullet),
        Paragraph("• Al calcular el mapeo inverso <code>(x, y) = T⁻¹(x', y')</code> se obtienen coordenadas con parte decimal.", s_bullet),
        Paragraph("• <b>¿Por qué Bicúbica?</b> Emplea un vecindario de <b>16 píxeles (4 × 4)</b> mediante polinomios de 3er grado. A diferencia de la bilineal, conserva la nitidez y continuidad en bordes delgados de 1 píxel de espesor.", s_bullet),
        Spacer(1, 4),
        Paragraph("<b>Código en preprocessor.py:</b>", s_body),
        Paragraph("<code>cv2.resize(img_bgr, (224, 224), interpolation=cv2.INTER_CUBIC)</code>", s_code)
    ]

    img_f_lum = os.path.join(FORMULAS_DIR, "formula_luminancia.png")
    col_e2 = [
        Paragraph("1.2. Eliminación de Redundancia Cromática", s_card_title),
        Paragraph("• En superficies de concreto, tanto el cemento como la fisura son monocromáticos (<b>R ≈ G ≈ B</b>).", s_bullet),
        Paragraph("• Procesar 3 canales triplica el consumo computacional sin aportar ventajas de discriminación.", s_bullet),
        Paragraph("• Se aplica la conversión perceptual estándar recomendada por ITU-R BT.601:", s_bullet),
        Spacer(1, 4),
        Image(img_f_lum, width=280, height=28) if os.path.exists(img_f_lum) else Paragraph("Y = 0.299·R + 0.587·G + 0.114·B", s_body),
        Spacer(1, 4),
        Paragraph("<b>Código en preprocessor.py:</b>", s_body),
        Paragraph("<code>cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)</code>", s_code)
    ]

    t_s4 = Table([[col_e1, col_e2]], colWidths=[350, 350], hAlign='CENTER')
    t_s4.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_s4)
    story.append(PageBreak())

    # ==============================================================
    # DIAPOSITIVA 5: ETAPA 3 (RUIDO Y FILTRADO GAUSSIANO)
    # ==============================================================
    story.append(Paragraph("ETAPA 3 DEL PIPELINE", s_tag))
    story.append(Paragraph("Modelado de Ruido y Filtrado Espacial Gaussiano", s_title))

    img_f_ruido = os.path.join(FORMULAS_DIR, "formula_ruido.png")
    img_f_gauss = os.path.join(FORMULAS_DIR, "formula_gaussiana.png")

    col_g1 = [
        Paragraph("1.3. Modelo de Ruido Aditivo de Alta Frecuencia", s_card_title),
        Paragraph("La porosidad del concreto, arena e imperfecciones del sensor se modelan formalmente como ruido aditivo:", s_bullet),
        Spacer(1, 4),
        Image(img_f_ruido, width=200, height=28) if os.path.exists(img_f_ruido) else Paragraph("g(x, y) = f(x, y) + η(x, y)", s_body),
        Spacer(1, 4),
        Paragraph("• <b>f(x, y):</b> Imagen ideal de la superficie.", s_bullet),
        Paragraph("• <b>η(x, y):</b> Ruido aleatorio generado por la textura granular.", s_bullet),
        Paragraph("• <b>g(x, y):</b> Imagen real observada por la cámara.", s_bullet),
        Paragraph("• <b>Orden secuencial:</b> El filtro va <b>antes</b> de CLAHE para evitar que el realce de contraste amplifique cada poro como si fuera una fisura.", s_bullet)
    ]

    col_g2 = [
        Paragraph("Filtro Gaussiano Bidimensional (3 × 3)", s_card_title),
        Paragraph("La función continua de ponderación espacial viene dada por:", s_bullet),
        Spacer(1, 4),
        Image(img_f_gauss, width=240, height=35) if os.path.exists(img_f_gauss) else Paragraph("G(x, y) = [1 / (2π·σ²)] · e^(-(x²+y²)/(2σ²))", s_body),
        Spacer(1, 4),
        Paragraph("• Asigna pesos decrecientes desde el centro hacia las esquinas según la campana normal, atenuando el ruido granular sin difuminar destructivamente los bordes.", s_bullet),
        Spacer(1, 4),
        Paragraph("<b>Código en preprocessor.py:</b>", s_body),
        Paragraph("<code>cv2.GaussianBlur(img_gray, (3, 3), sigmaX=0)</code>", s_code)
    ]

    t_s5 = Table([[col_g1, col_g2]], colWidths=[350, 350], hAlign='CENTER')
    t_s5.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_s5)
    story.append(PageBreak())

    # ==============================================================
    # DIAPOSITIVA 6: ETAPA 4 (CLAHE Y GRÁFICAS DE HISTOGRAMAS)
    # ==============================================================
    story.append(Paragraph("ETAPA 4 DEL PIPELINE", s_tag))
    story.append(Paragraph("1.4. Análisis de Histogramas y Ecualización Adaptativa (CLAHE)", s_title))

    img_pos_file = os.path.join(IMG_DIR, "comparativa_positive.png")
    col_hist_img = [
        Image(img_pos_file, width=370, height=265) if os.path.exists(img_pos_file) else Paragraph("[Imagen comparativa_positive.png]", s_body),
        Paragraph("Figura 2: Imagen Original vs Preprocesada y sus respectivos Histogramas (Clase Positive)", s_caption)
    ]

    col_hist_info = [
        Paragraph("Evidencia Matemática del Histograma", s_card_title),
        Paragraph("• <b>Histograma Original (Izquierda):</b> Rango dinámico sumamente comprimido (110 a 160). La fisura y el concreto están atrapados en los mismos niveles tonales.", s_bullet),
        Paragraph("• <b>Histograma CLAHE (Derecha):</b> Se redistribuye sobre todo el rango [0, 255]. Los valles oscuros de la grieta caen en [0, 60] y la superficie en [120, 240].", s_bullet),
        Paragraph("• <b>Ecualización Local vs Global:</b> Se descartó <code>cv2.equalizeHist()</code> porque ante sombras proyectadas sobreamplifica el ruido en zonas homogéneas; CLAHE opera por teselas locales de 8×8 con corte de pico a 2.5.", s_bullet),
        Spacer(1, 4),
        Paragraph("<b>Código en preprocessor.py:</b>", s_body),
        Paragraph("<code>clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))<br/>enhanced = clahe.apply(img_denoised)</code>", s_code)
    ]

    t_s6 = Table([[col_hist_img, col_hist_info]], colWidths=[385, 315], hAlign='CENTER')
    t_s6.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_s6)
    story.append(PageBreak())

    # ==============================================================
    # DIAPOSITIVA 7: ETAPA 5 (MORFOLOGÍA MATEMÁTICA Y CIERRE)
    # ==============================================================
    story.append(Paragraph("ETAPA 5 DEL PIPELINE", s_tag))
    story.append(Paragraph("1.5. Morfología Matemática: Operación de Cierre", s_title))

    img_f_cierre = os.path.join(FORMULAS_DIR, "formula_cierre.png")

    col_m1 = [
        Paragraph("Operación de Cierre Morfológico", s_card_title),
        Paragraph("El cierre se define formalmente como una dilatación seguida de una erosión:", s_bullet),
        Spacer(1, 4),
        Image(img_f_cierre, width=220, height=28) if os.path.exists(img_f_cierre) else Paragraph("A • B = (A ⊕ B) ⊖ B", s_body),
        Spacer(1, 4),
        Paragraph("• <b>1. Dilatación (A ⊕ B):</b> Expande temporalmente la región oscura de la grieta; los fragmentos discontinuos por polvo se tocan y forman un puente continuo.", s_bullet),
        Paragraph("• <b>2. Erosión posterior (⊖ B):</b> Restaura el contorno y grosor original exterior de la fisura, pero <b>el puente de unión permanece</b>.", s_bullet),
        Paragraph("• <b>Elemento Estructurador (B):</b> Máscara rectangular sólida de 3 × 3 píxeles.", s_bullet)
    ]

    col_m2 = [
        Paragraph("¿Por qué Cierre y NO Apertura?", s_card_title),
        Paragraph("• <b>Apertura (A ∘ B = (A ⊖ B) ⊕ B):</b> Comienza erosionando. En micro-grietas delgadas de 1 o 2 píxeles de ancho, la erosión inicial las consideraría ruido y las <b>eliminaría por completo</b>.", s_bullet),
        Paragraph("• <b>Cierre:</b> Protege y conecta grietas sin engrosar el defecto de manera irreversible.", s_bullet),
        Spacer(1, 6),
        Paragraph("<b>Código en preprocessor.py:</b>", s_body),
        Paragraph("<code>kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))<br/>closed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)</code>", s_code)
    ]

    t_s7 = Table([[col_m1, col_m2]], colWidths=[350, 350], hAlign='CENTER')
    t_s7.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_s7)
    story.append(PageBreak())

    # ==============================================================
    # DIAPOSITIVA 8: VALIDACIÓN EN SUPERFICIE SANA (NEGATIVE)
    # ==============================================================
    story.append(Paragraph("RESULTADOS Y VALIDACIÓN", s_tag))
    story.append(Paragraph("Validación en Superficie Sana (Clase Negative)", s_title))

    img_neg_file = os.path.join(IMG_DIR, "comparativa_negative.png")
    col_neg_img = [
        Image(img_neg_file, width=370, height=265) if os.path.exists(img_neg_file) else Paragraph("[Imagen comparativa_negative.png]", s_body),
        Paragraph("Figura 3: Imagen Original vs Preprocesada y sus Histogramas (Clase Negative - Concreto Sano)", s_caption)
    ]

    col_neg_info = [
        Paragraph("Evaluación de Robustez del Pipeline", s_card_title),
        Paragraph("• <b>Ausencia de Falsos Positivos:</b> Al pasar por el filtro Gaussiano, CLAHE y Cierre, la superficie sana mantiene una distribución homogénea sin líneas fantasma ni artefactos inventados.", s_bullet),
        Paragraph("• <b>Histograma Controlado:</b> El histograma procesado expande la visibilidad del grano sin colapsar en picos artificiales.", s_bullet),
        Paragraph("• <b>Inocuidad Comprobada:</b> Un buen preprocesamiento no solo debe destacar el defecto, sino ser inocuo sobre las muestras que no contienen anomalías.", s_bullet),
        Paragraph("• <b>Estandarización:</b> Ambas clases (Positive y Negative) quedan con la misma dinámica numérica y resolución de 224 × 224.", s_bullet)
    ]

    t_s8 = Table([[col_neg_img, col_neg_info]], colWidths=[385, 315], hAlign='CENTER')
    t_s8.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_s8)
    story.append(PageBreak())

    # ==============================================================
    # DIAPOSITIVA 9: CONCLUSIONES Y PREGUNTAS
    # ==============================================================
    story.append(Paragraph("CIERRE DE LA EXPOSICIÓN", s_tag))
    story.append(Paragraph("Conclusiones y Respuestas a Preguntas del Docente", s_title))

    col_c1 = [
        Paragraph("Logros Principales del Proyecto", s_card_title),
        Paragraph("• <b>Dataset Desafiador Dominado:</b> De imágenes crudas con grano e iluminación dispar a matrices estandarizadas de alta calidad.", s_bullet),
        Paragraph("• <b>Sinergia Teórica Total:</b> Se articularon 5 temas del curso: muestreo bicúbico, espacios de color, ruido/Gaussiano, CLAHE y morfología.", s_bullet),
        Paragraph("• <b>Listo para la Fase 2:</b> Datos estructurados en <code>dataset_preprocesado/</code> listos para extracción de características o Deep Learning.", s_bullet)
    ]

    col_c2 = [
        Paragraph("Respuestas Técnicas Preparadas", s_card_title),
        Paragraph("• <b>¿Por qué 2 carpetas?:</b> Muestra Original ('Antes') para trazabilidad y Dataset Preprocesado ('Después') para el modelo.", s_bullet),
        Paragraph("• <b>¿Por qué Bicúbico?:</b> Para no difuminar bordes sutiles de 1 píxel al escalar a 224×224.", s_bullet),
        Paragraph("• <b>¿Por qué CLAHE?:</b> Porque la ecualización global quema zonas con sombras y sobreamplifica ruido en zonas lisas.", s_bullet),
        Paragraph("• <b>¿Por qué Cierre?:</b> Porque reconecta fisuras discontinuas sin borrarlas como haría la apertura.", s_bullet)
    ]

    t_s9 = Table([[col_c1, col_c2]], colWidths=[350, 350], hAlign='CENTER')
    t_s9.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_s9)

    doc.build(story, canvasmaker=SlideCanvas)
    print(f"Diapositivas en PDF generadas exitosamente en: {OUTPUT_PDF}")


if __name__ == "__main__":
    build_slides_pdf()
