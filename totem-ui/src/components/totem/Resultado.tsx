import React, { useState } from "react";
import { MessageCircle, QrCode } from "lucide-react";
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
 * Implementa compartilhamento via WhatsApp e QR Code (UC-05).
 */
export function Resultado({ r, perfil, onReiniciar }: ResultadoProps) {
  const [mostrarQRCode, setMostrarQRCode] = useState(false);

  // Pesos adaptativos do motor híbrido (alpha da combinação convexa)
  const pesoRegras = Math.round(
    (r.peso_conhecimento_vs_feedback?.peso_conteudo_regras ?? 0.65) * 100,
  );
  const pesoFeedback = Math.round(
    (r.peso_conhecimento_vs_feedback?.peso_feedback_clientes ?? 0.35) * 100,
  );

  // Mensagem e link formatados para compartilhamento no WhatsApp / QR Code (UC-05)
  const textoWhatsApp = encodeURIComponent(
    `🌿 *Meu Diagnóstico Capilar na Vila Cachos*\n\n` +
      `✨ *Diagnóstico:* ${r.persona}\n\n` +
      `🧴 *Top 3 Cosméticos Prescritos:*\n` +
      r.produtos
        .slice(0, 3)
        .map(
          (p, idx) =>
            `${idx + 1}. *${p.nome}* (${p.categoria || "Tratamento"})\n   👉 Motivo: ${p.motivo}`,
        )
        .join("\n\n") +
      `\n\nPrescrição gerada pelo Totem Inteligente Vila Cachos AI 🍃`,
  );
  const linkWhatsApp = `https://api.whatsapp.com/send?text=${textoWhatsApp}`;

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

      {/* Ações de Fidelização e Compartilhamento: WhatsApp & QR Code (UC-05) */}
      <div className="mt-12 flex flex-col items-center justify-between gap-4 rounded-3xl border border-primary/20 bg-primary/5 p-6 sm:flex-row">
        <div>
          <h3 className="font-serif text-lg font-bold text-foreground">
            Deseja levar seu cronograma capilar no celular?
          </h3>
          <p className="mt-0.5 text-xs text-muted-foreground">
            Escaneie o QR Code no totem ou envie os 3 cosméticos recomendados diretamente para o seu
            WhatsApp.
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <button
            onClick={() => setMostrarQRCode(!mostrarQRCode)}
            className="flex items-center gap-2 rounded-full border border-primary/40 bg-card px-4 py-2.5 text-xs font-semibold text-foreground transition hover:bg-primary/10 cursor-pointer"
          >
            <QrCode className="h-4 w-4 text-primary" />
            <span>{mostrarQRCode ? "Ocultar QR Code" : "Exibir QR Code"}</span>
          </button>
          <a
            href={linkWhatsApp}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 rounded-full bg-emerald-700 px-5 py-2.5 text-xs font-semibold text-white shadow-sm transition hover:bg-emerald-600"
          >
            <MessageCircle className="h-4 w-4" />
            <span>Enviar no WhatsApp</span>
          </a>
        </div>
      </div>

      {/* Modal/Box de QR Code na tela do Totem */}
      {mostrarQRCode && (
        <div className="mt-4 flex flex-col items-center justify-center rounded-2xl border border-border bg-card p-6 text-center animate-rise">
          <p className="text-xs font-medium text-muted-foreground mb-3">
            Aponte a câmera do seu smartphone para abrir sua prescrição tricológica:
          </p>
          <img
            src={`https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=${encodeURIComponent(linkWhatsApp)}`}
            alt="QR Code da Recomendação Capilar"
            className="h-44 w-44 rounded-xl border border-border/80 p-2 shadow-inner"
          />
        </div>
      )}
    </section>
  );
}
