import React from "react";
import { Activity, Database, FlaskConical } from "lucide-react";

export type AbaAdmin = "telemetria" | "catalogo" | "simulador";

interface AdminNavigationProps {
  abaAtiva: AbaAdmin;
  setAbaAtiva: (aba: AbaAdmin) => void;
  totalProdutos: number;
}

export function AdminNavigation({ abaAtiva, setAbaAtiva, totalProdutos }: AdminNavigationProps) {
  const abas: { id: AbaAdmin; label: string; icon: React.ReactNode; badge?: string | number }[] = [
    {
      id: "telemetria",
      label: "1. Telemetria & RNF-12",
      icon: <Activity className="h-4 w-4" />,
      badge: "K=4",
    },
    {
      id: "catalogo",
      label: "2. Catálogo & Matriz de Cosméticos",
      icon: <Database className="h-4 w-4" />,
      badge: totalProdutos,
    },
    {
      id: "simulador",
      label: "3. Simulador de Recomendação",
      icon: <FlaskConical className="h-4 w-4" />,
      badge: "XAI",
    },
  ];

  return (
    <div className="border-b border-emerald-950/70 bg-[#09100d]/90 backdrop-blur-md">
      <div className="mx-auto flex max-w-7xl px-4 sm:px-6">
        <nav className="flex space-x-2 sm:space-x-3 overflow-x-auto py-2.5">
          {abas.map((tab) => {
            const ativa = abaAtiva === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setAbaAtiva(tab.id)}
                className={`flex shrink-0 items-center gap-2 rounded-xl px-4 py-2 text-xs sm:text-sm font-semibold transition-all ${
                  ativa
                    ? "bg-emerald-950/90 text-emerald-200 shadow-md border border-emerald-700/70"
                    : "text-stone-400 hover:text-stone-100 hover:bg-stone-900/80 border border-transparent"
                }`}
              >
                <span className={ativa ? "text-emerald-400" : "text-stone-500"}>{tab.icon}</span>
                <span>{tab.label}</span>
                {tab.badge !== undefined && (
                  <span
                    className={`rounded-full px-2 py-0.5 text-[10px] font-bold ${
                      ativa
                        ? "bg-emerald-800 text-emerald-100"
                        : "bg-stone-800 text-stone-400 border border-stone-700/60"
                    }`}
                  >
                    {tab.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>
      </div>
    </div>
  );
}
