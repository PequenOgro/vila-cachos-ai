// tests/e2e/fluxo_totem.e2e.js
// Teste E2E do fluxo completo do Totem Vila Cachos (executado via Playwright MCP).
// Uso: browser_run_code_unsafe { filename: "tests/e2e/fluxo_totem.e2e.js" }
// Para testar localmente, troque BASE_URL por http://localhost:5173/
async (page) => {
  const BASE_URL = 'https://vila-cachos-ai.vercel.app/';
  const ROOT = 'C:/Users/Marcos Vinícius/Documents/TCC';
  const FOTO = `${ROOT}/dataset_cachos/val/tipo_3_cacheado/aug_000_base.jpg`;
  const SHOTS = `${ROOT}/.playwright-mcp`;

  const relatorio = { etapas: [], console: [], erros_pagina: [], api: [] };
  const etapa = (nome, ok, detalhe = '') => relatorio.etapas.push({ nome, ok, detalhe });

  page.on('console', (m) => {
    if (['error', 'warning'].includes(m.type())) relatorio.console.push(`${m.type()}: ${m.text()}`);
  });
  page.on('pageerror', (e) => relatorio.erros_pagina.push(String(e)));
  const inicio = new Map();
  page.on('request', (r) => { if (r.url().includes('onrender.com')) inicio.set(r, Date.now()); });
  page.on('requestfinished', async (r) => {
    if (!inicio.has(r)) return;
    const resp = await r.response();
    relatorio.api.push({ metodo: r.method(), url: r.url(), status: resp ? resp.status() : null, ms: Date.now() - inicio.get(r) });
  });
  page.on('requestfailed', (r) => {
    if (r.url().includes('onrender.com')) relatorio.api.push({ metodo: r.method(), url: r.url(), status: 'FALHOU', erro: r.failure()?.errorText });
  });

  // 1. Tela inicial
  await page.goto(BASE_URL, { waitUntil: 'networkidle' });
  etapa('1. Tela inicial carrega', await page.getByRole('heading', { name: /Descubra o produto/ }).isVisible());

  // 2. Dark / Light mode
  const temaAntes = await page.evaluate(() => document.documentElement.className + '|' + document.body.className + '|' + (document.querySelector('#root > div')?.className || ''));
  await page.getByRole('button', { name: 'Alternar Tema' }).click();
  const temaDepois = await page.evaluate(() => document.documentElement.className + '|' + document.body.className + '|' + (document.querySelector('#root > div')?.className || ''));
  etapa('2. Alternar tema muda classes', temaAntes !== temaDepois, temaDepois.includes('dark') ? 'dark ativo' : 'sem classe dark');
  await page.screenshot({ path: `${SHOTS}/e2e_01_tema.png` });

  // 3. Wizard
  await page.getByRole('button', { name: 'Iniciar Diagnóstico' }).click();
  etapa('3. Abre wizard (passo 1)', await page.getByText('Qual é o tipo de curvatura').isVisible());

  // 4. Upload de foto (YOLO Vision AI)
  await page.locator('input[type="file"]').setInputFiles(FOTO);
  const resultado = page.getByText('Resultado YOLO:');
  const erroVisao = page.locator('.bg-red-900\\/40');
  await Promise.race([
    resultado.waitFor({ timeout: 90000 }).catch(() => {}),
    erroVisao.waitFor({ timeout: 90000 }).catch(() => {}),
  ]);
  if (await resultado.isVisible()) {
    await page.getByRole('button', { name: 'Aplicar ao Diagnóstico' }).click();
    etapa('4. Diagnóstico por imagem', true, (await resultado.locator('..').innerText()).replace(/\s+/g, ' '));
  } else {
    etapa('4. Diagnóstico por imagem', false, (await erroVisao.innerText().catch(() => 'sem resposta em 90s')).trim());
  }
  await page.screenshot({ path: `${SHOTS}/e2e_02_upload.png`, fullPage: true });

  // 5. Avança passos 1→4 e gera recomendação
  for (let i = 0; i < 3; i++) await page.getByRole('button', { name: 'Próximo' }).click();
  await page.getByRole('button', { name: 'Gerar Recomendação' }).click();
  const feedbackBtn = page.getByTitle('Dar nota 5').first();
  await feedbackBtn.waitFor({ timeout: 90000 }).catch(() => {});
  const temResultado = await feedbackBtn.isVisible();
  etapa('5. Recomendações exibidas', temResultado, temResultado ? `${await page.getByTitle('Dar nota 5').count()} produtos` : 'sem resultado em 90s');
  await page.screenshot({ path: `${SHOTS}/e2e_03_resultado.png`, fullPage: true });

  // 6. Feedback loop
  if (temResultado) {
    await feedbackBtn.click();
    const ok = await page.getByText('Obrigado pelo seu feedback!').first().waitFor({ timeout: 30000 }).then(() => true).catch(() => false);
    etapa('6. Feedback registrado', ok);
  } else {
    etapa('6. Feedback registrado', false, 'pulado: sem recomendações');
  }

  // 7. Responsividade (celular 390x844)
  await page.setViewportSize({ width: 390, height: 844 });
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
  etapa('7. Sem scroll horizontal no celular', !overflow);
  await page.screenshot({ path: `${SHOTS}/e2e_04_mobile.png`, fullPage: true });

  return JSON.stringify(relatorio, null, 2);
}
