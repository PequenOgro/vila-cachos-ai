# -*- coding: utf-8 -*-
"""
scripts/gerar_audio_pitch.py
Gera áudios de alta fidelidade em português brasileiro (.wav) para cada slide
e a apresentação completa contínua de 5 minutos do Seminário 1 (TCC Vila Cachos AI).
Utiliza a voz natural OneCore da Microsoft (Daniel).
"""

import os
import subprocess
import wave

AUDIO_DIR = os.path.abspath(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "faculdade_ifma",
    "tcc_1_monografia",
    "seminario_apresentacao",
    "audios_pitch"
))

# Textos exatos para pronúncia fluida e natural no sintetizador
SLIDES_TEXTO = [
    {
        "id": "slide_01_capa",
        "titulo": "Slide 1: Capa e Abertura",
        "tempo": "0:00 - 0:25",
        "texto": (
            "Bom dia a todos os professores da banca, orientador, coorientador e colegas. "
            "Meu nome é Marcos Vinícius e apresento hoje o projeto do meu Trabalho de Conclusão de Curso: "
            "Vila Cachos AI: Sistema Especialista de Recomendação Capilar com Visão Computacional e Fusão Multimodal. "
            "Um projeto desenvolvido no curso de Sistemas de Informação do IFMA, sob orientação do professor Doutor Luís Carlos e coorientação do professor Mestre Daniel."
        )
    },
    {
        "id": "slide_02_contexto_dor",
        "titulo": "Slide 2: Contexto e a Dor Real no Salão",
        "tempo": "0:25 - 1:00",
        "texto": (
            "Passando ao contexto, a nossa pesquisa nasceu dentro do salão especializado Vila Cachos, aqui em São Luís. "
            "O mercado de cabelos cacheados e crespos está em forte expansão, mas a indicação cosmética ainda é um grande desafio. "
            "No salão, identificamos quatro dores críticas: primeiro, a subjetividade na avaliação empírica das cabeleireiras; "
            "segundo, o turnover, onde a troca de profissionais quebra o padrão de atendimento; "
            "terceiro, a barreira do Cold Start, pois clientes novas chegam sem nenhum histórico de compras; "
            "e quarto, a ausência de métricas analíticas sobre os perfis atendidos."
        )
    },
    {
        "id": "slide_03_pergunta_hipotese",
        "titulo": "Slide 3: Pergunta Problema e Hipótese",
        "tempo": "1:00 - 1:35",
        "texto": (
            "Diante desse cenário, formulamos a nossa pergunta norteadora: "
            "Como uma arquitetura híbrida de inteligência artificial leve pode mitigar o Cold Start e padronizar o diagnóstico cosmético em um salão especializado, operando via Web App escalável? "
            "A nossa hipótese é que a união de regras clínicas com agrupamento K-Means e regularização bayesiana permite recomendações personalizadas, padronizadas e explicáveis logo no primeiro contato da cliente, "
            "estabilizando os rankings de produtos mesmo com um banco de dados inicial pequeno."
        )
    },
    {
        "id": "slide_04_justificativa",
        "titulo": "Slide 4: Justificativa e Decisões de Projeto",
        "tempo": "1:35 - 2:05",
        "texto": (
            "A justificativa do projeto se apoia em três pilares: "
            "Cientificamente, aplicamos inteligência artificial híbrida em cenários de extrema esparseza de dados, unindo Média Bayesiana e Explicabilidade em IA. "
            "Socialmente, valorizamos a estética afro e cacheada e empoderamos a microempresa maranhense com padronização técnica. "
            "E como decisão de engenharia, optamos por um Web App responsivo em nuvem. Isso dispensou o custo de comprar totens físicos caros, "
            "permitindo o acesso universal por celular ou tablet com manutenção centralizada."
        )
    },
    {
        "id": "slide_05_objetivos",
        "titulo": "Slide 5: Objetivos Geral e Específicos",
        "tempo": "2:05 - 2:40",
        "texto": (
            "O nosso objetivo geral é projetar, implementar e validar esse motor híbrido integrado ao Web App para o salão Vila Cachos. "
            "Definimos seis objetivos específicos: modelar a taxonomia de André Walker e catalogar 27 cosméticos profissionais; "
            "integrar o modelo YOLO para inferir curvatura e frizz por foto; calibrar o K-Means sobre 8 variáveis clínicas para segmentar personas; "
            "aplicar a Média Bayesiana Amortecida para ancorar as notas contra o Cold Start; "
            "construir o Web App com justificativas transparentes; e validar o sistema com métricas de acurácia, inércia e Silhouette Score."
        )
    },
    {
        "id": "slide_06_metodologia",
        "titulo": "Slide 6: Metodologia: Como Fiz Tudo",
        "tempo": "2:40 - 3:35",
        "texto": (
            "E como isso foi desenvolvido na prática? Estruturamos um pipeline metodológico em cinco etapas: "
            "Etapa um: Curadoria da base real com 1.058 prontuários clínicos do Vila Cachos e repositórios abertos do Kaggle para gabarito conhecido. "
            "Etapa dois: Visão computacional com YOLOv8 treinado em 4 classes. Atendendo à orientação, não dividimos em 7 classes para evitar ruído entre 3B e 3C, e incluímos uma classe de controle para rejeitar carecas e peles lisas. "
            "Etapa três: Clusterização K-Means em 8 variáveis tricológicas padronizadas, agrupando em 4 personas clínicas. "
            "Etapa quatro: Motor híbrido com regras de contraindicação combinadas à Média Bayesiana com alfa igual a 10 e prior 4 ponto 2. "
            "E etapa cinco: Arquitetura desacoplada em FastAPI e React Vite, operando estritamente sob o teto de 512 megabytes de memória RAM do Render."
        )
    },
    {
        "id": "slide_07_arquitetura_mvp",
        "titulo": "Slide 7: Arquitetura da Solução e MVP Funcional",
        "tempo": "3:35 - 4:05",
        "texto": (
            "O MVP já está completamente desenvolvido e funcional. "
            "O frontend Totem UI possui triagem guiada em 4 etapas, modo escuro e conformidade com a LGPD através de timeout automático. "
            "O backend em FastAPI responde com latência inferior a 5 milissegundos por inferência na CPU. "
            "Todos os testes de integração automatizados possuem 100% de sucesso, e o K-Means atingiu Silhouette Score de 0 ponto 21 85, "
            "perfeitamente condizente com a sobreposição de variáveis clínicas ordinais."
        )
    },
    {
        "id": "slide_08_validacao_matriz",
        "titulo": "Slide 8: Validação Experimental: Matriz 4x4",
        "tempo": "4:05 - 4:40",
        "texto": (
            "Aqui apresento a validação experimental solicitada pelo meu coorientador: "
            "No teste preliminar de 3 classes, o modelo sofria com ruído de flash nas fotos e alcançava 59 ponto 3 por cento de acurácia. "
            "Ao aplicarmos a partição de 200 imagens de treino e 100 imagens de validação cega com gabarito conhecido em 4 classes, "
            "a nossa acurácia global saltou para 87 ponto 4 por cento! "
            "O maior destaque foi a classe de controle: obtivemos 100 por cento de sensibilidade na rejeição de calvície e ausência de cabelo, "
            "com zero falsos positivos nos cachos. E as curvaturas tipo 4 crespo e tipo 3 cacheado atingiram 89 ponto 6 e 84 ponto 4 por cento de acurácia. "
            "Isso comprova que a fusão multimodal blinda o sistema contra qualquer erro fotográfico."
        )
    },
    {
        "id": "slide_09_cronograma_conclusao",
        "titulo": "Slide 9: Cronograma e Próximos Passos",
        "tempo": "4:40 - 5:00",
        "texto": (
            "Para concluir, no Seminário 2 fechamos a redação da monografia e o protocolo ético. "
            "E no TCC 2 realizaremos a homologação em salão real com as cabeleireiras e clientes do Vila Cachos, mensurando a satisfação prática. "
            "Agradeço imensamente ao meu orientador, coorientador e à banca pela atenção. Estou aberto para dúvidas e contribuições."
        )
    }
]


def sintetizar_audio(texto: str, relative_filename: str):
    """Executa script PowerShell gerando o áudio via SAPI OneCore na pasta de áudio."""
    texto_limpo = texto.replace('"', '""').replace("\n", " ")
    
    ps_script = f"""$voice = New-Object -ComObject SAPI.SpVoice
$token = New-Object -ComObject SAPI.SpObjectToken
$token.SetId("HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech_OneCore\\Voices\\Tokens\\MSTTS_V110_ptBR_DanielM")
$voice.Voice = $token
$voice.Rate = 2  # Velocidade padrão de fala acadêmica clara

$stream = New-Object -ComObject SAPI.SpFileStream
$stream.Open("{relative_filename}", 3, $false)
$voice.AudioOutputStream = $stream
$voice.Speak("{texto_limpo}")
$stream.Close()
"""
    tmp_ps1 = os.path.join(AUDIO_DIR, "tmp_exec.ps1")
    with open(tmp_ps1, "w", encoding="utf-8-sig") as f:
        f.write(ps_script)

    subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "tmp_exec.ps1"], cwd=AUDIO_DIR, capture_output=True)
    if os.path.exists(tmp_ps1):
        os.remove(tmp_ps1)


def get_wav_duration_seconds(file_path: str) -> float:
    try:
        with wave.open(file_path, "r") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            return frames / float(rate)
    except Exception:
        return 0.0


def main():
    os.makedirs(AUDIO_DIR, exist_ok=True)
    print(f"=== GERANDO ÁUDIOS DO PITCH DE 5 MINUTOS (TCC VILA CACHOS AI) ===", flush=True)
    print(f"[*] Destino: {AUDIO_DIR}", flush=True)

    texto_completo_pitch = []
    duracoes = []

    # 1. Gera áudios individuais por slide
    for item in SLIDES_TEXTO:
        s_id = item["id"]
        rel_name = f"{s_id}.wav"
        full_path = os.path.join(AUDIO_DIR, rel_name)
        print(f"[+] Sintetizando {item['titulo']} ({item['tempo']})...", end=" ", flush=True)
        sintetizar_audio(item["texto"], rel_name)
        if os.path.exists(full_path):
            dur = get_wav_duration_seconds(full_path)
            duracoes.append(dur)
            size_kb = round(os.path.getsize(full_path) / 1024, 1)
            print(f"OK! ({round(dur, 1)}s | {size_kb} KB)", flush=True)
        else:
            print("FALHA!", flush=True)
        texto_completo_pitch.append(item["texto"])

    # 2. Gera o áudio contínuo do Pitch Completo (5 min)
    full_pitch_text = " ... ".join(texto_completo_pitch)
    full_rel_name = "pitch_completo_5min.wav"
    full_audio_file = os.path.join(AUDIO_DIR, full_rel_name)
    print(f"\n[*] Sintetizando Pitch Completo Contínuo ({full_rel_name})...", end=" ", flush=True)
    sintetizar_audio(full_pitch_text, full_rel_name)
    if os.path.exists(full_audio_file):
        total_dur = get_wav_duration_seconds(full_audio_file)
        size_mb = round(os.path.getsize(full_audio_file) / (1024 * 1024), 2)
        mins = int(total_dur // 60)
        secs = int(total_dur % 60)
        print(f"OK! ({mins}m {secs:02d}s | {size_mb} MB)", flush=True)

    print(f"\n=== SÍNTESE CONCLUÍDA COM SUCESSO! ===", flush=True)
    print(f"Total de áudios gerados: {len(SLIDES_TEXTO) + 1}")
    print(f"Duração Total Estimada: {sum(duracoes):.1f} segundos (~{sum(duracoes)/60:.1f} minutos)", flush=True)


if __name__ == "__main__":
    main()
