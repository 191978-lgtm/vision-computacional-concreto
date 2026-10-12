import os
import matplotlib.pyplot as plt
import base64

base_dir = r"c:\Users\wtfcl\Desktop\VISION COMPUTACIONAL\proyecto_preprocesamiento"
img_dir = os.path.join(base_dir, "reportes_visuales")
formulas_dir = os.path.join(img_dir, "formulas")
out_html = os.path.join(base_dir, "presentacion_preprocesamiento.html")

os.makedirs(formulas_dir, exist_ok=True)

# 1. Generar fórmulas matemáticas nítidas con matplotlib en color claro para fondo oscuro
def render_formula(latex_str, filename, fontsize=18, fig_w=6, fig_h=1.1):
    fpath = os.path.join(formulas_dir, filename)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    # Color #38bdf8 (celeste brillante) o #f1f5f9 (blanco limpio)
    ax.text(0.5, 0.5, latex_str, fontsize=fontsize, ha='center', va='center', color='#38bdf8')
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(fpath, dpi=300, bbox_inches='tight', transparent=True)
    plt.close()
    return fpath

f_gauss_path = render_formula(
    r'$G(x, y) = \frac{1}{2\pi \sigma^2} \exp\left(-\frac{x^2 + y^2}{2\sigma^2}\right)$',
    'formula_gaussiana_dark.png', fontsize=20, fig_w=6.5, fig_h=1.3
)
f_lum_path = render_formula(
    r'$Y = 0.299 \cdot R + 0.587 \cdot G + 0.114 \cdot B$',
    'formula_luminancia_dark.png', fontsize=18, fig_w=6, fig_h=0.9
)
f_ruido_path = render_formula(
    r'$g(x, y) = f(x, y) + \eta(x, y)$',
    'formula_ruido_dark.png', fontsize=18, fig_w=4.8, fig_h=0.9
)
f_cierre_path = render_formula(
    r'$A \bullet B = (A \oplus B) \ominus B$',
    'formula_cierre_dark.png', fontsize=19, fig_w=5.2, fig_h=0.9
)

def get_base64(path):
    with open(path, "rb") as f:
        return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"

img_pasos = get_base64(os.path.join(img_dir, "desglose_paso_a_paso.png"))
img_pos = get_base64(os.path.join(img_dir, "comparativa_positive.png"))
img_neg = get_base64(os.path.join(img_dir, "comparativa_negative.png"))

b64_gauss = get_base64(f_gauss_path)
b64_lum = get_base64(f_lum_path)
b64_ruido = get_base64(f_ruido_path)
b64_cierre = get_base64(f_cierre_path)

html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Preprocesamiento de Dataset de Imágenes - Domingo Quispe</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-dark: #090d16;
      --card-bg: rgba(18, 26, 44, 0.75);
      --card-border: rgba(99, 133, 195, 0.2);
      --primary: #3b82f6;
      --primary-light: #60a5fa;
      --accent: #06b6d4;
      --text-main: #f1f5f9;
      --text-muted: #94a3b8;
      --success: #10b981;
      --warning: #f59e0b;
      --glow: rgba(59, 130, 246, 0.25);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
    }}

    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      background: radial-gradient(circle at 15% 15%, #131c31 0%, var(--bg-dark) 55%, #05070c 100%);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}

    /* Top Bar */
    header {{
      height: 58px;
      padding: 0 2rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--card-border);
      background: rgba(9, 13, 22, 0.85);
      backdrop-filter: blur(14px);
      z-index: 100;
    }}

    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
      font-weight: 700;
      font-size: 0.95rem;
      letter-spacing: 0.5px;
    }}

    .brand-badge {{
      background: linear-gradient(135deg, var(--primary), var(--accent));
      color: white;
      font-size: 0.72rem;
      font-weight: 800;
      padding: 4px 10px;
      border-radius: 999px;
      text-transform: uppercase;
      letter-spacing: 1px;
      box-shadow: 0 0 14px var(--glow);
    }}

    .deck-info {{
      font-size: 0.85rem;
      color: var(--text-muted);
      display: flex;
      gap: 1.5rem;
    }}

    .deck-info span strong {{
      color: var(--text-main);
    }}

    /* Main Slide Container */
    main {{
      flex: 1;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 1.5rem 2rem 5.5rem 2rem;
      overflow: hidden;
    }}

    .slide {{
      position: absolute;
      width: min(1200px, 94vw);
      height: min(650px, 80vh);
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 2.2rem 2.8rem;
      display: flex;
      flex-direction: column;
      backdrop-filter: blur(20px);
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.45), 0 0 40px var(--glow);
      opacity: 0;
      transform: scale(0.96) translateY(20px);
      pointer-events: none;
      transition: all 0.45s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    .slide.active {{
      opacity: 1;
      transform: scale(1) translateY(0);
      pointer-events: auto;
      z-index: 10;
    }}

    /* Slide Header */
    .slide-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 1.2rem;
      padding-bottom: 0.8rem;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }}

    .step-tag {{
      display: inline-flex;
      align-items: center;
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1.2px;
      color: var(--accent);
      background: rgba(6, 182, 212, 0.12);
      border: 1px solid rgba(6, 182, 212, 0.3);
      padding: 4px 12px;
      border-radius: 6px;
      margin-bottom: 6px;
    }}

    .slide-title {{
      font-size: 1.65rem;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.2;
    }}

    .slide-subtitle {{
      font-size: 0.95rem;
      color: var(--text-muted);
      margin-top: 4px;
    }}

    .slide-body {{
      flex: 1;
      display: grid;
      gap: 1.5rem;
      align-items: center;
      overflow-y: auto;
      padding-right: 6px;
    }}

    .slide-body.split-2 {{
      grid-template-columns: 1.05fr 0.95fr;
    }}

    .slide-body.full {{
      grid-template-columns: 1fr;
    }}

    /* Card Box Inside Slides */
    .info-card {{
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 14px;
      padding: 1.2rem 1.4rem;
      display: flex;
      flex-direction: column;
      gap: 0.8rem;
    }}

    .card-title {{
      font-size: 0.95rem;
      font-weight: 700;
      color: var(--primary-light);
    }}

    .info-list {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 0.65rem;
    }}

    .info-list li {{
      font-size: 0.9rem;
      line-height: 1.45;
      color: #cbd5e1;
      display: flex;
      align-items: flex-start;
      gap: 8px;
    }}

    .info-list li::before {{
      content: "•";
      color: var(--accent);
      font-weight: bold;
      font-size: 1.2rem;
      line-height: 1;
    }}

    /* Math Formula Image Box */
    .formula-img-card {{
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(96, 165, 250, 0.35);
      border-radius: 12px;
      padding: 0.8rem 1.2rem;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.5), 0 4px 15px rgba(0, 0, 0, 0.25);
    }}

    .formula-img-card .label {{
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--text-muted);
      margin-bottom: 6px;
      display: block;
      align-self: flex-start;
      font-weight: 600;
    }}

    .formula-img-card img {{
      max-width: 100%;
      height: auto;
      display: block;
      filter: drop-shadow(0 2px 8px rgba(56, 189, 248, 0.25));
    }}

    /* Code Snippet */
    .code-box {{
      background: #0b1120;
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 10px;
      padding: 0.9rem 1.1rem;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.8rem;
      color: #e2e8f0;
      overflow-x: auto;
    }}

    .code-box code {{
      display: block;
      line-height: 1.5;
    }}

    .code-box .kw {{ color: #f43f5e; }}
    .code-box .fn {{ color: #38bdf8; }}
    .code-box .str {{ color: #a3e635; }}

    /* Slide Images */
    .slide-img-container {{
      width: 100%;
      height: 100%;
      min-height: 250px;
      max-height: 420px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background: rgba(0, 0, 0, 0.35);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 14px;
      overflow: hidden;
      padding: 0.6rem;
    }}

    .slide-img-container img {{
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
      border-radius: 10px;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
    }}

    .img-caption {{
      font-size: 0.75rem;
      color: var(--text-muted);
      margin-top: 6px;
      text-align: center;
    }}

    /* Cover Slide Specifics */
    .cover-content {{
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100%;
      text-align: center;
      gap: 1.2rem;
    }}

    .cover-badge {{
      display: inline-flex;
      align-items: center;
      padding: 6px 16px;
      background: rgba(59, 130, 246, 0.12);
      border: 1px solid rgba(59, 130, 246, 0.3);
      border-radius: 999px;
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--primary-light);
      letter-spacing: 1px;
      text-transform: uppercase;
    }}

    .cover-title {{
      font-size: 2.5rem;
      font-weight: 800;
      line-height: 1.15;
      background: linear-gradient(135deg, #ffffff 30%, #93c5fd 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      max-width: 900px;
    }}

    .cover-sub {{
      font-size: 1.15rem;
      color: #94a3b8;
      max-width: 750px;
      line-height: 1.5;
    }}

    .cover-meta {{
      display: flex;
      gap: 2.5rem;
      margin-top: 1.2rem;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.08);
      padding: 1rem 2rem;
      border-radius: 14px;
    }}

    .meta-item {{
      display: flex;
      flex-direction: column;
      gap: 3px;
      text-align: left;
    }}

    .meta-label {{
      font-size: 0.7rem;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--text-muted);
    }}

    .meta-val {{
      font-size: 0.95rem;
      font-weight: 700;
      color: #f8fafc;
    }}

    /* Bottom Control Bar */
    footer {{
      position: fixed;
      bottom: 0;
      left: 0;
      width: 100%;
      height: 70px;
      padding: 0 2.5rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: rgba(9, 13, 22, 0.9);
      backdrop-filter: blur(16px);
      border-top: 1px solid var(--card-border);
      z-index: 100;
    }}

    .progress-wrapper {{
      display: flex;
      align-items: center;
      gap: 15px;
      flex: 1;
      max-width: 500px;
    }}

    .progress-bar {{
      flex: 1;
      height: 6px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 999px;
      overflow: hidden;
    }}

    .progress-fill {{
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, var(--primary), var(--accent));
      border-radius: 999px;
      transition: width 0.3s ease;
    }}

    .counter {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.88rem;
      font-weight: 700;
      color: var(--text-muted);
      min-width: 60px;
    }}

    .nav-buttons {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .btn {{
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.12);
      color: #ffffff;
      padding: 8px 18px;
      border-radius: 10px;
      font-family: inherit;
      font-size: 0.88rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s ease;
    }}

    .btn:hover:not(:disabled) {{
      background: rgba(59, 130, 246, 0.25);
      border-color: var(--primary);
      transform: translateY(-1px);
      box-shadow: 0 0 14px var(--glow);
    }}

    .btn:disabled {{
      opacity: 0.35;
      cursor: not-allowed;
    }}

    .btn.primary {{
      background: linear-gradient(135deg, var(--primary), #2563eb);
      border: none;
    }}

    .btn.primary:hover:not(:disabled) {{
      box-shadow: 0 0 20px var(--glow);
    }}

    /* Keyboard Hint */
    .keyboard-hint {{
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 0.75rem;
      color: var(--text-muted);
    }}

    .kbd {{
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 4px;
      padding: 2px 6px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.7rem;
      color: #e2e8f0;
    }}

    /* Custom Scrollbar */
    .slide-body::-webkit-scrollbar {{
      width: 6px;
    }}
    .slide-body::-webkit-scrollbar-thumb {{
      background: rgba(255, 255, 255, 0.15);
      border-radius: 6px;
    }}

    /* Responsive */
    @media (max-width: 900px) {{
      .slide-body.split-2 {{
        grid-template-columns: 1fr;
      }}
      .deck-info, .keyboard-hint {{
        display: none;
      }}
      .cover-title {{
        font-size: 1.8rem;
      }}
      .cover-meta {{
        flex-direction: column;
        gap: 0.8rem;
      }}
    }}
  </style>
</head>
<body>

  <!-- Header -->
  <header>
    <div class="brand">
      <div class="brand-badge">UNSAAC</div>
      <span>Visión Computacional • Proyecto Semestral</span>
    </div>
    <div class="deck-info">
      <span>Estudiante: <strong>Domingo de Guzman Quispe Mamani</strong></span>
      <span>Docente: <strong>Prof. Hans H. Ccacyahuillca Bejar</strong></span>
    </div>
  </header>

  <!-- Slide Deck -->
  <main>

    <!-- SLIDE 1: PORTADA -->
    <section class="slide active" id="slide-1">
      <div class="cover-content">
        <div class="cover-badge">Fase 1: Preprocesamiento de Dataset</div>
        <h1 class="cover-title">Detección y Clasificación Automatizada de Grietas en Superficies de Concreto</h1>
        <p class="cover-sub">Diseño, Fundamentación Matemática e Implementación del Pipeline de Preprocesamiento de Imágenes para Inspección Estructural</p>
        
        <div class="cover-meta">
          <div class="meta-item">
            <span class="meta-label">Estudiante</span>
            <span class="meta-val">Domingo de Guzman Quispe Mamani</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">Docente</span>
            <span class="meta-val">Prof. Hans H. Ccacyahuillca Bejar</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">Dataset Oficial</span>
            <span class="meta-val">Concrete Crack (Özgenel & Sorguç)</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">Universidad</span>
            <span class="meta-val">UNSAAC - Cusco 2026</span>
          </div>
        </div>
      </div>
    </section>

    <!-- SLIDE 2: POR QUÉ ES DESAFIADOR EL DATASET -->
    <section class="slide" id="slide-2">
      <div class="slide-header">
        <div>
          <span class="step-tag">Contexto y Selección</span>
          <h2 class="slide-title">¿Por qué es un Dataset Altamente Desafiador?</h2>
          <p class="slide-subtitle">Concrete Crack Images for Classification (40,000 imágenes originales)</p>
        </div>
      </div>
      <div class="slide-body split-2">
        <div class="info-card">
          <div class="card-title">Desafíos Reales en Entornos de Ingeniería Civil</div>
          <ul class="info-list">
            <li><strong>Ruido de Textura de Alta Frecuencia:</strong> La rugosidad, arena y poros del concreto generan fluctuaciones que se confunden fácilmente con micro-fisuras.</li>
            <li><strong>Bajo Rango Dinámico (Histograma Estrecho):</strong> Las fisuras (gris oscuro) y el concreto (gris medio) tienen una diferencia tonal mínima.</li>
            <li><strong>Iluminación Heterogénea:</strong> Sombras proyectadas y gradientes de luz solar que alteran métodos de umbralización simple.</li>
            <li><strong>Fisuras Discontinuas:</strong> Pequeñas partículas de polvo interrumpen visualmente las grietas reales.</li>
          </ul>
        </div>
        <div class="info-card">
          <div class="card-title">Estructura de Clases del Proyecto</div>
          <ul class="info-list">
            <li><strong>Positive (Con Grieta):</strong> 20,000 fotos de concreto con defectos estructurales.</li>
            <li><strong>Negative (Sin Grieta):</strong> 20,000 fotos de superficies sanas.</li>
            <li><strong>Muestra Balanceada para Git:</strong> 500 imágenes (250 Positive + 250 Negative) procesadas para mantener el repositorio ágil y reproducible.</li>
            <li><strong>Ambientes Reales:</strong> No es un dataset sintético ni de estudio con fondo plano; presenta imperfecciones reales de obra donde técnicas básicas fallan.</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- SLIDE 3: ARQUITECTURA GENERAL DEL PIPELINE -->
    <section class="slide" id="slide-3">
      <div class="slide-header">
        <div>
          <span class="step-tag">Arquitectura del Sistema</span>
          <h2 class="slide-title">El Pipeline de Preprocesamiento Completo</h2>
          <p class="slide-subtitle">Desglose secuencial de las 6 etapas implementadas en preprocessor.py</p>
        </div>
      </div>
      <div class="slide-body full">
        <div class="slide-img-container" style="max-height: 220px;">
          <img src="{img_pasos}" alt="Desglose Paso a Paso">
          <span class="img-caption">Figura 1: Evolución visual de una grieta a lo largo de las fases de preprocesamiento</span>
        </div>
        <div class="info-card" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
          <div>
            <span style="color: var(--accent); font-weight: 700; font-size: 0.85rem;">1. Bicubic Resize</span>
            <p style="font-size: 0.82rem; color: #cbd5e1; margin-top: 3px;">Estandarización a 224x224 preservando bordes finos de 16 vecinos.</p>
          </div>
          <div>
            <span style="color: var(--accent); font-weight: 700; font-size: 0.85rem;">2. Grayscale</span>
            <p style="font-size: 0.82rem; color: #cbd5e1; margin-top: 3px;">Supresión de redundancia cromática (ahorro del 66% de datos).</p>
          </div>
          <div>
            <span style="color: var(--accent); font-weight: 700; font-size: 0.85rem;">3. Gaussian Denoise</span>
            <p style="font-size: 0.82rem; color: #cbd5e1; margin-top: 3px;">Filtro 3x3 para atenuar la textura granular de la arena.</p>
          </div>
          <div>
            <span style="color: var(--accent); font-weight: 700; font-size: 0.85rem;">4. Realce CLAHE</span>
            <p style="font-size: 0.82rem; color: #cbd5e1; margin-top: 3px;">Ecualización adaptativa local 8x8 con clip limit 2.5.</p>
          </div>
          <div>
            <span style="color: var(--accent); font-weight: 700; font-size: 0.85rem;">5. Cierre Morfológico</span>
            <p style="font-size: 0.82rem; color: #cbd5e1; margin-top: 3px;">Operación (A ⊕ B) ⊖ B para unir fisuras discontinuas.</p>
          </div>
          <div>
            <span style="color: var(--accent); font-weight: 700; font-size: 0.85rem;">6. Normalización</span>
            <p style="font-size: 0.82rem; color: #cbd5e1; margin-top: 3px;">Conversión a float32 [0.0, 1.0] para estabilidad numérica.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- SLIDE 4: PASO 1 Y 2 (INTERPOLACIÓN Y ESCALA DE GRISES) -->
    <section class="slide" id="slide-4">
      <div class="slide-header">
        <div>
          <span class="step-tag">Etapas 1 y 2</span>
          <h2 class="slide-title">Remuestreo Bicúbico y Reducción Tonal</h2>
          <p class="slide-subtitle">Fundamentos de Muestreo Espacial y Supresión de Redundancia Cromática</p>
        </div>
      </div>
      <div class="slide-body split-2">
        <div class="info-card">
          <div class="card-title">1.1. Interpolación Bicúbica (cv2.INTER_CUBIC)</div>
          <ul class="info-list">
            <li>El dataset original mide <strong>227 × 227</strong> y se normaliza al estándar <strong>224 × 224</strong>.</li>
            <li>Al realizar el mapeo inverso <code>(x, y) = T⁻¹(x', y')</code>, surgen coordenadas decimales flotantes.</li>
            <li><strong>¿Por qué Bicúbica?</strong> Analiza <strong>16 píxeles vecinos (4 × 4)</strong> con polinomios de 3er grado. A diferencia de la bilineal que difumina, mantiene la nitidez en bordes de 1 píxel.</li>
          </ul>
          <div class="code-box">
            <code><span class="kw">def</span> <span class="fn">resize_bicubic</span>(img_bgr):<br>
            &nbsp;&nbsp;<span class="kw">return</span> cv2.<span class="fn">resize</span>(img_bgr, (<span class="str">224</span>, <span class="str">224</span>), interpolation=cv2.<span class="str">INTER_CUBIC</span>)</code>
          </div>
        </div>
        <div class="info-card">
          <div class="card-title">1.2. Eliminación de Redundancia Cromática</div>
          <ul class="info-list">
            <li>En concreto, tanto la pared como la grieta son tonos neutros: <strong>R ≈ G ≈ B</strong>.</li>
            <li>Procesar 3 canales duplica o triplica el costo sin aportar valor diagnóstico.</li>
            <li>Se aplica la ponderación perceptual estándar (ITU-R BT.601):</li>
          </ul>
          <div class="formula-img-card">
            <span class="label">Conversión a Luminancia (Y)</span>
            <img src="{b64_lum}" alt="Fórmula de Luminancia" style="max-height: 38px;">
          </div>
          <div class="code-box">
            <code><span class="kw">def</span> <span class="fn">to_grayscale</span>(img_bgr):<br>
            &nbsp;&nbsp;<span class="kw">return</span> cv2.<span class="fn">cvtColor</span>(img_bgr, cv2.<span class="str">COLOR_BGR2GRAY</span>)</code>
          </div>
        </div>
      </div>
    </section>

    <!-- SLIDE 5: PASO 3 (RUIDO Y FILTRO GAUSSIANO) -->
    <section class="slide" id="slide-5">
      <div class="slide-header">
        <div>
          <span class="step-tag">Etapa 3</span>
          <h2 class="slide-title">Modelado de Ruido y Filtrado Espacial Gaussiano</h2>
          <p class="slide-subtitle">Atenuación de fluctuaciones granulares antes de la amplificación de contraste</p>
        </div>
      </div>
      <div class="slide-body split-2">
        <div class="info-card">
          <div class="card-title">1.3. Ruido Aditivo de Alta Frecuencia</div>
          <div class="formula-img-card">
            <span class="label">Modelo de Ruido Aditivo</span>
            <img src="{b64_ruido}" alt="Modelo de Ruido" style="max-height: 38px;">
          </div>
          <ul class="info-list">
            <li><strong>f(x, y):</strong> Imagen ideal y limpia de la escena.</li>
            <li><strong>η(x, y):</strong> Ruido de textura generado por arena, grava y ruido del sensor.</li>
            <li><strong>g(x, y):</strong> Imagen ruidosa capturada.</li>
            <li><strong>Orden secuencial:</strong> El filtro va antes de CLAHE porque aplicar CLAHE sobre la imagen cruda amplificaría cada grano de arena como una falsa fisura.</li>
          </ul>
        </div>
        <div class="info-card">
          <div class="card-title">Filtro Gaussiano Bidimensional 3×3</div>
          <div class="formula-img-card">
            <span class="label">Función de Ponderación Gaussiana 2D</span>
            <img src="{b64_gauss}" alt="Función de Ponderación Gaussiana 2D" style="max-height: 58px;">
          </div>
          <ul class="info-list">
            <li>Pondera los vecinos dando el peso mayor al píxel central y decreciendo hacia las esquinas según la campana de Gauss.</li>
            <li>Evita el efecto borroso plano del filtro de promedio simple.</li>
          </ul>
          <div class="code-box">
            <code><span class="kw">def</span> <span class="fn">reduce_noise</span>(img_gray):<br>
            &nbsp;&nbsp;<span class="kw">return</span> cv2.<span class="fn">GaussianBlur</span>(img_gray, (<span class="str">3</span>, <span class="str">3</span>), sigmaX=<span class="str">0</span>)</code>
          </div>
        </div>
      </div>
    </section>

    <!-- SLIDE 6: PUNTO 1.4 (CLAHE Y GRÁFICAS DE HISTOGRAMAS) -->
    <section class="slide" id="slide-6">
      <div class="slide-header">
        <div>
          <span class="step-tag">Etapa 4 • Punto Central</span>
          <h2 class="slide-title">1.4. Análisis de Histogramas y Ecualización CLAHE</h2>
          <p class="slide-subtitle">Resolviendo el bajo contraste y la iluminación heterogénea mediante CLAHE</p>
        </div>
      </div>
      <div class="slide-body split-2">
        <div class="slide-img-container">
          <img src="{img_pos}" alt="Comparativa e Histogramas Positive">
          <span class="img-caption">Figura 2: Imagen Original vs Preprocesada y sus respectivos Histogramas (Clase Positive)</span>
        </div>
        <div class="info-card">
          <div class="card-title">Evidencia Matemática del Histograma</div>
          <ul class="info-list">
            <li><strong>Histograma Original (Izquierda):</strong> Muestra un rango sumamente comprimido (110 a 160). La fisura y el concreto están atrapados en los mismos niveles.</li>
            <li><strong>Histograma CLAHE (Derecha):</strong> Se redistribuye sobre todo el rango dinámico [0, 255]. Los valles oscuros de la grieta caen en [0, 60] y la pared en [120, 240].</li>
            <li><strong>Ecualización Local vs Global:</strong> Se descartó cv2.equalizeHist() porque ante sombras o luz desigual sobresatura y amplifica ruido de fondo; CLAHE opera por teselas locales de 8x8 con corte de pico a 2.5.</li>
          </ul>
          <div class="code-box">
            <code>clahe = cv2.<span class="fn">createCLAHE</span>(clipLimit=<span class="str">2.5</span>, tileGridSize=(<span class="str">8</span>, <span class="str">8</span>))<br>
            enhanced = clahe.<span class="fn">apply</span>(img_denoised)</code>
          </div>
        </div>
      </div>
    </section>

    <!-- SLIDE 7: PASO 5 (MORFOLOGÍA MATEMÁTICA Y CIERRE) -->
    <section class="slide" id="slide-7">
      <div class="slide-header">
        <div>
          <span class="step-tag">Etapa 5</span>
          <h2 class="slide-title">1.5. Morfología Matemática: Cierre Morfológico</h2>
          <p class="slide-subtitle">Reconexión de fisuras discontinuas mediante Elemento Estructurador</p>
        </div>
      </div>
      <div class="slide-body split-2">
        <div class="info-card">
          <div class="card-title">Operación de Cierre Morfológico</div>
          <div class="formula-img-card">
            <span class="label">Definición de Cierre (Dilatación seguida de Erosión)</span>
            <img src="{b64_cierre}" alt="Fórmula de Cierre Morfológico" style="max-height: 38px;">
          </div>
          <ul class="info-list">
            <li><strong>1. Dilatación (A ⊕ B):</strong> Engrosa temporalmente la región oscura de la grieta; los extremos rotos por polvo se tocan y forman un puente continuo.</li>
            <li><strong>2. Erosión posterior (⊖ B):</strong> Restaura el contorno y grosor original exterior de la fisura, pero <strong>el puente de unión se conserva</strong>.</li>
            <li><strong>Elemento Estructurador (B):</strong> Matriz rectangular sólida 3 × 3.</li>
            <li><strong>Propósito:</strong> Repara las discontinuidades causadas por polvo en la pared sin agrandar la grieta artificialmente.</li>
          </ul>
        </div>
        <div class="info-card">
          <div class="card-title">¿Por qué Cierre y NO Apertura?</div>
          <ul class="info-list">
            <li><strong>Apertura (A ∘ B = (A ⊖ B) ⊕ B):</strong> Comienza erosionando. En micro-grietas de 1 o 2 píxeles de ancho, la erosión inicial las consideraría ruido y <strong>las borraría</strong>.</li>
            <li><strong>Cierre:</strong> Protege y conecta grietas sin engrosar el defecto de manera irreversible.</li>
          </ul>
          <div class="code-box">
            <code>kernel = cv2.<span class="fn">getStructuringElement</span>(cv2.<span class="str">MORPH_RECT</span>, (<span class="str">3</span>, <span class="str">3</span>))<br>
            closed = cv2.<span class="fn">morphologyEx</span>(img, cv2.<span class="str">MORPH_CLOSE</span>, kernel)</code>
          </div>
        </div>
      </div>
    </section>

    <!-- SLIDE 8: RESULTADOS COMPARATIVOS (NEGATIVE - SUPERFICIE SANA) -->
    <section class="slide" id="slide-8">
      <div class="slide-header">
        <div>
          <span class="step-tag">Resultados y Validación</span>
          <h2 class="slide-title">Validación en Superficie Sana (Clase Negative)</h2>
          <p class="slide-subtitle">Demostración de que el pipeline no introduce falsas fisuras ni artefactos</p>
        </div>
      </div>
      <div class="slide-body split-2">
        <div class="slide-img-container">
          <img src="{img_neg}" alt="Comparativa e Histogramas Negative">
          <span class="img-caption">Figura 3: Imagen Original vs Preprocesada y sus Histogramas (Clase Negative - Concreto Sano)</span>
        </div>
        <div class="info-card">
          <div class="card-title">Evaluación de Robustez del Pipeline</div>
          <ul class="info-list">
            <li><strong>Ausencia de Falsos Positivos:</strong> Al pasar por el filtro Gaussiano, CLAHE y Cierre, la superficie sana mantiene una distribución homogénea sin líneas fantasma.</li>
            <li><strong>Histograma Controlado:</strong> El histograma final expande la visibilidad del grano sin colapsar en picos artificiales.</li>
            <li><strong>Estandarización:</strong> Ambas clases (Positive y Negative) quedan con la misma dinámica numérica y resolución de 224 × 224.</li>
            <li><strong>Inocuidad Comprobada:</strong> Un buen preprocesamiento no solo debe destacar el defecto, sino ser inocuo sobre las muestras sanas.</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- SLIDE 9: CONCLUSIONES Y PREGUNTAS -->
    <section class="slide" id="slide-9">
      <div class="slide-header">
        <div>
          <span class="step-tag">Cierre de la Exposición</span>
          <h2 class="slide-title">Conclusiones y Respuestas a Preguntas del Docente</h2>
          <p class="slide-subtitle">Resumen ejecutivo para la evaluación final</p>
        </div>
      </div>
      <div class="slide-body split-2">
        <div class="info-card">
          <div class="card-title">Logros del Pipeline</div>
          <ul class="info-list">
            <li><strong>Dataset Desafiador Dominado:</strong> De imágenes crudas con ruido granular a matrices normalizadas de alta calidad.</li>
            <li><strong>Sinergia Teórica Total:</strong> Aplicación de 5 temas del curso (muestreo bicúbico, espacios de color, ruido/Gaussiano, CLAHE y morfología).</li>
            <li><strong>Listo para Fase 2:</strong> Datos estructurados en <code>dataset_preprocesado/</code> listos para extracción de descriptores o Deep Learning.</li>
          </ul>
        </div>
        <div class="info-card">
          <div class="card-title">Respuestas Rápidas Preparadas</div>
          <ul class="info-list">
            <li><strong>¿Por qué 2 carpetas?:</strong> Muestra Original ('Antes') para trazabilidad y Dataset Preprocesado ('Después') para el modelo.</li>
            <li><strong>¿Por qué Bicúbico?:</strong> Para no difuminar bordes sutiles de 1 píxel al escalar a 224x224.</li>
            <li><strong>¿Por qué CLAHE?:</strong> Porque la ecualización global quema zonas con sombras y sobreamplifica ruido en zonas lisas.</li>
          </ul>
          <div style="background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 10px; padding: 0.8rem; text-align: center; color: #86efac; font-size: 0.82rem; font-weight: 700; letter-spacing: 0.5px;">
            ESTADO DE LA ENTREGA 1: Pipeline Completado • Reportes 300 DPI • Repositorio Listo
          </div>
        </div>
      </div>
    </section>

  </main>

  <!-- Footer Controls -->
  <footer>
    <div class="progress-wrapper">
      <span class="counter" id="slide-counter">01 / 09</span>
      <div class="progress-bar">
        <div class="progress-fill" id="progress-fill"></div>
      </div>
    </div>

    <div class="keyboard-hint">
      <span>Navegar con</span>
      <span class="kbd">←</span>
      <span class="kbd">→</span>
      <span>o</span>
      <span class="kbd">Espacio</span>
    </div>

    <div class="nav-buttons">
      <button class="btn" id="prev-btn" onclick="prevSlide()">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"></polyline></svg>
        Anterior
      </button>
      <button class="btn primary" id="next-btn" onclick="nextSlide()">
        Siguiente
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
      </button>
    </div>
  </footer>

  <script>
    const slides = document.querySelectorAll('.slide');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const counter = document.getElementById('slide-counter');
    const progressFill = document.getElementById('progress-fill');

    let currentSlide = 0;
    const totalSlides = slides.length;

    function updateDeck() {{
      slides.forEach((slide, idx) => {{
        slide.classList.toggle('active', idx === currentSlide);
      }});

      const slideNum = (currentSlide + 1).toString().padStart(2, '0');
      const totalNum = totalSlides.toString().padStart(2, '0');
      counter.textContent = `${{slideNum}} / ${{totalNum}}`;

      const pct = (currentSlide / (totalSlides - 1)) * 100;
      progressFill.style.width = `${{pct}}%`;

      prevBtn.disabled = currentSlide === 0;
      if (currentSlide === totalSlides - 1) {{
        nextBtn.textContent = 'Fin';
        nextBtn.disabled = true;
      }} else {{
        nextBtn.innerHTML = 'Siguiente <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>';
        nextBtn.disabled = false;
      }}
    }}

    function nextSlide() {{
      if (currentSlide < totalSlides - 1) {{
        currentSlide++;
        updateDeck();
      }}
    }}

    function prevSlide() {{
      if (currentSlide > 0) {{
        currentSlide--;
        updateDeck();
      }}
    }}

    // Teclado
    document.addEventListener('keydown', (e) => {{
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{
        nextSlide();
      }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{
        prevSlide();
      }} else if (e.key === 'Home') {{
        currentSlide = 0;
        updateDeck();
      }} else if (e.key === 'End') {{
        currentSlide = totalSlides - 1;
        updateDeck();
      }}
    }});

    // Inicializar
    updateDeck();
  </script>
</body>
</html>
"""

with open(out_html, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Presentación con imágenes de fórmulas generada con éxito en: {out_html}")
