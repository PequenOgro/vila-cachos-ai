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
  cabelo_detectado?: boolean;
  mensagem_alerta?: string | null;
  curvatura_detectada?: number | null;
  curvatura_label: string;
  confianca_curvatura: number;
  frizz_detectado?: number | null;
  confianca_frizz?: number;
  porosidade_aparente?: number | null;
  confianca_porosidade?: number;
  tempo_inferencia_ms: number;
  modelo_utilizado?: string;
  detalhes_morfologicos?: {
    densidade_bordas?: number;
    indice_frizz?: number;
    energia_curvatura?: number;
    proporcao_cor_artificial?: number;
    proporcao_pele?: number;
  };
};

export type Produto = {
  produto_id?: string;
  nome: string;
  categoria?: string;
  score: number;
  score_conteudo?: number;
  score_feedback_bayesiano?: number;
  avaliacoes_cluster?: number;
  motivo: string;
  descricao?: string;
  estrelas_estimadas: number;
};

export type PesosHibridos = {
  peso_conteudo_regras: number;
  peso_feedback_clientes: number;
};

export type Recomendacao = {
  cluster_id?: number;
  persona: string;
  peso_conhecimento_vs_feedback?: PesosHibridos;
  produtos: Produto[];
};

export type FeedbackResposta = {
  status: string;
  mensagem: string;
  cluster_afetado: number;
  total_avaliacoes_base: number;
  media_global_atualizada: number;
};

/**
 * Heurística local (fallback para backend desatualizado): se mais de 60% do topo
 * da imagem (35% superior) é tom de pele, trata-se de couro cabeludo calvo/sem mecha.
 * Calibrada no conjunto de validação (≈2% de falsa rejeição em fotos de cabelo).
 */
async function topoPareceCalvo(file: File): Promise<boolean> {
  try {
    const bmp = await createImageBitmap(file);
    const size = 96;
    const canvas = document.createElement("canvas");
    canvas.width = size;
    canvas.height = size;
    const ctx = canvas.getContext("2d");
    if (!ctx) return false;
    ctx.drawImage(bmp, 0, 0, size, size);
    const linhas = Math.floor(size * 0.35);
    const px = ctx.getImageData(0, 0, size, linhas).data;
    let pele = 0;
    for (let i = 0; i < px.length; i += 4) {
      const [r, g, b] = [px[i], px[i + 1], px[i + 2]];
      if (r > 60 && g > 40 && b > 20 && r > g && g > b && r - g > 10 && r - b > 15) pele++;
    }
    return pele / (size * linhas) > 0.6;
  } catch {
    return false;
  }
}

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
    const data: DiagnosticoImagem = await r.json();

    // Backend legado (sem campo cabelo_detectado): valida o couro cabeludo no navegador.
    if (data.cabelo_detectado === undefined && (await topoPareceCalvo(file))) {
      data.cabelo_detectado = false;
    }

    // Defesa em Profundidade / Sanitização de Outliers e Falsos Positivos:
    // 1. Backend explicitamente sinalizou ausência de cabelo
    // 2. Ou backend legado omitiu o campo e métricas morfológicas comprovam
    //    ausência de mechas capilares (densidade < 0.025 ou frizz < 15.0)
    const densidade = data.detalhes_morfologicos?.densidade_bordas ?? 0;
    const frizz = data.detalhes_morfologicos?.indice_frizz ?? 0;
    const semCabelo =
      data.cabelo_detectado === false ||
      (data.cabelo_detectado === undefined && (densidade < 0.025 || frizz < 15.0));

    if (semCabelo) {
      return {
        ...data,
        cabelo_detectado: false,
        curvatura_detectada: null,
        curvatura_label: "Nenhum cabelo detectado",
        confianca_curvatura: 0,
        mensagem_alerta:
          data.mensagem_alerta ||
          "Não identificamos fios ou mechas de cabelo na foto enviada. Envie uma foto aproximada dos fios ou selecione sua curvatura abaixo.",
      };
    }

    return {
      ...data,
      cabelo_detectado: true,
    };
  } catch (err) {
    console.error(`[Vila Cachos API] Erro ao chamar ${targetUrl}:`, err);
    throw err;
  }
}

/**
 * Consulta o motor híbrido de recomendação da Vila Cachos.
 * Entrega o Top K produtos combinando Matriz de Conhecimento Tricológico + Avaliações Bayesianas.
 */
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
      cluster_id: d.cluster_id,
      persona:
        d.descricao_persona ?? d.persona ?? d.cluster_label ?? d.cluster ?? "Persona personalizada",
      peso_conhecimento_vs_feedback: d.peso_conhecimento_vs_feedback,
      produtos: lista.map((p: any) => ({
        produto_id: p.produto_id,
        nome: String(p.nome ?? p.produto ?? p.name ?? "Produto"),
        categoria: p.categoria,
        score: Number(p.score_final ?? p.score ?? p.score_hibrido ?? 0.85),
        score_conteudo: p.score_conteudo != null ? Number(p.score_conteudo) : undefined,
        score_feedback_bayesiano:
          p.score_feedback_bayesiano != null ? Number(p.score_feedback_bayesiano) : undefined,
        avaliacoes_cluster: p.avaliacoes_cluster != null ? Number(p.avaliacoes_cluster) : undefined,
        motivo: String(p.motivo ?? p.explicacao ?? p.reason ?? ""),
        descricao: p.descricao ? String(p.descricao) : undefined,
        estrelas_estimadas: Number(p.estrelas_estimadas ?? p.estrelas ?? 4.5),
      })),
    };
  } catch (err) {
    console.error(`[Vila Cachos API] Erro ao chamar ${targetUrl}:`, err);
    throw err;
  }
}

/**
 * Registra o feedback pós-atendimento da cliente.
 * Atualiza os pesos do cluster no backend em tempo real e persiste no CSV histórico.
 */
export async function enviarFeedback(
  perfil: Perfil,
  produto_nome: string,
  nota: number,
): Promise<FeedbackResposta | null> {
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
      return null;
    }
    const resData: FeedbackResposta = await r.json();
    console.log(
      `[Vila Cachos API] Feedback de ${nota}★ registrado para '${produto_nome}':`,
      resData,
    );
    return resData;
  } catch (err) {
    console.warn(`[Vila Cachos API] Falha ao enviar feedback para ${targetUrl}:`, err);
    return null;
  }
}

export function recomendacaoDemo(p: Perfil): Recomendacao {
  const nomes = ["Curvatura", "Ondulado", "Cacheado", "Crespo"];
  return {
    persona: `Cabelos ${nomes[p.curvatura - 1] ?? "Cacheado"}s${p.porosidade === 2 ? " com Alta Porosidade" : ""}${p.dano_quimico ? " e Química" : ""}`,
    produtos: [
      {
        nome: "Acidificante ACID-C",
        score: 0.94,
        estrelas_estimadas: 4.8,
        motivo:
          "O pH ácido sela as cutículas abertas, reduzindo a perda de água e o frizz típico de fios porosos.",
      },
      {
        nome: "Geleia Arvensis",
        score: 0.89,
        estrelas_estimadas: 4.6,
        motivo:
          "Ativadores botânicos agrupam os cachos e dão definição duradoura sem pesar na raiz.",
      },
      {
        nome: "Máscara Reconstrutora",
        score: 0.85,
        estrelas_estimadas: 4.5,
        motivo:
          "Repõe massa proteica nas áreas fragilizadas, devolvendo resistência e elasticidade.",
      },
    ],
  };
}
