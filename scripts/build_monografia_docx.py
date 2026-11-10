import os
import shutil
import subprocess
import docx
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCX_PATH = os.path.join(BASE_DIR, "faculdade_ifma", "tcc_1_monografia", "documentos", "Modelo_Projeto_TCC.docx")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_document():
    doc = docx.Document()

    # Page setup - A4 with ABNT margins (3cm top/left, 2cm bottom/right)
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(3.0)
    section.left_margin = Cm(3.0)
    section.bottom_margin = Cm(2.0)
    section.right_margin = Cm(2.0)

    # Base styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)

    def add_p(text="", align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, line_spacing=1.5, bold=False, first_indent=1.25, font_size=12, italic=False, all_caps=False, keep_with_next=False):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.line_spacing = line_spacing
        p.paragraph_format.widow_control = True
        if keep_with_next or (bold and first_indent == 0):
            p.paragraph_format.keep_with_next = True
        if first_indent > 0:
            p.paragraph_format.first_line_indent = Cm(first_indent)
        else:
            p.paragraph_format.first_line_indent = Cm(0)
            
        if text:
            run = p.add_run(text.upper() if all_caps else text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(font_size)
            run.bold = bold
            run.italic = italic
        return p

    def add_blank(lines=1, font_size=12):
        for _ in range(lines):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            r = p.add_run()
            r.font.name = 'Times New Roman'
            r.font.size = Pt(font_size)

    # ==========================================
    # 1. CAPA
    # ==========================================
    add_p("INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DO MARANHÃO", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, first_indent=0, space_after=2)
    add_p("CAMPUS SÃO LUÍS - MONTE CASTELO", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, first_indent=0, space_after=2)
    add_p("DEPARTAMENTO DE COMPUTAÇÃO", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, first_indent=0, space_after=2)
    add_p("CURSO DE BACHARELADO EM SISTEMAS DE INFORMAÇÃO", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, first_indent=0, space_after=12)

    add_blank(7)

    add_p("MARCOS VINÍCIUS", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, first_indent=0, space_after=12)

    add_blank(7)

    add_p("VILA CACHOS AI: SISTEMA HÍBRIDO DE RECOMENDAÇÃO CAPILAR COM APRENDIZADO NÃO SUPERVISIONADO E INFERÊNCIA BAYESIANA", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, first_indent=0, space_after=6)
    add_p("Um Web App de Diagnóstico Integrado para o Salão Vila Cachos", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, first_indent=0, space_after=12)

    add_blank(15)

    add_p("SÃO LUÍS – MA", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, first_indent=0, space_after=2)
    add_p("2026", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, first_indent=0, space_after=0)

    doc.add_page_break()

    # ==========================================
    # 2. FOLHA DE ROSTO
    # ==========================================
    add_p("MARCOS VINÍCIUS", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, first_indent=0, space_after=12)

    add_blank(6)

    add_p("VILA CACHOS AI: SISTEMA HÍBRIDO DE RECOMENDAÇÃO CAPILAR COM APRENDIZADO NÃO SUPERVISIONADO E INFERÊNCIA BAYESIANA", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, first_indent=0, space_after=6)
    add_p("Um Web App de Diagnóstico Integrado para o Salão Vila Cachos", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, first_indent=0, space_after=12)

    add_blank(4)

    # Natureza do trabalho (recuo de 8 cm à esquerda, espaçamento simples, tamanho 10 ou 11)
    p_nat = doc.add_paragraph()
    p_nat.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_nat.paragraph_format.left_indent = Cm(8.0)
    p_nat.paragraph_format.space_before = Pt(0)
    p_nat.paragraph_format.space_after = Pt(12)
    p_nat.paragraph_format.line_spacing = 1.0
    r_nat = p_nat.add_run("Projeto de Trabalho de Conclusão de Curso, apresentado à disciplina Monografia I, ministrada pelo Prof. Dr. Hélder Pereira Borges, como requisito básico para o Trabalho de Conclusão de Curso do Bacharelado em Sistemas de Informação.")
    r_nat.font.name = 'Times New Roman'
    r_nat.font.size = Pt(10)

    # Orientadores
    p_ori = doc.add_paragraph()
    p_ori.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_ori.paragraph_format.left_indent = Cm(8.0)
    p_ori.paragraph_format.space_before = Pt(6)
    p_ori.paragraph_format.space_after = Pt(2)
    p_ori.paragraph_format.line_spacing = 1.0
    r_ori = p_ori.add_run("Orientador: Prof. Me. Alex Martins Pereira\nCoorientadora: Profa. Me. Eveline de Jesus Viana Silva")
    r_ori.font.name = 'Times New Roman'
    r_ori.font.size = Pt(10)
    r_ori.bold = True

    add_blank(18)

    add_p("SÃO LUÍS – MA", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, first_indent=0, space_after=2)
    add_p("2026", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, first_indent=0, space_after=0)

    doc.add_page_break()

    # ==========================================
    # 3. RESUMO
    # ==========================================
    add_p("RESUMO", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, first_indent=0, space_after=18)

    resumo_texto = (
        "O presente projeto de monografia circunscreve-se na interseção entre Inteligência Artificial e "
        "Engenharia de Software, propondo o desenvolvimento, implementação e validação do Vila Cachos AI, "
        "um sistema especialista híbrido de diagnóstico e recomendação capilar voltado para salões de beleza "
        "especializados em cabelos com curvatura (ondulados, cacheados e crespos). O atendimento especializado "
        "neste nicho ressente-se da ausência de bases históricas estruturadas e da inerente subjetividade diagnóstica "
        "humana, configurando o entrave clássico do Cold Start. Para superar essa restrição, a arquitetura concebida "
        "combina heurísticas clínicas de especialistas, segmentação não supervisionada por agrupamento K-Means e "
        "aprendizado contínuo através de Média Bayesiana Amortecida (Damped Average), prevenindo distorções estatísticas "
        "em amostras incipientes. Em contraposição ao modelo físico de totens dedicados de alto custo, a solução é "
        "materializada sob um Web App reativo (React/Vite e FastAPI), permitindo acesso escalável via smartphone ou tablet, "
        "isenção de custos logísticos de hardware e governança centralizada de regras terapêuticas em nuvem. A transparência "
        "das indicações é garantida mediante Inteligência Artificial Explicável (XAI) em linguagem natural. A validação técnica "
        "abrange a análise de coesão e separação dos clusters por meio do Coeficiente Silhouette e do Método do Cotovelo. "
        "Espera-se fornecer padronização diagnóstica, redução substancial da variabilidade de atendimento no salão Vila Cachos "
        "e fidelização sustentada em prescrições assertivas fundamentadas em dados."
    )
    add_p(resumo_texto, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=12, line_spacing=1.0, first_indent=0)

    p_kw = add_p("Palavras-chave: ", bold=True, first_indent=0, space_after=0, line_spacing=1.0)
    p_kw.runs[0].font.size = Pt(12)
    r_kw = p_kw.add_run("Sistemas de Recomendação. K-Means. Inferência Bayesiana. Cold Start. Diagnóstico Capilar. Web App.")
    r_kw.font.name = 'Times New Roman'
    r_kw.font.size = Pt(12)
    r_kw.bold = False

    doc.add_page_break()

    # ==========================================
    # 4. SUMÁRIO
    # ==========================================
    add_p("SUMÁRIO", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, first_indent=0, space_after=18)

    sumario_items = [
        ("1. INTRODUÇÃO", "5"),
        ("1.1 PROBLEMA", "6"),
        ("1.1.1 PERGUNTA PROBLEMA", "6"),
        ("1.1.2 HIPÓTESE DA PESQUISA", "6"),
        ("1.2 JUSTIFICATIVA", "6"),
        ("1.3 OBJETIVOS", "7"),
        ("1.3.1 GERAL", "7"),
        ("1.3.2 ESPECÍFICOS", "7"),
        ("2. REFERENCIAL TEÓRICO", "9"),
        ("2.1 SISTEMAS DE RECOMENDAÇÃO E O DESAFIO DO COLD START", "9"),
        ("2.2 CLUSTERIZAÇÃO K-MEANS PARA SEGMENTAÇÃO DE PERSONAS", "9"),
        ("2.3 INFERÊNCIA BAYESIANA E RANKING AMORTECIDO", "10"),
        ("2.4 EXPLICABILIDADE EM INTELIGÊNCIA ARTIFICIAL (XAI)", "11"),
        ("3. METODOLOGIA DA PESQUISA", "12"),
        ("3.1 CLASSIFICAÇÃO DA PESQUISA", "12"),
        ("3.2 PROCEDIMENTOS TÉCNICOS E COLETA DE DADOS", "12"),
        ("3.3 ARQUITETURA DO SISTEMA E VALIDAÇÃO", "12"),
        ("4. CRONOGRAMA DE EXECUÇÃO", "13"),
        ("5. CONSIDERAÇÕES PRELIMINARES", "14"),
        ("REFERÊNCIAS", "15"),
        ("ANEXO 1: FICHA DE ACEITE", "16"),
    ]

    for title, pg in sumario_items:
        p_sum = doc.add_paragraph()
        p_sum.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_sum.paragraph_format.space_before = Pt(0)
        p_sum.paragraph_format.space_after = Pt(3)
        p_sum.paragraph_format.line_spacing = 1.0
        p_sum.paragraph_format.first_line_indent = Cm(0)
        
        is_primary = not title.startswith("1.") and not title.startswith("2.") and not title.startswith("3.") and not title.startswith("4.") and not title.startswith("5.")
        if any(title.startswith(f"{i}. ") for i in range(1, 10)) or title in ["REFERÊNCIAS", "ANEXO 1: FICHA DE ACEITE"]:
            is_bold = True
        else:
            is_bold = False
            
        r_title = p_sum.add_run(title)
        r_title.font.name = 'Times New Roman'
        r_title.font.size = Pt(11)
        r_title.bold = is_bold
        
        # Dots
        dots_count = max(5, 75 - len(title))
        r_dots = p_sum.add_run(" " + "." * dots_count + " ")
        r_dots.font.name = 'Times New Roman'
        r_dots.font.size = Pt(10)
        r_dots.bold = False
        
        r_pg = p_sum.add_run(pg)
        r_pg.font.name = 'Times New Roman'
        r_pg.font.size = Pt(11)
        r_pg.bold = is_bold

    doc.add_page_break()

    # ==========================================
    # 5. SEÇÃO 1: INTRODUÇÃO
    # ==========================================
    add_p("1. INTRODUÇÃO", bold=True, first_indent=0, space_after=12)

    add_p(
        "O setor de estética e cosméticos capilares no Brasil tem experimentado transformações estruturais marcadas "
        "pelo avanço do movimento de transição capilar e pela expressiva valorização da textura natural dos fios com curvatura "
        "— abrangendo cabelos ondulados, cacheados e crespos (tipos 2A a 4C segundo a classificação internacional de Walker). "
        "A morfologia singular desses fios, caracterizada pela distribuição elíptica e helicoidal que dificulta a migração da "
        "oleosidade natural ao longo da haste capilar, impõe demandas bioquímicas altamente específicas de nutrição, hidratação "
        "e reconstrução lipídica. Paralelamente a esse crescimento mercadológico, emergiu uma proliferação de formulações cosméticas "
        "compostos por princípios ativos diferenciados, gerando um ecossistema complexo no qual a identificação do tratamento "
        "correto exige profundo discernimento técnico."
    )

    add_p(
        "Apesar da sofisticação química dos produtos disponíveis, o diagnóstico capilar em micro e pequenos salões de beleza "
        "especializados — a exemplo do salão Vila Cachos, localizado em São Luís - MA — permanece majoritariamente fundamentado "
        "em práticas empíricas e na percepção subjetiva de profissionais individuais. Tal cenário resulta em significativa "
        "variabilidade no atendimento, tornando a experiência da cliente dependente do profissional que a assiste e "
        "dificultando a padronização operacional do estabelecimento. Adicionalmente, as abordagens tradicionais de Sistemas "
        "de Recomendação (SR) computacionais falham em atender a esse nicho de negócios, pois pressupõem volumosos históricos de "
        "interação prévia de clientes para aplicação de Filtragem Colaborativa — um requisito inviável diante do problema "
        "clássico de partida a frio (Cold Start)."
    )

    add_p(
        "Nesse contexto, o presente projeto de monografia propõe o desenvolvimento, implementação e validação matemática do "
        "Vila Cachos AI, um sistema especialista multimodal e híbrido que combina inteligência heurística baseada no conhecimento "
        "clínico de especialistas, agrupamento não supervisionado por K-Means para identificação de personas e aprendizado contínuo "
        "fundamentado na Média Bayesiana Amortecida. Operando sob uma arquitetura de Web App reativo em nuvem, a solução "
        "dispensa investimentos em totens físicos dedicados, promovendo a democratização do acesso tecnológico à microempresa "
        "e viabilizando diagnósticos padronizados, precisos e explicáveis desde o primeiro contato da cliente."
    )

    doc.add_page_break()

    # 1.1 PROBLEMA
    add_p("1.1 PROBLEMA", bold=True, first_indent=0, space_after=12)

    add_p(
        "O modelo operacional vigente em salões especializados em curvatura capilar enfrenta um tríplice entrave: "
        "(1) a subjetividade e a inconsistência diagnóstica humana, onde profissionais distintas chegam a conclusões divergentes "
        "acerca da curvatura, porosidade e nível de dano capilar de uma mesma cliente; (2) o turnover rotineiro de cabeleireiras "
        "e assistentes, que descontinua o padrão de atendimento e dispersa o conhecimento tácito do salão; e (3) a escassez "
        "de dados históricos digitalizados sobre novos clientes e produtos recém-integrados ao estoque, impossibilitando a "
        "adoção de algoritmos convencionais de recomendação baseados em correlação estatística pura (Cold Start)."
    )

    add_p(
        "Na ausência de uma ferramenta tecnológica formal que una rigor analítico e simplicidade operacional, o salão "
        "enfrenta perdas decorrentes de prescrições inadequadas, retrabalho em procedimentos químicos e frustração das clientes, "
        "além da incapacidade de extrair inteligência de negócio a partir do perfil epidemiológico capilar da sua base atendida."
    )

    # 1.1.1 Pergunta Problema
    add_p("1.1.1 Pergunta Problema", bold=True, first_indent=0, space_after=6)
    add_p(
        "Diante do cenário delineado, formula-se o seguinte questionamento científico que orienta esta pesquisa: "
        "De que maneira a combinação de uma arquitetura híbrida de Inteligência Artificial — integrando clusterização "
        "K-Means para segmentação de personas e Média Bayesiana Amortecida para aprendizado contínuo — pode mitigar o "
        "problema do Cold Start e padronizar o diagnóstico de cosméticos em um salão de beleza especializado, operando "
        "sob uma interface Web App altamente escalável?"
    )

    # 1.1.2 Hipótese da Pesquisa
    add_p("1.1.2 Hipótese da Pesquisa", bold=True, first_indent=0, space_after=6)
    add_p(
        "A integração estruturada de heurísticas clínicas especialistas com técnicas de clusterização não supervisionada "
        "(K-Means) e regularização por Média Bayesiana Amortecida (Damped Average) permite gerar prescrições cosméticas "
        "personalizadas, consistentes e explicáveis desde o primeiro atendimento da cliente (mitigando o Cold Start), "
        "reduzindo a variabilidade diagnóstica entre profissionais e estabilizando rankings de recomendação mesmo perante "
        "amostras de avaliação incipientes."
    )

    # 1.2 JUSTIFICATIVA
    add_p("1.2 JUSTIFICATIVA", bold=True, first_indent=0, space_after=12)

    add_p(
        "A justificativa desta investigação alicerça-se em três pilares fundamentais: acadêmico-científico, prático-social e tecnológico-arquitetural."
    )

    add_p(
        "Sob a ótica acadêmico-científica, o estudo contribui para a literatura de Sistemas de Recomendação ao explorar "
        "mecanismos híbridos aplicados a um domínio empírico com severa escassez de dados abertos e formalizados. A modelagem "
        "matemática da Média Bayesiana Amortecida como regulador de incerteza contra flutuações de pequenas amostras e o "
        "emprego de métricas consolidadas de validação de agrupamentos (Coeficiente Silhouette e Inércia Intra-cluster) fornecem "
        "rigor metodológico a uma área frequentemente desprovida de suporte computacional analítico."
    )

    add_p(
        "Do ponto de vista prático e social, a pesquisa materializa uma intervenção aplicada no salão Vila Cachos, "
        "uma microempresa maranhense focada na valorização da autoimagem e saúde capilar da população afro-brasileira. "
        "A padronização diagnóstica empodera o negócio local, reduz custos com produtos prescritos incorretamente e "
        "promove a fidelização da clientela por meio de uma experiência transparente pautada em dados."
    )

    add_p(
        "Por fim, a justificativa arquitetural centra-se na decisão estratégica de conceber a solução como um Web App "
        "responsivo (React/Vite e FastAPI) hospedado em nuvem, em substituição a protótipos baseados em totens físicos de hardware. "
        "A eliminação de custos com gabinetes industriais, telas touch dedicadas e cabeamento democratiza o acesso do software "
        "a negócios de pequeno porte, assegura escalabilidade imediata para execução nos smartphones das clientes ou profissionais "
        "e viabiliza atualizações algorítmicas centralizadas sem necessidade de deslocamento técnico presencial."
    )

    # 1.3 OBJETIVOS
    add_p("1.3 OBJETIVOS", bold=True, first_indent=0, space_after=12)

    # 1.3.1 Geral
    add_p("1.3.1 Geral", bold=True, first_indent=0, space_after=6)
    add_p(
        "Projetar, implementar e validar um Motor Híbrido de Recomendação Capilar integrado a um Web App de Diagnóstico, "
        "concebido especificamente para mitigar o problema do Cold Start e padronizar o atendimento técnico do salão Vila Cachos."
    )

    # 1.3.2 Específicos
    add_p("1.3.2 Específicos", bold=True, first_indent=0, space_after=6)
    especificos = [
        "Modelar a taxonomia clínica do domínio capilar (curvatura, porosidade, histórico de intervenções químicas e queixas terapêuticas), estruturando uma matriz de afinidade entre atributos biológicos do fio e composições de produtos cosméticos;",
        "Desenvolver e calibrar o algoritmo de clusterização não supervisionada (K-Means) para segmentação do espaço multidimensional de dados capilares, identificando personas comportamentais dominantes;",
        "Implementar a camada de aprendizado contínuo (Feedback Loop) utilizando a formulação matemática de Média Bayesiana Amortecida, assegurando robustez estatística e mitigação de ruídos em avaliações iniciais;",
        "Construir e disponibilizar uma interface web responsiva (React/Vite) integrada a uma API RESTful de alta performance (FastAPI), provendo transparência diagnóstica por meio de justificativas em linguagem natural (XAI);",
        "Avaliar metricamente a qualidade dos agrupamentos gerados com base nos coeficientes matemáticos de Inércia (WCSS), Método do Cotovelo (Elbow Method) e Coeficiente Silhouette, atestando a separabilidade e coesão dos grupos."
    ]
    for esp in especificos:
        p_esp = doc.add_paragraph()
        p_esp.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_esp.paragraph_format.left_indent = Cm(1.25)
        p_esp.paragraph_format.first_line_indent = Cm(-0.5)
        p_esp.paragraph_format.space_before = Pt(0)
        p_esp.paragraph_format.space_after = Pt(4)
        p_esp.paragraph_format.line_spacing = 1.5
        r_bullet = p_esp.add_run("• ")
        r_bullet.font.name = 'Times New Roman'
        r_bullet.bold = True
        r_text = p_esp.add_run(esp)
        r_text.font.name = 'Times New Roman'
        r_text.font.size = Pt(12)

    doc.add_page_break()

    # ==========================================
    # 6. SEÇÃO 2: REFERENCIAL TEÓRICO
    # ==========================================
    add_p("2. REFERENCIAL TEÓRICO", bold=True, first_indent=0, space_after=12)

    add_p(
        "A fundamentação teórica deste projeto estrutura-se na intersecção entre quatro eixos do conhecimento: "
        "Sistemas de Recomendação com foco em partida a frio, Algoritmos de Clusterização Não Supervisionada, "
        "Inferência Bayesiana aplicada a mecanismos de ranqueamento e Inteligência Artificial Explicável (XAI)."
    )

    add_p("2.1 SISTEMAS DE RECOMENDAÇÃO E O DESAFIO DO COLD START", bold=True, first_indent=0, space_after=6)
    add_p(
        "Conforme preconizado por Aggarwal (2016), Sistemas de Recomendação configuram mecanismos algorítmicos concebidos "
        "para estimar a preferência ou utilidade de determinados itens para usuários específicos. Classicamente divididos em "
        "Filtragem Baseada em Conteúdo (Content-Based) e Filtragem Colaborativa (Collaborative Filtering), estes sistemas "
        "esbarram na restrição do Cold Start quando confrontados com novos usuários ou novos itens desprovidos de histórico. "
        "No contexto do salão Vila Cachos, a ausência de transações históricas prévias de novas clientes inviabiliza abordagens "
        "puramente colaborativas, exigindo a adoção de sistemas baseados em conhecimento e arquiteturas híbridas de recomendação."
    )

    add_p("2.2 CLUSTERIZAÇÃO K-MEANS PARA SEGMENTAÇÃO DE PERSONAS", bold=True, first_indent=0, space_after=6)
    add_p(
        "O algoritmo K-Means, amplamente fundamentado por Tan, Steinbach e Kumar (2019), é um método de particionamento não supervisionado "
        "que divide um conjunto de dados n-dimensional em k grupos disjuntos, minimizando a soma dos quadrados das distâncias "
        "euclidianas intra-cluster (Inércia ou WCSS). A definição ótima do número de clusters k é norteada pelo Método do Cotovelo "
        "e validada pelo Coeficiente Silhouette (Kaufman; Rousseeuw, 1990), que quantifica a coesão interna e a separação "
        "mútua entre agrupamentos em uma escala normalizada entre -1 e +1."
    )

    # Imagem da Silhouette e Elbow se existirem
    img_elbow = os.path.join(ASSETS_DIR, "fig_elbow_method.png")
    if os.path.exists(img_elbow):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        run_img = p_img.add_run()
        run_img.add_picture(img_elbow, width=Inches(5.0))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(12)
        r_cap = p_cap.add_run("Figura 1: Determinação de clusters ótimos via Método do Cotovelo (Inércia WCSS).\nFonte: Produção do Autor (2026).")
        r_cap.font.name = 'Times New Roman'
        r_cap.font.size = Pt(10)
        r_cap.italic = True

    add_p("2.3 INFERÊNCIA BAYESIANA E RANKING AMORTECIDO", bold=True, first_indent=0, space_after=6)
    add_p(
        "Mecanismos de avaliação simplificados, tais como a média aritmética de notas (1 a 5 estrelas), apresentam severa "
        "vulnerabilidade em cenários com baixo volume amostral: um produto cosmético avaliado com uma única nota 5 assumiria "
        "indevidamente a liderança sobre um produto com cem avaliações e média 4.8. Para estabilizar essa dinâmica, emprega-se "
        "o estimador da Média Bayesiana Amortecida (Damped Average), formulado como R = (C * m + sum(v)) / (C + n), onde m representa "
        "o prior global da base, n o número de avaliações do produto e C o parâmetro de confiança (amortecimento). Com essa regularização, "
        "produtos novos convergem gradualmente ao seu mérito real à medida que coletam evidências, protegendo o sistema contra ruídos."
    )

    img_bayes = os.path.join(ASSETS_DIR, "fig_bayesian_feedback.png")
    if os.path.exists(img_bayes):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        run_img = p_img.add_run()
        run_img.add_picture(img_bayes, width=Inches(5.2))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(12)
        r_cap = p_cap.add_run("Figura 2: Curva de estabilização bayesiana versus média aritmética em pequenas amostras.\nFonte: Produção do Autor (2026).")
        r_cap.font.name = 'Times New Roman'
        r_cap.font.size = Pt(10)
        r_cap.italic = True

    add_p("2.4 EXPLICABILIDADE EM INTELIGÊNCIA ARTIFICIAL (XAI)", bold=True, first_indent=0, space_after=6)
    add_p(
        "A adoção de modelos de 'caixa-preta' gera resistência em ambientes clínicos e estéticos, nos quais a profissional e "
        "a cliente necessitam compreender a motivação de cada prescrição. A Inteligência Artificial Explicável (XAI) estabelece "
        "estruturas semânticas que traduzem os pesos numéricos de similaridade em justificativas legíveis em linguagem natural "
        "(e.g., 'Indicado pela alta porosidade do fio combinada com necessidade de reposição de massa lipídica decorrente de descoloração prévia')."
    )

    doc.add_page_break()

    # ==========================================
    # 7. SEÇÃO 3: METODOLOGIA DA PESQUISA
    # ==========================================
    add_p("3. METODOLOGIA DA PESQUISA", bold=True, first_indent=0, space_after=12)

    add_p(
        "A metodologia desta monografia delineia a classificação epistemológica do estudo, os procedimentos técnicos "
        "de coleta e modelagem de dados, bem como o fluxo arquitetural de engenharia de software empregado."
    )

    add_p("3.1 CLASSIFICAÇÃO DA PESQUISA", bold=True, first_indent=0, space_after=6)
    add_p(
        "Em conformidade com as diretrizes do Projeto Pedagógico do Curso de Bacharelado em Sistemas de Informação do IFMA "
        "(Resolução nº 088/2022), a presente investigação qualifica-se como pesquisa aplicada quanto à sua natureza, tendo "
        "por finalidade imediata a solução de um problema concreto e operacional do salão Vila Cachos. Quanto aos objetivos, "
        "assume caráter exploratório e descritivo, visando caracterizar as correlações morfológicas capilares e validar "
        "a viabilidade de algoritmos de aprendizado híbrido no domínio cosmético."
    )

    add_p("3.2 PROCEDIMENTOS TÉCNICOS E COLETA DE DADOS", bold=True, first_indent=0, space_after=6)
    add_p(
        "A pesquisa desenvolve-se através das seguintes etapas procedimentais: (1) Levantamento da taxonomia capilar junto "
        "aos especialistas do salão Vila Cachos, catalogando 8 variáveis essenciais de anamnese (curvatura, porosidade, espessura, "
        "densidade, histórico químico, couro cabeludo, queixa principal e objetivo imediato); (2) Catalogação oficial de 27 cosméticos "
        "do portfólio ativo do salão, associando composição ativa e indicação terapêutica; (3) Construção de um gerador sintético "
        "com causalidade probabilística para simular 1.000 atendimentos realistas, mimetizando a distribuição condicional observada "
        "em ambiente real; e (4) Treinamento, calibração e teste do motor híbrido em ambiente de testes automatizados."
    )

    add_p("3.3 ARQUITETURA DO SISTEMA E VALIDAÇÃO", bold=True, first_indent=0, space_after=6)
    add_p(
        "A solução divide-se em duas camadas: a API RESTful construída em FastAPI (Python 3.11), responsável pela inferência "
        "do K-Means (scikit-learn), cálculo bayesiano amortecido e rate limiting; e a interface Web responsiva desenvolvida em "
        "React com TypeScript e Vite (totem-ui), implementando fluxo de anamnese guiada em 4 etapas, timeout de inatividade por "
        "privacidade e renderização das recomendações com explicabilidade. A validação técnica afere métricas de inércia, "
        "silhouette score e testes funcionais end-to-end de integração."
    )

    doc.add_page_break()

    # ==========================================
    # 8. SEÇÃO 4: CRONOGRAMA DE EXECUÇÃO
    # ==========================================
    add_p("4. CRONOGRAMA DE EXECUÇÃO", bold=True, first_indent=0, space_after=6)

    add_p(
        "O cronograma divide as etapas de pesquisa e desenvolvimento articuladas entre as disciplinas de TCC I e TCC II, "
        "assegurando a exequibilidade temporal da proposta perante os prazos regimentais do IFMA.",
        space_after=8
    )

    # Tabela do Cronograma
    table = doc.add_table(rows=10, cols=10)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    col_widths = [Cm(7.0)] + [Cm(1.0)] * 9
    col_widths_dxa = [4000] + [563] * 9

    tblPr = table._tbl.tblPr
    tblW = tblPr.find(qn('w:tblW'))
    if tblW is not None:
        tblPr.remove(tblW)
    tblPr.append(parse_xml(f'<w:tblW {nsdecls("w")} w:w="9067" w:type="dxa"/>'))

    grid = table._tbl.tblGrid
    grid.clear()
    for w_dxa in col_widths_dxa:
        grid.append(parse_xml(f'<w:gridCol {nsdecls("w")} w:w="{w_dxa}"/>'))

    for i, col in enumerate(table.columns):
        col.width = col_widths[i]

    headers = ["Atividade / Etapa", "Set/26", "Out/26", "Nov/26", "Dez/26", "Fev/27", "Mar/27", "Abr/27", "Mai/27", "Jun/27"]
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        hdr_cells[i].width = col_widths[i]
        set_cell_background(hdr_cells[i], "D9D9D9")
        set_cell_margins(hdr_cells[i], 20, 20, 30, 30)
        
        tcPr = hdr_cells[i]._tc.get_or_add_tcPr()
        old_tcW = tcPr.find(qn('w:tcW'))
        if old_tcW is not None:
            tcPr.remove(old_tcW)
        tcPr.append(parse_xml(f'<w:tcW {nsdecls("w")} w:w="{col_widths_dxa[i]}" w:type="dxa"/>'))

        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        p.runs[0].font.name = 'Times New Roman'
        p.runs[0].font.size = Pt(7.5)
        p.runs[0].bold = True

    schedule_data = [
        ("TCC I: Levantamento bibliográfico sistemático e Modelagem", ["X", "X", "", "", "", "", "", "", ""]),
        ("TCC I: Definição da taxonomia de domínio com o salão", ["", "X", "X", "", "", "", "", "", ""]),
        ("TCC I: Desenvolvimento do MVP Arquitetural (API + Web App)", ["", "", "X", "X", "", "", "", "", ""]),
        ("TCC I: Redação e entrega do Projeto de Monografia", ["", "", "", "X", "", "", "", "", ""]),
        ("TCC II: Geração e análise matemática de dados (Silhouette/Elbow)", ["", "", "", "", "X", "X", "", "", ""]),
        ("TCC II: Homologação em Staging com o Cliente (UAT)", ["", "", "", "", "", "X", "X", "", ""]),
        ("TCC II: Refatoração, Ajustes XAI e Deploy em Produção", ["", "", "", "", "", "", "X", "X", ""]),
        ("TCC II: Redação dos Capítulos de Resultados e Discussão", ["", "", "", "", "", "", "", "X", "X"]),
        ("TCC II: Defesa Final perante Banca Examinadora", ["", "", "", "", "", "", "", "", "X"]),
    ]

    for row_idx, (act, checks) in enumerate(schedule_data, start=1):
        row_cells = table.rows[row_idx].cells
        row_cells[0].text = act
        row_cells[0].width = col_widths[0]
        set_cell_margins(row_cells[0], 20, 20, 30, 30)
        
        tcPr = row_cells[0]._tc.get_or_add_tcPr()
        old_tcW = tcPr.find(qn('w:tcW'))
        if old_tcW is not None:
            tcPr.remove(old_tcW)
        tcPr.append(parse_xml(f'<w:tcW {nsdecls("w")} w:w="{col_widths_dxa[0]}" w:type="dxa"/>'))

        p = row_cells[0].paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        p.runs[0].font.name = 'Times New Roman'
        p.runs[0].font.size = Pt(7.5)
        p.runs[0].bold = True if "TCC II: Defesa" in act or "TCC I: Redação" in act else False
        
        for c_idx, val in enumerate(checks, start=1):
            row_cells[c_idx].text = val
            row_cells[c_idx].width = col_widths[c_idx]
            set_cell_margins(row_cells[c_idx], 20, 20, 15, 15)
            
            tcPr_c = row_cells[c_idx]._tc.get_or_add_tcPr()
            old_tcW_c = tcPr_c.find(qn('w:tcW'))
            if old_tcW_c is not None:
                tcPr_c.remove(old_tcW_c)
            tcPr_c.append(parse_xml(f'<w:tcW {nsdecls("w")} w:w="{col_widths_dxa[c_idx]}" w:type="dxa"/>'))

            p_val = row_cells[c_idx].paragraphs[0]
            p_val.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_val.paragraph_format.space_before = Pt(0)
            p_val.paragraph_format.space_after = Pt(0)
            p_val.paragraph_format.line_spacing = 1.0
            if len(p_val.runs) > 0:
                p_val.runs[0].font.name = 'Times New Roman'
                p_val.runs[0].font.size = Pt(7.5)
                p_val.runs[0].bold = True

    # Quebra de página para que Considerações Preliminares ocupe uma página exclusiva
    doc.add_page_break()

    # 5. CONSIDERAÇÕES PRELIMINARES
    add_p("5. CONSIDERAÇÕES PRELIMINARES", bold=True, first_indent=0, space_after=12)

    add_p(
        "A formulação deste Projeto de Monografia atesta a viabilidade técnico-científica do Vila Cachos AI como resposta "
        "robusta à variabilidade do diagnóstico capilar especializado e ao desafio do Cold Start em Sistemas de Recomendação. "
        "A modelagem híbrida concebida ancora-se em bases sólidas da Ciência da Computação e Engenharia de Software, aliando "
        "simplicidade operacional para a equipe do salão a garantias matemáticas de estabilidade e explicabilidade algorítmica. "
        "Os passos subsequentes, a serem formalizados na disciplina de TCC II, concentrar-se-ão no refinamento empírico da "
        "solução em ambiente real de salão e na quantificação estrita de seus impactos operacionais."
    )

    doc.add_page_break()

    # ==========================================
    # 9. REFERÊNCIAS
    # ==========================================
    add_p("REFERÊNCIAS", bold=True, first_indent=0, space_after=18)

    referencias = [
        "AGGARWAL, Charu C. Recommender Systems: The Textbook. 1. ed. Cham: Springer International Publishing, 2016.",
        "INSTITUTO FEDERAL DO MARANHÃO (IFMA). Resolução nº 088/2022. Aprova o Regulamento do Trabalho de Conclusão de Curso (TCC) dos Cursos de Graduação do IFMA. São Luís: Conselho Superior do IFMA, 2022.",
        "KAUFMAN, Leonard; ROUSSEEUW, Peter J. Finding Groups in Data: An Introduction to Cluster Analysis. New York: John Wiley & Sons, 1990.",
        "PRESSMAN, Roger S.; MAXIM, Bruce R. Engenharia de Software: Uma Abordagem Profissional. 9. ed. Porto Alegre: AMGH, 2021.",
        "RUSSELL, Stuart J.; NORVIG, Peter. Inteligência Artificial: Uma Abordagem Moderna. 4. ed. Rio de Janeiro: GEN LTC, 2022.",
        "SOMMERVILLE, Ian. Engenharia de Software. 10. ed. São Paulo: Pearson Education do Brasil, 2019.",
        "TAN, Pang-Ning; STEINBACH, Michael; KUMAR, Vipin. Introdução ao Data Mining - Mineração de Dados. 2. ed. Rio de Janeiro: Ciência Moderna, 2019."
    ]

    for ref in referencias:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.first_line_indent = Cm(0)
        p_ref.paragraph_format.space_before = Pt(0)
        p_ref.paragraph_format.space_after = Pt(8)
        p_ref.paragraph_format.line_spacing = 1.0
        
        # Format title in bold according to ABNT
        parts = ref.split(". ")
        # Author
        r_author = p_ref.add_run(parts[0] + ". ")
        r_author.font.name = 'Times New Roman'
        r_author.font.size = Pt(12)
        
        # Title (in bold)
        if len(parts) > 1:
            r_title = p_ref.add_run(parts[1] + ". ")
            r_title.font.name = 'Times New Roman'
            r_title.font.size = Pt(12)
            r_title.bold = True
        
        # Rest of citation
        if len(parts) > 2:
            r_rest = p_ref.add_run(". ".join(parts[2:]))
            r_rest.font.name = 'Times New Roman'
            r_rest.font.size = Pt(12)

    doc.add_page_break()

    # ==========================================
    # 10. ANEXO 1: FICHA DE ACEITE
    # ==========================================
    add_p("ANEXO 1: FICHA DE ACEITE DE ORIENTAÇÃO DE TCC", bold=True, first_indent=0, space_after=18)

    add_p(
        "Declaro para os devidos fins de registro acadêmico junto à Coordenação do Curso de Bacharelado em Sistemas de Informação "
        "do Instituto Federal do Maranhão (IFMA) - Campus São Luís Monte Castelo, que aceito orientar o discente MARCOS VINÍCIUS "
        "no desenvolvimento do Trabalho de Conclusão de Curso intitulado:\n"
        "\"VILA CACHOS AI: SISTEMA HÍBRIDO DE RECOMENDAÇÃO CAPILAR COM APRENDIZADO NÃO SUPERVISIONADO E INFERÊNCIA BAYESIANA: Um Web App de Diagnóstico Integrado para o Salão Vila Cachos\".",
        space_after=24
    )

    add_blank(4)

    p_sig1 = add_p("____________________________________________________", align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, space_after=2)
    p_sig1.runs[0].bold = True
    add_p("Prof. Me. Alex Martins Pereira\nOrientador", align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, space_after=18, bold=True)

    add_blank(2)

    p_sig2 = add_p("____________________________________________________", align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, space_after=2)
    p_sig2.runs[0].bold = True
    add_p("Profa. Me. Eveline de Jesus Viana Silva\nCoorientadora", align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, space_after=18, bold=True)

    add_blank(2)

    add_p("São Luís - MA, ____ de ___________________ de 2026.", align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, space_after=0)

    # Save document
    doc.save(DOCX_PATH)
    print(f"Document successfully created and saved to {DOCX_PATH}")

    # Convert to PDF via LibreOffice
    soffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"
    out_dir = os.path.dirname(DOCX_PATH)
    cmd = [soffice_path, "--headless", "--convert-to", "pdf", DOCX_PATH, "--outdir", out_dir]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("LibreOffice PDF export result:", res.returncode, res.stdout)

    # Sync with Seminario1_Texto_MarcosVinicius.pdf
    pdf_generated = os.path.join(out_dir, "Modelo_Projeto_TCC.pdf")
    pdf_seminario = os.path.join(out_dir, "Seminario1_Texto_MarcosVinicius.pdf")
    if os.path.exists(pdf_generated):
        shutil.copyfile(pdf_generated, pdf_seminario)
        print(f"Synced successfully with {pdf_seminario}")

if __name__ == "__main__":
    create_document()
