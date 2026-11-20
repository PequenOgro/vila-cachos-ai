import React, { Suspense, lazy, useState, useMemo } from "react";
import {
  Sparkles,
  Users,
  CheckCircle2,
  Award,
  Star,
  Database,
  Activity,
  FlaskConical,
  ArrowRight,
  ShieldCheck,
  Layers,
  Zap,
  Cpu,
  BarChart3,
  Clock,
  Sparkle,
  Compass,
} from "lucide-react";
import { type ItemCatalogo, type MetricasHealth } from "@/lib/api";
import { getImagemProduto } from "@/components/totem/product-images";
import { type AbaAdmin } from "./AdminNavigation";

const ProductDetailModal = lazy(() =>
  import("./ProductDetailModal").then((m) => ({ default: m.ProductDetailModal })),
);

interface DashboardGeralTabProps {
  metricas: MetricasHealth | null;
  catalogo: ItemCatalogo[];
  isOnline: boolean;
  onNavegar: (aba: AbaAdmin) => void;
}

export function DashboardGeralTab({
  metricas,
  catalogo,
  isOnline,
  onNavegar,
}: DashboardGeralTabProps) {
  const [produtoModal, setProdutoModal] = useState<ItemCatalogo | null>(null);

  // Estatísticas calculadas do Catálogo
  const estatisticas = useMemo(() => {
    const total = catalogo.length;
    const ondulados = catalogo.filter((p) => p.curvaturas_indicadas.includes(2)).length;
    const cacheados = catalogo.filter((p) => p.curvaturas_indicadas.includes(3)).length;
    const crespos = catalogo.filter((p) => p.curvaturas_indicadas.includes(4)).length;

    const marcasMap: Record<string, number> = {};
    catalogo.forEach((p) => {
      marcasMap[p.marca] = (marcasMap[p.marca] || 0) + 1;
    });

    const marcasList = Object.entries(marcasMap).map(([marca, count]) => ({
      marca,
      count,
      pct: total > 0 ? Math.round((count / total) * 100) : 0,
    }));

    return {
      total,
      ondulados,
      cacheados,
      crespos,
      marcasList,
    };
  }, [catalogo]);

  // Cosméticos Destaque das 4 Personas Clínicas
  const cosméticosDestaque = useMemo(() => {
    const ids = ["PROD_01", "PROD_02", "PROD_03", "PROD_06"];
    return catalogo.filter((p) => ids.includes(p.id));
  }, [catalogo]);

  // Etapas do Funil Tricológico
  const etapasFunil = [
    {
      passo: "01",
      nome: "Anamnese & Queixas",
      subtitulo: "Entrada do Cliente",
      detalhe: "Walker 2A-4C, porosidade, químicas e queixas capilares.",
      status: "100% Interativo",
      badgeCor: "border-sky-800/80 bg-sky-950/80 text-sky-300",
      acao: () => onNavegar("simulador"),
      botaoTexto: "Testar no Simulador",
    },
    {
      passo: "02",
      nome: "Visão IA (YOLOv8)",
      subtitulo: "Validação Fotográfica",
      detalhe: "Inferência ONNX Runtime leve com rejeição de não-cabelo.",
      status: "< 20ms Latência",
      badgeCor: "border-emerald-800/80 bg-emerald-950/80 text-emerald-300",
      acao: () => onNavegar("telemetria"),
      botaoTexto: "Ver RNF-12",
    },
    {
      passo: "03",
      nome: "K-Means Clustering",
      subtitulo: "Persona Tricológica",
      detalhe: "Vetorização 8D agrupando em 4 clusters científicos.",
      status: "Silhouette 0.448",
      badgeCor: "border-teal-800/80 bg-teal-950/80 text-teal-300",
      acao: () => onNavegar("telemetria"),
      botaoTexto: "Auditar 4 Personas",
    },
    {
      passo: "04",
      nome: "Ponderação Híbrida",
      subtitulo: "Matriz + Feedback",
      detalhe: "Combinação convexa (65% Regras do Salão + 35% Avaliações).",
      status: "Laplace C=5.0",
      badgeCor: "border-amber-800/80 bg-amber-950/80 text-amber-300",
      acao: () => onNavegar("simulador"),
      botaoTexto: "Ver Equilíbrio XAI",
    },
    {
      passo: "05",
      nome: "Prescrição Personalizada",
      subtitulo: "Saída de Alto Valor",
      detalhe: "Top 3 cosméticos homologados com explicabilidade tricológica.",
      status: "27 Fórmulas",
      badgeCor: "border-purple-800/80 bg-purple-950/80 text-purple-300",
      acao: () => onNavegar("catalogo"),
      botaoTexto: "Abrir Catálogo",
    },
  ];

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Modal de Detalhes de Produto */}
      {produtoModal && (
        <Suspense fallback={<div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm" />}>
          <ProductDetailModal produto={produtoModal} onClose={() => setProdutoModal(null)} />
        </Suspense>
      )}

      {/* 1. HERO DO CENTRO DE COMANDO & BOAS-VINDAS */}
      <div className="relative overflow-hidden rounded-3xl border border-emerald-900/60 bg-gradient-to-br from-[#12221b] via-[#101b16] to-[#0c1410] p-6 sm:p-8 shadow-2xl shadow-black/40">
        <div className="absolute -right-16 -top-16 h-64 w-64 rounded-full bg-emerald-500/10 blur-3xl pointer-events-none" />
        <div className="absolute right-1/4 -bottom-20 h-52 w-52 rounded-full bg-amber-500/5 blur-3xl pointer-events-none" />

        <div className="relative z-10 flex flex-col justify-between gap-6 lg:flex-row lg:items-center">
          <div className="max-w-3xl space-y-2">
            <div className="inline-flex items-center gap-2 rounded-full border border-emerald-700/60 bg-emerald-950/80 px-3 py-1 text-xs font-semibold text-emerald-300">
              <Sparkles className="h-3.5 w-3.5 text-emerald-400" />
              <span>Centro de Comando Tricológico • Vila Cachos AI</span>
            </div>

            <h1 className="font-serif text-2xl sm:text-3xl lg:text-4xl font-bold tracking-tight text-stone-100 leading-tight">
              Visão Executiva &amp; Funil de Inteligência Capilar
            </h1>

            <p className="text-xs sm:text-sm text-stone-300/90 leading-relaxed">
              Painel unificado para o gestor técnico: acompanhe em um único lugar a saúde da IA
              híbrida, a aderência dos 27 cosméticos homologados e o comportamento de diagnóstico
              das clientes em tempo real.
            </p>
          </div>

          {/* Badges de Operação Rápida */}
          <div className="flex flex-wrap lg:flex-col gap-2 shrink-0">
            <div className="inline-flex items-center gap-2 rounded-xl border border-stone-800 bg-[#0d1512]/90 px-3 py-2 text-xs font-semibold text-stone-200">
              <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
              <span>{isOnline ? "Backend Conectado (Render)" : "Operação Resiliente Local"}</span>
            </div>
            <div className="inline-flex items-center gap-2 rounded-xl border border-stone-800 bg-[#0d1512]/90 px-3 py-2 text-xs font-semibold text-stone-300">
              <Clock className="h-3.5 w-3.5 text-amber-400" />
              <span>Inferência Ultrarrápida &lt; 20ms</span>
            </div>
            <div className="inline-flex items-center gap-2 rounded-xl border border-stone-800 bg-[#0d1512]/90 px-3 py-2 text-xs font-semibold text-stone-300">
              <ShieldCheck className="h-3.5 w-3.5 text-emerald-400" />
              <span>Memória Restrita 512MB RAM</span>
            </div>
          </div>
        </div>
      </div>

      {/* 2. OS 4 MACRO KPIS EXECUTIVOS */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <h2 className="font-serif text-base sm:text-lg font-bold text-stone-200 flex items-center gap-2">
            <BarChart3 className="h-4 w-4 text-emerald-400" />
            <span>Indicadores Globais de Performance &amp; Salão</span>
          </h2>
          <span className="text-xs text-stone-400">Atualizado dinamicamente</span>
        </div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {/* Card 1: Atendimentos */}
          <div
            onClick={() => onNavegar("telemetria")}
            className="group cursor-pointer rounded-2xl border border-stone-800/90 bg-[#131d18]/90 p-5 shadow-xl shadow-black/20 transition-all duration-200 hover:border-emerald-600/70 hover:bg-[#16221c] hover:-translate-y-0.5"
          >
            <div className="flex items-center justify-between">
              <span className="text-[11px] font-bold uppercase tracking-wider text-stone-400">
                Histórico de Atendimentos
              </span>
              <div className="rounded-xl bg-sky-950/80 border border-sky-800/60 p-2 text-sky-400 group-hover:scale-105 transition-transform">
                <Users className="h-4 w-4" />
              </div>
            </div>
            <div className="mt-3 flex items-baseline gap-2">
              <span className="text-3xl font-serif font-bold text-stone-100">
                {metricas?.total_clientes_historico ?? 1084}
              </span>
              <span className="text-xs font-semibold text-sky-400">clientes reais</span>
            </div>
            <p className="mt-2 text-xs text-stone-400 leading-relaxed">
              Base enriquecida com avaliações pós-procedimento.
            </p>
            <div className="mt-3 flex items-center gap-1 text-[11px] font-bold text-sky-400 group-hover:text-sky-300">
              <span>Ver detalhes na Telemetria</span>
              <ArrowRight className="h-3 w-3 transition-transform group-hover:translate-x-1" />
            </div>
          </div>

          {/* Card 2: Catálogo Canônico */}
          <div
            onClick={() => onNavegar("catalogo")}
            className="group cursor-pointer rounded-2xl border border-stone-800/90 bg-[#131d18]/90 p-5 shadow-xl shadow-black/20 transition-all duration-200 hover:border-emerald-600/70 hover:bg-[#16221c] hover:-translate-y-0.5"
          >
            <div className="flex items-center justify-between">
              <span className="text-[11px] font-bold uppercase tracking-wider text-stone-400">
                Acervo Canônico 2024
              </span>
              <div className="rounded-xl bg-emerald-950/80 border border-emerald-800/60 p-2 text-emerald-400 group-hover:scale-105 transition-transform">
                <Database className="h-4 w-4" />
              </div>
            </div>
            <div className="mt-3 flex items-baseline gap-2">
              <span className="text-3xl font-serif font-bold text-emerald-400">
                {estatisticas.total}
              </span>
              <span className="text-xs font-semibold text-emerald-300">cosméticos</span>
            </div>
            <p className="mt-2 text-xs text-stone-400 leading-relaxed">
              100% No/Low-Poo nas 4 marcas parceiras homologadas.
            </p>
            <div className="mt-3 flex items-center gap-1 text-[11px] font-bold text-emerald-400 group-hover:text-emerald-300">
              <span>Inspecionar fórmulas do acervo</span>
              <ArrowRight className="h-3 w-3 transition-transform group-hover:translate-x-1" />
            </div>
          </div>

          {/* Card 3: Silhouette Score */}
          <div
            onClick={() => onNavegar("telemetria")}
            className="group cursor-pointer rounded-2xl border border-emerald-700/60 bg-gradient-to-br from-emerald-950/80 to-[#131d18] p-5 shadow-xl shadow-black/30 transition-all duration-200 hover:border-emerald-500/80 hover:-translate-y-0.5"
          >
            <div className="flex items-center justify-between">
              <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-300">
                Robustez RNF-12 (Silhouette)
              </span>
              <div className="rounded-xl bg-emerald-900/80 border border-emerald-600/60 p-2 text-emerald-300 group-hover:scale-105 transition-transform">
                <Award className="h-4 w-4" />
              </div>
            </div>
            <div className="mt-3 flex items-baseline gap-2">
              <span className="text-3xl font-mono font-bold text-emerald-200">
                {metricas?.silhouette_score?.toFixed(3) ?? "0.448"}
              </span>
              <span className="rounded-full bg-emerald-900/90 border border-emerald-600/60 px-2 py-0.5 text-[10px] font-bold text-emerald-200">
                Robusto (&gt;0.40)
              </span>
            </div>
            <p className="mt-2 text-xs text-emerald-300/80 leading-relaxed">
              Alta separabilidade matemática dos 4 clusters de clientes.
            </p>
            <div className="mt-3 flex items-center gap-1 text-[11px] font-bold text-emerald-300 group-hover:text-emerald-200">
              <span>Auditar personas científicas</span>
              <ArrowRight className="h-3 w-3 transition-transform group-hover:translate-x-1" />
            </div>
          </div>

          {/* Card 4: Satisfação Salão */}
          <div
            onClick={() => onNavegar("simulador")}
            className="group cursor-pointer rounded-2xl border border-stone-800/90 bg-[#131d18]/90 p-5 shadow-xl shadow-black/20 transition-all duration-200 hover:border-amber-600/70 hover:bg-[#16221c] hover:-translate-y-0.5"
          >
            <div className="flex items-center justify-between">
              <span className="text-[11px] font-bold uppercase tracking-wider text-stone-400">
                Média Bayesiana do Salão
              </span>
              <div className="rounded-xl bg-amber-950/80 border border-amber-800/60 p-2 text-amber-400 group-hover:scale-105 transition-transform">
                <Star className="h-4 w-4 fill-amber-400 text-amber-400" />
              </div>
            </div>
            <div className="mt-3 flex items-baseline gap-2">
              <span className="text-3xl font-serif font-bold text-stone-100">
                {metricas?.media_satisfacao_global
                  ? metricas.media_satisfacao_global.toFixed(2)
                  : "4.54"}
              </span>
              <span className="text-xs font-bold text-amber-400">★ ★ ★ ★ ★</span>
            </div>
            <p className="mt-2 text-xs text-stone-400 leading-relaxed">
              Ponderação com amortecedor de Laplace contra viés amostral.
            </p>
            <div className="mt-3 flex items-center gap-1 text-[11px] font-bold text-amber-400 group-hover:text-amber-300">
              <span>Testar no simulador clínico</span>
              <ArrowRight className="h-3 w-3 transition-transform group-hover:translate-x-1" />
            </div>
          </div>
        </div>
      </div>

      {/* 3. O FUNIL TRICOLÓGICO DA VILA CACHOS (VISÃO PASSO-A-PASSO) */}
      <div className="rounded-3xl border border-stone-800/90 bg-[#131d18]/90 p-6 sm:p-7 shadow-2xl shadow-black/30">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-stone-800 pb-4">
          <div>
            <h2 className="font-serif text-lg sm:text-xl font-bold text-stone-100 flex items-center gap-2">
              <Compass className="h-5 w-5 text-emerald-400" />
              <span>O Funil de Recomendação do Diagnóstico Capilar</span>
            </h2>
            <p className="mt-1 text-xs text-stone-400">
              Da captura visual à prescrição final: veja como o sistema toma decisões explicáveis
              passo a passo.
            </p>
          </div>
          <span className="self-start rounded-full bg-emerald-950 border border-emerald-700/80 px-3 py-1 text-xs font-bold text-emerald-300">
            Pipeline 5 Estágios
          </span>
        </div>

        <div className="mt-6 grid grid-cols-1 gap-4 md:grid-cols-5">
          {etapasFunil.map((etapa, idx) => (
            <div
              key={etapa.passo}
              className="relative flex flex-col justify-between rounded-2xl border border-stone-800/90 bg-[#0d1411]/90 p-4 transition hover:border-emerald-700/70 hover:bg-[#101915]"
            >
              <div>
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs font-bold text-stone-500">
                    Etapa {etapa.passo}
                  </span>
                  <span
                    className={`rounded-full px-2 py-0.5 text-[10px] font-bold border ${etapa.badgeCor}`}
                  >
                    {etapa.status}
                  </span>
                </div>

                <h3 className="mt-2.5 font-serif text-sm font-bold text-stone-100">{etapa.nome}</h3>
                <p className="text-[11px] font-semibold text-emerald-400">{etapa.subtitulo}</p>

                <p className="mt-2 text-xs text-stone-400 leading-relaxed">{etapa.detalhe}</p>
              </div>

              <button
                onClick={etapa.acao}
                className="mt-4 flex w-full items-center justify-center gap-1.5 rounded-xl border border-stone-700/80 bg-stone-900/90 py-1.5 text-xs font-semibold text-stone-300 transition hover:bg-emerald-950 hover:border-emerald-600 hover:text-emerald-200"
              >
                <span>{etapa.botaoTexto}</span>
                <ArrowRight className="h-3 w-3" />
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* 4. DISTRIBUIÇÃO DO ACERVO & MARCAS PARCEIRAS */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        {/* Distribuição por Curvatura (6 colunas) */}
        <div className="rounded-3xl border border-stone-800/90 bg-[#131d18]/90 p-6 shadow-xl shadow-black/30 lg:col-span-6 space-y-5">
          <div className="flex items-center justify-between border-b border-stone-800 pb-3">
            <h3 className="font-serif text-base font-bold text-stone-100 flex items-center gap-2">
              <Layers className="h-4 w-4 text-emerald-400" />
              <span>Cobertura por Curvatura (Walker)</span>
            </h3>
            <span className="text-xs text-stone-400 font-medium">
              Total: {estatisticas.total} cosméticos
            </span>
          </div>

          <p className="text-xs text-stone-400">
            Proporção de cosméticos formulados para cada padrão de mecha capilar atendida no salão.
          </p>

          <div className="space-y-4">
            {/* Tipo 2 */}
            <div>
              <div className="flex items-center justify-between text-xs mb-1.5">
                <span className="font-semibold text-teal-300">
                  Tipo 2 • Ondulados (2A / 2B / 2C)
                </span>
                <span className="font-mono text-stone-300">
                  {estatisticas.ondulados} cosméticos (
                  {Math.round((estatisticas.ondulados / estatisticas.total) * 100)}%)
                </span>
              </div>
              <div className="h-2 w-full overflow-hidden rounded-full bg-stone-900 border border-stone-800">
                <div
                  className="h-full rounded-full bg-gradient-to-r from-teal-500 to-emerald-400 transition-all duration-700"
                  style={{
                    width: `${Math.round((estatisticas.ondulados / estatisticas.total) * 100)}%`,
                  }}
                />
              </div>
            </div>

            {/* Tipo 3 */}
            <div>
              <div className="flex items-center justify-between text-xs mb-1.5">
                <span className="font-semibold text-emerald-300">
                  Tipo 3 • Cacheados (3A / 3B / 3C)
                </span>
                <span className="font-mono text-stone-300">
                  {estatisticas.cacheados} cosméticos (
                  {Math.round((estatisticas.cacheados / estatisticas.total) * 100)}%)
                </span>
              </div>
              <div className="h-2 w-full overflow-hidden rounded-full bg-stone-900 border border-stone-800">
                <div
                  className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-teal-400 transition-all duration-700"
                  style={{
                    width: `${Math.round((estatisticas.cacheados / estatisticas.total) * 100)}%`,
                  }}
                />
              </div>
            </div>

            {/* Tipo 4 */}
            <div>
              <div className="flex items-center justify-between text-xs mb-1.5">
                <span className="font-semibold text-amber-300">
                  Tipo 4 • Crespos (4A / 4B / 4C)
                </span>
                <span className="font-mono text-stone-300">
                  {estatisticas.crespos} cosméticos (
                  {Math.round((estatisticas.crespos / estatisticas.total) * 100)}%)
                </span>
              </div>
              <div className="h-2 w-full overflow-hidden rounded-full bg-stone-900 border border-stone-800">
                <div
                  className="h-full rounded-full bg-gradient-to-r from-amber-500 to-orange-400 transition-all duration-700"
                  style={{
                    width: `${Math.round((estatisticas.crespos / estatisticas.total) * 100)}%`,
                  }}
                />
              </div>
            </div>
          </div>

          <div className="pt-2 border-t border-stone-800 flex justify-end">
            <button
              onClick={() => onNavegar("catalogo")}
              className="inline-flex items-center gap-1.5 text-xs font-bold text-emerald-400 hover:text-emerald-300 transition"
            >
              <span>Filtrar curvaturas no Catálogo</span>
              <ArrowRight className="h-3.5 w-3.5" />
            </button>
          </div>
        </div>

        {/* Mix de Marcas Homologadas (6 colunas) */}
        <div className="rounded-3xl border border-stone-800/90 bg-[#131d18]/90 p-6 shadow-xl shadow-black/30 lg:col-span-6 space-y-4">
          <div className="flex items-center justify-between border-b border-stone-800 pb-3">
            <h3 className="font-serif text-base font-bold text-stone-100 flex items-center gap-2">
              <Database className="h-4 w-4 text-emerald-400" />
              <span>Mix de Marcas Parceiras Homologadas</span>
            </h3>
            <span className="text-xs text-amber-400 font-bold">4 Marcas Oficiais</span>
          </div>

          <p className="text-xs text-stone-400">
            Fornecedores profissionais certificados para rotinas de Slow Beauty e saúde da fibra.
          </p>

          <div className="grid grid-cols-2 gap-3">
            {estatisticas.marcasList.map((m) => (
              <div
                key={m.marca}
                className="flex flex-col justify-between rounded-2xl border border-stone-800 bg-[#0d1411]/90 p-3.5 transition hover:border-emerald-700/60"
              >
                <div>
                  <div className="flex items-center justify-between">
                    <h4 className="font-serif font-bold text-stone-100 text-sm">{m.marca}</h4>
                    <span className="rounded-full bg-stone-900 border border-stone-700 px-2 py-0.5 font-mono text-[10px] font-bold text-emerald-300">
                      {m.pct}%
                    </span>
                  </div>
                  <p className="mt-1 text-xs text-stone-400">
                    <strong className="text-stone-200">{m.count}</strong> fórmulas ativas
                  </p>
                </div>
                <div className="mt-3 text-[11px] text-stone-500 font-medium">
                  {m.marca === "Arvensis" && "Ativadores, Geleias e Co-Wash"}
                  {m.marca === "Curly Care" && "Acidificantes, Manteigas e Mousse"}
                  {m.marca === "Deva Curl" && "Delight, Angéll e No-Poo Original"}
                  {m.marca === "Kah-Noa" && "Finalizadores e Umectantes Naturais"}
                </div>
              </div>
            ))}
          </div>

          <div className="pt-2 border-t border-stone-800 flex justify-end">
            <button
              onClick={() => onNavegar("catalogo")}
              className="inline-flex items-center gap-1.5 text-xs font-bold text-emerald-400 hover:text-emerald-300 transition"
            >
              <span>Ver tabela completa das 4 marcas</span>
              <ArrowRight className="h-3.5 w-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* 5. PRODUTOS CARRO-CHEFE MAIS PRECRITOS PELO MOTOR */}
      <div className="rounded-3xl border border-stone-800/90 bg-[#131d18]/90 p-6 sm:p-7 shadow-2xl shadow-black/30 space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-stone-800 pb-4">
          <div>
            <h2 className="font-serif text-lg sm:text-xl font-bold text-stone-100 flex items-center gap-2">
              <Sparkle className="h-5 w-5 text-amber-400" />
              <span>Cosméticos Carro-Chefe da Matriz (Alta Prescrição)</span>
            </h2>
            <p className="mt-1 text-xs text-stone-400">
              Fórmulas-chave que respondem pelas maiores taxas de compatibilidade nas 4 personas.
            </p>
          </div>
          <button
            onClick={() => onNavegar("catalogo")}
            className="inline-flex items-center gap-1.5 text-xs font-bold text-emerald-400 hover:text-emerald-300"
          >
            <span>Ver todos os 27 cosméticos</span>
            <ArrowRight className="h-3.5 w-3.5" />
          </button>
        </div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {cosméticosDestaque.map((prod) => (
            <div
              key={prod.id}
              className="group flex flex-col justify-between rounded-2xl border border-stone-800/90 bg-[#0d1411]/90 p-4 transition-all duration-200 hover:border-emerald-600/70 hover:bg-[#101915] hover:-translate-y-0.5"
            >
              <div>
                <div className="flex items-center gap-3">
                  <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-xl border border-stone-800 bg-stone-900/90 p-1.5 shadow-inner">
                    <img
                      src={getImagemProduto(prod.nome)}
                      alt={prod.nome}
                      width={64}
                      height={64}
                      className="max-h-full max-w-full object-contain"
                      loading="lazy"
                      decoding="async"
                    />
                  </div>
                  <div className="min-w-0">
                    <span className="rounded bg-stone-900 border border-stone-800 px-1.5 py-0.5 font-mono text-[9px] font-bold text-stone-400">
                      {prod.id}
                    </span>
                    <h4 className="mt-1 font-serif font-bold text-stone-100 text-xs line-clamp-2 leading-snug">
                      {prod.nome}
                    </h4>
                    <span className="text-[11px] font-semibold text-amber-400">{prod.marca}</span>
                  </div>
                </div>

                <p className="mt-3 text-[11px] text-stone-400 line-clamp-2 leading-relaxed">
                  {prod.descricao}
                </p>

                <div className="mt-3 flex items-center justify-between text-[11px] border-t border-stone-800 pt-2">
                  <span className="text-stone-500">Curvaturas:</span>
                  <div className="flex gap-1">
                    {prod.curvaturas_indicadas.map((c) => (
                      <span
                        key={c}
                        className="rounded bg-stone-900 border border-stone-700 px-1 py-0.2 text-[9px] font-bold text-stone-300"
                      >
                        {c}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              <button
                onClick={() => setProdutoModal(prod)}
                className="mt-4 w-full rounded-xl border border-stone-700/80 bg-stone-900/90 py-1.5 text-xs font-semibold text-stone-200 transition hover:bg-emerald-950 hover:border-emerald-600 hover:text-emerald-200"
              >
                Inspecionar Ficha
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* 6. ATALHOS DIRETOS PARA AS TELAS SEGUINTES DO FUNIL */}
      <div>
        <h2 className="font-serif text-base sm:text-lg font-bold text-stone-200 mb-3 flex items-center gap-2">
          <Zap className="h-4 w-4 text-emerald-400" />
          <span>Aprofundar nos Módulos Especialistas</span>
        </h2>

        <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
          {/* Card Atalho 1: Telemetria */}
          <div
            onClick={() => onNavegar("telemetria")}
            className="group cursor-pointer rounded-2xl border border-stone-800/90 bg-[#131d18]/90 p-5 shadow-xl transition-all duration-200 hover:border-emerald-600/70 hover:bg-[#16221c] hover:-translate-y-0.5"
          >
            <div className="flex items-center gap-3">
              <div className="rounded-xl bg-emerald-950/90 border border-emerald-800/70 p-2.5 text-emerald-400 group-hover:scale-105 transition-transform">
                <Activity className="h-5 w-5" />
              </div>
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-400">
                  Módulo 02
                </span>
                <h3 className="font-serif font-bold text-stone-100 text-base">
                  Telemetria &amp; RNF-12
                </h3>
              </div>
            </div>
            <p className="mt-3 text-xs text-stone-400 leading-relaxed">
              Inspecione a coesão dos 4 clusters de K-Means, coeficientes estatísticos e
              especificações de infraestrutura do servidor.
            </p>
            <div className="mt-4 flex items-center gap-1.5 text-xs font-bold text-emerald-400 group-hover:text-emerald-300">
              <span>Acessar Telemetria Científica</span>
              <ArrowRight className="h-3.5 w-3.5 transition-transform group-hover:translate-x-1" />
            </div>
          </div>

          {/* Card Atalho 2: Catálogo */}
          <div
            onClick={() => onNavegar("catalogo")}
            className="group cursor-pointer rounded-2xl border border-stone-800/90 bg-[#131d18]/90 p-5 shadow-xl transition-all duration-200 hover:border-emerald-600/70 hover:bg-[#16221c] hover:-translate-y-0.5"
          >
            <div className="flex items-center gap-3">
              <div className="rounded-xl bg-emerald-950/90 border border-emerald-800/70 p-2.5 text-emerald-400 group-hover:scale-105 transition-transform">
                <Database className="h-5 w-5" />
              </div>
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-400">
                  Módulo 03
                </span>
                <h3 className="font-serif font-bold text-stone-100 text-base">
                  Catálogo &amp; Fórmulas
                </h3>
              </div>
            </div>
            <p className="mt-3 text-xs text-stone-400 leading-relaxed">
              Consulte e filtre os 27 cosméticos canônicos por marca, curvatura, densidade e alterne
              entre visualização em Cards ou Tabela Técnica.
            </p>
            <div className="mt-4 flex items-center gap-1.5 text-xs font-bold text-emerald-400 group-hover:text-emerald-300">
              <span>Abrir Gestão do Catálogo</span>
              <ArrowRight className="h-3.5 w-3.5 transition-transform group-hover:translate-x-1" />
            </div>
          </div>

          {/* Card Atalho 3: Simulador */}
          <div
            onClick={() => onNavegar("simulador")}
            className="group cursor-pointer rounded-2xl border border-stone-800/90 bg-[#131d18]/90 p-5 shadow-xl transition-all duration-200 hover:border-amber-600/70 hover:bg-[#16221c] hover:-translate-y-0.5"
          >
            <div className="flex items-center gap-3">
              <div className="rounded-xl bg-amber-950/90 border border-amber-800/70 p-2.5 text-amber-400 group-hover:scale-105 transition-transform">
                <FlaskConical className="h-5 w-5" />
              </div>
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider text-amber-400">
                  Módulo 04
                </span>
                <h3 className="font-serif font-bold text-stone-100 text-base">
                  Simulador Clínico (XAI)
                </h3>
              </div>
            </div>
            <p className="mt-3 text-xs text-stone-400 leading-relaxed">
              Audite em tempo real a resposta do motor: simule diagnósticos personalizados e
              inspecione a divisão convexa entre regras e salão.
            </p>
            <div className="mt-4 flex items-center gap-1.5 text-xs font-bold text-amber-400 group-hover:text-amber-300">
              <span>Iniciar Auditoria Clínica</span>
              <ArrowRight className="h-3.5 w-3.5 transition-transform group-hover:translate-x-1" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
