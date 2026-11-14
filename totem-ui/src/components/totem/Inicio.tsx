import React from "react";
import { Link } from "@tanstack/react-router";
import { Settings } from "lucide-react";
import hero from "@/assets/hero.jpg";
import { Logo } from "./Logo";

interface InicioProps {
  /** Função de callback invocada quando o usuário toca para iniciar o diagnóstico */
  onStart: () => void;
}

/**
 * =====================================================================
 * TELA INICIAL (BOAS-VINDAS & APRESENTAÇÃO DO TOTEM)
 * =====================================================================
 * Primeira tela interativa exibida no totem físico ou navegador.
 * Destaca os pilares tricológicos (Slow Beauty, IA Híbrida e Diagnóstico Rápido).
 */
export function Inicio({ onStart }: InicioProps) {
  const selosDiferenciais = [
    "100% Personalizado",
    "IA Híbrida Especialista",
    "Explicabilidade Tricológica",
  ];

  return (
    <section className="relative min-h-dvh overflow-hidden">
      {/* Imagem de Fundo Heroica em Alta Resolução */}
      <img
        src={hero}
        alt="Mulher com cabelos cacheados volumosos e saudáveis"
        width={1280}
        height={1600}
        className="absolute inset-0 h-full w-full object-cover"
      />
      {/* Camada de Contraste e Véu Fotográfico */}
      <div className="absolute inset-0 bg-veil" />

      {/* Conteúdo Principal Sobreposto */}
      <div className="relative flex min-h-dvh flex-col justify-between p-8 md:p-14">
        <header className="flex items-start justify-between">
          <Logo light />
          <div className="flex flex-col items-end gap-2">
            <p className="max-w-[14rem] text-right text-sm tracking-wide text-primary-foreground/80">
              Totem Inteligente de Diagnóstico Capilar
            </p>
            <Link
              to="/admin"
              className="inline-flex items-center gap-1.5 rounded-full border border-primary-foreground/30 bg-black/25 px-3 py-1 text-xs font-medium text-primary-foreground/90 backdrop-blur-md transition hover:bg-black/40 hover:text-white"
              title="Acessar painel de administração e telemetria"
            >
              <Settings className="h-3 w-3" />
              <span>Painel do Gestor</span>
            </Link>
          </div>
        </header>

        <div className="max-w-2xl animate-rise pb-6">
          <p className="mb-4 text-sm uppercase tracking-[0.3em] text-primary-foreground/70">
            Slow Beauty &amp; Ciência Capilar
          </p>
          <h1 className="text-5xl font-light leading-[1.05] text-primary-foreground md:text-7xl">
            Seu cacho tem <span className="font-bold italic">uma história.</span>
          </h1>
          <p className="mt-6 max-w-lg text-lg text-primary-foreground/85">
            Descubra em menos de 1 minuto os cuidados ideais para a sua curvatura.
          </p>

          {/* Selos de Garantia e Metodologia Científica */}
          <div className="mt-8 flex flex-wrap gap-2">
            {selosDiferenciais.map((selo) => (
              <span
                key={selo}
                className="rounded-full border border-primary-foreground/40 px-4 py-2 text-sm text-primary-foreground backdrop-blur-md"
              >
                {selo}
              </span>
            ))}
          </div>

          {/* Botão de Call-to-Action com Feedback Tátil */}
          <button
            onClick={onStart}
            className="mt-10 min-h-16 rounded-full bg-primary px-10 text-lg font-semibold text-primary-foreground animate-breathe transition hover:bg-sage-soft active:scale-95"
          >
            Iniciar Diagnóstico Capilar
          </button>
        </div>
      </div>
    </section>
  );
}
