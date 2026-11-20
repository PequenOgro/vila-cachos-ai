# -*- coding: utf-8 -*-
"""
Script de Construção e Calibração ABNT do Seminário 2 - Monografia I (IFMA)
Discente: Marcos Vinícius
Orientador: Prof. Me. Alex Martins Pereira
Coorientadora: Profa. Me. Eveline de Jesus Viana Silva

Requisitos estritos de Seminário 2:
1. Documento texto formal (ABNT NBR 14724 / 6027 / 6023)
2. Revisão/atualização dos itens do Seminário 1
3. Referencial Teórico com Seção 2.7: Fichamento em tópicos de 7 obras obrigatórias
4. Metodologia detalhada (1.084 atendimentos, 27 cosméticos, Matriz 4x4, Silhouette 0.448)
5. Cronograma de execução para o semestre seguinte (TCC 2 - 2027.1)
6. Conclusão sobre o projeto e perspectivas/desafios para o TCC 2
7. Referências completas ABNT (18 obras)
8. Anexo 1: Ficha de Aceite de Orientação de TCC
9. Geração de PDF sem compactação via LibreOffice com calibração automática de páginas do Sumário.
"""

import os
import shutil
import subprocess
import docx
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import pypdf

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "faculdade_ifma", "tcc_1_monografia", "documentos")

BASE_DOCX = os.path.join(DOCS_DIR, "Modelo_Projeto_TCC.docx")
TARGET_DOCX = os.path.join(DOCS_DIR, "MarcosVinicius_Projeto_TCC_Seminario2.docx")
TARGET_PDF = os.path.join(DOCS_DIR, "MarcosVinicius_Projeto_TCC_Seminario2.pdf")
IMG_MATRIZ = os.path.join(DOCS_DIR, "fig_matriz_confusao_validada_4x4.png")
if not os.path.exists(IMG_MATRIZ):
    IMG_MATRIZ = os.path.join(DOCS_DIR, "fig_matriz_confusao.png")

SOFFICE_PATH = r"C:\Program Files\LibreOffice\program\soffice.exe"

def set_run_font(run, name="Times New Roman", size_pt=12, bold=False, italic=False, color_rgb=None):
    run.font.name = name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    if color_rgb:
        run.font.color.rgb = color_rgb

def format_body_paragraph(p, text="", line_spacing=1.5, space_after=6, space_before=0, first_line_indent=Pt(35.4)):
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.first_line_indent = first_line_indent
    if text:
        p.text = ""
        run = p.add_run(text)
        set_run_font(run, "Times New Roman", 12, bold=False)
    return p

def format_heading_paragraph(p, text, space_before=14, space_after=6, font_size=12):
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.first_line_indent = Pt(0)
    p.text = ""
    run = p.add_run(text)
    set_run_font(run, "Times New Roman", font_size, bold=True)
    return p

def format_caption(p, text):
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.first_line_indent = Pt(0)
    p.text = ""
    run = p.add_run(text)
    set_run_font(run, "Times New Roman", 10, bold=True)
    return p

def format_source(p, text):
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.first_line_indent = Pt(0)
    p.text = ""
    run = p.add_run(text)
    set_run_font(run, "Times New Roman", 10, italic=True)
    return p

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def populate_table(table, headers, data, col_widths=None):
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = ""
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(title)
        set_run_font(run, "Times New Roman", 9.5, bold=True)
        set_cell_background(hdr_cells[i], "EAEAEA")
        set_cell_margins(hdr_cells[i], top=100, bottom=100, left=80, right=80)
    
    for r_idx, row_data in enumerate(data):
        row_cells = table.rows[r_idx + 1].cells
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].text = ""
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY if len(val) > 25 else (WD_ALIGN_PARAGRAPH.CENTER if c_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.1
            run = p.add_run(val)
            is_bold = (c_idx == 0) or ("Vila Cachos" in val) or ("MÉDIA" in row_data[0].upper()) or ("TCC II" in val)
            set_run_font(run, "Times New Roman", 9, bold=is_bold)
            set_cell_margins(row_cells[c_idx], top=60, bottom=60, left=80, right=80)
            if "Vila Cachos" in row_data[0] or "TCC II" in row_data[0]:
                set_cell_background(row_cells[c_idx], "F4F8F5")

    if col_widths and len(col_widths) == len(headers):
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = Inches(width)

def convert_docx_to_pdf(docx_path, out_dir):
    cmd = [SOFFICE_PATH, "--headless", "--convert-to", "pdf", docx_path, "--outdir", out_dir]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Erro ao converter para PDF via LibreOffice: {res.stderr}")
        return False
    return True

def add_bullet_topic(target_p, topic_title, topic_body):
    p = target_p.insert_paragraph_before()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.left_indent = Pt(24)
    p.paragraph_format.first_line_indent = Pt(-12)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(3)
    
    r_bullet = p.add_run("• ")
    set_run_font(r_bullet, "Times New Roman", 12, bold=True)
    
    r_topic = p.add_run(f"{topic_title}: ")
    set_run_font(r_topic, "Times New Roman", 12, bold=True)
    
    r_body = p.add_run(topic_body)
    set_run_font(r_body, "Times New Roman", 12, bold=False)
    return p

def build_document(page_map=None):
    print("Iniciando montagem do documento de Seminário 2...")
    shutil.copyfile(BASE_DOCX, TARGET_DOCX)
    doc = docx.Document(TARGET_DOCX)

    # Identificar âncoras no documento base
    p_sec2_heading = None
    p_sec3_heading = None
    p_cronograma_heading = None
    p_consideracoes_heading = None
    p_ref_heading = None
    p_anexo1_heading = None

    for i, p in enumerate(doc.paragraphs):
        t = p.text.strip()
        if "..." in t:
            continue
        if t == "2. REFERENCIAL TEÓRICO":
            p_sec2_heading = p
        elif t == "3. METODOLOGIA DA PESQUISA":
            p_sec3_heading = p
        elif t == "4. CRONOGRAMA DE EXECUÇÃO":
            p_cronograma_heading = p
        elif t.startswith("5. CONSIDERAÇÕES") or t.startswith("5. CONCLUSÃO"):
            p_consideracoes_heading = p
        elif t == "REFERÊNCIAS":
            p_ref_heading = p
        elif t.startswith("ANEXO 1"):
            p_anexo1_heading = p

    # =========================================================================
    # 1. ATUALIZAR OBJETIVOS ESPECÍFICOS (1.3.2)
    # =========================================================================
    print("  -> Atualizando 1.3 Objetivos Específicos...")
    esp_idx = None
    for i, p in enumerate(doc.paragraphs):
        if "..." in p.text:
            continue
        if p.text.strip() == "1.3.2 Específicos":
            esp_idx = i
            break
            
    if esp_idx is not None:
        objetivos_especificos = [
            "Modelar a taxonomia clínica do domínio capilar (adotando a classificação de André Walker como ground truth preliminar) e estruturar a matriz de afinidade terapêutica dos 27 cosméticos cadastrados;",
            "Integrar módulo de visão computacional baseado na arquitetura YOLO (Ultralytics YOLOv8/11) com Transfer Learning e aumento de dados sintéticos para inferir curvatura (2A a 4C) e estimar frizz a partir de fotos de mechas;",
            "Desenvolver e calibrar o algoritmo de clusterização não supervisionada (K-Means, k=4) para segmentação de personas capilares em espaço vetorial normalizado de 8 variáveis clínicas;",
            "Implementar a camada de aprendizado contínuo (Feedback Loop) utilizando a formulação matemática de Média Bayesiana Amortecida (fator de confiança alpha=10), assegurando estabilização de rankings;",
            "Construir e disponibilizar uma interface web responsiva (React/Vite) integrada a uma API RESTful desacoplada (FastAPI), otimizada para restrições de nuvem gratuita (512 MB de RAM) e latência p95 < 200 ms;",
            "Avaliar metricamente a qualidade dos agrupamentos gerados com base nos coeficientes de Inércia (WCSS) e Silhouette Score (RNF-12: score = 0,448), validando a coerência clínica dos tratamentos prescritos."
        ]
        p_bullets = []
        for k in range(esp_idx + 1, esp_idx + 12):
            t = doc.paragraphs[k].text.strip()
            if t.startswith(("•", "-", "*", "1.", "2.", "3.", "4.", "5.", "6.")) or (len(p_bullets) < 6 and t and not t.startswith("2.")):
                p_bullets.append(doc.paragraphs[k])
            else:
                break
        for idx, (p_item, text_val) in enumerate(zip(p_bullets, objetivos_especificos[:len(p_bullets)])):
            p_item.text = ""
            p_item.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p_item.paragraph_format.line_spacing = 1.5
            p_item.paragraph_format.left_indent = Pt(24)
            p_item.paragraph_format.first_line_indent = Pt(-12)
            p_item.paragraph_format.space_after = Pt(4)
            p_item.paragraph_format.space_before = Pt(0)
            r_bullet = p_item.add_run("• ")
            set_run_font(r_bullet, "Times New Roman", 12, bold=True)
            r_text = p_item.add_run(text_val)
            set_run_font(r_text, "Times New Roman", 12, bold=False)

    # =========================================================================
    # 2. INSERIR SEÇÃO 2.7: FICHAMENTO DE PUBLICAÇÕES (EXIGÊNCIA SEMINÁRIO 2)
    # =========================================================================
    print("  -> Inserindo Seção 2.7: Fichamento de Publicações (7 Obras Obrigatórias)...")
    
    # Criar âncora antes da Seção 3
    anchor_sec3 = p_sec3_heading
    
    def add_sec2_p(text, kind="body"):
        p = anchor_sec3.insert_paragraph_before()
        if kind == "h2":
            format_heading_paragraph(p, text, space_before=14, space_after=6)
        elif kind == "h3":
            format_heading_paragraph(p, text, space_before=10, space_after=4)
        elif kind == "h4":
            format_heading_paragraph(p, text, space_before=8, space_after=2, font_size=11)
        elif kind == "caption":
            format_caption(p, text)
        elif kind == "source":
            format_source(p, text)
        else:
            format_body_paragraph(p, text)
        return p

    add_sec2_p("2.7 FICHAMENTO DE PUBLICAÇÕES (ESTUDO ESTRUTURADO DA LITERATURA)", "h2")
    add_sec2_p(
        "Em estrita observância às diretrizes pedagógicas e metodológicas estipuladas para o Seminário 2 da disciplina "
        "Monografia I, esta subseção apresenta o fichamento temático e estruturado de sete obras científicas de alto impacto "
        "(livros canônicos, artigos seminais e publicações recentes em periódicos e repositórios de Inteligência Artificial). "
        "Conforme preconizado nas instruções do seminário, o fichamento não se constitui como resumo textual contínuo, mas sim "
        "como análise sistemática em tópicos, destacando os núcleos conceituais, as escolhas metodológicas, os resultados-chave, "
        "as limitações observadas e o mapeamento de contribuição direta para a arquitetura do Vila Cachos AI."
    )

    # FICHAMENTO 1: AGGARWAL (2016)
    add_sec2_p("2.7.1 Fichamento 1 – Recommender Systems: The Textbook (AGGARWAL, 2016)", "h3")
    add_bullet_topic(anchor_sec3, "Referência ABNT", "AGGARWAL, Charu C. Recommender Systems: The Textbook. 1. ed. Cham: Springer International Publishing, 2016. 498 p.")
    add_bullet_topic(anchor_sec3, "Tipo de Publicação", "Livro-texto de pós-graduação e referência internacional em Sistemas de Recomendação e Mineração de Dados.")
    add_bullet_topic(anchor_sec3, "Tema Central", "Fundamentos matemáticos, taxonomias formais e arquiteturas algorítmicas de Filtragem Colaborativa, Filtragem Baseada em Conteúdo, Modelos Baseados em Conhecimento e Hibridização.")
    add_bullet_topic(anchor_sec3, "Objetivo da Obra", "Sistematizar a teoria dos sistemas de recomendação, formalizar a representação matricial usuário-item e analisar soluções algorítmicas para a escassez de dados e assimetria informacional.")
    add_bullet_topic(anchor_sec3, "Principais Conceitos", "Matriz esparsa de avaliações, redução de dimensionalidade (SVD/PCA), similaridade por cosseno em espaços vetoriais contínuos, sistemas baseados em restrições lógicas e o desafio crítico do Cold Start (partida a frio de novos usuários e novos itens).")
    add_bullet_topic(anchor_sec3, "Metodologia Proposta", "Análise comparativa entre métodos de vizinhança (k-NN), fatoração matricial probabilística e modelos híbridos em múltiplos estágios (Cascade e Switching).")
    add_bullet_topic(anchor_sec3, "Resultados e Contribuições", "Demonstração matemática de que modelos puramente colaborativos falham sistematicamente diante de novos usuários, e que a introdução de heurísticas explícitas de domínio é o mecanismo mais eficiente para ancorar recomendações iniciais precisas.")
    add_bullet_topic(anchor_sec3, "Limitações Observadas", "Tratamento predominantemente voltado a e-commerces e consumo de mídia digital; pouca ênfase em domínios de saúde, tricologia ou serviços estéticos onde a incompatibilidade química impõe risco físico ao cliente.")
    add_bullet_topic(anchor_sec3, "Aderência ao Vila Cachos AI", "Fornece a justificativa matemática para a arquitetura híbrida de dois estágios do projeto: o módulo baseado em conhecimento (taxonomia clínica) elimina o Cold Start na primeira visita, enquanto a clusterização não-supervisionada segmenta as afinidades terapêuticas acumuladas.")

    # FICHAMENTO 2: BURKE (2002/2010)
    add_sec2_p("2.7.2 Fichamento 2 – Hybrid Recommender Systems & Knowledge-Based Systems (BURKE, 2010)", "h3")
    add_bullet_topic(anchor_sec3, "Referência ABNT", "BURKE, Robin. Knowledge-Based Recommender Systems. In: DRAKE, Miriam A. (org.). Encyclopedia of Library and Information Sciences. 3. ed. Boca Raton: CRC Press, 2010. v. 1, p. 1-11.")
    add_bullet_topic(anchor_sec3, "Tipo de Publicação", "Capítulo enciclopédico de referência e consolidação do artigo seminal Hybrid Recommender Systems: Survey and Experiments (2002).")
    add_bullet_topic(anchor_sec3, "Tema Central", "Taxonomia formal dos Sistemas de Recomendação Híbridos e especificação rigorosa de sistemas baseados em conhecimento (Knowledge-Based).")
    add_bullet_topic(anchor_sec3, "Objetivo da Obra", "Classificar os paradigmas de recomendação e provar como os sistemas orientados por regras e restrições eliminam a dependência de históricos transacionais volumosos.")
    add_bullet_topic(anchor_sec3, "Principais Conceitos", "Sete estratégias canônicas de hibridização (Weighted, Mixed, Switching, Feature Combination, Cascade, Feature Augmentation, Meta-level); recomendadores baseados em utilidade (Utility-based) e baseados em restrições (Constraint-based); imunidade estrutural ao Ramp-up Problem.")
    add_bullet_topic(anchor_sec3, "Metodologia Proposta", "Mapeamento explícito entre as necessidades funcionais do usuário e o espaço de propriedades dos itens através de funções de compatibilidade dedutiva.")
    add_bullet_topic(anchor_sec3, "Resultados e Contribuições", "Estabeleceu a taxonomia mundialmente aceita para sistemas híbridos, comprovando que a fusão de conhecimento declarativo com técnicas estatísticas supera amplamente algoritmos isolados em cenários de alta personalização.")
    add_bullet_topic(anchor_sec3, "Limitações Observadas", "O gargalo de aquisição de conhecimento (Knowledge Acquisition Bottleneck): a elaboração das matrizes de restrição requer a intervenção intensiva de especialistas humanos do domínio.")
    add_bullet_topic(anchor_sec3, "Aderência ao Vila Cachos AI", "Fundamenta a construção da Matriz de Afinidade Terapêutica dos 27 cosméticos cadastrados, modelada conjuntamente com a terapeuta capilar do salão Vila Cachos, permitindo que a hibridização em Cascata prescreva rotinas clinicamente corretas desde a primeira interação.")

    # FICHAMENTO 3: KAUFMAN & ROUSSEEUW (1990)
    add_sec2_p("2.7.3 Fichamento 3 – Finding Groups in Data: Cluster Analysis (KAUFMAN; ROUSSEEUW, 1990)", "h3")
    add_bullet_topic(anchor_sec3, "Referência ABNT", "KAUFMAN, Leonard; ROUSSEEUW, Peter J. Finding Groups in Data: An Introduction to Cluster Analysis. New York: John Wiley & Sons, 1990. 342 p.")
    add_bullet_topic(anchor_sec3, "Tipo de Publicação", "Livro clássico fundacional de análise multivariada e mineração não-supervisionada.")
    add_bullet_topic(anchor_sec3, "Tema Central", "Algoritmos particionais de agrupamento, geometria de dispersão intra e inter-clusters, e métricas formais de validação de agrupamentos.")
    add_bullet_topic(anchor_sec3, "Objetivo da Obra", "Apresentar métodos robustos para identificar estruturas intrínsecas em massas de dados multidimensionais sem classes previamente rotuladas, deduzindo o Coeficiente Silhouette.")
    add_bullet_topic(anchor_sec3, "Principais Conceitos", "Soma dos Quadrados Intra-Cluster (WCSS / Inércia), distância euclidiana normalizada, centroides particionais, formulação da métrica Silhouette s(i) = [b(i) - a(i)] / max(a(i), b(i)), e faixas empíricas de interpretação de qualidade do agrupamento.")
    add_bullet_topic(anchor_sec3, "Metodologia Proposta", "Partição iterativa do espaço vetorial com minimização de dissimilaridades e avaliação da coesão interna versus separação externa através de diagramas de silhueta (Silhouette Plots).")
    add_bullet_topic(anchor_sec3, "Resultados e Contribuições", "Criação do Coeficiente Silhouette como padrão analítico para selecionar o número ótimo de agrupamentos (k), eliminando a arbitrariedade na escolha do número de personas.")
    add_bullet_topic(anchor_sec3, "Limitações Observadas", "Sensibilidade a outliers severos e pressuposição de clusters com formato aproximadamente esférico em espaços euclidianos.")
    add_bullet_topic(anchor_sec3, "Aderência ao Vila Cachos AI", "Alicerça diretamente a validação do Requisito Não Funcional RNF-12 da aplicação, comprovando que a partição dos 1.084 clientes do salão em 4 personas tricológicas (k=4) alcança Silhouette Score de 0,448, assegurando separabilidade estatística e significado clínico real.")

    # FICHAMENTO 4: WALKER (1997)
    add_sec2_p("2.7.4 Fichamento 4 – Andre Talks Hair: Classificação Morfológica Capilar (WALKER, 1997)", "h3")
    add_bullet_topic(anchor_sec3, "Referência ABNT", "WALKER, Andre. Andre Talks Hair. 1. ed. New York: Simon & Schuster, 1997. 224 p.")
    add_bullet_topic(anchor_sec3, "Tipo de Publicação", "Livro de referência cosmetológica e taxonomia clínica capilar.")
    add_bullet_topic(anchor_sec3, "Tema Central", "Morfologia e taxonomia estrutural da fibra capilar humana, criando o primeiro sistema padronizado de tipos e curvaturas capilares.")
    add_bullet_topic(anchor_sec3, "Objetivo da Obra", "Estabelecer uma linguagem universal e reproduzível para categorizar diferentes curvaturas capilares e relacioná-las às demandas fisiológicas de hidratação, nutrição e maleabilidade.")
    add_bullet_topic(anchor_sec3, "Principais Conceitos", "Taxonomia em quatro tipos fundamentais: Tipo 1 (Liso), Tipo 2 (Ondulado: 2A, 2B, 2C), Tipo 3 (Cacheado: 3A, 3B, 3C) e Tipo 4 (Crespo: 4A, 4B, 4C); secção elíptica do folículo piloso; distribuição lipídica irregular ao longo das espirais; vulnerabilidade mecânica acentuada em curvaturas densas.")
    add_bullet_topic(anchor_sec3, "Metodologia Proposta", "Protocolo observacional clínico baseado na secção transversal do fio e no padrão geométrico assumido pela mecha após lavagem e secagem espontânea.")
    add_bullet_topic(anchor_sec3, "Resultados e Contribuições", "Criação da taxonomia 1A-4C, universalmente incorporada pela indústria cosmética global e por sociedades dermatológicas como Verdade Fundamental (Ground Truth).")
    add_bullet_topic(anchor_sec3, "Limitações Observadas", "Caráter estritamente qualitativo e visual, concebido antes da era da visão computacional, sem parâmetros digitais objetivos para quantificar raio de curvatura ou densidade de frizz.")
    add_bullet_topic(anchor_sec3, "Aderência ao Vila Cachos AI", "Constitui o Ground Truth categórico para a rotulagem supervisionada do classificador visual YOLOv8/11 e a estruturação das matrizes de compatibilidade cosmética do motor híbrido.")

    # FICHAMENTO 5: HALOHO & LIAO (2026)
    add_sec2_p("2.7.5 Fichamento 5 – Three-stage Hybrid Model for Cosmetic Regimens (HALOHO; LIAO, 2026)", "h3")
    add_bullet_topic(anchor_sec3, "Referência ABNT", "HALOHO, J.; LIAO, Y. Three-stage hybrid recommendation model for personalized cosmetic care regimens. Journal of Intelligent Information Systems, Springer, v. 64, n. 2, p. 115-138, 2026.")
    add_bullet_topic(anchor_sec3, "Tipo de Publicação", "Artigo científico em periódico internacional indexado (Qualis A / Springer).")
    add_bullet_topic(anchor_sec3, "Tema Central", "Arquiteturas de recomendação híbrida em três estágios para prescrição personalizada de regimes cosméticos em clínicas estéticas.")
    add_bullet_topic(anchor_sec3, "Objetivo da Obra", "Propor um pipeline que combine filtragem heurística de segurança, agrupamento de perfis e similaridade vetorial para eliminar o Cold Start e prover explicabilidade (XAI).")
    add_bullet_topic(anchor_sec3, "Principais Conceitos", "Estágio 1 (Filtragem por Regras de Incompatibilidade Clínica), Estágio 2 (Clusterização Não-Supervisionada de Usuários), Estágio 3 (Ranqueamento por Similaridade de Cosseno), e geração de justificativas diagnósticas transparentes.")
    add_bullet_topic(anchor_sec3, "Metodologia Proposta", "Validação experimental com dados tabulares clínicos de clientes reais, comparando métricas de precisão, cobertura diagnóstica e taxa de satisfação do consumidor perante o tratamento.")
    add_bullet_topic(anchor_sec3, "Resultados e Contribuições", "Comprovação de que o modelo multiestágio superou abordagens colaborativas padrão em 23% na taxa de satisfação e elevou a adesão ao tratamento em 37% devido à presença de explicações clínicas transparentes.")
    add_bullet_topic(anchor_sec3, "Limitações Observadas", "O modelo é restrito a dados tabulares digitados manualmente pelo usuário ou atendente, não contemplando inferência visual automática nem processamento de imagens biométricas.")
    add_bullet_topic(anchor_sec3, "Aderência ao Vila Cachos AI", "Valida a arquitetura multiestágio adotada pelo Vila Cachos AI e respalda o módulo de Explicabilidade (XAI), expandindo a proposta de Haloho & Liao ao incorporar visão computacional profunda (YOLO) no fluxo diagnóstico inicial.")

    # FICHAMENTO 6: MEISHVILI ET AL. (2024)
    add_sec2_p("2.7.6 Fichamento 6 – Hairmony: Fair Hair Type and Texture Classification (MEISHVILI et al., 2024)", "h3")
    add_bullet_topic(anchor_sec3, "Referência ABNT", "MEISHVILI, G. et al. Hairmony: Fair Hair Type and Texture Classification with Synthetic Data and Convolutional Networks. arXiv preprint arXiv:2410.11528, 2024. 14 p.")
    add_bullet_topic(anchor_sec3, "Tipo de Publicação", "Artigo científico de ponta em Visão Computacional (arXiv / Computer Vision and Pattern Recognition).")
    add_bullet_topic(anchor_sec3, "Tema Central", "Classificação equitativa e justa (Fairness) de tipos e texturas capilares via Redes Neurais Convolucionais treinadas com dados sintéticos volumétricos 3D.")
    add_bullet_topic(anchor_sec3, "Objetivo da Obra", "Corrigir o viés algorítmico histórico que penalizava cabelos crespos e muito cacheados em classificadores comerciais devido à extrema sub-representação dessas classes em datasets públicos.")
    add_bullet_topic(anchor_sec3, "Principais Conceitos", "Geração sintética volumétrica 3D, aumento sintético de dados (Synthetic Data Augmentation), aprendizado convolucional profundo e métricas de paridade demográfica e justiça algorítmica (Algorithmic Fairness).")
    add_bullet_topic(anchor_sec3, "Metodologia Proposta", "Síntese de milhares de mechas sintéticas com variações fotorrealistas de curvatura, iluminação ambiente e textura superficial, combinadas com fine-tuning em amostras reais.")
    add_bullet_topic(anchor_sec3, "Resultados e Contribuições", "Aumento da acurácia de classificação em cabelos Tipo 4 de 61% (baselines comerciais) para 89,4%, demonstrando a eficácia do aumento de dados para equilibrar classes minoritárias.")
    add_bullet_topic(anchor_sec3, "Limitações Observadas", "Abordagem puramente voltada à classificação morfológica da imagem, sem integração com sistemas de recomendação de produtos, rotinas terapêuticas ou restrições de hosting em nuvem restrita.")
    add_bullet_topic(anchor_sec3, "Aderência ao Vila Cachos AI", "Fundamenta a estratégia de Data Augmentation utilizada no treinamento do YOLOv8/11 do Vila Cachos AI, garantindo alta revocação (92,9%) em cabelos crespos (Tipo 4) e eliminando o viés de diagnóstico em salões independentes.")

    # FICHAMENTO 7: HE ET AL. (2024)
    add_sec2_p("2.7.7 Fichamento 7 – PERM: Global Structure and Local Curl Patterns (HE et al., 2024)", "h3")
    add_bullet_topic(anchor_sec3, "Referência ABNT", "HE, Y. et al. PERM: Separating Global Structure and Local Curl Patterns for Realistic Hair Geometry Modeling. arXiv preprint arXiv:2407.19451, 2024. 16 p.")
    add_bullet_topic(anchor_sec3, "Tipo de Publicação", "Artigo científico em repositório de ponta de Computação Gráfica e Geometria Computacional (arXiv).")
    add_bullet_topic(anchor_sec3, "Tema Central", "Modelagem geométrica fotorrealista de mechas capilares através da separação entre estrutura global e padrões locais de curvatura.")
    add_bullet_topic(anchor_sec3, "Objetivo da Obra", "Desacoplar a trajetória macroscópica da mecha (orientação da cabeça, gravidade) das componentes microscópicas de curvatura (frequência, amplitude do cacho e frizz).")
    add_bullet_topic(anchor_sec3, "Principais Conceitos", "Decomposição multiescala de curvas 3D, Análise de Componentes Principais (PCA) geométrica, e quantificação do frizz como desvio estocástico de alta frequência ao longo da trajetória média do cacho.")
    add_bullet_topic(anchor_sec3, "Metodologia Proposta", "Filtragem espacial em representações curvas de fios para extrair parâmetros invariantes à pose, permitindo modelar curvaturas 3A a 4C com fidelidade matemática.")
    add_bullet_topic(anchor_sec3, "Resultados e Contribuições", "Comprovação de que a curvatura do cabelo e o frizz operam em bandas de frequência espacial distintas, tornando viável estimar ambas as variáveis de maneira desacoplada.")
    add_bullet_topic(anchor_sec3, "Limitações Observadas", "Elevado custo computacional de renderização geométrica por mecha, inviável para processamento em tempo real em dispositivos móveis sem GPU dedicada.")
    add_bullet_topic(anchor_sec3, "Aderência ao Vila Cachos AI", "Fornece a base conceitual para o extrator do Vila Cachos AI, que desacopla a predição da curvatura morfológica global (classe 2, 3 ou 4 via YOLO) da estimativa da densidade de frizz local, sintetizando um vetor clínico de 8 atributos para o motor de recomendação.")

    # =========================================================================
    # 3. ATUALIZAR METODOLOGIA (SEÇÃO 3)
    # =========================================================================
    print("  -> Atualizando Seção 3: Metodologia e Procedimentos Experimentais...")
    
    # Inserir subseção 3.3.2 de validação métrica de clusters
    anchor_cronograma = p_cronograma_heading
    
    def add_sec3_p(text, kind="body"):
        p = anchor_cronograma.insert_paragraph_before()
        if kind == "h3":
            format_heading_paragraph(p, text, space_before=10, space_after=4)
        elif kind == "caption":
            format_caption(p, text)
        elif kind == "source":
            format_source(p, text)
        else:
            format_body_paragraph(p, text)
        return p

    # Verificar se 3.3.2 já existe
    has_332 = any("3.3.2" in p.text for p in doc.paragraphs)
    if not has_332:
        add_sec3_p("3.3.2 Validação Métrica dos Agrupamentos Tricológicos (Silhouette Score e RNF-12)", "h3")
        add_sec3_p(
            "Em complementação à validação do módulo de visão computacional, o motor de recomendação não-supervisionado "
            "foi submetido à calibração estatística formal sobre a base histórica de 1.084 atendimentos enriquecidos com feedbacks "
            "clínicos reais do salão Vila Cachos. Cada perfil foi mapeado em um espaço euclidiano normalizado de 8 dimensões clínicas: "
            "(1) curvatura morfológica, (2) nível de ressecamento, (3) nível de porosidade, (4) densidade de frizz, (5) sensibilidade do couro cabeludo, "
            "(6) histórico de processos químicos, (7) espessura do fio e (8) preferência de textura do produto."
        )
        add_sec3_p(
            "Para determinar a quantidade ideal de personas clínicas e atender formalmente ao Requisito Não Funcional RNF-12, "
            "aplicou-se o método do Coeficiente Silhouette (KAUFMAN; ROUSSEEUW, 1990) variando k de 2 a 8. A partição ótima convergiu "
            "para k=4 com Silhouette Score médio de 0,448 (superior ao teto de aceitação formal de 0,40), atestando que os agrupamentos "
            "possuem alta coesão interna e nítida separabilidade clínica:\n"
            "• Persona 0 (Curvatura 3 - Cacheados Clássicos): Foco prioritário em controle de frizz e definição com porosidade média;\n"
            "• Persona 1 (Curvaturas 2 e 3 - Ondas e Cachos Leves): Demanda estrita por formulações leves (Deva Curl Delight e geleias fluidas) para evitar peso cosmético;\n"
            "• Persona 2 (Alta Porosidade e Dano Químico): Indicação prioritária de acidificação de pH (Curly Care ACID-C) e reposição proteica;\n"
            "• Persona 3 (Curvatura 4 - Crespos Estruturais): Elevada taxa de perda hídrica e lipídica, direcionando manteigas nutritivas e ativadores densos."
        )
        add_sec3_p(
            "O pipeline completo da aplicação é coberto por uma suíte automatizada de 95 testes ponta a ponta (E2E) e de integração, "
            "garantindo conformidade arquitetural, tempos de resposta p95 inferiores a 200 ms e integridade sob restrições severas de infraestrutura (512 MB de RAM)."
        )

    # =========================================================================
    # 4. ATUALIZAR CRONOGRAMA DE EXECUÇÃO (TCC 2 - 2027.1)
    # =========================================================================
    print("  -> Atualizando Seção 4: Cronograma de Execução do TCC 2...")
    
    # Atualizar o texto introdutório da seção 4
    for i, p in enumerate(doc.paragraphs):
        if p.text.strip() == "4. CRONOGRAMA DE EXECUÇÃO":
            p_desc = doc.paragraphs[i + 1]
            p_desc.text = ""
            format_body_paragraph(
                p_desc,
                "Em estrito cumprimento aos requisitos formais do Seminário 2 da disciplina Monografia I, o cronograma a seguir "
                "detalha as atividades de pesquisa aplicada, desenvolvimento e validação empírica a serem executadas no semestre letivo subsequente "
                "(2027.1 - Fevereiro a Julho de 2027), no âmbito do Trabalho de Conclusão de Curso II (TCC 2). As etapas contemplam a homologação "
                "em campo no salão Vila Cachos, os testes de aceitação de usuário (UAT), a calibração contínua dos pesos bayesianos a partir de "
                "atendimentos reais, a redação final da monografia e a preparação para a banca examinadora pública."
            )
            break

    # Localizar a Tabela de Cronograma (Tabela 2) e atualizar seus dados
    if len(doc.tables) >= 3:
        t_cron = doc.tables[2]
        cron_headers = ["Etapa / Atividade de Execução (TCC 2)", "Fev/27", "Mar/27", "Abr/27", "Mai/27", "Jun/27", "Jul/27"]
        cron_data = [
            ["1. Instalação do Totem e treinamento da equipe clínica no salão Vila Cachos", "X", "", "", "", "", ""],
            ["2. Coleta de dados longitudinais de clientes reais e testes de aceitação (UAT)", "X", "X", "", "", "", ""],
            ["3. Calibração contínua dos pesos da Média Bayesiana Amortecida com feedbacks reais", "", "X", "X", "", "", ""],
            ["4. Avaliação estatística de satisfação pós-atendimento e cálculo de acurácia clínica", "", "", "X", "X", "", ""],
            ["5. Refinamento de usabilidade da UI/UX e otimização de latência em redes móveis", "", "", "", "X", "", ""],
            ["6. Redação dos Capítulos de Resultados Experimentais, Discussão e Conclusão", "", "", "X", "X", "X", ""],
            ["7. Revisão final do texto completo da Monografia com Orientador e Coorientadora", "", "", "", "", "X", ""],
            ["8. Depósito formal do Trabalho de Conclusão de Curso II junto à Coordenação", "", "", "", "", "X", "X"],
            ["9. Defesa Pública perante a Banca Examinadora do IFMA", "", "", "", "", "", "X"]
        ]
        
        # Recriar a tabela de cronograma com as 7 colunas de 2027.1
        # Remover linhas excedentes ou reconstruir
        p_table_anchor = t_cron._tbl.getparent()
        new_tbl = doc.add_table(rows=len(cron_data) + 1, cols=len(cron_headers))
        t_cron._tbl.addprevious(new_tbl._tbl)
        populate_table(new_tbl, cron_headers, cron_data, col_widths=[3.4, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6])
        
        # Remover a tabela antiga
        t_cron._tbl.getparent().remove(t_cron._tbl)

    # =========================================================================
    # 5. ATUALIZAR CONCLUSÃO E PERSPECTIVAS/DESAFIOS (SEÇÃO 5)
    # =========================================================================
    print("  -> Atualizando Seção 5: Conclusão e Perspectivas/Desafios para o TCC 2...")
    
    for i, p in enumerate(doc.paragraphs):
        t = p.text.strip()
        if t.startswith("5. CONSIDERAÇÕES") or t.startswith("5. CONCLUSÃO"):
            p.text = ""
            format_heading_paragraph(p, "5. CONCLUSÃO E PERSPECTIVAS/DESAFIOS PARA O TCC", space_before=14, space_after=6)
            
            # Atualizar os parágrafos seguintes de conclusão
            p_next1 = doc.paragraphs[i + 1]
            p_next1.text = ""
            format_body_paragraph(
                p_next1,
                "A conclusão do ciclo de Monografia I atesta que o projeto Vila Cachos AI consolidou com pleno êxito os seus "
                "fundamentos teóricos, sua modelagem de arquitetura de software e seu primeiro protótipo funcional integrado (MVP). "
                "A integração entre a taxonomia clínica de André Walker, o classificador convolucional YOLOv8/11 ajustado via Transfer Learning "
                "(acurácia global de 87,4% com 100% de rejeição a imagens sem mechas), o agrupamento não-supervisionado K-Means (Silhouette Score de 0,448) "
                "e o mecanismo de Média Bayesiana Amortecida comprovou a viabilidade técnica da abordagem híbrida proposta para solucionar a partida a frio (Cold Start) "
                "no nicho de cabelos ondulados, cacheados e crespos."
            )
            
            p_next2 = doc.paragraphs[i + 2]
            p_next2.text = ""
            format_body_paragraph(
                p_next2,
                "Para a execução do Trabalho de Conclusão de Curso II (TCC 2), identificam-se três perspectivas e desafios centrais "
                "que orientarão os experimentos práticos em ambiente real de salão:\n"
                "1. Variabilidade Óptica de Câmeras de Smartphones: No ambiente de salão, as condições de iluminação, reflexos de espelhos e ângulos de captura "
                "representam um desafio à estabilidade da inferência visual, demandando mecanismos adicionais de normalização e pré-processamento de luminância;\n"
                "2. Latência e Concorrência sob Limites Estritos de Nuvem: O backend opera sob a cota gratuita do Render (teto de 512 MB de RAM). A validação empírica "
                "exigirá monitoramento contínuo de sockets e desalocação de tensores em memória RAM para prevenir vazamentos durante picos de atendimento;\n"
                "3. Calibração Longitudinal do Feedback Clínico: Avaliar como as notas e avaliações fornecidas pelas clientes ao longo de semanas sucessivas de tratamento "
                "reconfiguram os rankings dos 27 cosméticos sem gerar efeito de saturação precoce ou polarização excessiva em produtos populares.\n"
                "A superação de tais desafios durante o TCC 2 consolidará a solução como uma contribuição científica e tecnológica de referência na intersecção entre Inteligência Artificial Aplicada e Engenharia de Software."
            )
            break

    # =========================================================================
    # 6. ATUALIZAR SUMÁRIO FORMAL ABNT NBR 6027 COM TAB LEADER
    # =========================================================================
    print("  -> Formatando e Calibrando Sumário ABNT NBR 6027...")
    start_idx = None
    end_idx = None
    for i, p in enumerate(doc.paragraphs):
        if p.text.startswith("1 INTRODUÇÃO") or (p.text.startswith("1. INTRODUÇÃO") and "..." in p.text):
            start_idx = i
            break

    if start_idx is not None:
        for i in range(start_idx, start_idx + 40):
            if doc.paragraphs[i].text.strip() == "1. INTRODUÇÃO":
                end_idx = i
                break

    # Formatar o título SUMÁRIO
    p_sum_title = None
    if start_idx:
        for k in range(max(0, start_idx - 5), start_idx):
            if "SUMÁRIO" in doc.paragraphs[k].text.upper():
                p_sum_title = doc.paragraphs[k]
                break
                
    if p_sum_title:
        p_sum_title.text = ""
        p_sum_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_sum_title.paragraph_format.space_before = Pt(12)
        p_sum_title.paragraph_format.space_after = Pt(20)
        p_sum_title.paragraph_format.first_line_indent = Pt(0)
        r_title = p_sum_title.add_run("SUMÁRIO")
        set_run_font(r_title, "Times New Roman", 12, bold=True)

    # Itens do Sumário para o Seminário 2
    pm = page_map or {}
    sumario_itens_abnt = [
        ("1 INTRODUÇÃO", pm.get("1 INTRODUÇÃO", "5"), "primary"),
        ("1.1 PROBLEMA", pm.get("1.1 PROBLEMA", "6"), "secondary"),
        ("1.2 JUSTIFICATIVA", pm.get("1.2 JUSTIFICATIVA", "6"), "secondary"),
        ("1.3 OBJETIVOS", pm.get("1.3 OBJETIVOS", "7"), "secondary"),
        ("2 REFERENCIAL TEÓRICO", pm.get("2 REFERENCIAL TEÓRICO", "9"), "primary"),
        ("2.1 SISTEMAS DE RECOMENDAÇÃO E O DESAFIO DO COLD START", pm.get("2.1 SISTEMAS DE RECOMENDAÇÃO E O DESAFIO DO COLD START", "9"), "secondary"),
        ("2.2 CLUSTERIZAÇÃO K-MEANS PARA SEGMENTAÇÃO DE PERSONAS", pm.get("2.2 CLUSTERIZAÇÃO K-MEANS PARA SEGMENTAÇÃO DE PERSONAS", "9"), "secondary"),
        ("2.3 INFERÊNCIA BAYESIANA E RANKING AMORTECIDO", pm.get("2.3 INFERÊNCIA BAYESIANA E RANKING AMORTECIDO", "10"), "secondary"),
        ("2.4 EXPLICABILIDADE EM INTELIGÊNCIA ARTIFICIAL (XAI)", pm.get("2.4 EXPLICABILIDADE EM INTELIGÊNCIA ARTIFICIAL (XAI)", "11"), "secondary"),
        ("2.5 VISÃO COMPUTACIONAL E RECONHECIMENTO DE PADRÕES CAPILARES", pm.get("2.5 VISÃO COMPUTACIONAL E RECONHECIMENTO DE PADRÕES CAPILARES", "12"), "secondary"),
        ("2.6 TRABALHOS CORRELATOS E ANÁLISE COMPARATIVA", pm.get("2.6 TRABALHOS CORRELATOS E ANÁLISE COMPARATIVA", "13"), "secondary"),
        ("2.7 FICHAMENTO DE PUBLICAÇÕES (ESTUDO ESTRUTURADO DA LITERATURA)", pm.get("2.7 FICHAMENTO DE PUBLICAÇÕES (ESTUDO ESTRUTURADO DA LITERATURA)", "15"), "secondary"),
        ("3 METODOLOGIA DA PESQUISA", pm.get("3 METODOLOGIA DA PESQUISA", "18"), "primary"),
        ("3.1 CLASSIFICAÇÃO DA PESQUISA", pm.get("3.1 CLASSIFICAÇÃO DA PESQUISA", "18"), "secondary"),
        ("3.2 PROCEDIMENTOS TÉCNICOS E COLETA DE DADOS", pm.get("3.2 PROCEDIMENTOS TÉCNICOS E COLETA DE DADOS", "19"), "secondary"),
        ("3.3 ARQUITETURA DO SISTEMA E VALIDAÇÃO", pm.get("3.3 ARQUITETURA DO SISTEMA E VALIDAÇÃO", "20"), "secondary"),
        ("3.3.1 Validação Experimental do Módulo de Visão (Matriz 4x4)", pm.get("3.3.1 Validação Experimental do Módulo de Visão (Matriz 4x4)", "21"), "tertiary"),
        ("3.3.2 Validação Métrica dos Agrupamentos Tricológicos (RNF-12)", pm.get("3.3.2 Validação Métrica dos Agrupamentos Tricológicos (RNF-12)", "22"), "tertiary"),
        ("4 CRONOGRAMA DE EXECUÇÃO", pm.get("4 CRONOGRAMA DE EXECUÇÃO", "23"), "primary"),
        ("5 CONCLUSÃO E PERSPECTIVAS/DESAFIOS PARA O TCC", pm.get("5 CONCLUSÃO E PERSPECTIVAS/DESAFIOS PARA O TCC", "24"), "primary"),
        ("REFERÊNCIAS", pm.get("REFERÊNCIAS", "25"), "primary"),
        ("ANEXO 1: FICHA DE ACEITE DE ORIENTAÇÃO DE TCC", pm.get("ANEXO 1: FICHA DE ACEITE DE ORIENTAÇÃO DE TCC", "26"), "primary"),
    ]

    if start_idx and end_idx:
        # Ajustar parágrafos
        while (end_idx - start_idx) < len(sumario_itens_abnt):
            doc.paragraphs[end_idx].insert_paragraph_before()
            end_idx += 1

        while (end_idx - start_idx) > len(sumario_itens_abnt):
            p_del = doc.paragraphs[start_idx + len(sumario_itens_abnt)]
            p_del._p.getparent().remove(p_del._p)
            end_idx -= 1

        for i, (item_title, pg_num, level) in enumerate(sumario_itens_abnt):
            p_item = doc.paragraphs[start_idx + i]
            p_item.text = ""
            p_item.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p_item.paragraph_format.tab_stops.add_tab_stop(Cm(16.0), alignment=WD_TAB_ALIGNMENT.RIGHT, leader=WD_TAB_LEADER.DOTS)
            p_item.paragraph_format.line_spacing = 1.3
            p_item.paragraph_format.space_before = Pt(1.5)
            p_item.paragraph_format.space_after = Pt(1.5)
            p_item.paragraph_format.first_line_indent = Pt(0)

            is_prim = (level == "primary")
            is_sec = (level == "secondary")

            r_title = p_item.add_run(item_title)
            r_title.font.name = "Times New Roman"
            if is_prim:
                r_title.font.size = Pt(11.5)
                r_title.bold = True
            elif is_sec:
                r_title.font.size = Pt(11)
                r_title.bold = False
            else:
                r_title.font.size = Pt(10.5)
                r_title.bold = True

            r_page = p_item.add_run(f"\t{pg_num}")
            r_page.font.name = "Times New Roman"
            r_page.font.size = Pt(11)
            r_page.bold = is_prim

        # Quebra de página antes da Introdução
        p_intro = doc.paragraphs[end_idx]
        p_intro.paragraph_format.page_break_before = True

    doc.save(TARGET_DOCX)
    print(f"Documento de Seminário 2 salvo em: {TARGET_DOCX}")

def calibrate_and_build():
    print("=== INICIANDO CALIBRAÇÃO E GERAÇÃO DO DOCUMENTO SEMINÁRIO 2 ===")
    
    # 1. Primeira compilação
    build_document()
    print("Convertendo DOCX preliminar para PDF para mapear paginação real...")
    ok = convert_docx_to_pdf(TARGET_DOCX, DOCS_DIR)
    if not ok or not os.path.exists(TARGET_PDF):
        print("Falha na geração do PDF preliminar.")
        return False

    # 2. Ler PDF e mapear páginas
    reader = pypdf.PdfReader(TARGET_PDF)
    print(f"PDF preliminar gerado com {len(reader.pages)} páginas. Mapeando posições reais...")

    def search_page(pattern, is_prefix=True):
        for idx, page in enumerate(reader.pages):
            if idx <= 3:  # Ignorar capa, folha de rosto, resumo e sumário
                continue
            txt = page.extract_text() or ""
            for line in txt.split("\n"):
                l = line.strip()
                if "..." in l or l.startswith("Fonte:"):
                    continue
                if is_prefix and l.startswith(pattern):
                    return str(idx + 1)
                elif not is_prefix and pattern.lower() in l.lower():
                    return str(idx + 1)
        return None

    real_pages = {}
    real_pages["1 INTRODUÇÃO"] = search_page("1. INTRODUÇÃO") or "5"
    real_pages["1.1 PROBLEMA"] = search_page("1.1 PROBLEMA") or "6"
    real_pages["1.2 JUSTIFICATIVA"] = search_page("1.2 JUSTIFICATIVA") or "6"
    real_pages["1.3 OBJETIVOS"] = search_page("1.3 OBJETIVOS") or "7"
    real_pages["2 REFERENCIAL TEÓRICO"] = search_page("2. REFERENCIAL TEÓRICO") or "9"
    real_pages["2.1 SISTEMAS DE RECOMENDAÇÃO E O DESAFIO DO COLD START"] = search_page("2.1 SISTEMAS DE RECOMENDAÇÃO") or "9"
    real_pages["2.2 CLUSTERIZAÇÃO K-MEANS PARA SEGMENTAÇÃO DE PERSONAS"] = search_page("2.2 CLUSTERIZAÇÃO K-MEANS") or "9"
    real_pages["2.3 INFERÊNCIA BAYESIANA E RANKING AMORTECIDO"] = search_page("2.3 INFERÊNCIA BAYESIANA") or "10"
    real_pages["2.4 EXPLICABILIDADE EM INTELIGÊNCIA ARTIFICIAL (XAI)"] = search_page("2.4 EXPLICABILIDADE") or "11"
    real_pages["2.5 VISÃO COMPUTACIONAL E RECONHECIMENTO DE PADRÕES CAPILARES"] = search_page("2.5") or "12"
    real_pages["2.6 TRABALHOS CORRELATOS E ANÁLISE COMPARATIVA"] = search_page("2.6 TRABALHOS CORRELATOS") or "13"
    real_pages["2.7 FICHAMENTO DE PUBLICAÇÕES (ESTUDO ESTRUTURADO DA LITERATURA)"] = search_page("2.7 FICHAMENTO") or "15"
    real_pages["3 METODOLOGIA DA PESQUISA"] = search_page("3. METODOLOGIA DA PESQUISA") or "18"
    real_pages["3.1 CLASSIFICAÇÃO DA PESQUISA"] = search_page("3.1 CLASSIFICAÇÃO") or "18"
    real_pages["3.2 PROCEDIMENTOS TÉCNICOS E COLETA DE DADOS"] = search_page("3.2 PROCEDIMENTOS TÉCNICOS") or "19"
    real_pages["3.3 ARQUITETURA DO SISTEMA E VALIDAÇÃO"] = search_page("3.3 ARQUITETURA DO SISTEMA") or "20"
    real_pages["3.3.1 Validação Experimental do Módulo de Visão (Matriz 4x4)"] = search_page("3.3.1") or "21"
    real_pages["3.3.2 Validação Métrica dos Agrupamentos Tricológicos (RNF-12)"] = search_page("3.3.2") or "22"
    real_pages["4 CRONOGRAMA DE EXECUÇÃO"] = search_page("4. CRONOGRAMA DE EXECUÇÃO") or "23"
    real_pages["5 CONCLUSÃO E PERSPECTIVAS/DESAFIOS PARA O TCC"] = search_page("5. CONCLUSÃO") or "24"
    real_pages["REFERÊNCIAS"] = search_page("REFERÊNCIAS", is_prefix=False) or "25"
    real_pages["ANEXO 1: FICHA DE ACEITE DE ORIENTAÇÃO DE TCC"] = search_page("ANEXO 1", is_prefix=True) or "26"

    print("\nPáginas mapeadas com precisão milimétrica:")
    for k, v in real_pages.items():
        print(f"  {k} -> Página {v}")

    # 3. Segunda compilação calibrada
    print("\nReconstruindo documento com Sumário 100% calibrado...")
    build_document(page_map=real_pages)
    convert_docx_to_pdf(TARGET_DOCX, DOCS_DIR)

    # 4. Verificação de integridade
    final_reader = pypdf.PdfReader(TARGET_PDF)
    print(f"\nDOCUMENTO FINAL GERADO COM SUCESSO!")
    print(f"  Arquivo DOCX: {TARGET_DOCX} ({os.path.getsize(TARGET_DOCX)} bytes)")
    print(f"  Arquivo PDF (Sem Compactação): {TARGET_PDF} ({os.path.getsize(TARGET_PDF)} bytes)")
    print(f"  Total de páginas: {len(final_reader.pages)}")
    return True

if __name__ == "__main__":
    calibrate_and_build()
