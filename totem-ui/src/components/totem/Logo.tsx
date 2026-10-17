import React from "react";

/**
 * Propriedades visuais do logotipo Vila Cachos.
 */
interface LogoProps {
  /** Se verdadeiro, inverte para cor clara para fundos escuros/fotográficos */
  light?: boolean;
}

/**
 * =====================================================================
 * LOGOTIPO VILA CACHOS (IDENTIDADE VISUAL DA MARCA)
 * =====================================================================
 * Renderiza o ícone orgânico do cacho capilar estilizado juntamente com
 * a tipografia serifada minimalista da marca Vila Cachos.
 */
export function Logo({ light = false }: LogoProps) {
  return (
    <div
      className={`flex items-center gap-3 ${light ? "text-primary-foreground" : "text-foreground"}`}
    >
      <svg
        viewBox="0 0 40 56"
        className="h-11 w-8"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.6"
        aria-hidden="true"
      >
        <rect x="2" y="2" width="36" height="52" rx="18" />
        <path d="M14 46 C 10 30, 12 18, 22 10 M20 46 C 18 32, 22 22, 30 16 M12 22 c 6 -2, 10 2, 10 8" />
      </svg>
      <div className="font-serif leading-none">
        <div className="text-2xl font-light">Vila</div>
        <div className="text-2xl font-light">Cachos</div>
      </div>
    </div>
  );
}
