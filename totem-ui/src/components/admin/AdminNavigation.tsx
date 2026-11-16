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
    <div className="border-b border-stone-200/80 bg-stone-100/60 backdrop-blur-sm">
      <div className="mx-auto flex max-w-7xl px-4 sm:px-6">
        <nav className="flex space-x-2 sm:space-x-4 overflow-x-auto py-2">
          {abas.map((tab) => {
            const ativa = abaAtiva === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setAbaAtiva(tab.id)}
                className={`flex shrink-0 items-center gap-2 rounded-xl px-3.5 py-2 text-xs sm:text-sm font-semibold transition-all ${
                  ativa
                    ? "bg-white text-emerald-900 shadow-xs border border-stone-200/80"
                    : "text-stone-600 hover:text-stone-900 hover:bg-stone-200/50"
                }`}
              >
                <span className={ativa ? "text-emerald-700" : "text-stone-400"}>{tab.icon}</span>
                <span>{tab.label}</span>
                {tab.badge !== undefined && (
                  <span
                    className={`rounded-full px-2 py-0.2 text-[10px] font-bold ${
                      ativa ? "bg-emerald-100 text-emerald-900" : "bg-stone-200/80 text-stone-600"
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
