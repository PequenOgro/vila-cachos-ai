import { createFileRoute } from "@tanstack/react-router";
import React, { useEffect, useState } from "react";
import {
  obterHealth,
  obterCatalogo,
  CATALOGO_OFICIAL_27,
  type ItemCatalogo,
  type MetricasHealth,
} from "@/lib/api";
import { AdminHeader } from "@/components/admin/AdminHeader";
import { AdminNavigation, type AbaAdmin } from "@/components/admin/AdminNavigation";
import { TelemetriaTab } from "@/components/admin/TelemetriaTab";
import { CatalogoTab } from "@/components/admin/CatalogoTab";
import { SimuladorTab } from "@/components/admin/SimuladorTab";

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

export function AdminPage() {
  const [abaAtiva, setAbaAtiva] = useState<AbaAdmin>("catalogo");
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
        {abaAtiva === "telemetria" && <TelemetriaTab metricas={metricas} />}
        {abaAtiva === "catalogo" && <CatalogoTab catalogo={catalogo} />}
        {abaAtiva === "simulador" && <SimuladorTab />}
      </main>
    </div>
  );
}
