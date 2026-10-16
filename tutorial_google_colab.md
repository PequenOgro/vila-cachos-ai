# Guia Prático: Como Rodar e Hospedar o YOLO no Google Colab (GPU Gratuita)

> **Documento de Apoio ao TCC — Vila Cachos AI**  
> **Autor:** Marcos Vinícius (Sistemas de Informação - IFMA)  

---

## 1. Por que o seu Professor/Orientador sugeriu o Google Colab?

Modelos de Visão Computacional da família **YOLO (You Only Look Once)** e redes neurais profundas exigem processamento matricial intenso.  
- **No computador pessoal comum ou servidores gratuitos (ex: Render.com):** A inferência e o treinamento rodam na CPU, que possui memória limitada (512MB no Render) e sem aceleração gráfica.
- **No Google Colab (`https://colab.research.google.com`):** O Google disponibiliza **gratuitamente uma GPU dedicada NVIDIA T4 de 16 GB de VRAM**, capaz de treinar e processar imagens em **milissegundos**.

---

## 2. Como Usar o Notebook Pronto (`vila_cachos_yolo_colab.ipynb`)

Criamos um notebook pronto chamado [`vila_cachos_yolo_colab.ipynb`](file:///c:/Users/Marcos%20Vin%C3%ADcius/Documents/TCC/vila_cachos_yolo_colab.ipynb) na raiz do projeto.

### 📌 Passo a Passo de 3 Cliques:

1. **Acessar o Google Colab:**
   - Entre em [colab.research.google.com](https://colab.research.google.com) com a sua conta Google.
2. **Fazer Upload do Notebook:**
   - Clique em **Fazer Upload** (ou *Upload notebook*) e selecione o arquivo:
     `c:\Users\Marcos Vinícius\Documents\TCC\vila_cachos_yolo_colab.ipynb`
3. **Ativar a Placa de Vídeo (GPU T4):**
   - No menu superior do Colab, clique em:  
     `Ambiente de execução` ➔ `Alterar tipo de ambiente de execução`.
   - Em **Acelerador de hardware**, escolha **GPU T4** e clique em **Salvar**.

---

## 3. O que acontece quando você executa as células:

### ⚡ Célula 1: Verificação da GPU
Executa o comando `!nvidia-smi` para confirmar que a GPU Tesla T4 com 15-16 GB de VRAM está alocada para você.

### 📦 Célula 2: Instalação Automática
Instala a biblioteca oficial da Ultralytics (`ultralytics`), FastAPI, PyTorch e PyNgrok no ambiente em nuvem da Google.

### 🧠 Célula 3: Treinamento ou Inferência
Carrega o modelo YOLOv8. Se você tiver um dataset de mechas de cabelo, ele faz o *transfer learning* em minutos.

### 🌐 Célula 4: Servidor Online com Link Público

Agora utilizamos o **Cloudflare Tunnel (`cloudflared`)**, que é **100% gratuito e não exige nenhum cadastro, token ou cartão**:
```text
=================================================================
🚀 SERVIDOR GOOGLE COLAB ATIVO COM GPU NVIDIA T4!
Aguarde alguns segundos... o link HTTPS aparecerá abaixo:
+----------------------------------------------------------------+
|  Your quick Tunnel has been created! Visit it at:              |
|  https://nome-aleatorio-gerado.trycloudflare.com              |
+----------------------------------------------------------------+
=================================================================
```

*(Caso prefira usar o Ngrok tradicional, basta criar uma conta gratuita em [dashboard.ngrok.com](https://dashboard.ngrok.com) e colar seu token com `ngrok.set_auth_token('SEU_TOKEN')`).*

---

## 4. Como Conectar o seu Totem / Backend ao Colab

Nosso arquivo [`vision_engine.py`](file:///c:/Users/Marcos%20Vin%C3%ADcius/Documents/TCC/vision_engine.py) já foi atualizado com **suporte nativo e automático**:

1. No seu arquivo `.env` (ou no terminal do Windows), você pode definir:
   ```bash
   YOLO_REMOTE_URL=https://sua-url-do-ngrok.ngrok-free.app
   ```
2. **Vantagem de Nível Científico (Zero Downtime):**
   - Se o Google Colab estiver ligado, o sistema envia a foto para a GPU do Google Colab e recebe a inferência ultra-rápida.
   - Se a sessão do Colab for encerrada ou a internet oscilar, o nosso sistema **faz fallback automático e transparente** para a inferência local sem travar o atendimento e sem dar erro na tela da cliente!

---

## 5. As Duas Estratégias para Apresentar na Banca:

| Estratégia | Como Funciona | Quando Usar |
|---|---|---|
| **Estratégia A: Treinar no Colab & Baixar Pesos (`best.pt`)** | Você treina no Colab aproveitando a GPU T4, clica com o botão direito no arquivo `best.pt` gerado e faz download para a pasta do TCC. O sistema local passa a usar os pesos treinados offline. | **Mais recomendada para produção final**, pois não depende do Colab ficar com a aba aberta. |
| **Estratégia B: Hospedagem ao Vivo (Live Demo)** | Você deixa o Colab rodando durante a apresentação do TCC e mostra a requisição batendo na GPU em tempo real. | **Excelente para demonstração ao vivo para a banca examinadora**. |
