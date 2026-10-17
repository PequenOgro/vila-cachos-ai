import React from "react";
import { type Perfil, type Recomendacao } from "@/lib/api";
import { Logo } from "./Logo";
import { ProdutoCard } from "./ProdutoCard";
import { getImagemProduto } from "./product-images";

interface ResultadoProps {
  /** Objeto de recomendação retornado pela API */
  r: Recomendacao;
  /** Perfil capilar avaliado */
  perfil: Perfil;
  /** Função de callback para reiniciar o questionário */
  onReiniciar: () => void;
}

/**
 * =====================================================================
 * TELA DE RESULTADO (PRESCRIÇÃO TERAPÊUTICA & XAI)
 * =====================================================================
 * Apresenta a Persona identificada pelo agrupamento não-supervisionado K-Means,
 * a decomposição dos pesos híbridos (Conhecimento Especialista vs. Média Bayesiana)
 * e o Top 3 de cosméticos com explicabilidade semântica (XAI).
 */
export function Resultado({ r, perfil, onReiniciar }: ResultadoProps) {
  // Pesos adaptativos do motor híbrido (alpha da combinação convexa)
  const pesoRegras = Math.round(
    (r.peso_conhecimento_vs_feedback?.peso_conteudo_regras ?? 0.65) * 100,
  );
  const pesoFeedback = Math.round(
    (r.peso_conhecimento_vs_feedback?.peso_feedback_clientes ?? 0.35) * 100,
  );

  return (
    <section className="mx-auto max-w-6xl px-6 py-10 md:px-10">
      {/* Cabeçalho de Navegação com Botão de Reiniciar */}
      <header className="flex items-center justify-between">
        <Logo />
        <button
          onClick={onReiniciar}
          className="min-h-12 rounded-full border-2 border-primary px-6 font-semibold text-primary transition hover:bg-primary hover:text-primary-foreground"
        >
          Realizar novo diagnóstico
        </button>
      </header>

      {/* Título da Persona Capilar Identificada */}
      <div className="mt-12 animate-rise">
        <div className="flex items-center gap-2">
          <span className="rounded-full bg-primary/10 px-3 py-1 text-xs font-semibold text-primary">
            {r.cluster_id != null ? `Cluster Clínico #${r.cluster_id}` : "Prescrição Personalizada"}
          </span>
          <span className="text-xs uppercase tracking-widest text-muted-foreground">
            Diagnóstico Tricológico Vila Cachos
          </span>
        </div>
        <h1 className="mt-3 max-w-3xl text-3xl font-light md:text-5xl">
          <span className="font-bold italic">{r.persona}</span>
        </h1>
      </div>

      {/* Painel XAI: Inteligência Artificial Explicável & Equilíbrio Híbrido */}
      <div className="mt-8 rounded-3xl border border-border/60 bg-card p-6 shadow-soft animate-rise">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <span className="text-xs font-semibold uppercase tracking-wider text-primary">
              Transparência Algorítmica (XAI)
            </span>
            <h2 className="text-lg font-semibold text-foreground">
              Composição da Recomendação Híbrida
            </h2>
            <p className="mt-0.5 text-xs text-muted-foreground">
              Equilíbrio ponderado entre a ciência capilar e a avaliação de mais de 1.000 clientes
              reais.
            </p>
          </div>

          <div className="flex items-center gap-6 text-sm">
            <div className="flex items-center gap-2">
              <span className="h-3 w-3 rounded-full bg-primary" />
              <div>
                <p className="font-bold text-foreground">{pesoRegras}%</p>
                <p className="text-[11px] text-muted-foreground">Matriz Especialista</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <span className="h-3 w-3 rounded-full bg-amber" />
              <div>
                <p className="font-bold text-foreground">{pesoFeedback}%</p>
                <p className="text-[11px] text-muted-foreground">Média Bayesiana (Salão)</p>
              </div>
            </div>
          </div>
        </div>

        {/* Barra visual proporcional da combinação convexa */}
        <div className="mt-4 flex h-2 w-full overflow-hidden rounded-full bg-secondary">
          <div
            className="bg-primary transition-all duration-700"
            style={{ width: `${pesoRegras}%` }}
            title={`Peso da Matriz Especialista: ${pesoRegras}%`}
          />
          <div
            className="bg-amber transition-all duration-700"
            style={{ width: `${pesoFeedback}%` }}
            title={`Peso das Avaliações Reais de Salão: ${pesoFeedback}%`}
          />
        </div>
      </div>

      {/* Grid de Cosméticos Recomendados (Top 3) */}
      <div className="mt-10 grid gap-6 lg:grid-cols-3">
        {r.produtos.slice(0, 3).map((p, i) => (
          <ProdutoCard
            key={p.nome}
            p={p}
            img={getImagemProduto(p.nome)}
            perfil={perfil}
            delay={i * 120}
          />
        ))}
      </div>
    </section>
  );
}
