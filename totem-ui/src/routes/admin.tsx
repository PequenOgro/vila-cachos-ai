import { createFileRoute } from "@tanstack/react-router";
import React, { Suspense, lazy, useEffect, useState } from "react";
import { obterHealth, obterCatalogo, type ItemCatalogo, type MetricasHealth } from "@/lib/api";
import { CATALOGO_OFICIAL_27 } from "@/lib/catalogo-oficial";
import { AdminHeader } from "@/components/admin/AdminHeader";
import { AdminNavigation, type AbaAdmin } from "@/components/admin/AdminNavigation";
import { DashboardGeralTab } from "@/components/admin/DashboardGeralTab";

const TelemetriaTab = lazy(() =>
  import("@/components/admin/TelemetriaTab").then((m) => ({ default: m.TelemetriaTab })),
);
const CatalogoTab = lazy(() =>
  import("@/components/admin/CatalogoTab").then((m) => ({ default: m.CatalogoTab })),
);
const SimuladorTab = lazy(() =>
  import("@/components/admin/SimuladorTab").then((m) => ({ default: m.SimuladorTab })),
);

function AdminTabFallback() {
  return (
    <div className="rounded-2xl border border-stone-800/90 bg-[#131d18]/90 p-12 text-center text-stone-300">
      Carregando módulo analítico...
    </div>
  );
}

export const Route = createFileRoute("/admin")({
  head: () => ({
    meta: [
      { title: "Vila Cachos — Painel do Gestor Técnico (Admin)" },
      {
        name: "description",
        content:
          "Painel de telemetria, qualidade científica de IA (RNF-12) e gestão do catálogo de cosméticos da Vila Cachos.",
      },
    ],
  }),
  component: AdminPage,
});

function AdminPage() {
  const [abaAtiva, setAbaAtiva] = useState<AbaAdmin>("dashboard");
  // Inicialização instantânea (0ms de espera) com catálogo canônico de 27 cosméticos
  const [catalogo, setCatalogo] = useState<ItemCatalogo[]>(CATALOGO_OFICIAL_27);
  const [metricas, setMetricas] = useState<MetricasHealth | null>({
    status: "operacional",
    motor_carregado: true,
    total_clientes_historico: 1084,
    media_satisfacao_global: 4.54,
    num_clusters: 4,
    silhouette_score: 0.448,
  });
  const [isOnline, setIsOnline] = useState(true);
  const [recarregando, setRecarregando] = useState(false);

  const carregarDados = async () => {
    setRecarregando(true);
    try {
      const [h, c] = await Promise.all([obterHealth(), obterCatalogo()]);
      setMetricas(h);
      if (Array.isArray(c) && c.length >= 27) {
        setCatalogo(c);
      }
      setIsOnline(!h.status.includes("resiliente"));
    } catch (err) {
      console.warn("[Admin] Operando em modo resiliente local:", err);
      setIsOnline(false);
    } finally {
      setRecarregando(false);
    }
  };

  useEffect(() => {
    // Sincronização não-bloqueante em background
    carregarDados();
  }, []);

  return (
    <div className="min-h-screen bg-[#0b120f] font-sans text-stone-100 antialiased selection:bg-emerald-900 selection:text-emerald-100 bg-[radial-gradient(ellipse_80%_60%_at_50%_-15%,rgba(16,185,129,0.12),rgba(0,0,0,0))]">
      {/* Topbar Superior */}
      <AdminHeader
        statusTexto={metricas?.status}
        isOnline={isOnline}
        recarregando={recarregando}
        onRecarregar={carregarDados}
      />

      {/* Navegação por Abas Principais */}
      <AdminNavigation
        abaAtiva={abaAtiva}
        setAbaAtiva={setAbaAtiva}
        totalProdutos={catalogo.length}
      />

      {/* Área Central de Conteúdo */}
      <main className="mx-auto max-w-7xl px-4 py-6 sm:px-6 sm:py-8">
        {abaAtiva === "dashboard" && (
          <DashboardGeralTab
            metricas={metricas}
            catalogo={catalogo}
            isOnline={isOnline}
            onNavegar={setAbaAtiva}
          />
        )}
        {abaAtiva !== "dashboard" && (
          <Suspense fallback={<AdminTabFallback />}>
            {abaAtiva === "telemetria" && <TelemetriaTab metricas={metricas} />}
            {abaAtiva === "catalogo" && <CatalogoTab catalogo={catalogo} />}
            {abaAtiva === "simulador" && <SimuladorTab />}
          </Suspense>
        )}
      </main>
    </div>
  );
}
