/* eslint-disable @typescript-eslint/no-explicit-any */
export const API_URL =
  (import.meta.env["VITE_API_URL"] as string | undefined) ?? "https://vila-cachos-ai.onrender.com";

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
  const r = await fetch(`${API_URL}/diagnostico/imagem`, { method: "POST", body: fd });
  if (!r.ok) throw new Error("falha");
  return r.json();
}

// Normaliza variações de formato do backend.
export async function recomendar(perfil: Perfil): Promise<Recomendacao> {
  const r = await fetch(`${API_URL}/recommend?top_k=3`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(perfil),
  });
  if (!r.ok) throw new Error("falha");
  const d = await r.json();
  const lista = d.produtos ?? d.recomendacoes ?? d.recommendations ?? [];
  return {
    persona: d.persona ?? d.cluster_label ?? d.cluster ?? "Persona personalizada",
    produtos: lista.map((p: any) => ({
      nome: String(p.nome ?? p.produto ?? p.name ?? "Produto"),
      score: Number(p.score ?? p.score_hibrido ?? 0),
      motivo: String(p.motivo ?? p.explicacao ?? p.reason ?? ""),
      estrelas_estimadas: Number(p.estrelas_estimadas ?? p.estrelas ?? 4.5),
    })),
  };
}

export async function enviarFeedback(perfil: Perfil, produto_nome: string, nota: number) {
  await fetch(`${API_URL}/feedback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ perfil, produto_nome, nota }),
  }).catch(() => undefined);
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
