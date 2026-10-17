/* eslint-disable @typescript-eslint/no-explicit-any */
function sanitizeApiUrl(raw?: string): string {
  if (!raw) return "https://vila-cachos-ai.onrender.com";
  // Extrai estritamente protocolo + domínio válido (alfanumérico, traço e ponto) + porta opcional.
  // Ignora formatações markdown como [url](url), parênteses, colchetes ou aspas acidentais.
  const match = raw.match(/https?:\/\/[a-zA-Z0-9.-]+(?::[0-9]+)?/);
  if (match) {
    return match[0];
  }
  return "https://vila-cachos-ai.onrender.com";
}

export const API_URL = sanitizeApiUrl(import.meta.env["VITE_API_URL"] as string | undefined);

if (typeof window !== "undefined") {
  console.log("[Vila Cachos API] Conectado ao backend:", API_URL);
}

export type Perfil = {
  curvatura: number;
  porosidade: number;
  dano_quimico: number;
  ressecamento_opacidade: number;
  alta_porosidade_quimica: number;
  frizz_falta_definicao: number;
  transicao_capilar: number;
  couro_sensivel_oleoso: number;
};

export type DiagnosticoImagem = {
  curvatura_detectada: number;
  curvatura_label: string;
  confianca_curvatura: number;
  frizz_detectado: number;
  porosidade_aparente: number;
  tempo_inferencia_ms: number;
};

export type Produto = {
  nome: string;
  score: number;
  motivo: string;
  estrelas_estimadas: number;
};

export type Recomendacao = { persona: string; produtos: Produto[] };

export async function diagnosticarImagem(file: File): Promise<DiagnosticoImagem> {
  const fd = new FormData();
  fd.append("file", file);
  const targetUrl = `${API_URL}/diagnostico/imagem`;
  try {
    const r = await fetch(targetUrl, { method: "POST", body: fd });
    if (!r.ok) {
      console.warn(`[Vila Cachos API] Falha HTTP ${r.status} em ${targetUrl}`);
      throw new Error(`HTTP ${r.status}`);
    }
    return await r.json();
  } catch (err) {
    console.error(`[Vila Cachos API] Erro ao chamar ${targetUrl}:`, err);
    throw err;
  }
}

// Normaliza variações de formato do backend.
export async function recomendar(perfil: Perfil): Promise<Recomendacao> {
  const targetUrl = `${API_URL}/recommend?top_k=3`;
  try {
    const r = await fetch(targetUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(perfil),
    });
    if (!r.ok) {
      console.warn(`[Vila Cachos API] Falha HTTP ${r.status} em ${targetUrl}`);
      throw new Error(`HTTP ${r.status}`);
    }
    const d = await r.json();
    const lista = d.recomendacoes ?? d.produtos ?? d.recommendations ?? [];
    return {
      persona: d.descricao_persona ?? d.persona ?? d.cluster_label ?? d.cluster ?? "Persona personalizada",
      produtos: lista.map((p: any) => ({
        nome: String(p.nome ?? p.produto ?? p.name ?? "Produto"),
        score: Number(p.score_final ?? p.score ?? p.score_hibrido ?? 0.85),
        motivo: String(p.motivo ?? p.explicacao ?? p.reason ?? ""),
        estrelas_estimadas: Number(p.estrelas_estimadas ?? p.estrelas ?? 4.5),
      })),
    };
  } catch (err) {
    console.error(`[Vila Cachos API] Erro ao chamar ${targetUrl}:`, err);
    throw err;
  }
}

export async function enviarFeedback(perfil: Perfil, produto_nome: string, nota: number) {
  const targetUrl = `${API_URL}/feedback`;
  try {
    const perfilSanitizado = {
      curvatura: Math.max(2, Math.min(4, Number(perfil.curvatura) || 3)),
      porosidade: Math.max(1, Math.min(3, Number(perfil.porosidade) || 2)),
      dano_quimico: perfil.dano_quimico ? 1 : 0,
      ressecamento_opacidade: perfil.ressecamento_opacidade ? 1 : 0,
      alta_porosidade_quimica: perfil.alta_porosidade_quimica ? 1 : 0,
      frizz_falta_definicao: perfil.frizz_falta_definicao ? 1 : 0,
      transicao_capilar: perfil.transicao_capilar ? 1 : 0,
      couro_sensivel_oleoso: perfil.couro_sensivel_oleoso ? 1 : 0,
    };
    const payload = {
      perfil_cliente: perfilSanitizado,
      nome_produto: produto_nome,
      nota_satisfacao: Math.max(1, Math.min(5, Math.round(nota))),
    };
    const r = await fetch(targetUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!r.ok) {
      const errText = await r.text();
      console.warn(`[Vila Cachos API] Falha HTTP ${r.status} em ${targetUrl}:`, errText);
      return;
    }
    const resData = await r.json();
    console.log(`[Vila Cachos API] Feedback de ${nota}★ registrado para '${produto_nome}':`, resData);
  } catch (err) {
    console.warn(`[Vila Cachos API] Falha ao enviar feedback para ${targetUrl}:`, err);
  }
}

export function recomendacaoDemo(p: Perfil): Recomendacao {
  const nomes = ["Curvatura", "Ondulado", "Cacheado", "Crespo"];
  return {
    persona: `Cabelos ${nomes[p.curvatura - 1] ?? "Cacheado"}s${p.porosidade === 2 ? " com Alta Porosidade" : ""}${p.dano_quimico ? " e Química" : ""}`,
    produtos: [
      { nome: "Acidificante ACID-C", score: 0.94, estrelas_estimadas: 4.8, motivo: "O pH ácido sela as cutículas abertas, reduzindo a perda de água e o frizz típico de fios porosos." },
      { nome: "Geleia Arvensis", score: 0.89, estrelas_estimadas: 4.6, motivo: "Ativadores botânicos agrupam os cachos e dão definição duradoura sem pesar na raiz." },
      { nome: "Máscara Reconstrutora", score: 0.85, estrelas_estimadas: 4.5, motivo: "Repõe massa proteica nas áreas fragilizadas, devolvendo resistência e elasticidade." },
    ],
  };
}
