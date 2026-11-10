"""
scripts/gerar_documentacao_analise_2_pdf.py
Compila toda a documentação da disciplina de Análise e Projeto de Sistemas II (IFMA)
em um único documento PDF executivo, incorporando os diagramas de sequência draw.io.
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from pypdf import PdfReader, PdfWriter

import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
DIAGRAMS_DIR = os.path.join(BASE_DIR, "diagramas")
IFMA_DIR = os.path.join(BASE_DIR, "faculdade_ifma", "analise_e_projeto_sistemas_2", "avaliacao_1")

TEMP_TEXT_PDF = os.path.join(DOCS_DIR, "_temp_doc_analise_2.pdf")
SEQ_PDF = os.path.join(DIAGRAMS_DIR, "diagramas_sequencia_drawio_completo.pdf")
OUTPUT_PDF = os.path.join(DOCS_DIR, "DOCUMENTACAO_COMPLETA_AVALIACAO_1_ANALISE_II.pdf")
OUTPUT_IFMA_PDF = os.path.join(IFMA_DIR, "DOCUMENTACAO_COMPLETA_AVALIACAO_1_ANALISE_II.pdf")


class NumberedCanvas(canvas.Canvas):
    """Canvas customizado para numeração de páginas 'Página X de Y' e cabeçalho sutil."""
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
            return  # Capa limpa sem cabeçalho/rodapé
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        # Cabeçalho
        self.drawString(54, 800, "Vila Cachos AI — Documentação Integrada de Software (Análise II)")
        self.setStrokeColor(colors.HexColor("#CCCCCC"))
        self.setLineWidth(0.5)
        self.line(54, 792, 541, 792)
        # Rodapé
        self.line(54, 45, 541, 45)
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(541, 32, page_str)
        self.drawString(54, 32, "Equipe: Marcos Vinícius, Jordan, Rafael | Docente: Profª. Eveline Viana")
        self.restoreState()


def build_text_pdf():
    doc = SimpleDocTemplate(
        TEMP_TEXT_PDF,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Estilos customizados
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#1b4332"),
        alignment=1, # Centro
        spaceAfter=15
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#2d6a4f"),
        alignment=1,
        spaceAfter=25
    )

    meta_style = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#333333"),
        alignment=1
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#1b4332"),
        spaceBefore=18,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#2d6a4f"),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'Heading3_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#40916c"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#222222"),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )

    box_style = ParagraphStyle(
        'BoxText',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#1a1a1a")
    )

    # Estilos específicos para tabelas profissionais sem overflow e com excelente legibilidade
    th_style = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.whitesmoke
    )
    th_center = ParagraphStyle(
        'THCenter',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.whitesmoke,
        alignment=1
    )
    td_style = ParagraphStyle(
        'TD',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=10.5,
        textColor=colors.HexColor("#222222")
    )
    td_bold = ParagraphStyle(
        'TDBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=10.5,
        textColor=colors.HexColor("#222222")
    )
    td_center = ParagraphStyle(
        'TDCenter',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=10.5,
        textColor=colors.HexColor("#222222"),
        alignment=1
    )
    td_bold_center = ParagraphStyle(
        'TDBoldCenter',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=10.5,
        textColor=colors.HexColor("#222222"),
        alignment=1
    )
    td_code = ParagraphStyle(
        'TDCode',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.0,
        leading=10.2,
        textColor=colors.HexColor("#1a1a1a")
    )

    story = []

    # ==========================================
    # CAPA INSTITUCIONAL
    # ==========================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DO MARANHÃO", ParagraphStyle('Inst', alignment=1, fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=colors.HexColor("#333333"))))
    story.append(Paragraph("DEPARTAMENTO DE COMPUTAÇÃO — CURSO DE SISTEMAS DE INFORMAÇÃO", ParagraphStyle('Dept', alignment=1, fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor("#555555"))))
    story.append(Paragraph("DISCIPLINA: ANÁLISE E PROJETO DE SISTEMAS II — 2026.2", ParagraphStyle('Disc', alignment=1, fontName='Helvetica-Bold', fontSize=9, leading=13, textColor=colors.HexColor("#555555"))))
    story.append(Spacer(1, 80))

    story.append(Paragraph("DOCUMENTAÇÃO COMPLETA DE ENGENHARIA DE SOFTWARE", title_style))
    story.append(Paragraph("Compilado Oficial de Artefatos para a Avaliação 1 (Requisitos, Casos de Uso, Classes/Métodos e Sequência)", subtitle_style))
    story.append(HRFlowable(width="60%", thickness=1.5, color=colors.HexColor("#2d6a4f"), spaceAfter=30))

    story.append(Paragraph("<b>SISTEMA:</b> Vila Cachos AI — Totem Especialista de Diagnóstico Capilar & Recomendação Híbrida", meta_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>DOCENTE RESPONSÁVEL:</b> Profª. Eveline de Jesus Viana Sá", meta_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>EQUIPE DE DESENVOLVIMENTO:</b><br/>Marcos Vinícius (Gerente / Arquitetura)<br/>Jordan<br/>Rafael", meta_style))
    story.append(Spacer(1, 80))
    story.append(Paragraph("São Luís — MA<br/>Outubro de 2026", meta_style))
    story.append(PageBreak())

    # ==========================================
    # SUMÁRIO E ALINHAMENTO COM O CRONOGRAMA
    # ==========================================
    story.append(Paragraph("1. Alinhamento com o Cronograma da Disciplina", h1_style))
    story.append(Paragraph(
        "Este documento consolida 100% dos artefatos de modelagem produzidos ao longo das entregas parciais solicitadas pela Profª. Eveline de Jesus Viana Sá para a <b>Avaliação 1</b> da disciplina de Análise e Projeto de Sistemas II:",
        body_style
    ))

    cronograma_rows = [
        [
            Paragraph("Data Cobrada", th_center),
            Paragraph("Artefato Exigido no Cronograma", th_style),
            Paragraph("Capítulo Correspondente neste Documento", th_style),
            Paragraph("Status", th_center)
        ],
        [
            Paragraph("24/Setembro", td_center),
            Paragraph("Doc de Requisitos e Diagrama de Casos de Uso", td_style),
            Paragraph("Capítulo 2 (Requisitos) e Capítulo 3 (Casos de Uso)", td_style),
            Paragraph("<font color='#1b4332'><b>Concluído</b></font>", td_center)
        ],
        [
            Paragraph("01/Outubro", td_center),
            Paragraph("Diagrama de Classes (e Métodos)", td_style),
            Paragraph("Capítulo 4 (Diagrama de Classes &amp; Dicionário)", td_style),
            Paragraph("<font color='#1b4332'><b>Concluído</b></font>", td_center)
        ],
        [
            Paragraph("20/Outubro", td_center),
            Paragraph("Diagramas de Sequência", td_style),
            Paragraph("Capítulo 5 (6 Diagramas de Sequência Completos)", td_style),
            Paragraph("<font color='#1b4332'><b>Concluído</b></font>", td_center)
        ],
        [
            Paragraph("28/Outubro", td_center),
            Paragraph("AVALIAÇÃO 1 — Entrega e Apresentação", td_bold),
            Paragraph("Compilado Completo Unificado + Roteiro de Fala", td_style),
            Paragraph("<font color='#1b4332'><b>Pronto</b></font>", td_center)
        ]
    ]
    t_crono = Table(cronograma_rows, colWidths=[65, 175, 185, 60])
    t_crono.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1b4332")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CCCCCC")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F9FBF9")]),
    ]))
    story.append(t_crono)
    story.append(Spacer(1, 10))

    # Nota sobre "Diagrama de Método"
    story.append(Paragraph("<b>Nota Técnica sobre 'Diagrama de Método':</b> Na notação formal da UML (OMG), não existe uma categoria isolada denominada 'diagrama de método'. No escopo didático da disciplina, a exigência refere-se a: (a) A declaração formal da assinatura dos métodos (visibilidade, parâmetros e tipos de retorno) dentro do <b>Diagrama de Classes</b>; e (b) A representação comportamental das invocações de métodos e chamadas de API ao longo do tempo dentro dos <b>Diagramas de Sequência</b>. Ambos estão rigorosamente cobertos nos Capítulos 4 e 5.", ParagraphStyle('Note', parent=body_style, fontName='Helvetica-Oblique', backColor=colors.HexColor("#f0fdf4"), borderPadding=8, spaceBefore=6)))

    story.append(Spacer(1, 12))

    # ==========================================
    # CAPÍTULO 2: DOCUMENTO DE REQUISITOS
    # ==========================================
    story.append(Paragraph("2. Documento de Requisitos de Software", h1_style))
    story.append(Paragraph("<b>2.1 Atores do Sistema</b>", h2_style))
    story.append(Paragraph("• <b>Cliente do Salão (Ator Primário):</b> Usuária que acessa o Totem touch-screen ou Web App, insere seus dados capilares, consulta recomendações explicadas e avalia os produtos utilizados.", bullet_style))
    story.append(Paragraph("• <b>Profissional / Terapeuta Capilar (Ator Secundário):</b> Cabeleireira que auxilia a cliente na validação das variáveis e consulta composições no catálogo.", bullet_style))
    story.append(Paragraph("• <b>Gestor do Salão (Ator Administrativo):</b> Responsável por monitorar as métricas de clusterização da IA, volume de feedbacks e conformidade do catálogo.", bullet_style))
    story.append(Paragraph("• <b>Motor de IA / Recommender API (Ator de Sistema):</b> Serviço autônomo FastAPI que executa o pipeline K-Means, filtros de conhecimento tricológico, inferência YOLO e média bayesiana.", bullet_style))

    story.append(Spacer(1, 6))
    story.append(PageBreak())
    story.append(Paragraph("<b>2.2 Requisitos Funcionais (RF)</b>", h2_style))

    rfs_raw = [
        ["RF-01", "Permitir ao cliente selecionar a curvatura dos fios (2-Ondulado, 3-Cacheado, 4-Crespo).", "Alta"],
        ["RF-02", "Permitir ao cliente informar o nível de porosidade aparente (Baixa, Média, Alta).", "Alta"],
        ["RF-03", "Permitir ao cliente assinalar presença de danos químicos e queixas específicas.", "Alta"],
        ["RF-04", "Normalizar as 8 variáveis da anamnese e classificar a cliente em um Cluster K-Means.", "Alta"],
        ["RF-05", "Calcular pontuação terapêutica baseada em conhecimento clínico (Knowledge-Based).", "Alta"],
        ["RF-06", "Calcular a Média Bayesiana Amortecida por cluster para superar o Cold Start.", "Alta"],
        ["RF-07", "Aplicar ponderação convexa dinâmica entre Conhecimento Especialista e Feedback.", "Alta"],
        ["RF-08", "Gerar o Top 3 cosméticos recomendados com estimativa de estrelas (1.0 a 5.0).", "Alta"],
        ["RF-09", "Apresentar justificativa clínica explicável (XAI - Explainable AI) em linguagem natural.", "Alta"],
        ["RF-10", "Permitir à cliente registrar nota de satisfação (1 a 5 estrelas) pós-atendimento.", "Média"],
        ["RF-11", "Recalibrar os pesos do cluster dinamicamente no momento do registro do feedback.", "Média"],
        ["RF-12", "Permitir o upload de foto da mecha para inferência via Visão Computacional (YOLO).", "Média"],
        ["RF-13", "Identificar e alertar quando a imagem enviada não possuir cabelo ou mechas visíveis.", "Média"],
        ["RF-14", "Permitir a consulta completa do catálogo oficial de cosméticos com filtros.", "Média"],
        ["RF-15", "Disponibilizar endpoint de monitoramento de integridade e métricas de IA (/health).", "Média"]
    ]
    rfs_rows = [
        [
            Paragraph("Código", th_center),
            Paragraph("Descrição do Requisito Funcional", th_style),
            Paragraph("Prioridade", th_center)
        ]
    ]
    for code, desc, prio in rfs_raw:
        rfs_rows.append([
            Paragraph(f"<b>{code}</b>", td_center),
            Paragraph(desc, td_style),
            Paragraph(f"<font color='{'#1b4332' if prio == 'Alta' else '#555555'}'><b>{prio}</b></font>", td_center)
        ])
    t_rfs = Table(rfs_rows, colWidths=[50, 375, 60])
    t_rfs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2d6a4f")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CCCCCC")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F9FBF9")]),
    ]))
    story.append(t_rfs)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>2.3 Requisitos Não Funcionais (RNF)</b>", h2_style))
    story.append(Paragraph("• <b>RNF-01 (Desempenho):</b> A inferência da recomendação deve retornar com latência inferior a 1,5 segundos (mediana local: ~30ms).", bullet_style))
    story.append(Paragraph("• <b>RNF-02 (Rate Limiting):</b> Proteção contra abusos e DoS aplicando limite estrito de 10 req/min nas rotas de recomendação e 20 req/min na visão computacional.", bullet_style))
    story.append(Paragraph("• <b>RNF-03 (Timeout de Sessão):</b> O Totem público encerra e reinicia a sessão automaticamente após 15 minutos de inatividade, preservando a privacidade.", bullet_style))
    story.append(Paragraph("• <b>RNF-04 (Segurança OWASP):</b> Cabeçalhos de segurança obrigatórios (nosniff, DENY, XSS-Protection), sanitização contra CSV Formula Injection e validação de Magic Bytes.", bullet_style))
    story.append(Paragraph("• <b>RNF-05 (Concorrência):</b> Bloqueio atômico com threading.Lock na persistência em disco para evitar race conditions em acessos simultâneos.", bullet_style))
    story.append(Paragraph("• <b>RNF-06 (Portabilidade e Responsividade):</b> Interface construída em React/TanStack Start, responsiva para totens touch-screen (1080x1920) e smartphones.", bullet_style))

    story.append(PageBreak())

    # ==========================================
    # CAPÍTULO 3: CASOS DE USO (UML)
    # ==========================================
    story.append(Paragraph("3. Modelagem e Especificação de Casos de Uso (UML)", h1_style))
    story.append(Paragraph("<b>3.1 Mapeamento e Relações entre Casos de Uso</b>", h2_style))
    story.append(Paragraph(
        "A fronteira do sistema engloba 7 Casos de Uso estruturados que garantem a jornada completa da cliente, desde a anamnese até o loop de feedback contínuo:",
        body_style
    ))

    uc_raw = [
        ["UC-01", "Realizar Anamnese Capilar", "Cliente do Salão, Profissional", "&lt;&lt;include&gt;&gt; UC-02"],
        ["UC-02", "Gerar Diagnóstico e Recomendação", "Motor de IA (FastAPI)", "Incluso por UC-01"],
        ["UC-03", "Visualizar Top 3 Produtos e XAI", "Cliente do Salão, Profissional", "Estendido por UC-04"],
        ["UC-04", "Registrar Avaliação (Feedback Loop)", "Cliente do Salão", "&lt;&lt;include&gt;&gt; UC-05"],
        ["UC-05", "Recalibrar Média Bayesiana do Cluster", "Motor de IA (FastAPI)", "Incluso por UC-04"],
        ["UC-06", "Consultar Catálogo Oficial", "Cliente, Profissional, Gestor", "Caso Independente"],
        ["UC-07", "Monitorar Saúde e Métricas de IA", "Gestor do Salão, Motor de IA", "Caso Independente"]
    ]
    uc_rows = [
        [
            Paragraph("Identificador", th_center),
            Paragraph("Nome do Caso de Uso", th_style),
            Paragraph("Atores Envolvidos", th_style),
            Paragraph("Relações UML", th_center)
        ]
    ]
    for uid, name, actors, rel in uc_raw:
        uc_rows.append([
            Paragraph(f"<b>{uid}</b>", td_center),
            Paragraph(name, td_style),
            Paragraph(actors, td_style),
            Paragraph(f"<i>{rel}</i>", td_center)
        ])
    t_uc = Table(uc_rows, colWidths=[65, 160, 160, 100])
    t_uc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1b4332")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CCCCCC")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F9FBF9")]),
    ]))
    story.append(t_uc)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>3.2 Especificação Formal: UC-01 / UC-02 (Diagnóstico e Recomendação)</b>", h2_style))
    story.append(Paragraph("• <b>Atores:</b> Cliente do Salão (Primário) e Motor de IA (Secundário).", bullet_style))
    story.append(Paragraph("• <b>Pré-condições:</b> Totem operacional, motor K-Means ajustado (is_fitted=True) e catálogo oficial carregado.", bullet_style))
    story.append(Paragraph("• <b>Fluxo Principal (Happy Path):</b>", bullet_style))
    story.append(Paragraph("   1. Cliente inicia a anamnese no Totem tocando em 'Iniciar Diagnóstico'.", bullet_style))
    story.append(Paragraph("   2. Interface apresenta o Wizard coletando: Curvatura (2, 3 ou 4), Porosidade (1, 2 ou 3), Química (0 ou 1) e Queixas.", bullet_style))
    story.append(Paragraph("   3. Opcionalmente, a cliente envia foto da mecha para inferência YOLO de curvatura e frizz.", bullet_style))
    story.append(Paragraph("   4. Cliente submete o formulário. Interface dispara POST /recommend com o payload ClienteProfile.", bullet_style))
    story.append(Paragraph("   5. Motor normaliza o vetor com StandardScaler e infere o Cluster K-Means da cliente.", bullet_style))
    story.append(Paragraph("   6. Motor calcula afinidade de conteúdo (Knowledge-Based) e média bayesiana histórica do cluster.", bullet_style))
    story.append(Paragraph("   7. Motor aplica combinação convexa ponderada, ranqueia os cosméticos e monta justificativa XAI.", bullet_style))
    story.append(Paragraph("   8. API responde HTTP 200 OK com o Top 3 produtos, pontuações e explicação tricológica.", bullet_style))
    story.append(Paragraph("   9. Totem exibe os produtos recomendados com destaque visual ao match principal.", bullet_style))
    story.append(Paragraph("• <b>Fluxos de Exceção:</b>", bullet_style))
    story.append(Paragraph("   - <i>FE-01 (Timeout):</i> 15 minutos sem interação reinicia o Totem na tela inicial por segurança.", bullet_style))
    story.append(Paragraph("   - <i>FE-02 (Rate Limit):</i> Mais de 10 req/min por IP aciona HTTP 429 Too Many Requests.", bullet_style))
    story.append(Paragraph("   - <i>FE-03 (Imagem Sem Mechas):</i> Se o upload for de superfície lisa ou anúncio, a IA retorna HTTP 200 com flag cabelo_detectado=false e aviso explicativo sem travar o totem.", bullet_style))

    story.append(PageBreak())

    # ==========================================
    # CAPÍTULO 4: DIAGRAMA DE CLASSES E MÉTODOS
    # ==========================================
    story.append(Paragraph("4. Diagrama de Classes e Dicionário de Métodos (UML)", h1_style))
    story.append(Paragraph(
        "O Diagrama de Classes modela a estrutura estática orientada a objetos do sistema, aplicando os princípios de <b>Clean Architecture</b> e <b>Inversão de Dependência (DIP)</b>. Abaixo detalhamos as classes centrais, seus atributos e as assinaturas completas de seus métodos:",
        body_style
    ))

    # Tabela com classes e métodos detalhados (formatada com Paragraphs para impedir qualquer sobreposição)
    classes_rows = [
        [
            Paragraph("Classe", th_style),
            Paragraph("Responsabilidade", th_style),
            Paragraph("Atributos Principais", th_style),
            Paragraph("Métodos Principais (Assinatura e Retorno)", th_style)
        ],
        [
            Paragraph("<b>ClienteProfile</b><br/><font color='#2d6a4f'><i>&lt;&lt;Pydantic&gt;&gt;</i></font>", td_style),
            Paragraph("Contrato de validação dos dados de entrada da anamnese.", td_style),
            Paragraph("<b>+curvatura:</b> int<br/><b>+porosidade:</b> int<br/><b>+dano_quimico:</b> int<br/><b>+queixas:</b> int[5]", td_code),
            Paragraph("<b>+to_dict()</b> -&gt; Dict[str, Any]<br/><font color='#555555'>Valida tipos e intervalos estritos (Literal).</font>", td_code)
        ],
        [
            Paragraph("<b>FeedbackInput</b><br/><font color='#2d6a4f'><i>&lt;&lt;Pydantic&gt;&gt;</i></font>", td_style),
            Paragraph("Contrato de entrada para registro de notas da cliente.", td_style),
            Paragraph("<b>+ perfil:</b> ClienteProfile<br/><b>+ nome_produto:</b> str<br/><b>+ nota_satisfacao:</b> int", td_code),
            Paragraph("<b>+ model_validate()</b> -&gt; Self<br/><font color='#555555'>Valida se nota está entre 1 e 5 e bounds.</font>", td_code)
        ],
        [
            Paragraph("<b>VilaCachosRecommender</b><br/><font color='#2d6a4f'><i>&lt;&lt;Service / Engine&gt;&gt;</i></font>", td_style),
            Paragraph("Núcleo analítico da IA. Executa K-Means, filtros e média bayesiana.", td_style),
            Paragraph("<b>- n_clusters:</b> int<br/><b>- kmeans:</b> KMeans<br/><b>- scaler:</b> StandardScaler<br/><b>- df_historico:</b> DataFrame", td_code),
            Paragraph("<b>+ fit</b>(df_historico) -&gt; Self<br/><b>+ prever_cluster</b>(perfil) -&gt; int<br/><b>+ recomendar</b>(perfil, top_k) -&gt; Dict<br/><b>+ registrar_feedback</b>(perfil, prod, nota)<br/><b>+ avaliar_qualidade_clusters</b>() -&gt; Dict", td_code)
        ],
        [
            Paragraph("<b>FeedbackRepository</b><br/><font color='#2d6a4f'><i>&lt;&lt;Interface / DIP&gt;&gt;</i></font>", td_style),
            Paragraph("Abstração de persistência desacoplada da camada web.", td_style),
            Paragraph("<i>(Interface Abstrata)</i>", td_style),
            Paragraph("<b>+ obter_historico</b>() -&gt; DataFrame<br/><b>+ salvar_feedback</b>(perfil, prod, nota, cluster)<br/><b>+ obter_total_avaliacoes</b>() -&gt; int<br/><b>+ obter_media_global</b>() -&gt; float", td_code)
        ],
        [
            Paragraph("<b>CsvFeedbackRepository</b><br/><font color='#2d6a4f'><i>&lt;&lt;Repository / Concrete&gt;&gt;</i></font>", td_style),
            Paragraph("Implementação concreta thread-safe em arquivo CSV.", td_style),
            Paragraph("<b>- csv_path:</b> str<br/><b>- _lock:</b> Lock<br/><b>- _df_cache:</b> DataFrame", td_code),
            Paragraph("<b>+ _carregar_ou_inicializar</b>() -&gt; void<br/><b>+ obter_historico</b>() -&gt; DataFrame (Thread-safe)<br/><b>+ salvar_feedback</b>(...) -&gt; void (Sanitiza CSV)", td_code)
        ],
        [
            Paragraph("<b>YoloHairClassifier</b><br/><font color='#2d6a4f'><i>&lt;&lt;Vision Engine&gt;&gt;</i></font>", td_style),
            Paragraph("Inferência neural e morfológica de curvatura e mechas.", td_style),
            Paragraph("<b>- yolo_model:</b> YOLO<br/><b>- CONF_THRESHOLD:</b> float", td_code),
            Paragraph("<b>+ predict_image_bytes</b>(bytes, file) -&gt; Dict<br/><b>+ _extrair_metricas_morfologicas</b>(img) -&gt; Dict<br/><b>+ _verificar_presenca_mechas</b>(m) -&gt; Tuple", td_code)
        ]
    ]

    t_classes = Table(classes_rows, colWidths=[112, 108, 105, 160])
    t_classes.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1b4332")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CCCCCC")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F9FBF9")]),
    ]))
    story.append(t_classes)
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Dicionário de Métodos Críticos do Motor de IA:</b>", h2_style))
    story.append(Paragraph("• <code>recomendar(perfil_cliente: Dict, top_k: int = 3) -> Dict</code>: Executa a predição do cluster via K-Means, calcula a afinidade de regras tricológicas (Knowledge-Based) e a Média Bayesiana Amortecida dos produtos no cluster. Retorna a lista ranqueada com explicabilidade semântica (XAI).", bullet_style))
    story.append(Paragraph("• <code>registrar_feedback(perfil_cliente: Dict, nome_produto: str, nota: int) -> None</code>: Atualiza os pesos e notas do cluster em tempo real na memória do motor, recalibrando a média bayesiana para clientes futuras.", bullet_style))
    story.append(Paragraph("• <code>_verificar_presenca_mechas(metricas: Dict) -> Tuple[bool, Optional[str]]</code>: Avalia se a imagem possui textura e cores biológicas compatíveis com mechas capilares humanas, rejeitando fotografias lisas/carecas e banners publicitários.", bullet_style))

    story.append(PageBreak())

    # ==========================================
    # CAPÍTULO 5: INTRODUÇÃO AOS DIAGRAMAS DE SEQUÊNCIA
    # ==========================================
    story.append(Paragraph("5. Diagramas de Sequência UML (Comportamento Dinâmico)", h1_style))
    story.append(Paragraph(
        "Os Diagramas de Sequência modelam as trocas de mensagens e invocações de métodos ao longo do tempo para cada um dos casos de uso críticos do sistema. Todos foram concebidos sob o padrão <b>Boundary-Controller-Entity (BCE)</b>:",
        body_style
    ))
    story.append(Paragraph("• <b>Atores Humanos:</b> <code>Cliente do Salão</code> e <code>Gestor do Salão</code>.", bullet_style))
    story.append(Paragraph("• <b>Boundary (Fronteira):</b> <code>Interface Web / Totem</code> (React / TanStack Router).", bullet_style))
    story.append(Paragraph("• <b>Controller (Controlador):</b> <code>RecommenderAPI</code> (FastAPI com SlowAPI Rate Limiting e Pydantic).", bullet_style))
    story.append(Paragraph("• <b>Domain / Service:</b> <code>VilaCachosRecommender</code> (Algoritmo K-Means, Scoring e XAI).", bullet_style))
    story.append(Paragraph("• <b>Entity / Persistence:</b> <code>ProdutoCatalogo</code> e <code>RegistroHistorico (CSV Repository)</code>.", bullet_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Mapeamento das 6 Páginas de Diagramas em Anexo:</b>", h2_style))

    seq_rows = [
        [
            Paragraph("Página", th_center),
            Paragraph("Caso de Uso Modelado", th_style),
            Paragraph("Fluxos Especiais &amp; Operadores UML", th_style),
            Paragraph("Métodos e Códigos HTTP", th_style)
        ],
        [
            Paragraph("Pág. 1", td_bold_center),
            Paragraph("<b>UC-02:</b> Preencher Anamnese Capilar", td_style),
            Paragraph("Navegação não-destrutiva (opt), Timeout 15min (opt)", td_style),
            Paragraph("<b>setStep()</b>, <b>reset()</b>, <b>validate()</b>", td_code)
        ],
        [
            Paragraph("Pág. 2", td_bold_center),
            Paragraph("<b>UC-03:</b> Gerar Recomendação Híbrida", td_style),
            Paragraph("Rate Limit (alt), Cold Start (loop nos produtos)", td_style),
            Paragraph("<b>POST /recommend</b>, <b>fit()</b>, <b>predict()</b><br/><font color='#2d6a4f'><b>[200 / 422 / 429]</b></font>", td_code)
        ],
        [
            Paragraph("Pág. 3", td_bold_center),
            Paragraph("<b>UC-04:</b> Visualizar Diagnóstico e XAI", td_style),
            Paragraph("Fallback de visualização (alt), Badges de XAI", td_style),
            Paragraph("<b>render(Top3)</b>, <b>calcularPorcentagemPesos()</b>", td_code)
        ],
        [
            Paragraph("Pág. 4", td_bold_center),
            Paragraph("<b>UC-05:</b> Registrar Feedback de Produto", td_style),
            Paragraph("Validação de Catálogo (alt), Recalibração dinâmica", td_style),
            Paragraph("<b>POST /feedback</b>, <b>salvar_feedback()</b><br/><font color='#2d6a4f'><b>[200 / 400 / 429]</b></font>", td_code)
        ],
        [
            Paragraph("Pág. 5", td_bold_center),
            Paragraph("<b>UC-06:</b> Consultar Catálogo Oficial", td_style),
            Paragraph("Consulta de produtos, composições e ativos", td_style),
            Paragraph("<b>GET /catalogo</b> <font color='#2d6a4f'><b>[200 OK]</b></font>", td_code)
        ],
        [
            Paragraph("Pág. 6", td_bold_center),
            Paragraph("<b>UC-07:</b> Monitorar Saúde e Métricas", td_style),
            Paragraph("Auditoria de Silhouette Score e Inércia do K-Means", td_style),
            Paragraph("<b>GET /health</b>, <b>avaliar_qualidade_clusters()</b><br/><font color='#2d6a4f'><b>[200 OK]</b></font>", td_code)
        ]
    ]
    t_seq = Table(seq_rows, colWidths=[42, 128, 165, 150])
    t_seq.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2d6a4f")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CCCCCC")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F9FBF9")]),
    ]))
    story.append(t_seq)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<i>As páginas seguintes contêm a renderização gráfica vetorial oficial completa de cada um dos 6 diagramas de sequência, gerados a partir do arquivo 'diagramas/sequencias.drawio'.</i>", ParagraphStyle('NoteSeq', parent=body_style, fontName='Helvetica-Oblique', alignment=1)))

    # Constrói o PDF de texto base
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] PDF textual base gerado com sucesso em: {TEMP_TEXT_PDF}")


def merge_final_pdf():
    """Mescla o PDF de documentação textual com as 6 páginas vetoriais dos diagramas draw.io."""
    writer = PdfWriter()

    # 1. Lê o documento textual
    reader_text = PdfReader(TEMP_TEXT_PDF)
    for page in reader_text.pages:
        writer.add_page(page)

    # 2. Anexa as 6 páginas dos diagramas de sequência do draw.io
    if os.path.exists(SEQ_PDF):
        reader_seq = PdfReader(SEQ_PDF)
        print(f"[+] Anexando {len(reader_seq.pages)} páginas vetoriais do draw.io ({SEQ_PDF})...")
        for page in reader_seq.pages:
            writer.add_page(page)
    else:
        print(f"[!] Aviso: {SEQ_PDF} não encontrado!")

    # 3. Salva o PDF final unificado em docs/ e sincroniza com faculdade_ifma/
    with open(OUTPUT_PDF, "wb") as f_out:
        writer.write(f_out)

    os.makedirs(os.path.dirname(OUTPUT_IFMA_PDF), exist_ok=True)
    shutil.copyfile(OUTPUT_PDF, OUTPUT_IFMA_PDF)

    print(f"[SUCCESS] PDF COMPLETO UNIFICADO GERADO EM: {OUTPUT_PDF}")
    print(f"[SUCCESS] PDF SINCRONIZADO COM ÁRVORE ACADÊMICA: {OUTPUT_IFMA_PDF}")

    # Remove temporário se desejado
    if os.path.exists(TEMP_TEXT_PDF):
        os.remove(TEMP_TEXT_PDF)


if __name__ == "__main__":
    build_text_pdf()
    merge_final_pdf()
