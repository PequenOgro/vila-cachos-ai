"""
scripts/gerar_slides_analise_2_pptx.py
Gera a apresentação completa (14 slides widescreen 16:9) para a Avaliação 1
da disciplina de Análise e Projeto de Sistemas II (IFMA).

Divide a apresentação de forma equilibrada entre os 3 integrantes:
- Marcos Vinícius (Slides 1 a 5)
- Jordan (Slides 6 a 9)
- Rafael (Slides 10 a 14)

Incorpora imagens reais do projeto (totem, salão, infográficos de cachos,
diagrama arquitetural BCE, gráficos de IA e produtos).
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PPTX = os.path.join(
    BASE_DIR,
    "faculdade_ifma",
    "analise_e_projeto_sistemas_2",
    "avaliacao_1",
    "APRESENTACAO_AVALIACAO_1_ANALISE_II.pptx"
)
OUTPUT_DOCS_PPTX = os.path.join(
    BASE_DIR,
    "docs",
    "APRESENTACAO_AVALIACAO_1_ANALISE_II.pptx"
)

# Paleta Visual Executiva
COLOR_BG_DARK = RGBColor(15, 23, 42)      # Slate 900
COLOR_CARD_DARK = RGBColor(30, 41, 59)    # Slate 800
COLOR_BORDER = RGBColor(51, 65, 85)       # Slate 700
COLOR_EMERALD = RGBColor(16, 185, 129)    # Emerald 500 (Vila Cachos)
COLOR_GREEN_DARK = RGBColor(27, 67, 50)   # Forest Green
COLOR_CYAN = RGBColor(56, 189, 248)       # Sky 400
COLOR_AMBER = RGBColor(245, 158, 11)      # Amber 500
COLOR_WHITE = RGBColor(248, 250, 252)     # Slate 50
COLOR_MUTED = RGBColor(148, 163, 184)     # Slate 400

def set_slide_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BG_DARK

def add_header(slide, title, category, speaker_name, speaker_num):
    # Tag de Categoria + Speaker Badge
    tb_tag = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
    tf_tag = tb_tag.text_frame
    tf_tag.word_wrap = True
    tf_tag.margin_left = tf_tag.margin_right = tf_tag.margin_top = tf_tag.margin_bottom = 0
    p_tag = tf_tag.paragraphs[0]
    
    r_cat = p_tag.add_run()
    r_cat.text = f"{category.upper()}   |   "
    r_cat.font.name = "Arial"
    r_cat.font.size = Pt(10)
    r_cat.font.bold = True
    r_cat.font.color.rgb = COLOR_CYAN
    
    r_spk = p_tag.add_run()
    r_spk.text = f"🎤 APRESENTADOR {speaker_num}: {speaker_name.upper()}"
    r_spk.font.name = "Arial"
    r_spk.font.size = Pt(10)
    r_spk.font.bold = True
    r_spk.font.color.rgb = COLOR_EMERALD
    
    # Título Principal
    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.65))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title
    p_title.font.name = "Arial"
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_WHITE
    
    # Linha divisória
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.45), Inches(11.7), Pt(1.5))
    line.fill.solid()
    line.fill.fore_color.rgb = COLOR_EMERALD
    line.line.color.rgb = COLOR_EMERALD

def add_notes(slide, notes_text):
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = notes_text

def build_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    # Assets Paths
    hero_img = os.path.join(BASE_DIR, "totem-ui", "src", "assets", "hero.jpg")
    salon_img = os.path.join(BASE_DIR, "data", "midias_instagram_vila_cachos", "vilacachos_1609333475_highlight18118685677123033.jpg")
    curls_img = os.path.join(BASE_DIR, "assets", "infografico_tipos_cachos.png")
    bce_img = os.path.join(BASE_DIR, "assets", "diagrama_arquitetura_bce.png")
    elbow_img = os.path.join(BASE_DIR, "assets", "fig_elbow_method.png")
    bayesian_img = os.path.join(BASE_DIR, "assets", "fig_bayesian_feedback.png")
    prod_img = os.path.join(BASE_DIR, "totem-ui", "src", "assets", "produtos", "curly-care-acid-c.png")

    # ==========================================================
    # SLIDE 1: CAPA OFICIAL
    # ==========================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)
    
    # Imagem decorativa à direita
    if os.path.exists(hero_img):
        s1.shapes.add_picture(hero_img, Inches(8.5), Inches(0.8), Inches(4.0), Inches(5.9))
    
    # Bloco de Destaque Esquerda
    tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(7.4), Inches(4.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "INSTITUTO FEDERAL DO MARANHÃO — DEPARTAMENTO DE COMPUTAÇÃO\nDISCIPLINA: ANÁLISE E PROJETO DE SISTEMAS II — 2026.2"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.space_after = Pt(14)
    
    p = tf1.add_paragraph()
    p.text = "Vila Cachos AI"
    p.font.name = "Arial"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD
    p.space_after = Pt(4)
    
    p = tf1.add_paragraph()
    p.text = "Totem Inteligente de Diagnóstico Capilar & Recomendação Híbrida Explicável"
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.space_after = Pt(20)
    
    # Card da Equipe
    card_eq = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.7), Inches(7.4), Inches(2.0))
    card_eq.fill.solid()
    card_eq.fill.fore_color.rgb = COLOR_CARD_DARK
    card_eq.line.color.rgb = COLOR_BORDER
    
    tb_eq = s1.shapes.add_textbox(Inches(1.0), Inches(4.8), Inches(7.0), Inches(1.8))
    tf_eq = tb_eq.text_frame
    tf_eq.word_wrap = True
    
    p = tf_eq.paragraphs[0]
    p.text = "AVALIAÇÃO 1 — APRESENTAÇÃO DE MODELAGEM E ENGENHARIA DE SOFTWARE"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER
    p.space_after = Pt(6)
    
    p = tf_eq.add_paragraph()
    p.text = "• Docente Responsável: Profª. Me. Eveline de Jesus Viana Sá\n• Equipe de Apresentação (Divisão de 3 Integrantes):\n   1. Marcos Vinícius (Contexto, Tricologia, Problema e Requisitos)\n   2. Jordan (Modelagem Estrutural: Atores, Casos de Uso, Classes e Visão)\n   3. Rafael (Modelagem Dinâmica: Sequência BCE, Algoritmos de IA e Testes)"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_WHITE

    add_notes(s1, "ROTEIRO (Marcos Vinícius):\n'Boa noite, Professora Eveline e colegas. Hoje apresentamos a modelagem completa de software do Vila Cachos AI para a Avaliação 1 de Análise II. Nossa equipe é composta por mim, Marcos Vinícius, pelo Jordan e pelo Rafael. Estruturamos a apresentação em 3 blocos bem definidos: eu falarei do negócio, da tricologia capilar e dos requisitos; o Jordan abordará a modelagem estrutural (Casos de Uso, Classes/Métodos e Visão Computacional); e o Rafael concluirá com a modelagem dinâmica (Diagramas de Sequência BCE, motor de recomendação bayesiano e validação contínua).'")

    # ==========================================================
    # SLIDE 2: O PROBLEMA DE NEGÓCIO E O SALÃO VILA CACHOS
    # ==========================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "O Problema Real de Negócio & O Salão Vila Cachos", "Contexto de Mercado", "Marcos Vinícius", "1")
    
    # Card Esquerdo: Dor no Salão
    card_dor = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(6.0), Inches(5.2))
    card_dor.fill.solid()
    card_dor.fill.fore_color.rgb = COLOR_CARD_DARK
    card_dor.line.color.rgb = COLOR_BORDER
    
    tb_dor = s2.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(5.6), Inches(4.8))
    tf_dor = tb_dor.text_frame
    tf_dor.word_wrap = True
    
    p = tf_dor.paragraphs[0]
    p.text = "GARGALOS IDENTIFICADOS NO ATENDIMENTO TRADICIONAL"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER
    p.space_after = Pt(10)
    
    pontos_dor = [
        ("Subjetividade no Diagnóstico Manual: ", "Diferentes profissionais avaliam o mesmo cabelo de maneiras divergentes, indicando cronogramas conflitantes."),
        ("Gargalo na Recepção e Tempo Ocioso: ", "A anamnese manual consome de 15 a 25 minutos preciosos da profissional antes de iniciar a lavagem ou corte."),
        ("Desafio do Cold Start com Novas Clientes: ", "Clientes sem histórico de compra prévio sofrem com recomendações genéricas sem embasamento clínico."),
        ("Dispersão do Conhecimento Especialista: ", "Quando uma terapeuta sai do salão, o histórico e o conhecimento tácito sobre as clientes se perdem."),
        ("Oportunidade Comercial Desperdiçada: ", "Clientes com dúvidas compram cosméticos errados no mercado comum em vez da linha especializada do salão.")
    ]
    for tit, desc in pontos_dor:
        p = tf_dor.add_paragraph()
        p.space_after = Pt(8)
        r1 = p.add_run()
        r1.text = "• " + tit
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(9)
        r2.font.color.rgb = COLOR_MUTED

    # Card Direito: Foto Real + Proposta de Valor
    if os.path.exists(salon_img):
        s2.shapes.add_picture(salon_img, Inches(7.1), Inches(1.7), Inches(5.4), Inches(3.4))
    
    card_val = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.1), Inches(5.3), Inches(5.4), Inches(1.6))
    card_val.fill.solid()
    card_val.fill.fore_color.rgb = COLOR_GREEN_DARK
    card_val.line.color.rgb = COLOR_EMERALD
    
    tb_val = s2.shapes.add_textbox(Inches(7.3), Inches(5.4), Inches(5.0), Inches(1.4))
    tf_val = tb_val.text_frame
    tf_val.word_wrap = True
    p = tf_val.paragraphs[0]
    p.text = "PROPOSTA DE VALOR DO VILA CACHOS AI:"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD
    p.space_after = Pt(4)
    p = tf_val.add_paragraph()
    p.text = "Autoatendimento interativo em Totem touch-screen que digitaliza o conhecimento tricológico, reduz o tempo de triagem para menos de 90 segundos e gera receita de cosméticos com transparência explicável (XAI)."
    p.font.name = "Arial"
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_WHITE

    add_notes(s2, "ROTEIRO (Marcos Vinícius):\n'O Salão Vila Cachos atende um nicho altamente técnico: cabelos ondulados, cacheados e crespos. O problema crítico é que a avaliação manual era demorada e subjetiva. Duas cabeleireiras diferentes recomendavam produtos diferentes para o mesmo cabelo. Além disso, quando uma cliente entra pela primeira vez no salão (o clássico Cold Start da computação), não havia como fazer recomendação colaborativa porque ela não tinha compras anteriores. O totem resolve isso na entrada do salão.'")

    # ==========================================================
    # SLIDE 3: A CIÊNCIA DOS CACHOS (TRICOLOGIA APLICADA)
    # ==========================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "A Ciência dos Cachos: Variáveis Tricológicas da IA", "Domínio do Problema", "Marcos Vinícius", "1")
    
    # Imagem do Infográfico Gerado
    if os.path.exists(curls_img):
        s3.shapes.add_picture(curls_img, Inches(0.8), Inches(1.7), Inches(6.8), Inches(4.5))
    
    # Card Explicativo das 8 Variáveis
    card_var = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.7), Inches(4.7), Inches(5.2))
    card_var.fill.solid()
    card_var.fill.fore_color.rgb = COLOR_CARD_DARK
    card_var.line.color.rgb = COLOR_BORDER
    
    tb_var = s3.shapes.add_textbox(Inches(8.0), Inches(1.85), Inches(4.3), Inches(4.8))
    tf_var = tb_var.text_frame
    tf_var.word_wrap = True
    
    p = tf_var.paragraphs[0]
    p.text = "O VETOR DE 8 VARIÁVEIS CLÍNICAS"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.space_after = Pt(8)
    
    var_list = [
        ("1. Curvatura dos Fios (2, 3 ou 4): ", "Dita a facilidade com que o sebo natural percorre o fio em espiral."),
        ("2. Porosidade Aparente (1, 2 ou 3): ", "Cutículas abertas perdem água rapidamente (necessitam acidificação)."),
        ("3. Presença de Química (0 ou 1): ", "Alisamento, descoloração ou tintura alteram a matriz de queratina."),
        ("4. Queixa: Frizz excessivo (0 ou 1): ", "Sensibilidade à umidade atmosférica e desalinhamento das fibras."),
        ("5. Queixa: Ressecamento (0 ou 1): ", "Déficit hídrico e lipídico estrutural."),
        ("6. Queixa: Queda / Quebra (0 ou 1): ", "Fragilidade na haste capilar que requer reconstrução com aminoácidos."),
        ("7. Queixa: Couro cabeludo sensível (0 ou 1): ", "Exige formulações Low-Poo / No-Poo sem sulfatos agressivos."),
        ("8. Fator Econômico / Orçamento: ", "Filtra produtos de acordo com a viabilidade financeira da cliente.")
    ]
    for v_tit, v_desc in var_list:
        p = tf_var.add_paragraph()
        p.space_after = Pt(4)
        r1 = p.add_run()
        r1.text = v_tit
        r1.font.bold = True
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p.add_run()
        r2.text = v_desc
        r2.font.size = Pt(8)
        r2.font.color.rgb = COLOR_MUTED

    add_notes(s3, "ROTEIRO (Marcos Vinícius):\n'Para que a IA recomende com precisão cirúrgica, nós não usamos perguntas genéricas. Modelamos a tabela de André Walker: Tipo 2 (Ondulados), Tipo 3 (Cacheados) e Tipo 4 (Crespos). Cabelos crespos, por exemplo, têm curvatura tão fechada que a oleosidade da raiz nunca chega às pontas, exigindo lipídios pesados. Se colocarmos um produto de crespo em um cabelo ondulado tipo 2A, ele pesa e perde o formato. É essa lógica bioquímica que o nosso modelo K-Means aprende.'")

    # ==========================================================
    # SLIDE 4: A SOLUÇÃO INTEGRADA: HARDWARE TOTEM + WEB APP
    # ==========================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "A Solução: Totem de Autoatendimento Interativo", "Arquitetura da Solução", "Marcos Vinícius", "1")
    
    # 3 Cards de Pilares
    pilares = [
        ("TOTEM TOUCH FÍSICO", "Hardware dedicado na entrada do salão com tela vertical 1080x1920, câmera macro integrada para captura de mechas e proteção contra fraudes.", COLOR_CYAN, Inches(0.8)),
        ("MOTOR DE IA AUTÔNOMO", "Microsserviço em FastAPI com inferência YOLO para mechas, normalização com StandardScaler e clusterização K-Means em milissegundos.", COLOR_EMERALD, Inches(4.8)),
        ("EXPERIÊNCIA EXPLICÁVEL", "Interface em React/TypeScript que exibe o diagnóstico visual, o Top 3 produtos cosméticos e a justificativa clínica em linguagem humana acessível.", COLOR_AMBER, Inches(8.8))
    ]
    for p_tit, p_desc, p_col, x_pos in pilares:
        c = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_pos, Inches(1.8), Inches(3.7), Inches(5.1))
        c.fill.solid()
        c.fill.fore_color.rgb = COLOR_CARD_DARK
        c.line.color.rgb = p_col
        c.line.width = Pt(1.5)
        
        tb = s4.shapes.add_textbox(x_pos + Inches(0.2), Inches(2.0), Inches(3.3), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = p_tit
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = p_col
        p.space_after = Pt(12)
        
        p = tf.add_paragraph()
        p.text = p_desc
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_WHITE
        p.space_after = Pt(16)
        
        # Benefícios chave
        p = tf.add_paragraph()
        p.text = "Destaques Técnicos:"
        p.font.name = "Arial"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_MUTED
        p.space_after = Pt(6)
        
        if "TOTEM" in p_tit:
            itens = ["Timeout automático de 15 minutos", "Design vertical otimizado para toque", "Fallback manual caso não queira foto"]
        elif "MOTOR" in p_tit:
            itens = ["Latência média de ~30ms no backend", "Média Bayesiana amortecida", "Rate limiting com SlowAPI (10 req/min)"]
        else:
            itens = ["Badges explicativas de porcentagem", "QR Code para levar rotina no celular", "Loop de feedback com nota 1 a 5"]
            
        for it in itens:
            p = tf.add_paragraph()
            p.text = "✓ " + it
            p.font.size = Pt(9)
            p.font.color.rgb = COLOR_WHITE
            p.space_after = Pt(4)

    add_notes(s4, "ROTEIRO (Marcos Vinícius):\n'A solução foi concebida sob três pilares integrados: a interface física do Totem de autoatendimento, o motor de inteligência artificial desacoplado e a entrega de valor com explicabilidade. A cliente não recebe apenas um nome de produto: ela vê a badge da sua curvatura, a porcentagem de compatibilidade e a explicação em português claro.'")

    # ==========================================================
    # SLIDE 5: DOCUMENTO DE REQUISITOS (RF & RNF)
    # ==========================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Engenharia de Requisitos: Funcionais (RF) e Não Funcionais (RNF)", "Requisitos de Software", "Marcos Vinícius", "1")
    
    # Coluna 1: Requisitos Funcionais
    c_rf = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.2))
    c_rf.fill.solid()
    c_rf.fill.fore_color.rgb = COLOR_CARD_DARK
    c_rf.line.color.rgb = COLOR_BORDER
    
    tb_rf = s5.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.3), Inches(4.8))
    tf_rf = tb_rf.text_frame
    tf_rf.word_wrap = True
    
    p = tf_rf.paragraphs[0]
    p.text = "REQUISITOS FUNCIONAIS CHAVE (15 RFs MAPEADOS)"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD
    p.space_after = Pt(8)
    
    rfs_exemplos = [
        ("RF-01 a RF-03: ", "Coleta estruturada de Curvatura (2-4), Porosidade (1-3), Danos e Queixas capilares."),
        ("RF-04: ", "Normalização das 8 variáveis com StandardScaler e inferência de Cluster K-Means."),
        ("RF-05 / RF-06: ", "Cálculo de score tricológico e Média Bayesiana Amortecida (superação de Cold Start)."),
        ("RF-07 / RF-08: ", "Geração e ordenação do Top 3 cosméticos recomendados com estimativa de estrelas (1.0 a 5.0)."),
        ("RF-09: ", "Apresentação de justificativa clínica em linguagem natural (XAI - Explainable AI)."),
        ("RF-10 / RF-11: ", "Coleta de avaliação da cliente (1 a 5 estrelas) e recalibração dinâmica dos pesos."),
        ("RF-12 / RF-13: ", "Inferência visual de mechas com YOLOv8 e rejeição de imagens sem cabelo (anti-fraude).")
    ]
    for r_cod, r_txt in rfs_exemplos:
        p = tf_rf.add_paragraph()
        p.space_after = Pt(5)
        r1 = p.add_run()
        r1.text = r_cod
        r1.font.bold = True
        r1.font.size = Pt(9)
        r1.font.color.rgb = COLOR_CYAN
        r2 = p.add_run()
        r2.text = r_txt
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = COLOR_WHITE

    # Coluna 2: Requisitos Não Funcionais
    c_rnf = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.2))
    c_rnf.fill.solid()
    c_rnf.fill.fore_color.rgb = COLOR_CARD_DARK
    c_rnf.line.color.rgb = COLOR_BORDER
    
    tb_rnf = s5.shapes.add_textbox(Inches(7.0), Inches(1.85), Inches(5.3), Inches(4.8))
    tf_rnf = tb_rnf.text_frame
    tf_rnf.word_wrap = True
    
    p = tf_rnf.paragraphs[0]
    p.text = "REQUISITOS NÃO FUNCIONAIS (CRITÉRIOS DE QUALIDADE)"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER
    p.space_after = Pt(8)
    
    rnfs_exemplos = [
        ("RNF-01 (Desempenho & Latência): ", "A resposta da recomendação deve retornar em menos de 1,5 segundos (mediana local medida em ~30ms)."),
        ("RNF-02 (Rate Limiting de Proteção): ", "Limitação estrita de 10 req/min nas rotas de recomendação e 20 req/min na visão computacional."),
        ("RNF-03 (Timeout & Privacidade no Totem): ", "Sessão reinicia automaticamente após 15 minutos de inatividade, limpando dados temporários da cliente."),
        ("RNF-04 (Segurança OWASP): ", "Headers de segurança (nosniff, DENY, XSS-Protection), sanitização contra CSV Formula Injection e validação de Magic Bytes."),
        ("RNF-05 (Concorrência Thread-Safe): ", "Bloqueio atômico com threading.Lock na escrita em disco para evitar race conditions simultâneas."),
        ("RNF-06 (Restrição de Memória Render 512MB): ", "Coleta de lixo forçada (gc.collect()), fechamento imediato de buffers OpenCV e limite de 50 conexões.")
    ]
    for r_cod, r_txt in rnfs_exemplos:
        p = tf_rnf.add_paragraph()
        p.space_after = Pt(6)
        r1 = p.add_run()
        r1.text = r_cod
        r1.font.bold = True
        r1.font.size = Pt(9)
        r1.font.color.rgb = COLOR_AMBER
        r2 = p.add_run()
        r2.text = r_txt
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = COLOR_WHITE

    add_notes(s5, "ROTEIRO (Marcos Vinícius):\n'Finalizando a minha parte, formalizamos 15 Requisitos Funcionais e 6 Requisitos Não Funcionais rigorosos. Destaco dois pontos cruciais da disciplina: o RNF-03 garante que, por ser um totem público, se a cliente se afastar da tela, os dados dela são apagados em 15 minutos; e o RNF-06 garante que o sistema opera dentro do teto estrito de 512MB de RAM do servidor gratuito. Agora passo a palavra para o Jordan, que apresentará a modelagem estrutural do sistema.'")

    # ==========================================================
    # SLIDE 6: ATORES DO SISTEMA & FRONTEIRAS
    # ==========================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Modelagem Conceitual: Atores do Sistema e Limites", "Modelagem Estrutural", "Jordan", "2")
    
    atores = [
        ("CLIENTE DO SALÃO\n(Ator Primário)", "Usuária que interage com a tela sensível ao toque, insere variáveis capilares, recebe diagnóstico explicável e avalia cosméticos.", COLOR_CYAN, Inches(0.8)),
        ("TERAPEUTA CAPILAR\n(Ator Secundário)", "Profissional do salão que orienta a cliente na validação de variáveis complexas e consulta formulações no catálogo.", COLOR_EMERALD, Inches(3.8)),
        ("GESTOR DO SALÃO\n(Ator Administrativo)", "Responsável por auditar as métricas de clusterização, volume de avaliações, inércia do K-Means e atualizar o catálogo.", COLOR_AMBER, Inches(6.8)),
        ("MOTOR IA / FASTAPI\n(Ator de Sistema)", "Serviço autônomo backend que processa imagens YOLOv8, roda K-Means, calcula médias bayesianas e gera explicabilidade XAI.", RGBColor(168, 85, 247), Inches(9.8))
    ]
    for tit, desc, col, x in atores:
        c = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.8), Inches(2.7), Inches(5.1))
        c.fill.solid()
        c.fill.fore_color.rgb = COLOR_CARD_DARK
        c.line.color.rgb = col
        c.line.width = Pt(1.5)
        
        tb = s6.shapes.add_textbox(x + Inches(0.15), Inches(2.0), Inches(2.4), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = tit
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(12)
        
        p = tf.add_paragraph()
        p.text = desc
        p.font.name = "Arial"
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_WHITE
        p.space_after = Pt(14)
        
        p = tf.add_paragraph()
        p.text = "Responsabilidades:"
        p.font.name = "Arial"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = COLOR_MUTED
        p.space_after = Pt(4)
        
        if "CLIENTE" in tit:
            resp = ["Preencher anamnese", "Tirar foto da mecha", "Dar nota de satisfação"]
        elif "TERAPEUTA" in tit:
            resp = ["Apoiar cliente em dúvida", "Validar curvatura 3A-4C", "Verificar ativos químicos"]
        elif "GESTOR" in tit:
            resp = ["Monitorar /health", "Auditar Silhouette Score", "Cadastrar novos produtos"]
        else:
            resp = ["Inferir cluster K-Means", "Calcular média bayesiana", "Retornar Top 3 com XAI"]
            
        for r in resp:
            p = tf.add_paragraph()
            p.text = "• " + r
            p.font.size = Pt(8.5)
            p.font.color.rgb = COLOR_WHITE
            p.space_after = Pt(3)

    add_notes(s6, "ROTEIRO (Jordan):\n'Boa noite, Professora Eveline. Assumo a partir daqui para detalhar a modelagem de software. Iniciamos pelos Atores do Sistema. Dividimos rigorosamente entre atores humanos e de sistema: a Cliente é o ator primário; a Terapeuta é o ator secundário que auxilia clientes com dúvidas em curvatura; o Gestor é o ator administrativo que monitora a saúde dos clusters; e o Motor de IA FastAPI é o ator de sistema que executa o processamento autônomo.'")

    # ==========================================================
    # SLIDE 7: DIAGRAMA DE CASOS DE USO (UML)
    # ==========================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Modelagem Funcional: Diagrama de Casos de Uso (UML)", "Casos de Uso", "Jordan", "2")
    
    # Grid de Casos de Uso
    ucs = [
        ("UC-01", "Realizar Anamnese Capilar", "Cliente do Salão, Terapeuta", "Inclui <<include>> UC-02", COLOR_CYAN, Inches(0.8), Inches(1.8)),
        ("UC-02", "Gerar Diagnóstico e Recomendação", "Motor de IA (FastAPI)", "Incluso por UC-01", COLOR_EMERALD, Inches(4.8), Inches(1.8)),
        ("UC-03", "Visualizar Top 3 Produtos e XAI", "Cliente do Salão, Terapeuta", "Estendido por <<extend>> UC-04", COLOR_CYAN, Inches(8.8), Inches(1.8)),
        ("UC-04", "Registrar Avaliação (Feedback Loop)", "Cliente do Salão", "Inclui <<include>> UC-05", COLOR_AMBER, Inches(0.8), Inches(4.4)),
        ("UC-05", "Recalibrar Média Bayesiana", "Motor de IA (FastAPI)", "Incluso por UC-04", COLOR_EMERALD, Inches(4.8), Inches(4.4)),
        ("UC-06 & 07", "Catálogo e Monitoramento de IA", "Gestor do Salão, Motor IA", "Casos Administrativos", RGBColor(168, 85, 247), Inches(8.8), Inches(4.4))
    ]
    for uid, unome, uatores, urel, ucol, x, y in ucs:
        c = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(3.7), Inches(2.5))
        c.fill.solid()
        c.fill.fore_color.rgb = COLOR_CARD_DARK
        c.line.color.rgb = ucol
        c.line.width = Pt(1.5)
        
        tb = s7.shapes.add_textbox(x + Inches(0.15), y + Inches(0.15), Inches(3.4), Inches(2.2))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = f"{uid}: {unome}"
        p.font.name = "Arial"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = ucol
        p.space_after = Pt(4)
        
        p = tf.add_paragraph()
        p.text = f"Atores: {uatores}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = COLOR_WHITE
        p.space_after = Pt(3)
        
        p = tf.add_paragraph()
        p.text = f"Relação UML: {urel}"
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_MUTED
        p.space_after = Pt(6)
        
        p = tf.add_paragraph()
        p.text = "Fluxos de Exceção documentados:"
        p.font.size = Pt(8)
        p.font.color.rgb = COLOR_AMBER
        
        if "UC-01" in uid:
            exc = "FE-01: Timeout de 15min reinicia formulário."
        elif "UC-02" in uid:
            exc = "FE-02: Rate Limit 429 se disparar > 10 req/min."
        elif "UC-03" in uid:
            exc = "FE-03: Imagem sem mechas não trava o sistema."
        elif "UC-04" in uid:
            exc = "FE-04: Nota inválida rejeitada por Pydantic (422)."
        elif "UC-05" in uid:
            exc = "FE-05: Concorrência bloqueada com threading.Lock."
        else:
            exc = "FE-06: Catálogo desatualizado aciona fallback."
            
        p = tf.add_paragraph()
        p.text = "• " + exc
        p.font.size = Pt(8)
        p.font.color.rgb = COLOR_WHITE

    add_notes(s7, "ROTEIRO (Jordan):\n'Aqui está o mapeamento dos 7 Casos de Uso. Destaco para a banca a modelagem formal das relações UML: o UC-01 (Preencher Anamnese) obrigatoriamente inclui o UC-02 (Gerar Diagnóstico) via <<include>>. Ao visualizar o Top 3 (UC-03), a cliente tem a opção de estender para a avaliação (UC-04 via <<extend>>). Quando ela avalia, o sistema inclui automaticamente a recalibração da média bayesiana (UC-05). Todos os fluxos possuem happy path e fluxos de exceção documentados.'")

    # ==========================================================
    # SLIDE 8: DIAGRAMA DE CLASSES E DICIONÁRIO DE MÉTODOS
    # ==========================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Diagrama de Classes & Dicionário de Métodos (DIP / Clean Arch)", "Modelagem Estrutural", "Jordan", "2")
    
    # 3 Cards de Classes Centrais
    classes = [
        ("VilaCachosRecommender\n<<Service / Engine>>", [
            "- n_clusters: int",
            "- kmeans: KMeans",
            "- scaler: StandardScaler",
            "- df_historico: DataFrame"
        ], [
            "+ fit(df) -> Self",
            "+ prever_cluster(perfil) -> int",
            "+ recomendar(perfil, top_k) -> Dict",
            "+ registrar_feedback(perfil, prod, nota)",
            "+ avaliar_qualidade_clusters() -> Dict"
        ], COLOR_EMERALD, Inches(0.8)),
        
        ("FeedbackRepository\n<<Interface / DIP>>", [
            "(Interface Abstrata / Contrato)",
            "Desacoplada da persistência web",
            "Permite trocar CSV por PostgreSQL"
        ], [
            "+ obter_historico() -> DataFrame",
            "+ salvar_feedback(perfil, prod, nota)",
            "+ obter_total_avaliacoes() -> int",
            "+ obter_media_global() -> float"
        ], COLOR_CYAN, Inches(4.8)),
        
        ("YoloHairClassifier\n<<Vision Engine>>", [
            "- yolo_model: YOLO",
            "- CONF_THRESHOLD: float = 0.75",
            "- classes: [ondulado, cacheado, crespo]"
        ], [
            "+ predict_image_bytes(bytes) -> Dict",
            "+ _extrair_metricas_morfologicas()",
            "+ _verificar_presenca_mechas() -> Tuple"
        ], COLOR_AMBER, Inches(8.8))
    ]
    for c_tit, c_attrs, c_meths, c_col, x in classes:
        c = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.8), Inches(3.7), Inches(5.1))
        c.fill.solid()
        c.fill.fore_color.rgb = COLOR_CARD_DARK
        c.line.color.rgb = c_col
        c.line.width = Pt(1.5)
        
        tb = s8.shapes.add_textbox(x + Inches(0.15), Inches(1.95), Inches(3.4), Inches(4.8))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = c_tit
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = c_col
        p.space_after = Pt(8)
        
        p = tf.add_paragraph()
        p.text = "Atributos Principais:"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = COLOR_MUTED
        p.space_after = Pt(3)
        for a in c_attrs:
            p = tf.add_paragraph()
            p.text = a
            p.font.size = Pt(8.5)
            p.font.color.rgb = COLOR_WHITE
            p.space_after = Pt(2)
            
        p = tf.add_paragraph()
        p.text = "\nMétodos Principais (Assinaturas):"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = COLOR_MUTED
        p.space_after = Pt(3)
        for m in c_meths:
            p = tf.add_paragraph()
            p.text = m
            p.font.size = Pt(8.5)
            p.font.bold = True
            p.font.color.rgb = COLOR_CYAN
            p.space_after = Pt(2)

    add_notes(s8, "ROTEIRO (Jordan):\n'Respondendo à exigência pedagógica da professora sobre o Diagrama de Classes e Métodos: na notação OMG/UML, os métodos residem no terceiro compartimento da classe. Destaco aqui o princípio de Inversão de Dependência (DIP do SOLID): nossa API não grava diretamente em arquivo. Ela se comunica com a interface abstrata FeedbackRepository. Hoje usamos a implementação concreta CsvFeedbackRepository com Lock thread-safe; amanhã, se o salão migrar para banco de dados SQL, o motor de IA não precisa mudar uma única linha.'")

    # ==========================================================
    # SLIDE 9: VISÃO COMPUTACIONAL (YOLOv8 + REJEIÇÃO ANTI-FRAUDE)
    # ==========================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Módulo de Visão Computacional (YOLOv8 & Morfologia)", "Visão Computacional", "Jordan", "2")
    
    # 2 Cards grandes
    card_yolo1 = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.1))
    card_yolo1.fill.solid()
    card_yolo1.fill.fore_color.rgb = COLOR_CARD_DARK
    card_yolo1.line.color.rgb = COLOR_BORDER
    
    tb_y1 = s9.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.7))
    tf_y1 = tb_y1.text_frame
    tf_y1.word_wrap = True
    p = tf_y1.paragraphs[0]
    p.text = "PIPELINE DE CLASSIFICAÇÃO NEURAL DA MECHA"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.space_after = Pt(10)
    
    passos_yolo = [
        ("1. Captura da Foto da Mecha: ", "A câmera macro do totem captura o enquadramento aproximado da mecha capilar da cliente."),
        ("2. Redimensionamento & Redução de Memória: ", "A imagem é convertida em buffer de memória, redimensionada para 640x640 e tratada com gc.collect() para respeitar a cota de 512MB."),
        ("3. Inferência Neural YOLOv8 (best.pt): ", "Rede convolucional treinada infere a classe de curvatura predominante (Tipo 2, 3 ou 4) com taxa de confiança."),
        ("4. Extração de Métricas Morfológicas: ", "Análise de entropia de textura, densidade de bordas e gradientes para estimar frizz e integridade cuticular.")
    ]
    for tit, desc in passos_yolo:
        p = tf_y1.add_paragraph()
        p.space_after = Pt(8)
        r1 = p.add_run()
        r1.text = "• " + tit
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(9)
        r2.font.color.rgb = COLOR_MUTED

    card_yolo2 = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1))
    card_yolo2.fill.solid()
    card_yolo2.fill.fore_color.rgb = COLOR_CARD_DARK
    card_yolo2.line.color.rgb = COLOR_BORDER
    
    tb_y2 = s9.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.7))
    tf_y2 = tb_y2.text_frame
    tf_y2.word_wrap = True
    p = tf_y2.paragraphs[0]
    p.text = "SEGURANÇA & VALIDAÇÃO ANTI-FRAUDE (HUMAN-IN-THE-LOOP)"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER
    p.space_after = Pt(10)
    
    seg_yolo = [
        ("Detecção de Superfície Lisa ou Careca: ", "Se a cliente ou um brincalhão apontar a câmera para uma mesa, parede ou pessoa careca, o algoritmo rejeita o processamento."),
        ("Detecção de Banners Publicitários: ", "Fotos de propagandas ou revistas são identificadas por uniformidade de cores sintéticas e rejeitadas."),
        ("Tratamento de Exceção Gracioso: ", "A API retorna HTTP 200 com flag 'cabelo_detectado=false' e mensagem educativa, abrindo o fallback manual sem travar o totem."),
        ("Human-in-the-Loop Obrigatório: ", "Se a confiança da IA for inferior a 75% (CONF_THRESHOLD), o totem sugere a confirmação visual da profissional capilar.")
    ]
    for tit, desc in seg_yolo:
        p = tf_y2.add_paragraph()
        p.space_after = Pt(8)
        r1 = p.add_run()
        r1.text = "✓ " + tit
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = COLOR_AMBER
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(9)
        r2.font.color.rgb = COLOR_WHITE

    add_notes(s9, "ROTEIRO (Jordan):\n'Para enriquecer o diagnóstico, incluímos o modelo YOLOv8 para visão computacional de mechas. Mas como engenheiros de software, nós não confiamos cegamente na IA: criamos uma rotina de validação anti-fraude. Se alguém tirar foto de uma parede, de uma mesa ou de uma foto de revista, o sistema detecta que não há mechas reais de cabelo e não quebra o sistema; ele abre graciosamente o seletor manual. Agora passo a palavra para o Rafael, que explicará a modelagem dinâmica de sequência e a matemática do recomendador.'")

    # ==========================================================
    # SLIDE 10: ARQUITETURA BCE & OS 6 DIAGRAMAS DE SEQUÊNCIA
    # ==========================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Modelagem Dinâmica: Padrão BCE e os 6 Diagramas de Sequência", "Diagramas de Sequência", "Rafael", "3")
    
    # Imagem da Arquitetura BCE
    if os.path.exists(bce_img):
        s10.shapes.add_picture(bce_img, Inches(0.8), Inches(1.7), Inches(11.7), Inches(2.6))
    
    # Tabela com as 6 Páginas do draw.io
    card_seq = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.5), Inches(11.7), Inches(2.5))
    card_seq.fill.solid()
    card_seq.fill.fore_color.rgb = COLOR_CARD_DARK
    card_seq.line.color.rgb = COLOR_BORDER
    
    tb_s = s10.shapes.add_textbox(Inches(1.0), Inches(4.6), Inches(11.3), Inches(2.3))
    tf_s = tb_s.text_frame
    tf_s.word_wrap = True
    
    p = tf_s.paragraphs[0]
    p.text = "MAPEAMENTO DOS 6 DIAGRAMAS DE SEQUÊNCIA VETORIAIS (DRAW.IO EM ANEXO)"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD
    p.space_after = Pt(6)
    
    seqs_resumo = [
        ("Pág. 1 • UC-02 (Preencher Anamnese): ", "Navegação não-destrutiva com operador 'opt' e timeout de sessão em 15 minutos."),
        ("Pág. 2 • UC-03 (Gerar Recomendação): ", "Coração da IA: normalização StandardScaler, cluster K-Means e scoring ponderado."),
        ("Pág. 3 • UC-04 (Visualizar Diagnóstico): ", "Renderização explicável XAI com badges e ordenação do Top 3 produtos cosméticos."),
        ("Pág. 4 • UC-05 (Registrar Avaliação): ", "Loop de feedback com persistência thread-safe em CSV e recálculo da Média Bayesiana."),
        ("Pág. 5 • UC-06 (Consultar Catálogo): ", "Auditoria de catálogo pelo gestor para verificar conformidade dos cosméticos cadastrados."),
        ("Pág. 6 • UC-07 (Monitorar Saúde de IA): ", "Endpoint /health que monitora o Silhouette Score e a Inércia dos clusters K-Means.")
    ]
    for tit, desc in seqs_resumo:
        p = tf_s.add_paragraph()
        p.space_after = Pt(3)
        r1 = p.add_run()
        r1.text = tit
        r1.font.bold = True
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = COLOR_CYAN
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = COLOR_WHITE

    add_notes(s10, "ROTEIRO (Rafael):\n'Boa noite, Professora Eveline. Assumo a parte final com o comportamento dinâmico do software. Nossos 6 diagramas de sequência foram modelados no draw.io sob o padrão arquitetural BCE: Boundary (Fronteira com Totem UI), Controller (Controlador com RecommenderAPI) e Entity/Service (VilaCachosRecommender e Repositório). Cada um dos 6 diagramas cobre um cenário crítico, utilizando operadores formais da UML como opt, alt e loop.'")

    # ==========================================================
    # SLIDE 11: O CORAÇÃO DA IA (K-MEANS + MÉDIA BAYESIANA)
    # ==========================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "O Motor Analítico de IA: K-Means e Média Bayesiana", "Algoritmos & IA", "Rafael", "3")
    
    # Imagem Gráfico Elbow / Silhouette
    if os.path.exists(elbow_img):
        s11.shapes.add_picture(elbow_img, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.9))
    
    # Card com Fórmulas e Equações
    card_eqs = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1))
    card_eqs.fill.solid()
    card_eqs.fill.fore_color.rgb = COLOR_CARD_DARK
    card_eqs.line.color.rgb = COLOR_BORDER
    
    tb_eqs = s11.shapes.add_textbox(Inches(7.0), Inches(1.95), Inches(5.3), Inches(4.8))
    tf_eqs = tb_eqs.text_frame
    tf_eqs.word_wrap = True
    
    p = tf_eqs.paragraphs[0]
    p.text = "EQUAÇÕES DA RECOMENDAÇÃO HÍBRIDA ADAPTATIVA"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER
    p.space_after = Pt(8)
    
    eqs_list = [
        ("1. Peso Adaptativo Convexo (RN-10):", "alpha = min(0.60, total_avaliacoes_cluster / 100)\npeso_conteudo = 1.0 - alpha\n(Em clusters novos, 100% da decisão vem da ciência; conforme avaliações chegam, o feedback ganha até 60% de peso)."),
        ("2. Média Bayesiana Amortecida (RN-09):", "media_amortecida = (5 * media_global + somanotas) / (5 + n)\n(Suavização de Laplace que impede que um produto com apenas 1 voto 5 estrelas vença produtos consagrados com 50 votos 4.8)."),
        ("3. Score Final Combinado:", "score_final = (peso_conteudo * score_conteudo) + (alpha * score_bayesiano)\nestrelas_estimadas = 1.0 + (score_final * 4.0)\n(Converte a afinidade matemática em uma escala familiar de 1.0 a 5.0 estrelas).")
    ]
    for e_tit, e_desc in eqs_list:
        p = tf_eqs.add_paragraph()
        p.space_after = Pt(6)
        r1 = p.add_run()
        r1.text = e_tit + "\n"
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = COLOR_CYAN
        r2 = p.add_run()
        r2.text = e_desc
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = COLOR_WHITE

    # Card inferior esquerdo (Silhouette)
    card_sil = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.9), Inches(5.6), Inches(2.0))
    card_sil.fill.solid()
    card_sil.fill.fore_color.rgb = COLOR_GREEN_DARK
    card_sil.line.color.rgb = COLOR_EMERALD
    
    tb_sil = s11.shapes.add_textbox(Inches(1.0), Inches(5.0), Inches(5.2), Inches(1.8))
    tf_sil = tb_sil.text_frame
    tf_sil.word_wrap = True
    p = tf_sil.paragraphs[0]
    p.text = "VALIDAÇÃO MATEMÁTICA DOS CLUSTERS (ELBOW METHOD):"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD
    p.space_after = Pt(4)
    p = tf_sil.add_paragraph()
    p.text = "Analisamos a inércia e o Silhouette Score para definir o número ótimo de personas capilares (clusters). O modelo convergiu com alta coesão interna e separação tricológica nítida entre cabelos ondulados (2), cacheados (3) e crespos (4)."
    p.font.name = "Arial"
    p.font.size = Pt(8.5)
    p.font.color.rgb = COLOR_WHITE

    add_notes(s11, "ROTEIRO (Rafael):\n'No coração da nossa inteligência artificial, superamos o problema do Cold Start com uma combinação convexa. Observem a primeira equação: quando o salão inaugura um cluster de clientes, alpha é zero, então o sistema confia 100% no conhecimento especialista dos ingredientes. Conforme as clientes vão avaliando com estrelas, o alpha sobe até 60%. E para amortecer produtos com poucas notas, aplicamos a Média Bayesiana com prior global.'")

    # ==========================================================
    # SLIDE 12: EXPLICABILIDADE (XAI) E FEEDBACK LOOP
    # ==========================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Explicabilidade Semântica (XAI) & Feedback Loop Contínuo", "Transparência da IA", "Rafael", "3")
    
    # Imagem do Produto
    if os.path.exists(prod_img):
        s12.shapes.add_picture(prod_img, Inches(0.8), Inches(1.8), Inches(3.6), Inches(2.6))
        
    # Card Exemplo Top 1
    card_top1 = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.6), Inches(5.6), Inches(2.3))
    card_top1.fill.solid()
    card_top1.fill.fore_color.rgb = COLOR_CARD_DARK
    card_top1.line.color.rgb = COLOR_EMERALD
    
    tb_t1 = s12.shapes.add_textbox(Inches(1.0), Inches(4.7), Inches(5.2), Inches(2.1))
    tf_t1 = tb_t1.text_frame
    tf_t1.word_wrap = True
    p = tf_t1.paragraphs[0]
    p.text = "EXEMPLO REAL DE RECOMENDAÇÃO (TOP 1 MATCH):"
    p.font.name = "Arial"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD
    p.space_after = Pt(4)
    p = tf_t1.add_paragraph()
    p.text = "• Produto: Curly Care ACID-C (Acidificante Antiporosidade)\n• Match Score: 0.881 (4.5 / 5.0 Estrelas Estimadas)\n• Justificativa XAI: 'Indicado porque seu cacho Tipo 3 apresentou porosidade alta e danos químicos. O pH 3.0 do ACID-C sela as cutículas abertas, blindando o córtex capilar contra a quebra.'"
    p.font.name = "Arial"
    p.font.size = Pt(8.5)
    p.font.color.rgb = COLOR_WHITE

    # Card Direito: Loop de Feedback
    card_fb = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1))
    card_fb.fill.solid()
    card_fb.fill.fore_color.rgb = COLOR_CARD_DARK
    card_fb.line.color.rgb = COLOR_BORDER
    
    tb_fb = s12.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.7))
    tf_fb = tb_fb.text_frame
    tf_fb.word_wrap = True
    
    p = tf_fb.paragraphs[0]
    p.text = "COMO FUNCIONA O CICLO DE APRENDIZADO CONTÍNUO"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.space_after = Pt(10)
    
    passos_fb = [
        ("1. Avaliação Pós-Atendimento: ", "Ao terminar de usar o produto na bancada do salão, a cliente informa sua nota de 1 a 5 estrelas no totem ou celular."),
        ("2. Validação Estrita via Pydantic: ", "O endpoint POST /feedback valida os bounds (1 <= nota <= 5) e checa se o produto consta no catálogo ativo."),
        ("3. Persistência Atômica Thread-Safe: ", "O CsvFeedbackRepository aciona threading.Lock para salvar o registro no histórico sem risco de colisão de escrita."),
        ("4. Recalibração Imediata na Memória: ", "O motor VilaCachosRecommender atualiza o somatório de notas do cluster em tempo real; a próxima cliente já usufrui da nova média amortecida.")
    ]
    for tit, desc in passos_fb:
        p = tf_fb.add_paragraph()
        p.space_after = Pt(8)
        r1 = p.add_run()
        r1.text = "• " + tit
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(9)
        r2.font.color.rgb = COLOR_MUTED

    add_notes(s12, "ROTEIRO (Rafael):\n'Outro diferencial do Vila Cachos AI é o XAI: Inteligência Artificial Explicável. A cliente entende exatamente por que aquele produto foi sugerido para ela. E o sistema fecha o ciclo com o Feedback Loop: quando a cliente avalia o produto com 5 estrelas, o motor recalibra a média bayesiana em tempo real na memória. O sistema aprende e fica mais inteligente a cada atendimento.'")

    # ==========================================================
    # SLIDE 13: ENGENHARIA DE VALIDAÇÃO (ZERO ERROS & RENDER)
    # ==========================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "Engenharia de Software e Validação Contínua (Zero Erros)", "Qualidade & Testes", "Rafael", "3")
    
    # 3 Cards de Qualidade
    cards_eng = [
        ("SUÍTE DE TESTES (TEST_API.PY)", [
            "Testes de integração automatizados",
            "100% de sucesso (Exit Code 0)",
            "Validação das rotas /health, /recommend e /feedback",
            "Testes de injeção e dados inválidos (HTTP 422)",
            "Testes de proteção contra imagens sem mechas"
        ], COLOR_EMERALD, Inches(0.8)),
        
        ("FRONTEND TOTEM UI (REACT)", [
            "Construído em React 19 + TypeScript",
            "TailwindCSS + TanStack Router",
            "Build executando sem erros de compilação",
            "Linter com 0 erros bloqueantes",
            "Design responsivo para tela vertical de Totem"
        ], COLOR_CYAN, Inches(4.8)),
        
        ("HIGIENE DE MEMÓRIA (RENDER 512MB)", [
            "Consciência do teto gratuito no Render",
            "Destruição imediata de buffers OpenCV",
            "Coleta de lixo forçada (gc.collect())",
            "Concorrência limitada a 50 sockets",
            "Prevenção ativa contra estouro de memória (OOM)"
        ], COLOR_AMBER, Inches(8.8))
    ]
    for tit, itens, col, x in cards_eng:
        c = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.8), Inches(3.7), Inches(5.1))
        c.fill.solid()
        c.fill.fore_color.rgb = COLOR_CARD_DARK
        c.line.color.rgb = col
        c.line.width = Pt(1.5)
        
        tb = s13.shapes.add_textbox(x + Inches(0.15), Inches(2.0), Inches(3.4), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = tit
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(12)
        
        for it in itens:
            p = tf.add_paragraph()
            p.text = "✓ " + it
            p.font.size = Pt(9)
            p.font.color.rgb = COLOR_WHITE
            p.space_after = Pt(6)

    add_notes(s13, "ROTEIRO (Rafael):\n'Como reza a boa prática de engenharia de software da nossa disciplina, nosso projeto não é apenas conceitual ou um mockup de slides: ele possui código executável com tolerância zero a erros. Nossa suíte automatizada em test_api.py valida desde a integridade do cluster até o comportamento sob falhas. Além disso, respeitamos a restrição de produção de operar sob o teto estrito de 512MB de RAM do servidor gratuito.'")

    # ==========================================================
    # SLIDE 14: CONCLUSÃO & STATUS DO PROJETO
    # ==========================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_header(s14, "Conclusão, Entregas da Avaliação 1 e Próximos Passos", "Fechamento", "Rafael", "3")
    
    # Card Resumo das Entregas
    card_fim = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(7.5), Inches(5.1))
    card_fim.fill.solid()
    card_fim.fill.fore_color.rgb = COLOR_CARD_DARK
    card_fim.line.color.rgb = COLOR_EMERALD
    card_fim.line.width = Pt(1.5)
    
    tb_fim = s14.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(7.1), Inches(4.7))
    tf_fim = tb_fim.text_frame
    tf_fim.word_wrap = True
    
    p = tf_fim.paragraphs[0]
    p.text = "STATUS DAS ENTREGAS COBRADAS NO CRONOGRAMA DA DISCIPLINA:"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD
    p.space_after = Pt(10)
    
    entregas = [
        ("24/Setembro — Doc de Requisitos & Diagrama de Casos de Uso: ", "100% CONCLUÍDO e especificado formalmente com fluxos principais e alternativos."),
        ("01/Outubro — Diagrama de Classes & Dicionário de Métodos: ", "100% CONCLUÍDO com estereótipos Pydantic, Clean Architecture e Inversão de Dependência."),
        ("20/Outubro — 6 Diagramas de Sequência Completos (draw.io): ", "100% CONCLUÍDO sob padrão BCE, cobrindo da anamnese à auditoria de métricas."),
        ("29/Outubro — Avaliação 1 (Compilado Unificado + Apresentação): ", "100% PRONTO. Documentação completa de 12 páginas em PDF e slides integrados.")
    ]
    for tit, desc in entregas:
        p = tf_fim.add_paragraph()
        p.space_after = Pt(8)
        r1 = p.add_run()
        r1.text = "✅ " + tit + "\n"
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = COLOR_CYAN
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(9)
        r2.font.color.rgb = COLOR_WHITE

    # Card da Direita: Fechamento da Equipe
    card_agradece = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.6), Inches(1.8), Inches(3.9), Inches(5.1))
    card_agradece.fill.solid()
    card_agradece.fill.fore_color.rgb = COLOR_GREEN_DARK
    card_agradece.line.color.rgb = COLOR_EMERALD
    
    tb_agr = s14.shapes.add_textbox(Inches(8.8), Inches(2.1), Inches(3.5), Inches(4.5))
    tf_agr = tb_agr.text_frame
    tf_agr.word_wrap = True
    
    p = tf_agr.paragraphs[0]
    p.text = "EQUIPE VILA CACHOS AI"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_EMERALD
    p.space_after = Pt(12)
    
    p = tf_agr.add_paragraph()
    p.text = "Marcos Vinícius\nJordan\nRafael\n\nDocente:\nProfª. Me. Eveline de Jesus Viana Sá\n\nIFMA — Campus Monte Castelo\nDepartamento de Computação"
    p.font.name = "Arial"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.space_after = Pt(16)
    
    p = tf_agr.add_paragraph()
    p.text = "Obrigado pela atenção!\nEstamos abertos a perguntas da banca avaliadora."
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.italic = True
    p.font.color.rgb = COLOR_CYAN

    add_notes(s14, "ROTEIRO (Rafael):\n'Para encerrar, consolidamos 100% de todos os artefatos de engenharia cobrados ao longo do semestre pela Professora Eveline. O Vila Cachos AI une rigor acadêmico de modelagem de software com inteligência artificial aplicada a um problema real do mercado maranhense. Agradecemos a atenção da professora e dos colegas, e Marcos, Jordan e eu estamos prontos para as perguntas da banca!'")

    # Salva os arquivos PPTX
    os.makedirs(os.path.dirname(OUTPUT_PPTX), exist_ok=True)
    prs.save(OUTPUT_PPTX)
    print(f"[SUCCESS] Apresentação salva em: {OUTPUT_PPTX}")
    
    os.makedirs(os.path.dirname(OUTPUT_DOCS_PPTX), exist_ok=True)
    prs.save(OUTPUT_DOCS_PPTX)
    print(f"[SUCCESS] Cópia sincronizada em: {OUTPUT_DOCS_PPTX}")

if __name__ == "__main__":
    build_presentation()

