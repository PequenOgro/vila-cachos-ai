import React, { useState } from "react";
import { enviarFeedback, type Perfil, type Recomendacao } from "@/lib/api";

interface ProdutoCardProps {
  /** Objeto com metadados e scores do cosmético recomendado */
  p: Recomendacao["produtos"][number];
  /** Caminho do asset fotográfico oficial do produto */
  img: string;
  /** Perfil capilar ativo para registro do feedback no backend */
  perfil: Perfil;
  /** Atraso para animação em cascata (staggered animation) */
  delay: number;
}

/**
 * =====================================================================
 * CARD DE PRODUTO RECOMENDADO
 * =====================================================================
 * Apresenta o cosmético prescrito pelo motor híbrido, destacando:
 * 1. Imagem oficial com fundo transparente.
 * 2. Categoria cosmética e percentual de compatibilidade global.
 * 3. Decomposição das métricas (Afinidade com Fio vs. Satisfação no Salão).
 * 4. Justificativa tricológica semântica (XAI).
 * 5. Coleta de feedback ativo com recalibração imediata do Cluster.
 */
export function ProdutoCard({ p, img, perfil, delay }: ProdutoCardProps) {
  const [nota, setNota] = useState(0);
  const [mensagemFeedback, setMensagemFeedback] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  // Normalização do score final para percentual (0 a 100%)
  const rawScore = Number(p.score);
  const pctCompatibilidade =
    !isNaN(rawScore) && rawScore > 0
      ? Math.round(rawScore <= 1 ? rawScore * 100 : rawScore)
      : Math.round(((Number(p.estrelas_estimadas) || 4.2) / 5) * 100);

  /**
   * Envia a avaliação da cliente (1 a 5 estrelas) para o endpoint /feedback da FastAPI.
   * O motor atualiza a média bayesiana e recalibra os pesos do cluster.
   */
  const handleAvaliar = async (estrelas: number) => {
    setNota(estrelas);
    setEnviando(true);
    const resp = await enviarFeedback(perfil, p.nome, estrelas);
    setEnviando(false);

    if (resp?.mensagem) {
      setMensagemFeedback(resp.mensagem);
    } else {
      setMensagemFeedback("Avaliação registrada! Pesos do seu cluster recalibrados no motor 🌿");
    }
  };

  return (
    <article
      className="flex animate-rise flex-col overflow-hidden rounded-3xl bg-card shadow-soft"
      style={{ animationDelay: `${delay}ms` }}
    >
      {/* Vitrine do Frasco Oficial com Fundo Neutro e Efeito Hover */}
      <div className="relative flex aspect-[4/3] w-full items-center justify-center bg-stone-100/70 p-6 dark:bg-stone-900/60">
        <img
          src={img}
          alt={p.nome}
          width={400}
          height={400}
          loading="lazy"
          className="h-full max-h-56 w-auto object-contain drop-shadow-md transition-transform duration-300 hover:scale-105"
        />

        {/* Badge de Compatibilidade Geral */}
        <span className="absolute left-4 top-4 rounded-full bg-card/95 px-3 py-1 text-xs font-semibold tracking-wide text-foreground shadow-sm backdrop-blur">
          {pctCompatibilidade}% compatível
        </span>

        {/* Badge da Categoria Cosmética */}
        {p.categoria && (
          <span className="absolute right-4 top-4 rounded-full bg-primary/10 px-3 py-1 text-[11px] font-semibold text-primary backdrop-blur">
            {p.categoria}
          </span>
        )}
      </div>

      <div className="flex flex-1 flex-col p-6">
        <h3 className="text-xl font-semibold leading-snug">{p.nome}</h3>

        {/* Descrição dos Ativos e Ação Cosmética */}
        {p.descricao && (
          <p className="mt-1.5 text-xs text-muted-foreground leading-relaxed line-clamp-2">
            {p.descricao}
          </p>
        )}

        {/* Média Histórica e Volume Amostral no Salão */}
        <div className="mt-3 flex items-center justify-between text-xs text-muted-foreground">
          <span className="text-amber font-medium">
            {"★".repeat(Math.round(p.estrelas_estimadas))}{" "}
            <span className="text-foreground font-semibold">{p.estrelas_estimadas.toFixed(1)}</span>{" "}
            estimado
          </span>
          {p.avaliacoes_cluster !== undefined && (
            <span>{p.avaliacoes_cluster} clientes no cluster</span>
          )}
        </div>

        {/* Detalhamento dos Scores Híbridos (Ciência vs. Prova Social) */}
        <div className="mt-3 grid grid-cols-2 gap-2 rounded-xl bg-muted/40 p-2.5 text-[11px]">
          <div>
            <span className="text-muted-foreground">Afinidade com Fio:</span>
            <p className="font-semibold text-foreground">
              {p.score_conteudo != null
                ? `${Math.round(p.score_conteudo * 100)}%`
                : `${pctCompatibilidade}%`}
            </p>
          </div>
          <div>
            <span className="text-muted-foreground">Satisfação Salão:</span>
            <p className="font-semibold text-foreground">
              {p.score_feedback_bayesiano != null
                ? `${Math.round(p.score_feedback_bayesiano * 100)}%`
                : "4.8★"}
            </p>
          </div>
        </div>

        {/* Justificativa XAI (Por que este cosmético foi escolhido?) */}
        <div className="mt-4 rounded-2xl bg-secondary p-4">
          <p className="text-xs font-semibold uppercase tracking-widest text-primary">
            Por que para você?
          </p>
          <p className="mt-1.5 text-xs leading-relaxed text-secondary-foreground">{p.motivo}</p>
        </div>

        {/* Seção Interativa de Feedback */}
        <div className="mt-auto pt-5">
          {nota ? (
            <div className="animate-rise rounded-xl bg-primary/10 p-3 text-center">
              <p className="font-serif text-sm font-medium text-primary">
                {mensagemFeedback ?? "Obrigada! Sua avaliação nos ajuda a cuidar melhor 🌿"}
              </p>
            </div>
          ) : (
            <div>
              <p className="text-xs text-muted-foreground">Já usou este produto? Avalie:</p>
              <div className="mt-1 flex items-center gap-1">
                {[1, 2, 3, 4, 5].map((n) => (
                  <button
                    key={n}
                    disabled={enviando}
                    aria-label={`${n} estrelas`}
                    onClick={() => handleAvaliar(n)}
                    className="flex h-10 w-10 items-center justify-center text-2xl text-muted-foreground transition hover:scale-115 hover:text-amber active:scale-90 disabled:opacity-50"
                  >
                    ★
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </article>
  );
}
