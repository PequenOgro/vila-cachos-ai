# -*- coding: utf-8 -*-
"""
Script de Construção da Apresentação Oficial do Seminário 2 - Monografia I (IFMA)
Discente: Marcos Vinícius
Orientador: Prof. Me. Alex Martins Pereira
Coorientadora: Profa. Me. Eveline de Jesus Viana Silva
Docente da Disciplina: Prof. Dr. Hélder Pereira Borges

Requisitos do Seminário 2:
1. Tempo de Apresentação: Rigorosamente 10 Minutos
2. Breve contextualização do Seminário 1 + Foco profundo nos requisitos do Seminário 2:
   - Referencial Teórico & Seção 2.7 Fichamento de 7 obras em tópicos
   - Metodologia de Coleta Multimodal e Arquitetura Desacoplada
   - Validação Experimental (Matriz 4x4 do YOLO, Silhouette Score 0.448)
   - Cronograma detalhado para o TCC 2 (2027.1)
   - Conclusão e Principais Desafios para o TCC 2
3. Saída em PPTX e PDF sem compactação via LibreOffice
"""

import os
import shutil
import subprocess
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEMINARIO_DIR = os.path.join(BASE_DIR, "faculdade_ifma", "tcc_1_monografia", "seminario_apresentacao")
DOCS_DIR = os.path.join(BASE_DIR, "faculdade_ifma", "tcc_1_monografia", "documentos")

PPTX_TEMPLATE = os.path.join(SEMINARIO_DIR, "template slides TCC_backup.pptx")
PPTX_OUT = os.path.join(SEMINARIO_DIR, "Seminario2_Apresentacao_MarcosVinicius.pptx")
PDF_OUT = os.path.join(SEMINARIO_DIR, "Seminario2_Apresentacao_MarcosVinicius.pdf")
IMG_MATRIZ = os.path.join(DOCS_DIR, "fig_matriz_confusao_validada_4x4.png")

SOFFICE_PATH = r"C:\Program Files\LibreOffice\program\soffice.exe"

# Cores do Design System Acadêmico & Emerald Tech
COLOR_PRIMARY = RGBColor(27, 54, 93)     # Deep Academic Navy (#1B365D)
COLOR_ACCENT = RGBColor(16, 124, 65)     # IFMA Emerald Green (#107C41)
COLOR_DARK = RGBColor(30, 41, 59)        # Slate Dark (#1E293B)
COLOR_MUTED = RGBColor(100, 116, 139)    # Slate Muted (#64748B)
COLOR_LIGHT_BG = RGBColor(248, 250, 252) # Light Card (#F8FAFC)
COLOR_BORDER = RGBColor(226, 232, 240)   # Border (#E2E8F0)
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_GOLD = RGBColor(180, 120, 20)

def add_run(p, text, font_name="Open Sans", size_pt=10, bold=False, italic=False, color_rgb=None):
    r = p.add_run()
    r.text = text
    r.font.name = font_name
    r.font.size = Pt(size_pt)
    r.font.bold = bold
    r.font.italic = italic
    if color_rgb:
        r.font.color.rgb = color_rgb
    return r

def create_presentation():
    print("=== INICIANDO CONSTRUÇÃO DOS SLIDES DO SEMINÁRIO 2 (10 MIN) ===")
    prs = pptx.Presentation(PPTX_TEMPLATE)
    
    # Extrair logo do IFMA do template se disponível
    logo_temp_path = os.path.join(BASE_DIR, "scratch", "ifma_logo_temp.png")
    if not os.path.exists(logo_temp_path):
        for s in prs.slides:
            for shp in s.shapes:
                if shp.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.PICTURE:
                    with open(logo_temp_path, "wb") as f:
                        f.write(shp.image.blob)
                    break
            if os.path.exists(logo_temp_path):
                break

    # Limpar slides antigos
    for _ in range(len(prs.slides)):
        rId = prs.slides._sldIdLst[0].rId
        prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[0]

    blank_layout = prs.slide_layouts[10] if len(prs.slide_layouts) > 10 else prs.slide_layouts[6]

    def add_header(slide, title_text, category="TCC I • SEMINÁRIO 2 (10 MIN)", time_tag=""):
        # Top Logo
        if os.path.exists(logo_temp_path):
            slide.shapes.add_picture(logo_temp_path, Inches(6.8), Inches(0.35), Inches(2.7), Inches(0.42))
        
        # Category tag + Time tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.32), Inches(5.5), Inches(0.3))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_right = tf_cat.margin_top = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper() + (f"  |  ⏱️ {time_tag}" if time_tag else "")
        p_cat.font.name = "Open Sans"
        p_cat.font.size = Pt(9.5)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_ACCENT
        
        # Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.62), Inches(5.8), Inches(0.75))
        tf = t_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Open Sans"
        p.font.size = Pt(21)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY

        # Divider line
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.38), Inches(8.4), Pt(1.5))
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_ACCENT
        shape.line.color.rgb = COLOR_ACCENT

    # ==========================================================
    # SLIDE 1: CAPA INSTITUCIONAL (0m00s - 0m30s)
    # ==========================================================
    s1 = prs.slides.add_slide(blank_layout)
    if os.path.exists(logo_temp_path):
        s1.shapes.add_picture(logo_temp_path, Inches(6.4), Inches(0.5), Inches(2.9), Inches(0.45))

    dec1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.15), Pt(6), Inches(2.35))
    dec1.fill.solid()
    dec1.fill.fore_color.rgb = COLOR_ACCENT
    dec1.line.fill.background()

    t1_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.05), Inches(8.0), Inches(2.4))
    tf1 = t1_box.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = 0

    p_tag = tf1.paragraphs[0]
    p_tag.text = "PROJETO DE TRABALHO DE CONCLUSÃO DE CURSO I  •  SEMINÁRIO 2"
    p_tag.font.name = "Open Sans"
    p_tag.font.size = Pt(11.5)
    p_tag.font.bold = True
    p_tag.font.color.rgb = COLOR_ACCENT
    p_tag.space_after = Pt(4)

    p_t = tf1.add_paragraph()
    p_t.text = "Vila Cachos AI"
    p_t.font.name = "Open Sans"
    p_t.font.size = Pt(36)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_PRIMARY
    p_t.space_after = Pt(4)

    p_sub = tf1.add_paragraph()
    p_sub.text = "Sistema Híbrido de Recomendação Capilar com Aprendizado Não Supervisionado e Inferência Bayesiana"
    p_sub.font.name = "Open Sans"
    p_sub.font.size = Pt(13.5)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_DARK
    p_sub.space_after = Pt(4)

    p_app = tf1.add_paragraph()
    p_app.text = "Um Web App de Diagnóstico Integrado para o Salão Vila Cachos"
    p_app.font.name = "Open Sans"
    p_app.font.size = Pt(12.5)
    p_app.font.italic = True
    p_app.font.color.rgb = COLOR_MUTED

    card1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.6), Inches(8.4), Inches(1.4))
    card1.fill.solid()
    card1.fill.fore_color.rgb = COLOR_LIGHT_BG
    card1.line.color.rgb = COLOR_BORDER

    m_box = s1.shapes.add_textbox(Inches(1.05), Inches(3.7), Inches(7.9), Inches(1.2))
    tf_m = m_box.text_frame
    tf_m.word_wrap = True
    tf_m.margin_left = tf_m.margin_right = tf_m.margin_top = tf_m.margin_bottom = 0

    pm1 = tf_m.paragraphs[0]
    pm1.text = "Autor: Marcos Vinícius  |  Curso: Bacharelado em Sistemas de Informação - IFMA"
    pm1.font.name = "Open Sans"
    pm1.font.size = Pt(12)
    pm1.font.bold = True
    pm1.font.color.rgb = COLOR_DARK
    pm1.space_after = Pt(4)

    pm2 = tf_m.add_paragraph()
    pm2.text = "Orientador: Prof. Me. Alex Martins Pereira  |  Coorientadora: Profa. Me. Eveline de Jesus Viana Silva"
    pm2.font.name = "Open Sans"
    pm2.font.size = Pt(11.5)
    pm2.font.color.rgb = COLOR_DARK
    pm2.space_after = Pt(4)

    pm3 = tf_m.add_paragraph()
    pm3.text = "Disciplina: Monografia I  •  Docente: Prof. Dr. Hélder Pereira Borges  •  Seminário 2 (2026)"
    pm3.font.name = "Open Sans"
    pm3.font.size = Pt(11)
    pm3.font.color.rgb = COLOR_MUTED

    # ==========================================================
    # SLIDE 2: CONTEXTO, PROBLEMA & HIPÓTESE (0m30s - 2m00s)
    # ==========================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Contexto & Problema de Pesquisa", time_tag="1m30s")

    # Card 1: Contexto e Gargalo
    c1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.55), Inches(4.0), Inches(3.5))
    c1.fill.solid()
    c1.fill.fore_color.rgb = COLOR_LIGHT_BG
    c1.line.color.rgb = COLOR_BORDER
    tb1 = s2.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(3.6), Inches(3.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = 0

    p = tf1.paragraphs[0]
    p.text = "O CENÁRIO CLÍNICO & MERCADO"
    p.font.name = "Open Sans"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    p.space_after = Pt(8)

    p_body = tf1.add_paragraph()
    p_body.text = (
        "• Mercado de Cachos e Crespos: Mais de 70% da população brasileira possui cabelos ondulados, cacheados ou crespos (Tipos 2A a 4C);\n\n"
        "• Diagnóstico Empírico e Subjetivo: A triagem capilar tradicional depende exclusivamente da percepção tátil da cabeleireira, gerando assimetria diagnóstica;\n\n"
        "• Desafio do Cold Start Absoluto: Novos clientes chegam ao salão sem nenhum histórico transacional, inviabilizando motores colaborativos padrão;\n\n"
        "• Risco de Incompatibilidade Química: O uso de cosméticos com pH ou densidade lipídica incorreta resulta em efeito rebote e perda de clientes."
    )
    p_body.font.name = "Open Sans"
    p_body.font.size = Pt(10)
    p_body.font.color.rgb = COLOR_DARK

    # Card 2: Pergunta-Problema e Hipótese
    c2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.2), Inches(1.55), Inches(4.0), Inches(3.5))
    c2.fill.solid()
    c2.fill.fore_color.rgb = COLOR_LIGHT_BG
    c2.line.color.rgb = COLOR_BORDER
    tb2 = s2.shapes.add_textbox(Inches(5.4), Inches(1.7), Inches(3.6), Inches(3.2))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_right = tf2.margin_top = tf2.margin_bottom = 0

    p = tf2.paragraphs[0]
    p.text = "PERGUNTA-PROBLEMA & HIPÓTESE"
    p.font.name = "Open Sans"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(8)

    p_quest = tf2.add_paragraph()
    p_quest.text = "❓ Pergunta-Problema:"
    p_quest.font.bold = True
    p_quest.font.size = Pt(10.5)
    p_quest.font.color.rgb = COLOR_DARK
    p_q_body = tf2.add_paragraph()
    p_q_body.text = "De que maneira a integração de um extrator morfológico por visão computacional a um motor híbrido (K-Means + Bayesiano) pode mitigar o Cold Start e prover recomendações capilares personalizadas e clinicamente consistentes?"
    p_q_body.font.size = Pt(9.5)
    p_q_body.font.italic = True
    p_q_body.font.color.rgb = COLOR_MUTED
    p_q_body.space_after = Pt(10)

    p_hyp = tf2.add_paragraph()
    p_hyp.text = "💡 Hipótese da Pesquisa:"
    p_hyp.font.bold = True
    p_hyp.font.size = Pt(10.5)
    p_hyp.font.color.rgb = COLOR_DARK
    p_h_body = tf2.add_paragraph()
    p_h_body.text = "A fusão estruturada da taxonomia de André Walker com segmentação não-supervisionada (k=4) e ponderação bayesiana permite atingir acurácia diagnóstica > 85%, eliminando a dependência de histórico prévio sem exceder restrições de nuvem gratuita (512 MB RAM)."
    p_h_body.font.size = Pt(9.5)
    p_h_body.font.italic = True
    p_h_body.font.color.rgb = COLOR_MUTED

    # ==========================================================
    # SLIDE 3: OBJETIVOS DO PROJETO (2m00s - 3m00s)
    # ==========================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Objetivos do Trabalho", time_tag="1m00s")

    # Banner Objetivo Geral
    bg_geral = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.55), Inches(8.4), Inches(0.95))
    bg_geral.fill.solid()
    bg_geral.fill.fore_color.rgb = COLOR_PRIMARY
    bg_geral.line.fill.background()

    tb_g = s3.shapes.add_textbox(Inches(1.05), Inches(1.65), Inches(7.9), Inches(0.75))
    tfg = tb_g.text_frame
    tfg.word_wrap = True
    tfg.margin_left = tfg.margin_right = tfg.margin_top = tfg.margin_bottom = 0
    pg1 = tfg.paragraphs[0]
    pg1.text = "OBJETIVO GERAL"
    pg1.font.bold = True
    pg1.font.size = Pt(10.5)
    pg1.font.color.rgb = COLOR_WHITE
    pg1.space_after = Pt(2)
    pg2 = tfg.add_paragraph()
    pg2.text = "Projetar, implementar e validar um Motor Híbrido de Recomendação Capilar integrado a uma aplicação web interativa para diagnóstico e prescrição cosmética personalizada de curvaturas 2A a 4C no Salão Vila Cachos."
    pg2.font.size = Pt(10.5)
    pg2.font.color.rgb = COLOR_WHITE

    # Grid 6 Objetivos Específicos (2x3)
    grid_y = Inches(2.65)
    col_w = Inches(4.05)
    row_h = Inches(0.82)
    gap_x = Inches(0.3)
    gap_y = Inches(0.12)

    objs = [
        ("1. Modelagem Taxonômica", "Formalizar a taxonomia clínica de curvaturas (Walker, 1997) e a matriz de afinidade terapêutica dos 27 cosméticos."),
        ("2. Visão Computacional", "Integrar modelo YOLOv8/11 ajustado via Transfer Learning para classificar mechas (Tipos 2, 3, 4 e controle negativo)."),
        ("3. Clusterização K-Means", "Calibrar agrupamento não-supervisionado em 8 variáveis clínicas normalizadas para segmentação em personas."),
        ("4. Aprendizado Bayesiano", "Implementar feedback loop contínuo via Média Bayesiana Amortecida (alpha=10) para estabilização de rankings."),
        ("5. Interface & Gateway API", "Construir Web App responsivo (React/Vite) desacoplado de API FastAPI sob limite de 512 MB de RAM."),
        ("6. Validação Métrica Formal", "Avaliar qualidade estatística por Inércia (WCSS) e Silhouette Score (RNF-12: score = 0,448) com 95 testes E2E.")
    ]

    for idx, (title, desc) in enumerate(objs):
        r = idx // 2
        c = idx % 2
        x = Inches(0.8) + c * (col_w + gap_x)
        y = grid_y + r * (row_h + gap_y)

        box_obj = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, col_w, row_h)
        box_obj.fill.solid()
        box_obj.fill.fore_color.rgb = COLOR_LIGHT_BG
        box_obj.line.color.rgb = COLOR_BORDER

        tb_o = s3.shapes.add_textbox(x + Inches(0.15), y + Inches(0.08), col_w - Inches(0.3), row_h - Inches(0.16))
        tfo = tb_o.text_frame
        tfo.word_wrap = True
        tfo.margin_left = tfo.margin_right = tfo.margin_top = tfo.margin_bottom = 0

        po1 = tfo.paragraphs[0]
        po1.text = title
        po1.font.bold = True
        po1.font.size = Pt(10)
        po1.font.color.rgb = COLOR_ACCENT

        po2 = tfo.add_paragraph()
        po2.text = desc
        po2.font.size = Pt(8.5)
        po2.font.color.rgb = COLOR_DARK

    # ==========================================================
    # SLIDE 4: REFERENCIAL TEÓRICO (3m00s - 4m30s)
    # ==========================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Referencial Teórico: Eixos Estruturantes", time_tag="1m30s")

    eixos = [
        ("Sistemas de Recomendação", "Aggarwal (2016) & Burke (2010)", "Filtragem Baseada em Conhecimento (Knowledge-Based) e restrições clínicas para aniquilar o Cold Start na primeira triagem."),
        ("Clusterização K-Means", "Kaufman & Rousseeuw (1990)", "Agrupamento particional não-supervisionado em 8 dimensões tricológicas; métrica Silhouette Score para seleção ótima de k=4 personas."),
        ("Inferência Bayesiana", "Média Amortecida (alpha=10)", "Mecanismo de feedback adaptativo que estabiliza rankings clínicos, evitando que poucas avaliações distorçam as prescrições."),
        ("Explicabilidade (XAI)", "Haloho & Liao (2026)", "Geração transparente de justificativas clínicas baseadas em afinidade dermatológica (porosidade, pH e hidratação)."),
        ("Visão Computacional", "YOLOv8/11 & Walker (1997)", "Extrator morfológico convolucional com taxonomia de curvatura e rejeição robusta de fotos fora do domínio capilar.")
    ]

    for idx, (title, auth, desc) in enumerate(eixos):
        y = Inches(1.55) + idx * Inches(0.68)
        card_e = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(8.4), Inches(0.60))
        card_e.fill.solid()
        card_e.fill.fore_color.rgb = COLOR_LIGHT_BG
        card_e.line.color.rgb = COLOR_BORDER

        tb_e = s4.shapes.add_textbox(Inches(0.95), y + Inches(0.08), Inches(8.1), Inches(0.48))
        tfe = tb_e.text_frame
        tfe.word_wrap = True
        tfe.margin_left = tfe.margin_right = tfe.margin_top = tfe.margin_bottom = 0

        p1 = tfe.paragraphs[0]
        r1 = add_run(p1, f"{idx+1}. {title} ", font_name="Open Sans", size_pt=10.5, bold=True, color_rgb=COLOR_PRIMARY)
        r2 = add_run(p1, f"({auth}): ", font_name="Open Sans", size_pt=9.5, bold=True, color_rgb=COLOR_ACCENT)
        r3 = add_run(p1, desc, font_name="Open Sans", size_pt=9, bold=False, color_rgb=COLOR_DARK)

    # ==========================================================
    # SLIDE 5: FICHAMENTO DE PUBLICAÇÕES (4m30s - 6m00s)
    # ==========================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Fichamento & Trabalhos Correlatos (Seção 2.7)", time_tag="1m30s")

    # Banner informativo do Seminário 2
    b_fich = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.50), Inches(8.4), Inches(0.55))
    b_fich.fill.solid()
    b_fich.fill.fore_color.rgb = COLOR_ACCENT
    b_fich.line.fill.background()

    tb_bf = s5.shapes.add_textbox(Inches(0.95), Inches(1.55), Inches(8.1), Inches(0.45))
    tf_bf = tb_bf.text_frame
    tf_bf.word_wrap = True
    tf_bf.margin_left = tf_bf.margin_right = tf_bf.margin_top = tf_bf.margin_bottom = 0
    pbf = tf_bf.paragraphs[0]
    pbf.text = "FICHAMENTO ESTRUTURADO EM TÓPICOS (7 OBRAS OBRIGATÓRIAS - SEMINÁRIO 2)"
    pbf.font.bold = True
    pbf.font.size = Pt(10)
    pbf.font.color.rgb = COLOR_WHITE
    pbf2 = tf_bf.add_paragraph()
    pbf2.text = "Análise sistemática: Conceitos, Metodologia, Resultados, Limitações e Aderência Direta ao Vila Cachos AI."
    pbf2.font.size = Pt(8.5)
    pbf2.font.color.rgb = COLOR_WHITE

    # Tabela com as 7 obras
    table_shape = s5.shapes.add_table(8, 4, Inches(0.8), Inches(2.15), Inches(8.4), Inches(2.95))
    t = table_shape.table
    t.columns[0].width = Inches(1.5) # Autor / Ano
    t.columns[1].width = Inches(2.0) # Obra / Veículo
    t.columns[2].width = Inches(2.4) # Núcleo Teórico & Metodologia
    t.columns[3].width = Inches(2.5) # Contribuição para Vila Cachos AI

    headers = ["Autor / Ano", "Obra / Veículo", "Núcleo Conceitual", "Aplicação Direta no Projeto"]
    for i, h in enumerate(headers):
        cell = t.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

    works_data = [
        ("Aggarwal (2016)", "Recommender Systems (Springer)", "Teoria formal de recomendadores e cold start", "Arquitetura híbrida de dois estágios contra esparsidade"),
        ("Burke (2010)", "Knowledge-Based Systems (CRC Press)", "Taxonomia de 7 híbridos e imunidade ao cold start", "Matriz de restrições clínicas dos 27 cosméticos"),
        ("Kaufman (1990)", "Finding Groups in Data (Wiley)", "Agrupamento particional e métrica Silhouette", "Validação formal do RNF-12 (Silhouette 0,448 com k=4)"),
        ("Walker (1997)", "Andre Talks Hair (Cosmetologia)", "Taxonomia universal de curvaturas 1A a 4C", "Ground truth categórico para o modelo de visão"),
        ("Haloho (2026)", "3-Stage Hybrid Model (Springer)", "Recomendação cosmética clínica multiestágio", "Módulo de Explicabilidade (XAI) e ranking vetorial"),
        ("Meishvili (2024)", "Hairmony (arXiv:2410.11528)", "Fairness em curvatura com dados sintéticos", "Data Augmentation para eliminar viés em crespos (Tipo 4)"),
        ("He et al. (2024)", "PERM (arXiv:2407.19451)", "Decomposição de geometria global e frizz local", "Desacoplamento da predição de curvatura e frizz via YOLO")
    ]

    for r_idx, row in enumerate(works_data):
        for c_idx, val in enumerate(row):
            cell = t.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_WHITE if r_idx % 2 == 0 else COLOR_LIGHT_BG
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8)
            p.font.color.rgb = COLOR_DARK
            if c_idx == 0:
                p.font.bold = True
                p.font.color.rgb = COLOR_PRIMARY

    # ==========================================================
    # SLIDE 6: METODOLOGIA DA PESQUISA & COLETA MULTIMODAL (6m00s - 7m30s)
    # ==========================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Metodologia & Coleta Multimodal", time_tag="1m30s")

    # Coluna Esquerda: Classificação e Coleta
    c_m1 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.55), Inches(4.0), Inches(3.5))
    c_m1.fill.solid()
    c_m1.fill.fore_color.rgb = COLOR_LIGHT_BG
    c_m1.line.color.rgb = COLOR_BORDER
    tbm1 = s6.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(3.6), Inches(3.2))
    tfm1 = tbm1.text_frame
    tfm1.word_wrap = True
    tfm1.margin_left = tfm1.margin_right = tfm1.margin_top = tfm1.margin_bottom = 0

    p = tfm1.paragraphs[0]
    p.text = "PROCEDIMENTOS METODOLÓGICOS"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(8)

    p_body = tfm1.add_paragraph()
    p_body.text = (
        "• Classificação da Pesquisa: Aplicada, quantitativa-qualitativa, de engenharia de software e ciência de dados;\n\n"
        "• Base Histórica de Atendimentos: 1.084 clientes enriquecidos com diagnósticos e feedbacks clínicos reais;\n\n"
        "• Catálogo Canônico Especializado: 27 cosméticos profissionais catalogados (Curly Care, Arvensis, Deva Curl, Kah-Noa) com matrizes de afinidade terapêutica;\n\n"
        "• Partição Cega de Teste: 91 fotografias reais e desafiadoras de mechas e couro cabeludo para validação sem viés."
    )
    p_body.font.size = Pt(9.5)
    p_body.font.color.rgb = COLOR_DARK

    # Coluna Direita: Arquitetura Desacoplada
    c_m2 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.2), Inches(1.55), Inches(4.0), Inches(3.5))
    c_m2.fill.solid()
    c_m2.fill.fore_color.rgb = COLOR_LIGHT_BG
    c_m2.line.color.rgb = COLOR_BORDER
    tbm2 = s6.shapes.add_textbox(Inches(5.4), Inches(1.7), Inches(3.6), Inches(3.2))
    tfm2 = tbm2.text_frame
    tfm2.word_wrap = True
    tfm2.margin_left = tfm2.margin_right = tfm2.margin_top = tfm2.margin_bottom = 0

    p = tfm2.paragraphs[0]
    p.text = "ARQUITETURA BCE & FLUXO MULTIMODAL"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = COLOR_ACCENT
    p.space_after = Pt(8)

    p_arc = tfm2.add_paragraph()
    p_arc.text = (
        "1. Boundary (Frontend React/Vite):\n"
        "Interface de autoatendimento no Totem e Painel Gestor com Telemetria (RNF-12) e catálogo interativo;\n\n"
        "2. Control (API FastAPI & Motor Híbrido):\n"
        "Gateway RESTful com injeção de dependência (DIP), orquestrando o pipeline de inferência YOLO e K-Means;\n\n"
        "3. Entity (Modelos & Repositórios):\n"
        "Contratos formais de domínio (CatalogRepository, SessionRepository) e armazenamento de histórico causal;\n\n"
        "4. Restrições de Nuvem:\n"
        "Otimizado para teto estrito de 512 MB de RAM no Render Cloud com tempo de resposta p95 < 200 ms."
    )
    p_arc.font.size = Pt(9)
    p_arc.font.color.rgb = COLOR_DARK

    # ==========================================================
    # SLIDE 7: RESULTADOS & VALIDAÇÃO EXPERIMENTAL (7m30s - 9m00s)
    # ==========================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Validação Métrica & Resultados Experimentais", time_tag="1m30s")

    # Coluna Esquerda: Imagem da Matriz de Confusão 4x4
    if os.path.exists(IMG_MATRIZ):
        s7.shapes.add_picture(IMG_MATRIZ, Inches(0.8), Inches(1.55), Inches(3.8), Inches(3.4))

    # Coluna Direita: Métricas Detalhadas do Modelo
    c_res = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(1.55), Inches(4.4), Inches(3.5))
    c_res.fill.solid()
    c_res.fill.fore_color.rgb = COLOR_LIGHT_BG
    c_res.line.color.rgb = COLOR_BORDER
    tb_res = s7.shapes.add_textbox(Inches(5.0), Inches(1.68), Inches(4.0), Inches(3.2))
    tf_res = tb_res.text_frame
    tf_res.word_wrap = True
    tf_res.margin_left = tf_res.margin_right = tf_res.margin_top = tf_res.margin_bottom = 0

    pr = tf_res.paragraphs[0]
    pr.text = "DESEMPENHO DOS MÓDULOS DE IA"
    pr.font.bold = True
    pr.font.size = Pt(11.5)
    pr.font.color.rgb = COLOR_PRIMARY
    pr.space_after = Pt(6)

    pr_body = tf_res.add_paragraph()
    pr_body.text = (
        "📊 Classificador Visual (YOLOv8/11 - Teste Cego 91 Amostras):\n"
        "• Acurácia Global Top-1: 87,4%\n"
        "• Tipo 2 (Ondulados): Recall 88,0% | F1-Score 86,3%\n"
        "• Tipo 3 (Cacheados): Precision 88,9% | F1-Score 85,7%\n"
        "• Tipo 4 (Crespos): Recall 92,9% | F1-Score 89,7%\n"
        "• Controle Negativo (Calvície/Sem mecha): 100,0% de sensibilidade (0 falsos positivos de cacho)\n\n"
        "🎯 Validação dos Agrupamentos Tricológicos (RNF-12):\n"
        "• Coeficiente Silhouette: 0,448 (Superior ao teto exigido de 0,40)\n"
        "• Estrutura dos 4 Clusters: Personas clínicas balanceadas e coesas\n\n"
        "🛡️ Qualidade de Engenharia de Software:\n"
        "• 95 testes automatizados (E2E e unitários) passando com 100% de sucesso."
    )
    pr_body.font.size = Pt(8.8)
    pr_body.font.color.rgb = COLOR_DARK

    # ==========================================================
    # SLIDE 8: CRONOGRAMA DE EXECUÇÃO DO TCC 2 (9m00s - 9m45s)
    # ==========================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Cronograma de Execução: TCC 2 (2027.1)", time_tag="0m45s")

    # Banner TCC 2
    b_cron = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.50), Inches(8.4), Inches(0.50))
    b_cron.fill.solid()
    b_cron.fill.fore_color.rgb = COLOR_PRIMARY
    b_cron.line.fill.background()

    tb_bc = s8.shapes.add_textbox(Inches(0.95), Inches(1.55), Inches(8.1), Inches(0.40))
    tf_bc = tb_bc.text_frame
    tf_bc.word_wrap = True
    tf_bc.margin_left = tf_bc.margin_right = tf_bc.margin_top = tf_bc.margin_bottom = 0
    pbc = tf_bc.paragraphs[0]
    pbc.text = "PLANEJAMENTO OPERACIONAL DO SEMESTRE SEGUINTE (FEVEREIRO A JULHO DE 2027)"
    pbc.font.bold = True
    pbc.font.size = Pt(10)
    pbc.font.color.rgb = COLOR_WHITE

    # Tabela Cronograma TCC 2
    tbl_cron_shape = s8.shapes.add_table(10, 7, Inches(0.8), Inches(2.10), Inches(8.4), Inches(3.0))
    tc = tbl_cron_shape.table
    tc.columns[0].width = Inches(4.2)
    for c in range(1, 7):
        tc.columns[c].width = Inches(0.7)

    c_headers = ["Etapa de Execução do TCC 2", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul"]
    for i, h in enumerate(c_headers):
        cell = tc.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

    cron_rows = [
        ("1. Instalação física do Totem e treinamento da equipe no salão", "X", "", "", "", "", ""),
        ("2. Coleta de dados longitudinais de clientes reais e testes UAT", "X", "X", "", "", "", ""),
        ("3. Calibração contínua dos pesos bayesianos com feedbacks reais", "", "X", "X", "", "", ""),
        ("4. Avaliação estatística de satisfação pós-atendimento e acurácia clínica", "", "", "X", "X", "", ""),
        ("5. Refinamento de UI/UX e otimização de latência em redes móveis", "", "", "", "X", "", ""),
        ("6. Redação dos Capítulos de Resultados Experimentais e Discussão", "", "", "X", "X", "X", ""),
        ("7. Revisão final do texto completo da Monografia com Orientadores", "", "", "", "", "X", ""),
        ("8. Depósito formal do TCC 2 junto à Coordenação do Curso", "", "", "", "", "X", "X"),
        ("9. Defesa Pública perante a Banca Examinadora do IFMA", "", "", "", "", "", "X")
    ]

    for r_idx, row in enumerate(cron_rows):
        for c_idx, val in enumerate(row):
            cell = tc.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_WHITE if r_idx % 2 == 0 else COLOR_LIGHT_BG
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8)
            p.font.color.rgb = COLOR_DARK
            if c_idx > 0:
                p.alignment = PP_ALIGN.CENTER
                p.font.bold = True
                p.font.color.rgb = COLOR_ACCENT

    # ==========================================================
    # SLIDE 9: CONCLUSÃO, DESAFIOS & REFERÊNCIAS (9m45s - 10m00s)
    # ==========================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Conclusão, Desafios & Referências", time_tag="0m45s")

    # Card Conclusão e Desafios
    c_c = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.55), Inches(4.3), Inches(3.5))
    c_c.fill.solid()
    c_c.fill.fore_color.rgb = COLOR_LIGHT_BG
    c_c.line.color.rgb = COLOR_BORDER
    tb_c = s9.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(3.9), Inches(3.2))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0

    pc = tf_c.paragraphs[0]
    pc.text = "CONCLUSÃO & DESAFIOS PARA O TCC 2"
    pc.font.bold = True
    pc.font.size = Pt(11)
    pc.font.color.rgb = COLOR_PRIMARY
    pc.space_after = Pt(6)

    pc_body = tf_c.add_paragraph()
    pc_body.text = (
        "✅ Entregas Consolidadas no TCC 1:\n"
        "• MVP arquitetural 100% funcional e operando sob restrições de nuvem;\n"
        "• Solução robusta do Cold Start via taxonomia especialista e K-Means;\n"
        "• Classificador visual 4x4 validado com 87,4% de acurácia global.\n\n"
        "🎯 Principais Desafios para o TCC 2:\n"
        "1. Variabilidade Óptica: Iluminação ambiente de salão em smartphones;\n"
        "2. Limites de Nuvem: Manter p95 < 200 ms sob 512 MB de RAM no Render;\n"
        "3. Calibração Longitudinal: Acompanhar a convergência das notas reais das clientes ao longo das semanas."
    )
    pc_body.font.size = Pt(8.8)
    pc_body.font.color.rgb = COLOR_DARK

    # Card Referências e Ficha de Aceite
    c_r = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.3), Inches(1.55), Inches(3.9), Inches(3.5))
    c_r.fill.solid()
    c_r.fill.fore_color.rgb = COLOR_LIGHT_BG
    c_r.line.color.rgb = COLOR_BORDER
    tb_r = s9.shapes.add_textbox(Inches(5.5), Inches(1.7), Inches(3.5), Inches(3.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0

    pr = tf_r.paragraphs[0]
    pr.text = "REFERÊNCIAS FUNDAMENTAIS & ACEITE"
    pr.font.bold = True
    pr.font.size = Pt(11)
    pr.font.color.rgb = COLOR_ACCENT
    pr.space_after = Pt(6)

    pr_body = tf_r.add_paragraph()
    pr_body.text = (
        "📚 Literatura Canônica (ABNT NBR 6023):\n"
        "• AGGARWAL, C. C. Recommender Systems. Springer, 2016.\n"
        "• BURKE, R. Knowledge-Based Systems. CRC Press, 2010.\n"
        "• KAUFMAN, L.; ROUSSEEUW, P. Finding Groups. Wiley, 1990.\n"
        "• HALOHO, J.; LIAO, Y. 3-Stage Model. Springer, 2026.\n"
        "• MEISHVILI, G. et al. Hairmony. arXiv, 2024.\n"
        "• WALKER, A. Andre Talks Hair. Simon & Schuster, 1997.\n\n"
        "✍️ Ficha de Aceite de Orientação (Anexo 1):\n"
        "• Orientador: Prof. Me. Alex Martins Pereira\n"
        "• Coorientadora: Profa. Me. Eveline de Jesus Viana Silva\n"
        "• Discente: Marcos Vinícius (IFMA - Monte Castelo)"
    )
    pr_body.font.size = Pt(8.2)
    pr_body.font.color.rgb = COLOR_DARK

    # Salvar apresentação PPTX
    prs.save(PPTX_OUT)
    # Também atualizar template slides TCC.pptx
    shutil.copyfile(PPTX_OUT, os.path.join(SEMINARIO_DIR, "template slides TCC.pptx"))
    print(f"Apresentação PPTX salva com sucesso em: {PPTX_OUT}")

    # Converter para PDF sem compactação via LibreOffice
    print("Convertendo apresentação para PDF sem compactação via LibreOffice...")
    cmd = [SOFFICE_PATH, "--headless", "--convert-to", "pdf", PPTX_OUT, "--outdir", SEMINARIO_DIR]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(PDF_OUT):
        print(f"Apresentação PDF gerada com sucesso em: {PDF_OUT} ({os.path.getsize(PDF_OUT)} bytes)")
    else:
        print(f"Erro na conversão PDF do PPTX: {res.stderr}")

if __name__ == "__main__":
    create_presentation()
