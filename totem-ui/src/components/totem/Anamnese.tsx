import React, { useState } from "react";
import { Logo } from "./Logo";
import { type FormAnamnese, Titulo, Opcao } from "./AnamneseShared";
import { PassoCurvatura } from "./PassoCurvatura";

interface AnamneseProps {
  form: FormAnamnese;
  setForm: (f: FormAnamnese) => void;
  onVoltar: () => void;
  onFinalizar: () => void;
}

const NOMES_PASSOS = ["Curvatura", "Porosidade", "Química", "Queixas"] as const;

/**
 * =====================================================================
 * ORQUESTRADOR DO FLUXO DE ANAMNESE CAPILAR (4 ETAPAS)
 * =====================================================================
 * Gerencia a navegação entre os 4 passos do diagnóstico tricológico:
 * 1. Curvatura (Ondas, Cachos, Crespos + IA Vision).
 * 2. Porosidade (Baixa, Média, Alta).
 * 3. Histórico Químico (Natural, Transição, Danificado).
 * 4. Queixas do Cotidiano (Frizz, Ressecamento, Couro, Quebra).
 */
export function Anamnese({ form, setForm, onVoltar, onFinalizar }: AnamneseProps) {
  const [passo, setPasso] = useState(0);

  // Validação para avanço do passo (impede prosseguir sem seleção nas etapas 1, 2 e 3)
  const podeAvancar = [form.curvatura, form.porosidade, form.quimica, true][passo] !== null;

  return (
    <section className="mx-auto flex min-h-dvh max-w-5xl flex-col px-6 py-8 md:px-10">
      {/* Header com Logo e Indicador Numérico */}
      <header className="flex items-center justify-between">
        <Logo />
        <span className="text-sm text-muted-foreground font-medium">
          Passo {passo + 1} de {NOMES_PASSOS.length}
        </span>
      </header>

      {/* Barra de Progresso Acessível */}
      <div
        className="mt-8 grid grid-cols-4 gap-2"
        role="progressbar"
        aria-valuenow={passo + 1}
        aria-valuemin={1}
        aria-valuemax={4}
      >
        {NOMES_PASSOS.map((nome, i) => (
          <div key={nome}>
            <div
              className={`h-1.5 rounded-full transition-colors duration-300 ${
                i <= passo ? "bg-primary" : "bg-secondary"
              }`}
            />
            <p
              className={`mt-2 text-xs uppercase tracking-widest ${
                i === passo ? "text-foreground font-semibold" : "text-muted-foreground"
              }`}
            >
              {nome}
            </p>
          </div>
        ))}
      </div>

      {/* Conteúdo Dinâmico da Etapa Atual */}
      <div key={passo} className="flex-1 animate-rise py-10">
        {passo === 0 && <PassoCurvatura form={form} setForm={setForm} />}

        {passo === 1 && (
          <>
            <Titulo
              t="Como seus fios absorvem água?"
              s="A porosidade indica o quanto as cutículas capilares estão abertas."
            />
            <div className="grid gap-4 md:grid-cols-3">
              {[
                ["Baixa", "Cutículas seladas, produto demora a penetrar."],
                ["Média", "Equilibrada, absorve e retém hidratação perfeitamente."],
                ["Alta", "Fios ásperos, secam rápido e perdem hidratação facilmente."],
              ].map(([t, d], i) => (
                <Opcao
                  key={t}
                  ativo={form.porosidade === i + 1}
                  onClick={() => setForm({ ...form, porosidade: i + 1 })}
                  titulo={t!}
                  desc={d!}
                />
              ))}
            </div>
          </>
        )}

        {passo === 2 && (
          <>
            <Titulo
              t="Qual o histórico químico dos fios?"
              s="Isso nos ajuda a equilibrar reposição lipídica e reconstrução proteica."
            />
            <div className="grid gap-4 md:grid-cols-3">
              {[
                ["100% Natural", "Sem nenhuma química agressiva nos fios."],
                ["Transição Capilar", "Parte do cabelo natural, parte ainda com química."],
                ["Danificado", "Descoloração, tinturas constantes, relaxamento ou progressiva."],
              ].map(([t, d], i) => (
                <Opcao
                  key={t}
                  ativo={form.quimica === i}
                  onClick={() => setForm({ ...form, quimica: i })}
                  titulo={t!}
                  desc={d!}
                />
              ))}
            </div>
          </>
        )}

        {passo === 3 && (
          <>
            <Titulo
              t="O que mais te incomoda no dia a dia?"
              s="Escolha quantas queixas quiser para direcionar o tratamento."
            />
            <div className="flex flex-wrap gap-3">
              {(
                [
                  ["frizz", "Frizz excessivo e falta de definição"],
                  ["ressecamento", "Ressecamento e pontas secas"],
                  ["couro", "Couro cabeludo sensível ou oleoso"],
                  ["quebra", "Perda de massa / quebra constante"],
                ] as const
              ).map(([chave, rotulo]) => {
                const ativo = form.queixas.includes(chave);
                return (
                  <button
                    key={chave}
                    aria-pressed={ativo}
                    onClick={() =>
                      setForm({
                        ...form,
                        queixas: ativo
                          ? form.queixas.filter((x) => x !== chave)
                          : [...form.queixas, chave],
                      })
                    }
                    className={`min-h-14 rounded-full border-2 px-6 text-base transition active:scale-95 ${
                      ativo
                        ? "border-terracotta bg-terracotta text-accent-foreground shadow-sm"
                        : "border-border bg-card hover:border-terracotta"
                    }`}
                  >
                    {ativo ? "✓ " : ""}
                    {rotulo}
                  </button>
                );
              })}
            </div>
          </>
        )}
      </div>

      {/* Rodapé com Navegação Voltar / Avançar */}
      <footer className="flex items-center justify-between gap-4 pb-4">
        <button
          onClick={() => (passo === 0 ? onVoltar() : setPasso(passo - 1))}
          className="min-h-14 rounded-full px-8 text-base text-muted-foreground transition hover:text-foreground active:scale-95"
        >
          ← Voltar
        </button>

        <button
          disabled={!podeAvancar}
          onClick={() => (passo === 3 ? onFinalizar() : setPasso(passo + 1))}
          className="min-h-14 rounded-full bg-primary px-10 text-base font-semibold text-primary-foreground transition hover:bg-sage-soft active:scale-95 disabled:opacity-40"
        >
          {passo === 3 ? "Ver minha prescrição" : "Continuar →"}
        </button>
      </footer>
    </section>
  );
}
