This is a single self-contained fix; keep it small and focused. Eliminar 100% dos falsos positivos e outliers no classificador YOLO e no motor de visão computacional (rejeitando fotos de pessoas calvas/carecas com ou sem barba, imagens sem mechas capilares, gráficos e objetos aleatórios), validando localmente com zero erros e sincronizando com o ambiente de produção no Render.

Integrity mode: demo
The team must NOT: read test source code to understand expected behaviour before implementing.

## Verification Resources
- Suíte de testes automatizados da API: `test_api.py`
- Imagens de teste locais de outliers e mechas capilares em `scratch/bald_with_beard.jpg` e no dataset do projeto
- Endpoint de produção da API: `https://vila-cachos-ai.onrender.com`

## Requirements

### R1. Rejeição Robusta de Outliers no YOLO e Motor de Visão
Rejeitar confiavelmente imagens que não contenham mechas capilares humanas visíveis no couro cabeludo (incluindo homens calvos ou carecas mesmo com barba, gráficos sintéticos, banners, objetos e superfícies lisas), retornando `cabelo_detectado: false`, `curvatura_detectada: null`, sem sugestão de perfil de cacho e com mensagem de alerta apropriada.

### R2. Execução Contínua de Testes com Tolerância Zero a Erros
Executar a suíte de testes automatizados da API (`python test_api.py`) localmente a cada ajuste, iterando na correção até que 100% dos testes passem diretamente no terminal com Exit Code 0 (zero falhas e zero exceções não tratadas).

### R3. Sincronização e Validação em Produção
Comitar e enviar as alterações para a branch `main` do repositório remoto para acionar o deploy automático no Render, verificando em seguida se a API em produção (`https://vila-cachos-ai.onrender.com`) está operacional e rejeitando corretamente os outliers sem erros.

## Acceptance Criteria

### Precisão de Rejeição e Classificação
- [ ] Fotos de pessoas calvas ou carecas (com ou sem barba), superfícies lisas e imagens sem mechas capilares retornam status HTTP 200 com `cabelo_detectado: false`, `curvatura_detectada: null` e mensagem informativa de ausência de mechas capilares.
- [ ] Fotos válidas contendo mechas de cabelo continuam sendo detectadas com `cabelo_detectado: true` e classificação de curvatura (tipo 2, 3 ou 4) com respectiva sugestão de perfil.

### Validação Local Automatizada
- [ ] O comando `python test_api.py` é executado no terminal e finaliza com Exit Code 0, sem falhas de asserção ou exceções.

### Validação em Produção
- [ ] As alterações no classificador e motor de visão são comitadas e enviadas para a branch `main` no repositório remoto.
- [ ] O endpoint `/diagnostico/imagem` em produção no Render responde com sucesso (HTTP 200) e confirma a rejeição correta de outliers com `cabelo_detectado: false`.
