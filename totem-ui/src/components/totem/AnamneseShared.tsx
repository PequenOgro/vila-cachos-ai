import React from "react";

/**
 * Estrutura de dados do formulário de anamnese capilar.
 */
export interface FormAnamnese {
  /** Código numérico da curvatura (2: Ondulado, 3: Cacheado, 4: Crespo) */
  curvatura: number | null;
  /** Nível de porosidade capilar (1: Baixa, 2: Média, 3: Alta) */
  porosidade: number | null;
  /** Histórico químico (0: 100% Natural, 1: Transição, 2: Danificado/Química) */
  quimica: number | null;
  /** Lista de queixas selecionadas ('frizz', 'ressecamento', 'couro', 'quebra') */
  queixas: string[];
}

/**
 * =====================================================================
 * CABEÇALHO DE TÍTULO & SUBTÍTULO DA ETAPA
 * =====================================================================
 */
export function Titulo({ t, s }: { t: string; s: string }) {
  return (
    <div className="mb-8">
      <h2 className="text-4xl font-light md:text-5xl">{t}</h2>
      <p className="mt-3 text-muted-foreground">{s}</p>
    </div>
  );
}

/**
 * =====================================================================
 * BOTÃO DE OPÇÃO CARD SELECIONÁVEL
 * =====================================================================
 */
export function Opcao({
  ativo,
  onClick,
  titulo,
  desc,
  icone,
}: {
  ativo: boolean;
  onClick: () => void;
  titulo: string;
  desc: string;
  icone?: React.ReactNode;
}) {
  return (
    <button
      onClick={onClick}
      aria-pressed={ativo}
      className={`flex min-h-32 flex-col items-start gap-3 rounded-3xl border-2 p-6 text-left transition ${
        ativo
          ? "border-primary bg-primary text-primary-foreground shadow-soft"
          : "border-transparent bg-card hover:border-sage-soft"
      }`}
    >
      {icone}
      <span className="font-serif text-xl font-semibold">{titulo}</span>
      <span className={`text-sm ${ativo ? "text-primary-foreground/85" : "text-muted-foreground"}`}>
        {desc}
      </span>
    </button>
  );
}

/**
 * =====================================================================
 * ILUSTRAÇÃO VETORIAL DA CURVATURA (ONDAS, CACHOS, CRESPOS)
 * =====================================================================
 */
export function Onda({ voltas }: { voltas: number }) {
  const d =
    voltas === 2
      ? "M4 30 Q 14 10, 24 30 T 44 30 T 64 30"
      : voltas === 3
        ? "M4 30 c 6 -16, 18 -16, 14 0 s 8 16, 14 0 s 8 -16, 14 0 s 8 16, 14 0"
        : "M4 30 l 5 -12 l 5 18 l 5 -18 l 5 18 l 5 -18 l 5 18 l 5 -18 l 5 18 l 5 -18 l 5 12";

  return (
    <svg
      viewBox="0 0 68 50"
      className="h-10 w-16"
      fill="none"
      stroke="currentColor"
      strokeWidth="2.2"
      strokeLinecap="round"
      aria-hidden="true"
    >
      <path d={d} />
    </svg>
  );
}
