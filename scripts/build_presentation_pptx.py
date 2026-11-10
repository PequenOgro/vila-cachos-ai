import os
import shutil
import subprocess
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

BASE_TCC1_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "faculdade_ifma", "tcc_1_monografia", "seminario_apresentacao")
PPTX_TEMPLATE = os.path.join(BASE_TCC1_DIR, "template slides TCC_backup.pptx")
PPTX_OUT = os.path.join(BASE_TCC1_DIR, "template slides TCC.pptx")
PPTX_OFFICIAL = os.path.join(BASE_TCC1_DIR, "Seminario1_Apresentacao_MarcosVinicius.pptx")
PDF_DIR = BASE_TCC1_DIR
SOFFICE_PATH = r"C:\Program Files\LibreOffice\program\soffice.exe"

# Colors matching academic standards
COLOR_PRIMARY = RGBColor(27, 54, 93)     # Deep Academic Navy
COLOR_ACCENT = RGBColor(16, 124, 65)     # IFMA Green
COLOR_DARK = RGBColor(30, 41, 59)        # Slate Dark
COLOR_MUTED = RGBColor(100, 116, 139)    # Slate Muted
COLOR_LIGHT_BG = RGBColor(248, 250, 252) # Light Card
COLOR_BORDER = RGBColor(226, 232, 240)   # Border

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
    prs = pptx.Presentation(PPTX_TEMPLATE)
    
    # Extract logo from slide 2
    logo_bytes = None
    slide2 = prs.slides[1]
    for s in slide2.shapes:
        if s.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.PICTURE:
            logo_bytes = s.image.blob
            break
            
    logo_temp_path = r"c:\Users\Marcos Vinícius\Documents\TCC\scratch\ifma_logo_temp.png"
    if logo_bytes:
        with open(logo_temp_path, "wb") as f:
            f.write(logo_bytes)

    # Remove all existing slides from prs
    for _ in range(len(prs.slides)):
        rId = prs.slides._sldIdLst[0].rId
        prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[0]

    blank_layout = prs.slide_layouts[10] # BLANK

    def add_header(slide, title_text, category="TCC I • SEMINÁRIO 1"):
        # Top Logo
        if os.path.exists(logo_temp_path):
            slide.shapes.add_picture(logo_temp_path, Inches(6.8), Inches(0.4), Inches(2.7), Inches(0.42))
        
        # Category tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(5.5), Inches(0.3))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_right = tf_cat.margin_top = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.name = "Open Sans"
        p_cat.font.size = Pt(9.5)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_ACCENT
        
        # Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(5.8), Inches(0.75))
        tf = t_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Open Sans"
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY

        # Divider line
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.42), Inches(8.4), Pt(1.5))
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_ACCENT
        shape.line.color.rgb = COLOR_ACCENT

    # ==========================================================
    # SLIDE 1: CAPA
    # ==========================================================
    s1 = prs.slides.add_slide(blank_layout)
    if os.path.exists(logo_temp_path):
        s1.shapes.add_picture(logo_temp_path, Inches(6.4), Inches(0.5), Inches(2.9), Inches(0.45))

    # Decorative accent block on left
    dec = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.15), Pt(6), Inches(2.35))
    dec.fill.solid()
    dec.fill.fore_color.rgb = COLOR_ACCENT
    dec.line.fill.background()

    # Title Box
    t1_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.05), Inches(8.0), Inches(2.4))
    tf1 = t1_box.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = 0

    p_tag = tf1.paragraphs[0]
    p_tag.text = "PROJETO DE TRABALHO DE CONCLUSÃO DE CURSO I"
    p_tag.font.name = "Open Sans"
    p_tag.font.size = Pt(12)
    p_tag.font.bold = True
    p_tag.font.color.rgb = COLOR_ACCENT
    p_tag.space_after = Pt(6)

    p_t = tf1.add_paragraph()
    p_t.text = "Vila Cachos AI"
    p_t.font.name = "Open Sans"
    p_t.font.size = Pt(36)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_PRIMARY
    p_t.space_after = Pt(6)

    p_sub = tf1.add_paragraph()
    p_sub.text = "Sistema Híbrido de Recomendação Capilar com Aprendizado Não Supervisionado e Inferência Bayesiana"
    p_sub.font.name = "Open Sans"
    p_sub.font.size = Pt(14)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_DARK
    p_sub.space_after = Pt(4)

    p_app = tf1.add_paragraph()
    p_app.text = "Um Web App de Diagnóstico Integrado para o Salão Vila Cachos"
    p_app.font.name = "Open Sans"
    p_app.font.size = Pt(13)
    p_app.font.italic = True
    p_app.font.color.rgb = COLOR_MUTED

    # Bottom Metadata Box (Card)
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
    pm3.text = "Disciplina: Monografia I  •  Docente: Prof. Dr. Hélder Pereira Borges  •  Seminário 1 (2026)"
    pm3.font.name = "Open Sans"
    pm3.font.size = Pt(11)
    pm3.font.color.rgb = COLOR_MUTED

    # ==========================================================
    # SLIDE 2: CONTEXTO E O PROBLEMA REAL
    # ==========================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Contexto & Problema de Pesquisa")

    # Card 1 (Contexto)
    c1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(4.0), Inches(3.4))
    c1.fill.solid()
    c1.fill.fore_color.rgb = COLOR_LIGHT_BG
    c1.line.color.rgb = COLOR_BORDER

    tb_c1 = s2.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(3.6), Inches(3.1))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    tf_c1.margin_left = tf_c1.margin_right = tf_c1.margin_top = tf_c1.margin_bottom = 0

    p = tf_c1.paragraphs[0]
    p.text = "O CENÁRIO DO MERCADO"
    p.font.name = "Open Sans"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    p.space_after = Pt(10)

    bullets_c1 = [
        ("Nicho em Alta: ", "Crescimento acelerado de salões especializados em curvaturas 2A a 4C."),
        ("Bioquímica Complexa: ", "Fios helicoidais exigem equilíbrio específico de hidratação, nutrição e lipídios."),
        ("Sobrecarga de Ativos: ", "Dezenas de princípios ativos tornam a indicação manual um desafio crítico.")
    ]
    for b_title, b_desc in bullets_c1:
        p_b = tf_c1.add_paragraph()
        p_b.space_after = Pt(12)
        add_run(p_b, "- " + b_title, size_pt=12, bold=True, color_rgb=COLOR_DARK)
        add_run(p_b, b_desc, size_pt=11.5, bold=False, color_rgb=COLOR_MUTED)

    # Card 2 (Problema no Salão)
    c2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.1), Inches(1.6), Inches(4.1), Inches(3.4))
    c2.fill.solid()
    c2.fill.fore_color.rgb = COLOR_LIGHT_BG
    c2.line.color.rgb = COLOR_BORDER

    tb_c2 = s2.shapes.add_textbox(Inches(5.3), Inches(1.75), Inches(3.7), Inches(3.1))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    tf_c2.margin_left = tf_c2.margin_right = tf_c2.margin_top = tf_c2.margin_bottom = 0

    p = tf_c2.paragraphs[0]
    p.text = "A DOR NO SALÃO VILA CACHOS"
    p.font.name = "Open Sans"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(194, 65, 12)
    p.space_after = Pt(8)

    bullets_c2 = [
        ("Subjetividade: ", "Profissionais distintas prescrevem produtos divergentes para o mesmo fio."),
        ("Turnover de Equipe: ", "A rotatividade de cabeleireiras dispersa o padrão técnico do salão."),
        ("Problema do Cold Start: ", "Clientes novas chegam sem histórico, inviabilizando recomendações puras."),
        ("Gestão no Escuro: ", "Ausência de métricas analíticas sobre o perfil da base atendida.")
    ]
    for b_title, b_desc in bullets_c2:
        p_b = tf_c2.add_paragraph()
        p_b.space_after = Pt(9)
        add_run(p_b, "! " + b_title, size_pt=11.5, bold=True, color_rgb=COLOR_DARK)
        add_run(p_b, b_desc, size_pt=11, bold=False, color_rgb=COLOR_MUTED)

    # ==========================================================
    # SLIDE 3: PERGUNTA PROBLEMA E HIPÓTESE
    # ==========================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Pergunta Problema & Hipótese de Pesquisa")

    # Card Pergunta Problema
    cp = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.55), Inches(8.4), Inches(1.65))
    cp.fill.solid()
    cp.fill.fore_color.rgb = COLOR_LIGHT_BG
    cp.line.color.rgb = COLOR_PRIMARY
    cp.line.width = Pt(1.5)

    tb_cp = s3.shapes.add_textbox(Inches(1.05), Inches(1.65), Inches(7.9), Inches(1.45))
    tf_cp = tb_cp.text_frame
    tf_cp.word_wrap = True
    tf_cp.margin_left = tf_cp.margin_right = tf_cp.margin_top = tf_cp.margin_bottom = 0

    p_cpt = tf_cp.paragraphs[0]
    p_cpt.text = "PERGUNTA PROBLEMA (QUESTÃO NORTEADORA)"
    p_cpt.font.name = "Open Sans"
    p_cpt.font.size = Pt(12)
    p_cpt.font.bold = True
    p_cpt.font.color.rgb = COLOR_PRIMARY
    p_cpt.space_after = Pt(4)

    p_cpq = tf_cp.add_paragraph()
    p_cpq.space_after = Pt(6)
    add_run(p_cpq, "“Como uma arquitetura híbrida de IA leve pode mitigar o Cold Start e padronizar o diagnóstico cosmético em um salão especializado, operando via Web App escalável?”", size_pt=12.5, bold=True, italic=True, color_rgb=COLOR_DARK)

    p_cp_b1 = tf_cp.add_paragraph()
    p_cp_b1.space_after = Pt(3)
    add_run(p_cp_b1, "• Desafio do Cold Start: ", size_pt=11.5, bold=True, color_rgb=RGBColor(194, 65, 12))
    add_run(p_cp_b1, "Prescrever cosméticos corretos na 1ª visita, sem histórico de compras prévio.", size_pt=11, bold=False, color_rgb=COLOR_MUTED)

    p_cp_b2 = tf_cp.add_paragraph()
    add_run(p_cp_b2, "• Arquitetura Híbrida Leve: ", size_pt=11.5, bold=True, color_rgb=COLOR_ACCENT)
    add_run(p_cp_b2, "União de K-Means (Personas) com Média Bayesiana Amortecida (Rankings dinâmicos).", size_pt=11, bold=False, color_rgb=COLOR_MUTED)

    # Card Hipótese
    ch = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.35), Inches(8.4), Inches(1.75))
    ch.fill.solid()
    ch.fill.fore_color.rgb = COLOR_LIGHT_BG
    ch.line.color.rgb = COLOR_ACCENT
    ch.line.width = Pt(1.5)

    tb_ch = s3.shapes.add_textbox(Inches(1.05), Inches(3.45), Inches(7.9), Inches(1.55))
    tf_ch = tb_ch.text_frame
    tf_ch.word_wrap = True
    tf_ch.margin_left = tf_ch.margin_right = tf_ch.margin_top = tf_ch.margin_bottom = 0

    p_cht = tf_ch.paragraphs[0]
    p_cht.text = "HIPÓTESE DA PESQUISA"
    p_cht.font.name = "Open Sans"
    p_cht.font.size = Pt(12)
    p_cht.font.bold = True
    p_cht.font.color.rgb = COLOR_ACCENT
    p_cht.space_after = Pt(4)

    p_chq = tf_ch.add_paragraph()
    p_chq.space_after = Pt(6)
    add_run(p_chq, "“A fusão de regras clínicas com K-Means e regularização bayesiana permite recomendações personalizadas, padronizadas e explicáveis desde o 1º contato, estabilizando rankings mesmo com poucos dados.”", size_pt=12, bold=True, italic=True, color_rgb=COLOR_DARK)

    p_ch_b1 = tf_ch.add_paragraph()
    p_ch_b1.space_after = Pt(3)
    add_run(p_ch_b1, "• Padronização Técnica: ", size_pt=11.5, bold=True, color_rgb=COLOR_PRIMARY)
    add_run(p_ch_b1, "Elimina a discrepância empírica e o turnover entre profissionais do salão.", size_pt=11, bold=False, color_rgb=COLOR_MUTED)

    p_ch_b2 = tf_ch.add_paragraph()
    add_run(p_ch_b2, "• Explicabilidade (XAI) & Estabilidade: ", size_pt=11.5, bold=True, color_rgb=COLOR_ACCENT)
    add_run(p_ch_b2, "Justificativas claras ao cliente e ranking robusto via amortecimento bayesiano.", size_pt=11, bold=False, color_rgb=COLOR_MUTED)

    # ==========================================================
    # SLIDE 4: JUSTIFICATIVA E DECISÕES DE PROJETO
    # ==========================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Justificativa & Decisões de Projeto")

    just_cards = [
        ("ACADÊMICO-CIENTÍFICA", COLOR_PRIMARY, [
            ("Sistemas Híbridos: ", "Aplicação prática de IA sob extrema esparseza de dados iniciais."),
            ("Média Bayesiana: ", "Ancoramento matemático formal para rankings em amostras pequenas."),
            ("Explicabilidade (XAI): ", "Recomendações com justificativas legíveis em linguagem natural.")
        ]),
        ("PRÁTICA & SOCIAL", COLOR_ACCENT, [
            ("Impacto Vila Cachos: ", "Empoderamento da microempresa maranhense e saúde capilar da cliente."),
            ("Padronização: ", "Atendimento técnico consistente, independente do profissional que realiza."),
            ("Retenção & Vendas: ", "Prescrição cosmética assertiva e controle baseado no perfil da demanda.")
        ]),
        ("ARQUITETURA WEB APP", RGBColor(194, 65, 12), [
            ("Dispensou Totem Físico: ", "Elimina custos de gabinetes pesados, telas dedicadas e manutenção física."),
            ("Acesso Universal: ", "Acessível por link/QR Code no smartphone da cliente ou tablet do salão."),
            ("Manutenção Central: ", "Atualizações no catálogo e no algoritmo em nuvem, sem intervenção local.")
        ])
    ]

    for idx, (j_title, j_color, j_items) in enumerate(just_cards):
        left_pos = Inches(0.8 + idx * 2.9)
        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.6), Inches(2.7), Inches(3.4))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_LIGHT_BG
        card.line.color.rgb = COLOR_BORDER

        tb = s4.shapes.add_textbox(left_pos + Inches(0.12), Inches(1.72), Inches(2.46), Inches(3.15))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = j_title
        p.font.name = "Open Sans"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = j_color
        p.space_after = Pt(10)

        for b_t, b_d in j_items:
            pb = tf.add_paragraph()
            pb.space_after = Pt(10)
            add_run(pb, "- " + b_t, size_pt=11.5, bold=True, color_rgb=COLOR_DARK)
            add_run(pb, b_d, size_pt=11, bold=False, color_rgb=COLOR_MUTED)

    # ==========================================================
    # SLIDE 5: OBJETIVOS DA PESQUISA
    # ==========================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Objetivos do Trabalho (Geral & Específicos)")

    # Objetivo Geral Banner
    cg = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(8.4), Inches(0.9))
    cg.fill.solid()
    cg.fill.fore_color.rgb = COLOR_LIGHT_BG
    cg.line.color.rgb = COLOR_PRIMARY
    cg.line.width = Pt(1.5)

    tb_cg = s5.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(8.0), Inches(0.8))
    tf_cg = tb_cg.text_frame
    tf_cg.word_wrap = True
    tf_cg.margin_left = tf_cg.margin_right = tf_cg.margin_top = tf_cg.margin_bottom = 0

    p_og = tf_cg.paragraphs[0]
    p_og.text = "OBJETIVO GERAL"
    p_og.font.name = "Open Sans"
    p_og.font.size = Pt(11.5)
    p_og.font.bold = True
    p_og.font.color.rgb = COLOR_PRIMARY
    p_og.space_after = Pt(3)

    p_ogt = tf_cg.add_paragraph()
    p_ogt.text = "Desenvolver e validar um Sistema Especialista Híbrido (Web App) para mitigar o Cold Start e padronizar o diagnóstico cosmético no salão Vila Cachos."
    p_ogt.font.name = "Open Sans"
    p_ogt.font.size = Pt(12)
    p_ogt.font.bold = True
    p_ogt.font.color.rgb = COLOR_DARK

    # Objetivos Específicos - Coluna 1: IA & Modelagem
    c_esp1 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.5), Inches(4.1), Inches(2.85))
    c_esp1.fill.solid()
    c_esp1.fill.fore_color.rgb = COLOR_LIGHT_BG
    c_esp1.line.color.rgb = COLOR_BORDER

    tb_esp1 = s5.shapes.add_textbox(Inches(0.95), Inches(2.6), Inches(3.8), Inches(2.65))
    tf_esp1 = tb_esp1.text_frame
    tf_esp1.word_wrap = True
    tf_esp1.margin_left = tf_esp1.margin_right = tf_esp1.margin_top = tf_esp1.margin_bottom = 0

    p_oe1 = tf_esp1.paragraphs[0]
    p_oe1.text = "OBJETIVOS ESPECÍFICOS: IA & MODELAGEM"
    p_oe1.font.name = "Open Sans"
    p_oe1.font.size = Pt(12)
    p_oe1.font.bold = True
    p_oe1.font.color.rgb = COLOR_ACCENT
    p_oe1.space_after = Pt(6)

    col1_items = [
        ("1. Taxonomia Capilar: ", "Modelar escala de Walker (2A-4C) e matriz de afinidade para 27 cosméticos;"),
        ("2. Visão (YOLOv8): ", "Inferir curvatura e frizz a partir de fotos via Transfer Learning;"),
        ("3. Fusão Multimodal: ", "Clusterizar 8 variáveis clínicas via K-Means para identificar personas.")
    ]
    for n_title, n_desc in col1_items:
        pe = tf_esp1.add_paragraph()
        pe.space_after = Pt(8)
        add_run(pe, n_title, size_pt=11.5, bold=True, color_rgb=COLOR_DARK)
        add_run(pe, n_desc, size_pt=11, bold=False, color_rgb=COLOR_MUTED)

    # Objetivos Específicos - Coluna 2: Sistema & Validação
    c_esp2 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.1), Inches(2.5), Inches(4.1), Inches(2.85))
    c_esp2.fill.solid()
    c_esp2.fill.fore_color.rgb = COLOR_LIGHT_BG
    c_esp2.line.color.rgb = COLOR_BORDER

    tb_esp2 = s5.shapes.add_textbox(Inches(5.25), Inches(2.6), Inches(3.8), Inches(2.65))
    tf_esp2 = tb_esp2.text_frame
    tf_esp2.word_wrap = True
    tf_esp2.margin_left = tf_esp2.margin_right = tf_esp2.margin_top = tf_esp2.margin_bottom = 0

    p_oe2 = tf_esp2.paragraphs[0]
    p_oe2.text = "OBJETIVOS ESPECÍFICOS: SISTEMA & VALIDAÇÃO"
    p_oe2.font.name = "Open Sans"
    p_oe2.font.size = Pt(12)
    p_oe2.font.bold = True
    p_oe2.font.color.rgb = COLOR_PRIMARY
    p_oe2.space_after = Pt(6)

    col2_items = [
        ("4. Loop Bayesiano: ", "Implementar Média Amortecida (alfa=10) para estabilizar notas no Cold Start;"),
        ("5. Web App & XAI: ", "Construir interface React e API FastAPI com justificativas transparentes;"),
        ("6. Validação Métrica: ", "Aferir acurácia visual (YOLO), Inércia (WCSS) e Silhouette Score.")
    ]
    for n_title, n_desc in col2_items:
        pe = tf_esp2.add_paragraph()
        pe.space_after = Pt(8)
        add_run(pe, n_title, size_pt=11.5, bold=True, color_rgb=COLOR_DARK)
        add_run(pe, n_desc, size_pt=11, bold=False, color_rgb=COLOR_MUTED)

    # ==========================================================
    # SLIDE 6: METODOLOGIA DA PESQUISA: PIPELINE END-TO-END
    # ==========================================================
    s6_met = prs.slides.add_slide(blank_layout)
    add_header(s6_met, "Metodologia da Pesquisa: Como Fiz Tudo")

    # 5 Horizontal Cards for the 5-Stage Pipeline
    step_cards_data = [
        ("1. Curadoria & Ground Truth", 
         "1.058 prontuários clínicos do salão Vila Cachos + Kaggle/Roboflow (amostra de 300 imagens com gabarito comprovado)."),
        ("2. Visão com Rejeição Nativa (YOLOv8)", 
         "200 treino / 100 validação cega. 4 classes consolidadas (Tipo 2, 3, 4 + Careca/Sem Cabelo), eliminando o ruído de 7 subtipos."),
        ("3. Clusterização Clínica Multidimensional (K-Means)", 
         "Vetor de 8 variáveis (porosidade, química, elasticidade) normalizado via StandardScaler. 4 personas clínicas (Silhouette 0,2185)."),
        ("4. Motor de Recomendação Híbrido & Cold Start", 
         "Filtragem por regras tricológicas de contraindicação + Média Bayesiana Amortecida (alfa=10, prior C=4.2) estabilizando rankings."),
        ("5. Engenharia de Software sob Cota Restrita", 
         "API REST FastAPI desacoplada com React Vite no Totem operando sob 512 MB de RAM no Render (inferência em CPU < 5 ms).")
    ]

    y_start = 1.55
    card_h = 0.66
    gap_y = 0.07
    for idx, (s_title, s_desc) in enumerate(step_cards_data):
        c_top = y_start + idx * (card_h + gap_y)
        card_box = s6_met.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(c_top), Inches(8.4), Inches(card_h))
        card_box.fill.solid()
        card_box.fill.fore_color.rgb = COLOR_LIGHT_BG
        card_box.line.color.rgb = COLOR_ACCENT if idx % 2 == 1 else COLOR_PRIMARY
        card_box.line.width = Pt(1.2)

        tb_step = s6_met.shapes.add_textbox(Inches(0.95), Inches(c_top + 0.05), Inches(8.1), Inches(card_h - 0.1))
        tf_step = tb_step.text_frame
        tf_step.word_wrap = True
        tf_step.margin_left = tf_step.margin_right = tf_step.margin_top = tf_step.margin_bottom = 0

        p_s = tf_step.paragraphs[0]
        p_s.text = s_title
        p_s.font.name = "Open Sans"
        p_s.font.size = Pt(12)
        p_s.font.bold = True
        p_s.font.color.rgb = COLOR_PRIMARY if idx % 2 == 0 else COLOR_ACCENT
        p_s.space_after = Pt(2)

        p_sd = tf_step.add_paragraph()
        p_sd.text = s_desc
        p_sd.font.name = "Open Sans"
        p_sd.font.size = Pt(11)
        p_sd.font.color.rgb = COLOR_DARK

    # ==========================================================
    # SLIDE 7: ARQUITETURA TÉCNICA E STATUS DO MVP (DEV)
    # ==========================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Arquitetura da Solução & MVP Funcional")

    # Left Column: Frontend & Backend Cards
    card_fe = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(4.0), Inches(1.6))
    card_fe.fill.solid()
    card_fe.fill.fore_color.rgb = COLOR_LIGHT_BG
    card_fe.line.color.rgb = COLOR_BORDER

    tb_fe = s6.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(3.6), Inches(1.4))
    tf_fe = tb_fe.text_frame
    tf_fe.word_wrap = True
    tf_fe.margin_left = tf_fe.margin_right = tf_fe.margin_top = tf_fe.margin_bottom = 0
    p = tf_fe.paragraphs[0]
    p.text = "FRONTEND: WEB APP (totem-ui)"
    p.font.name = "Open Sans"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(4)
    fe_items = [
        "React 18 + TypeScript + Vite (SPA responsivo em nuvem);",
        "Upload/Foto da mecha com triagem guiada em 4 etapas;",
        "Dark Mode nativo e Inactivity Timeout de 15 min (LGPD)."
    ]
    for it in fe_items:
        p_it = tf_fe.add_paragraph()
        p_it.text = "- " + it
        p_it.font.name = "Open Sans"
        p_it.font.size = Pt(10.5)
        p_it.font.color.rgb = COLOR_DARK

    card_be = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.35), Inches(4.0), Inches(1.65))
    card_be.fill.solid()
    card_be.fill.fore_color.rgb = COLOR_LIGHT_BG
    card_be.line.color.rgb = COLOR_BORDER

    tb_be = s6.shapes.add_textbox(Inches(1.0), Inches(3.45), Inches(3.6), Inches(1.45))
    tf_be = tb_be.text_frame
    tf_be.word_wrap = True
    tf_be.margin_left = tf_be.margin_right = tf_be.margin_top = tf_be.margin_bottom = 0
    p = tf_be.paragraphs[0]
    p.text = "BACKEND & MOTOR DE IA (FastAPI)"
    p.font.name = "Open Sans"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    p.space_after = Pt(4)
    be_items = [
        "API RESTful FastAPI (Python 3.11) sob cota de 512 MB RAM;",
        "Visão computacional YOLOv8/11 (/predict-curl com fallback);",
        "K-Means (4 personas), Média Bayesiana e Rate Limiting."
    ]
    for it in be_items:
        p_it = tf_be.add_paragraph()
        p_it.text = "- " + it
        p_it.font.name = "Open Sans"
        p_it.font.size = Pt(10.5)
        p_it.font.color.rgb = COLOR_DARK

    # Right Column: MVP Status & Results
    card_st = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.1), Inches(1.6), Inches(4.1), Inches(3.4))
    card_st.fill.solid()
    card_st.fill.fore_color.rgb = COLOR_LIGHT_BG
    card_st.line.color.rgb = COLOR_PRIMARY
    card_st.line.width = Pt(1.5)

    tb_st = s6.shapes.add_textbox(Inches(5.3), Inches(1.72), Inches(3.7), Inches(3.15))
    tf_st = tb_st.text_frame
    tf_st.word_wrap = True
    tf_st.margin_left = tf_st.margin_right = tf_st.margin_top = tf_st.margin_bottom = 0

    p = tf_st.paragraphs[0]
    p.text = "STATUS ATUAL DE DESENVOLVIMENTO"
    p.font.name = "Open Sans"
    p.font.size = Pt(12.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(6)

    mvp_bullets = [
        ("Base Sintética Realista: ", "Dataset probabilístico de 1.056 atendimentos mimetizando causalidade clínica."),
        ("Pipeline Multimodal & XAI: ", "Fusão de visão e anamnese com prescrição dos Top 3 produtos e justificativas."),
        ("Testes Automatizados: ", "Suíte de testes de integração com 100% de sucesso (HTTP 200, 422, Rate Limit)."),
        ("Validação Matemática: ", "Inércia WCSS (Cotovelo k=4) e Silhouette Score de 0,2185 condizente com dados ordinais.")
    ]
    for b_t, b_d in mvp_bullets:
        pb = tf_st.add_paragraph()
        pb.space_after = Pt(6)
        add_run(pb, "[OK] " + b_t, size_pt=11.5, bold=True, color_rgb=COLOR_ACCENT)
        add_run(pb, b_d, size_pt=10.5, bold=False, color_rgb=COLOR_DARK)

    # ==========================================================
    # SLIDE 8: VALIDAÇÃO EXPERIMENTAL: MATRIZ DE CONFUSÃO (YOLO)
    # ==========================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Validação da Visão: Matriz 4x4 & Casos Extremos")

    # Left Column: Image Card
    card_img = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(4.2), Inches(3.4))
    card_img.fill.solid()
    card_img.fill.fore_color.rgb = COLOR_LIGHT_BG
    card_img.line.color.rgb = COLOR_BORDER

    cm_img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "faculdade_ifma", "tcc_1_monografia", "seminario_apresentacao", "fig_matriz_confusao_4classes.png")
    if not os.path.exists(cm_img_path):
        cm_img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "faculdade_ifma", "tcc_1_monografia", "seminario_apresentacao", "fig_matriz_confusao.png")

    if os.path.exists(cm_img_path):
        s7.shapes.add_picture(cm_img_path, Inches(0.9), Inches(1.65), Inches(4.0), Inches(3.3))

    # Right Column: Metrics & Academic Insight
    card_m = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.1), Inches(1.6), Inches(4.1), Inches(3.4))
    card_m.fill.solid()
    card_m.fill.fore_color.rgb = COLOR_LIGHT_BG
    card_m.line.color.rgb = COLOR_PRIMARY
    card_m.line.width = Pt(1.5)

    tb_m = s7.shapes.add_textbox(Inches(5.3), Inches(1.72), Inches(3.7), Inches(3.15))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True
    tf_m.margin_left = tf_m.margin_right = tf_m.margin_top = tf_m.margin_bottom = 0

    p_mt = tf_m.paragraphs[0]
    p_mt.text = "VALIDAÇÃO EM HOLDOUT (GABARITO CONHECIDO)"
    p_mt.font.name = "Open Sans"
    p_mt.font.size = Pt(12)
    p_mt.font.bold = True
    p_mt.font.color.rgb = COLOR_PRIMARY
    p_mt.space_after = Pt(4)

    metrics_items = [
        ("Acurácia Top-1 Global: ", "87,4% (salto de 59,3% para 87,4% no holdout cego com 4 classes);"),
        ("Rejeição de Calvície: ", "100% de Recall na classe de controle (0 falsos positivos em cachos);"),
        ("Crespos & Cacheados: ", "89,6% de acurácia no crespo (Tipo 4) e 84,4% no cacheado (Tipo 3);")
    ]
    for mi_t, mi_d in metrics_items:
        p_mi = tf_m.add_paragraph()
        p_mi.space_after = Pt(4)
        add_run(p_mi, "[OK] " + mi_t, size_pt=11, bold=True, color_rgb=COLOR_ACCENT)
        add_run(p_mi, mi_d, size_pt=10.5, bold=False, color_rgb=COLOR_DARK)

    p_call = tf_m.add_paragraph()
    p_call.space_before = Pt(6)
    p_call.space_after = Pt(2)
    add_run(p_call, "RESPOSTA AO APONTAMENTO DO COORIENTADOR:", size_pt=11.5, bold=True, color_rgb=RGBColor(194, 65, 12))

    p_call_desc = tf_m.add_paragraph()
    p_call_desc.space_after = Pt(2)
    add_run(p_call_desc, "• Não fragmentar em 7 classes: ", size_pt=10.5, bold=True, color_rgb=COLOR_DARK)
    add_run(p_call_desc, "Evita o ruído entre 3B/3C com poucos dados. Consolidar em 3 macro-classes aumentou a precisão.\n", size_pt=10, bold=False, color_rgb=COLOR_MUTED)
    add_run(p_call_desc, "• Rejeição de Casos Extremos: ", size_pt=10.5, bold=True, color_rgb=COLOR_ACCENT)
    add_run(p_call_desc, "A 4ª classe negativa identificou 100% dos casos de calvície/ausência de cabelo sem comprometer a inferência.", size_pt=10, bold=False, color_rgb=COLOR_MUTED)

    # ==========================================================
    # SLIDE 9: CRONOGRAMA & PRÓXIMOS PASSOS
    # ==========================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Cronograma & Próximos Passos (Seminário 2)")

    card_nxt = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(8.4), Inches(2.2))
    card_nxt.fill.solid()
    card_nxt.fill.fore_color.rgb = COLOR_LIGHT_BG
    card_nxt.line.color.rgb = COLOR_BORDER

    tb_nxt = s8.shapes.add_textbox(Inches(1.0), Inches(1.72), Inches(8.0), Inches(1.95))
    tf_nxt = tb_nxt.text_frame
    tf_nxt.word_wrap = True
    tf_nxt.margin_left = tf_nxt.margin_right = tf_nxt.margin_top = tf_nxt.margin_bottom = 0

    p = tf_nxt.paragraphs[0]
    p.text = "ROADMAP PARA O SEMINÁRIO 2 E TCC II"
    p.font.name = "Open Sans"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(6)

    steps = [
        ("Novembro / Dezembro (Seminário 2): ", "Conclusão e aprofundamento do Referencial Teórico e fechamento da Metodologia com o protocolo de coleta."),
        ("Fevereiro / Março (TCC II): ", "Execução dos experimentos matemáticos de validação dos clusters (Inércia e Silhouette)."),
        ("Abril / Maio (TCC II): ", "Homologação do Web App em ambiente real de salão (UAT) e avaliação de aderência com a equipe."),
        ("Junho (TCC II): ", "Redação final da monografia completa e Defesa perante a Banca Examinadora.")
    ]
    for st_t, st_d in steps:
        p_st = tf_nxt.add_paragraph()
        p_st.space_after = Pt(5)
        add_run(p_st, "-> " + st_t, size_pt=11.5, bold=True, color_rgb=COLOR_DARK)
        add_run(p_st, st_d, size_pt=11, bold=False, color_rgb=COLOR_MUTED)

    # Thank you / Questions Banner
    card_ty = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.95), Inches(8.4), Inches(1.05))
    card_ty.fill.solid()
    card_ty.fill.fore_color.rgb = COLOR_PRIMARY
    card_ty.line.fill.background()

    tb_ty = s8.shapes.add_textbox(Inches(1.0), Inches(4.05), Inches(8.0), Inches(0.85))
    tf_ty = tb_ty.text_frame
    tf_ty.word_wrap = True
    tf_ty.margin_left = tf_ty.margin_right = tf_ty.margin_top = tf_ty.margin_bottom = 0

    p_ty1 = tf_ty.paragraphs[0]
    p_ty1.alignment = PP_ALIGN.CENTER
    p_ty1.text = "Obrigado pela atenção!"
    p_ty1.font.name = "Open Sans"
    p_ty1.font.size = Pt(18)
    p_ty1.font.bold = True
    p_ty1.font.color.rgb = RGBColor(255, 255, 255)

    p_ty2 = tf_ty.add_paragraph()
    p_ty2.alignment = PP_ALIGN.CENTER
    p_ty2.text = "Espaço aberto para dúvidas, críticas construtivas e sugestões do professor e colegas."
    p_ty2.font.name = "Open Sans"
    p_ty2.font.size = Pt(12)
    p_ty2.font.color.rgb = RGBColor(203, 213, 225)
    p_ty2.font.color.rgb = RGBColor(203, 213, 225)

    # Save to both paths
    prs.save(PPTX_OUT)
    prs.save(PPTX_OFFICIAL)
    print(f"Presentation successfully saved to:\n  - {PPTX_OUT}\n  - {PPTX_OFFICIAL}")

    # Clean up temp logo
    if os.path.exists(logo_temp_path):
        os.remove(logo_temp_path)

    # Convert to PDF via LibreOffice
    cmd = [SOFFICE_PATH, "--headless", "--convert-to", "pdf", PPTX_OFFICIAL, "--outdir", PDF_DIR]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("LibreOffice PDF export result:", res.returncode, res.stdout)

if __name__ == "__main__":
    create_presentation()
