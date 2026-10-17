import React, { useEffect, useState } from "react";
import { Logo } from "./Logo";

/**
 * Mensagens educativas que rotacionam durante o cálculo das inferências de IA.
 * Revelam os passos tricológicos que ocorrem nos bastidores.
 */
const MENSAGENS_PROCESSAMENTO = [
  "Processando vetor tricológico de 8 dimensões…",
  "Cruzando formulações com a matriz de afinidade dermatológica…",
  "Consultando histórico de 1.000+ clientes reais do salão…",
  "Ajustando ponderação adaptativa bayesiana…",
];

/**
 * =====================================================================
 * TELA DE PROCESSAMENTO (LOADING TRICOLÓGICO)
 * =====================================================================
 * Proporciona feedback visual e engajamento enquanto a API de recomendação
 * resolve o clustering e a ponderação híbrida no backend.
 */
export function Processando() {
  const [indiceMensagem, setIndiceMensagem] = useState(0);

  useEffect(() => {
    const intervalo = setInterval(() => {
      setIndiceMensagem((atual) => (atual + 1) % MENSAGENS_PROCESSAMENTO.length);
    }, 1400);

    return () => clearInterval(intervalo);
  }, []);

  return (
    <section className="flex min-h-dvh flex-col items-center justify-center bg-primary px-6 text-primary-foreground">
      {/* Efeito Ondulatório de Ondas Capilares (Ripple) */}
      <div className="relative flex h-56 w-56 items-center justify-center">
        {[0, 0.8, 1.6].map((atraso) => (
          <span
            key={atraso}
            className="absolute inset-0 rounded-full border-2 border-primary-foreground/60 animate-ripple"
            style={{ animationDelay: `${atraso}s` }}
          />
        ))}
        <Logo light />
      </div>

      {/* Rotação Dinâmica de Mensagens */}
      <p
        key={indiceMensagem}
        className="mt-14 max-w-md animate-rise text-center font-serif text-2xl font-light"
        aria-live="polite"
      >
        {MENSAGENS_PROCESSAMENTO[indiceMensagem]}
      </p>
    </section>
  );
}
