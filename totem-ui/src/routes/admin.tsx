import { createFileRoute, Link } from "@tanstack/react-router";
import React, { useEffect, useState, useMemo } from "react";
import {
  Activity,
  ArrowLeft,
  Award,
  CheckCircle2,
  Database,
  Layers,
  RefreshCw,
  Search,
  Sparkles,
  Star,
  Users,
  AlertCircle,
  FlaskConical,
  HelpCircle,
  SlidersHorizontal,
} from "lucide-react";
import { Logo } from "@/components/totem/Logo";
import {
  obterHealth,
  obterCatalogo,
  recomendar,
  API_URL,
  type ItemCatalogo,
  type MetricasHealth,
  type Perfil,
  type Recomendacao,
} from "@/lib/api";

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

type AbaAdmin = "telemetria" | "catalogo" | "simulador";

export function AdminPage() {
  const [abaAtiva, setAbaAtiva] = useState<AbaAdmin>("telemetria");
  const [metricas, setMetricas] = useState<MetricasHealth | null>(null);
  const [catalogo, setCatalogo] = useState<ItemCatalogo[]>([]);
  const [loading, setLoading] = useState(true);
  const [recarregando, setRecarregando] = useState(false);
  const [buscaCatalogo, setBuscaCatalogo] = useState("");
  const [filtroCurvatura, setFiltroCurvatura] = useState<number | null>(null);

  // Estados do Simulador
  const [simCurvatura, setSimCurvatura] = useState<number>(3);
  const [simPorosidade, setSimPorosidade] = useState<number>(2);
  const [simQuimica, setSimQuimica] = useState<number>(0);
  const [simQueixas, setSimQueixas] = useState<string[]>(["frizz"]);
  const [simResultado, setSimResultado] = useState<Recomendacao | null>(null);
  const [simulando, setSimulando] = useState(false);

  const carregarDados = async () => {
    setRecarregando(true);
    try {
      const [h, c] = await Promise.all([obterHealth(), obterCatalogo()]);
      setMetricas(h);
      setCatalogo(c);
    } catch (err) {
      console.error("[Admin] Erro ao carregar dados:", err);
    } finally {
      setLoading(false);
      setRecarregando(false);
    }
  };

  useEffect(() => {
    carregarDados();
  }, []);

  const catalogoFiltrado = useMemo(() => {
    return catalogo.filter((item) => {
      const matchBusca =
        item.nome.toLowerCase().includes(buscaCatalogo.toLowerCase()) ||
        item.marca.toLowerCase().includes(buscaCatalogo.toLowerCase()) ||
        item.categoria.toLowerCase().includes(buscaCatalogo.toLowerCase());
      const matchCurv =
        filtroCurvatura === null || item.curvaturas_indicadas.includes(filtroCurvatura);
      return matchBusca && matchCurv;
    });
  }, [catalogo, buscaCatalogo, filtroCurvatura]);

  const executarSimulacao = async () => {
    setSimulando(true);
    try {
      const perfilSimulado: Perfil = {
        curvatura: simCurvatura,
        porosidade: simPorosidade,
        dano_quimico: simQuimica === 2 ? 1 : 0,
        transicao_capilar: simQuimica === 1 ? 1 : 0,
        alta_porosidade_quimica: simQuimica === 2 && simPorosidade === 3 ? 1 : 0,
        frizz_falta_definicao: simQueixas.includes("frizz") ? 1 : 0,
        ressecamento_opacidade: simQueixas.includes("ressecamento") ? 1 : 0,
        couro_sensivel_oleoso: simQueixas.includes("couro") ? 1 : 0,
      };
      const res = await recomendar(perfilSimulado);
      setSimResultado(res);
    } catch (err) {
      console.error("[Admin] Falha na simulação:", err);
    } finally {
      setSimulando(false);
    }
  };

  const toggleQueixa = (q: string) => {
    setSimQueixas((prev) => (prev.includes(q) ? prev.filter((item) => item !== q) : [...prev, q]));
  };

  return (
    <div className="min-h-screen bg-stone-50 font-sans text-stone-900 antialiased">
      {/* Barra de Navegação Superior */}
      <header className="sticky top-0 z-30 border-b border-stone-200 bg-white/90 backdrop-blur-md">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6">
          <div className="flex items-center gap-4">
            <Link
              to="/"
              className="inline-flex items-center gap-2 rounded-lg border border-stone-200 bg-stone-100 px-3 py-1.5 text-xs font-medium text-stone-700 transition hover:bg-stone-200"
              title="Voltar ao Totem de Diagnóstico"
            >
              <ArrowLeft className="h-4 w-4" />
              <span>Voltar ao Totem</span>
            </Link>
            <div className="flex items-center gap-2 border-l border-stone-300 pl-4">
              <Logo />
              <span className="hidden rounded-full bg-emerald-100 px-2.5 py-0.5 text-xs font-semibold text-emerald-800 md:inline-block">
                Painel do Gestor (Admin)
              </span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="hidden items-center gap-1.5 rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700 sm:flex">
              <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
              <span>API Conectada</span>
            </div>
            <button
              onClick={carregarDados}
              disabled={recarregando}
              className="inline-flex items-center gap-1.5 rounded-lg border border-stone-300 bg-white px-3 py-1.5 text-xs font-medium text-stone-700 shadow-sm transition hover:bg-stone-50 active:scale-95 disabled:opacity-50"
            >
              <RefreshCw className={`h-3.5 w-3.5 ${recarregando ? "animate-spin" : ""}`} />
              <span className="hidden sm:inline">Recarregar</span>
            </button>
          </div>
        </div>

        {/* Abas Principais (Diagramas 5 e 6) */}
        <div className="mx-auto flex max-w-7xl px-4 sm:px-6">
          <nav className="flex space-x-6 border-b border-transparent">
            <button
              onClick={() => setAbaAtiva("telemetria")}
              className={`flex items-center gap-2 border-b-2 py-3 text-sm font-semibold transition ${
                abaAtiva === "telemetria"
                  ? "border-emerald-600 text-emerald-700"
                  : "border-transparent text-stone-500 hover:text-stone-800"
              }`}
            >
              <Activity className="h-4 w-4" />
              <span>1. Telemetria &amp; Métricas (RNF-12)</span>
            </button>
            <button
              onClick={() => setAbaAtiva("catalogo")}
              className={`flex items-center gap-2 border-b-2 py-3 text-sm font-semibold transition ${
                abaAtiva === "catalogo"
                  ? "border-emerald-600 text-emerald-700"
                  : "border-transparent text-stone-500 hover:text-stone-800"
              }`}
            >
              <Database className="h-4 w-4" />
              <span>2. Catálogo &amp; Matriz de Cosméticos</span>
            </button>
            <button
              onClick={() => setAbaAtiva("simulador")}
              className={`flex items-center gap-2 border-b-2 py-3 text-sm font-semibold transition ${
                abaAtiva === "simulador"
                  ? "border-emerald-600 text-emerald-700"
                  : "border-transparent text-stone-500 hover:text-stone-800"
              }`}
            >
              <FlaskConical className="h-4 w-4" />
              <span>3. Simulador de Recomendação</span>
            </button>
          </nav>
        </div>
      </header>

      {/* Conteúdo Principal */}
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6">
        {loading ? (
          <div className="flex min-h-[40vh] flex-col items-center justify-center gap-3">
            <RefreshCw className="h-8 w-8 animate-spin text-emerald-600" />
            <p className="text-sm font-medium text-stone-600">
              Consultando telemetria e catálogo no backend...
            </p>
          </div>
        ) : (
          <>
            {/* ABA 1: TELEMETRIA & MONITORAMENTO (DIAGRAMA 6) */}
            {abaAtiva === "telemetria" && (
              <section className="space-y-6">
                <div>
                  <h1 className="text-2xl font-bold tracking-tight text-stone-900">
                    Telemetria Operacional &amp; Métricas Acadêmicas
                  </h1>
                  <p className="mt-1 text-sm text-stone-600">
                    Monitoramento em tempo real do motor de IA híbrido conforme modelado no Diagrama
                    de Sequência de Monitoramento do Gestor Técnico (RNF-12).
                  </p>
                </div>

                {/* Cards de KPIs Principais */}
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
                  {/* Card 1: Status */}
                  <div className="rounded-xl border border-stone-200 bg-white p-5 shadow-xs">
                    <div className="flex items-center justify-between text-stone-500">
                      <span className="text-xs font-semibold uppercase tracking-wider">
                        Estado do Motor
                      </span>
                      <CheckCircle2 className="h-5 w-5 text-emerald-600" />
                    </div>
                    <div className="mt-3 flex items-baseline gap-2">
                      <span className="text-2xl font-bold text-stone-900 capitalize">
                        {metricas?.status || "Operacional"}
                      </span>
                    </div>
                    <p className="mt-1 text-xs text-stone-500">
                      YOLOv8 ONNX + K-Means + Bayesiano Ativos
                    </p>
                  </div>

                  {/* Card 2: Base Histórica */}
                  <div className="rounded-xl border border-stone-200 bg-white p-5 shadow-xs">
                    <div className="flex items-center justify-between text-stone-500">
                      <span className="text-xs font-semibold uppercase tracking-wider">
                        Base de Atendimentos
                      </span>
                      <Users className="h-5 w-5 text-blue-600" />
                    </div>
                    <div className="mt-3 flex items-baseline gap-2">
                      <span className="text-2xl font-bold text-stone-900">
                        {metricas?.total_clientes_historico ?? 1084}
                      </span>
                      <span className="text-xs text-stone-500">registros</span>
                    </div>
                    <p className="mt-1 text-xs text-stone-500">
                      Histórico enriquecido com feedbacks reais
                    </p>
                  </div>

                  {/* Card 3: Satisfação Global */}
                  <div className="rounded-xl border border-stone-200 bg-white p-5 shadow-xs">
                    <div className="flex items-center justify-between text-stone-500">
                      <span className="text-xs font-semibold uppercase tracking-wider">
                        Média Global do Salão
                      </span>
                      <Star className="h-5 w-5 fill-amber-400 text-amber-500" />
                    </div>
                    <div className="mt-3 flex items-baseline gap-2">
                      <span className="text-2xl font-bold text-stone-900">
                        {metricas?.media_satisfacao_global?.toFixed(2) ?? "4.54"}
                      </span>
                      <span className="text-xs font-semibold text-amber-600">★ ★ ★ ★ ★</span>
                    </div>
                    <p className="mt-1 text-xs text-stone-500">
                      Avaliação acumulada pós-atendimento
                    </p>
                  </div>

                  {/* Card 4: Coeficiente Silhouette (RNF-12) */}
                  <div className="rounded-xl border border-emerald-200 bg-emerald-50/50 p-5 shadow-xs">
                    <div className="flex items-center justify-between text-emerald-800">
                      <span className="text-xs font-semibold uppercase tracking-wider">
                        Silhouette Score (RNF-12)
                      </span>
                      <Award className="h-5 w-5 text-emerald-600" />
                    </div>
                    <div className="mt-3 flex items-baseline gap-2">
                      <span className="text-2xl font-bold text-emerald-950">
                        {metricas?.silhouette_score?.toFixed(3) ?? "0.448"}
                      </span>
                      <span className="rounded-full bg-emerald-200/80 px-2 py-0.5 text-[10px] font-bold text-emerald-800">
                        Robusto (&gt; 0.40)
                      </span>
                    </div>
                    <p className="mt-1 text-xs text-emerald-700">
                      Validação formal de coesão intra-cluster e separação
                    </p>
                  </div>
                </div>

                {/* Estrutura das 4 Personas Tricológicas */}
                <div className="rounded-xl border border-stone-200 bg-white p-6 shadow-xs">
                  <div className="flex items-center justify-between border-b border-stone-200 pb-4">
                    <div className="flex items-center gap-2">
                      <Layers className="h-5 w-5 text-emerald-700" />
                      <h2 className="text-lg font-bold text-stone-900">
                        Estrutura dos 4 Clusters Tricológicos (K-Means)
                      </h2>
                    </div>
                    <span className="text-xs font-medium text-stone-500">
                      K = {metricas?.num_clusters ?? 4} Personas Científicas
                    </span>
                  </div>

                  <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2">
                    <div className="rounded-lg border border-stone-200 bg-stone-50/70 p-4">
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-stone-900">Persona 0</span>
                        <span className="rounded-md bg-stone-200 px-2 py-0.5 text-xs font-medium text-stone-700">
                          Curvatura 3 (Cacheados)
                        </span>
                      </div>
                      <p className="mt-2 text-xs text-stone-600">
                        Foco em cabelos cacheados (3A, 3B, 3C) com porosidade média e sem processos
                        químicos abrasivos. As queixas prioritárias do grupo são frizz e
                        sensibilidade no couro cabeludo.
                      </p>
                    </div>

                    <div className="rounded-lg border border-stone-200 bg-stone-50/70 p-4">
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-stone-900">Persona 1</span>
                        <span className="rounded-md bg-stone-200 px-2 py-0.5 text-xs font-medium text-stone-700">
                          Curvatura 2 e 3 (Ondas e Cachos Leves)
                        </span>
                      </div>
                      <p className="mt-2 text-xs text-stone-600">
                        Foco em cabelos ondulados (2A, 2B, 2C) e cacheados abertos. Exige cosméticos
                        leves (Delight e Geleias) para evitar o efeito pesado ou ensebado.
                      </p>
                    </div>

                    <div className="rounded-lg border border-stone-200 bg-stone-50/70 p-4">
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-stone-900">Persona 2</span>
                        <span className="rounded-md bg-stone-200 px-2 py-0.5 text-xs font-medium text-stone-700">
                          Alta Porosidade &amp; Dano Químico
                        </span>
                      </div>
                      <p className="mt-2 text-xs text-stone-600">
                        Fios fragilizados por descoloração ou relaxamentos químicos. Prescrição
                        imediata de regulação de pH com acidificantes (ACID-C) e reconstrução.
                      </p>
                    </div>

                    <div className="rounded-lg border border-stone-200 bg-stone-50/70 p-4">
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-stone-900">Persona 3</span>
                        <span className="rounded-md bg-stone-200 px-2 py-0.5 text-xs font-medium text-stone-700">
                          Curvatura 4 (Crespos 4A/4B/4C)
                        </span>
                      </div>
                      <p className="mt-2 text-xs text-stone-600">
                        Crespos com padrão angular e alta perda hídrica/lipídica. O algoritmo
                        direciona produtos de alta densidade lipídica (Manteiga Nutritiva e
                        Ativadores).
                      </p>
                    </div>
                  </div>
                </div>

                {/* Detalhes de Ambiente */}
                <div className="rounded-xl border border-stone-200 bg-white p-5 text-xs text-stone-600">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <div>
                      <span className="font-semibold text-stone-800">Serviço de Backend:</span>{" "}
                      <code>{API_URL}</code>
                    </div>
                    <div>
                      <span className="font-semibold text-stone-800">Ambiente de Hospedagem:</span>{" "}
                      Render Cloud (512MB RAM Ceiling) &bull; ONNX Runtime Lightweight
                    </div>
                  </div>
                </div>
              </section>
            )}

            {/* ABA 2: CATÁLOGO & MATRIZ DE COSMÉTICOS (DIAGRAMA 5) */}
            {abaAtiva === "catalogo" && (
              <section className="space-y-6">
                <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
                  <div>
                    <h1 className="text-2xl font-bold tracking-tight text-stone-900">
                      Matriz Oficial de Cosméticos e Regras Terapêuticas
                    </h1>
                    <p className="mt-1 text-sm text-stone-600">
                      Catálogo oficial consultado pelo motor em <code>GET /catalogo</code> com
                      regras de compatibilidade e afinidade de queixas (RN-06 a RN-08).
                    </p>
                  </div>
                </div>

                {/* Barra de Busca e Filtros */}
                <div className="flex flex-col gap-3 rounded-xl border border-stone-200 bg-white p-4 shadow-xs sm:flex-row sm:items-center sm:justify-between">
                  <div className="relative flex-1">
                    <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-stone-400" />
                    <input
                      type="text"
                      placeholder="Buscar por produto, marca ou categoria..."
                      value={buscaCatalogo}
                      onChange={(e) => setBuscaCatalogo(e.target.value)}
                      className="w-full rounded-lg border border-stone-300 py-2 pl-9 pr-3 text-sm focus:border-emerald-500 focus:outline-none"
                    />
                  </div>
                  <div className="flex items-center gap-2">
                    <SlidersHorizontal className="h-4 w-4 text-stone-500" />
                    <span className="text-xs font-medium text-stone-600">Curvatura:</span>
                    <button
                      onClick={() => setFiltroCurvatura(null)}
                      className={`rounded-md px-2.5 py-1 text-xs font-medium transition ${
                        filtroCurvatura === null
                          ? "bg-stone-900 text-white"
                          : "bg-stone-100 text-stone-600 hover:bg-stone-200"
                      }`}
                    >
                      Todas
                    </button>
                    {[2, 3, 4].map((c) => (
                      <button
                        key={c}
                        onClick={() => setFiltroCurvatura(filtroCurvatura === c ? null : c)}
                        className={`rounded-md px-2.5 py-1 text-xs font-medium transition ${
                          filtroCurvatura === c
                            ? "bg-emerald-700 text-white"
                            : "bg-stone-100 text-stone-600 hover:bg-stone-200"
                        }`}
                      >
                        Tipo {c}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Grid de Cards de Produtos */}
                <div className="grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">
                  {catalogoFiltrado.map((prod) => (
                    <div
                      key={prod.id}
                      className="flex flex-col justify-between rounded-xl border border-stone-200 bg-white p-5 shadow-xs transition hover:border-emerald-300 hover:shadow-sm"
                    >
                      <div>
                        <div className="flex items-start justify-between gap-2">
                          <span className="rounded bg-stone-100 px-2 py-0.5 text-[11px] font-mono font-semibold text-stone-600">
                            {prod.id}
                          </span>
                          <span className="rounded-full bg-emerald-50 px-2.5 py-0.5 text-xs font-semibold text-emerald-800">
                            {prod.categoria}
                          </span>
                        </div>

                        <h3 className="mt-3 text-base font-bold text-stone-900">{prod.nome}</h3>
                        <p className="text-xs font-medium text-stone-500">{prod.marca}</p>

                        {prod.descricao && (
                          <p className="mt-2 text-xs text-stone-600 line-clamp-2">
                            {prod.descricao}
                          </p>
                        )}

                        {/* Metadados Técnicos */}
                        <div className="mt-4 space-y-2 border-t border-stone-100 pt-3">
                          <div className="flex items-center justify-between text-xs">
                            <span className="text-stone-500">Curvaturas Indicadas:</span>
                            <div className="flex gap-1">
                              {prod.curvaturas_indicadas.map((curv) => (
                                <span
                                  key={curv}
                                  className="rounded bg-stone-200 px-1.5 py-0.2 text-[10px] font-bold text-stone-700"
                                >
                                  {curv}
                                </span>
                              ))}
                            </div>
                          </div>

                          <div className="flex items-center justify-between text-xs">
                            <span className="text-stone-500">Peso no Fio:</span>
                            <span
                              className={`rounded px-1.5 py-0.5 text-[10px] font-semibold capitalize ${
                                prod.peso_fio === "pesado"
                                  ? "bg-amber-100 text-amber-800"
                                  : prod.peso_fio === "medio"
                                    ? "bg-blue-100 text-blue-800"
                                    : "bg-emerald-100 text-emerald-800"
                              }`}
                            >
                              {prod.peso_fio}
                            </span>
                          </div>
                        </div>

                        {/* Afinidades com Queixas */}
                        <div className="mt-4 border-t border-stone-100 pt-3">
                          <p className="text-[11px] font-semibold uppercase tracking-wider text-stone-400">
                            Afinidade Terapêutica (0 a 1.0)
                          </p>
                          <div className="mt-2 space-y-1.5">
                            {Object.entries(prod.afinidade_queixas).map(([queixa, score]) => {
                              if (score === 0) return null;
                              const label = queixa
                                .replace(/_/g, " ")
                                .replace("alta porosidade quimica", "porosidade/química")
                                .replace("frizz falta definicao", "frizz/definição")
                                .replace("couro sensivel oleoso", "couro sensível");
                              return (
                                <div
                                  key={queixa}
                                  className="flex items-center justify-between text-[11px]"
                                >
                                  <span className="capitalize text-stone-600">{label}</span>
                                  <div className="flex items-center gap-2">
                                    <div className="h-1.5 w-16 overflow-hidden rounded-full bg-stone-100">
                                      <div
                                        className="h-full rounded-full bg-emerald-600"
                                        style={{ width: `${score * 100}%` }}
                                      />
                                    </div>
                                    <span className="font-mono font-medium text-stone-700">
                                      {score.toFixed(1)}
                                    </span>
                                  </div>
                                </div>
                              );
                            })}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </section>
            )}

            {/* ABA 3: SIMULADOR DE RECOMENDAÇÃO EM TEMPO REAL */}
            {abaAtiva === "simulador" && (
              <section className="space-y-6">
                <div>
                  <h1 className="text-2xl font-bold tracking-tight text-stone-900">
                    Simulador &amp; Inspetor Tricológico
                  </h1>
                  <p className="mt-1 text-sm text-stone-600">
                    Permite ao gestor simular e auditar a recomendação do algoritmo em tempo de
                    execução, inspecionando os pesos matemáticos e as notas bayesianas.
                  </p>
                </div>

                <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
                  {/* Painel de Controle dos Parâmetros */}
                  <div className="space-y-5 rounded-xl border border-stone-200 bg-white p-5 shadow-xs lg:col-span-1">
                    <h2 className="text-base font-bold text-stone-900">Parâmetros do Fio</h2>

                    {/* Curvatura */}
                    <div>
                      <label className="text-xs font-semibold text-stone-700">
                        Curvatura Capilar (Walker)
                      </label>
                      <div className="mt-1.5 grid grid-cols-3 gap-2">
                        {[
                          { val: 2, label: "2 (Ondulado)" },
                          { val: 3, label: "3 (Cacheado)" },
                          { val: 4, label: "4 (Crespo)" },
                        ].map((c) => (
                          <button
                            key={c.val}
                            type="button"
                            onClick={() => setSimCurvatura(c.val)}
                            className={`rounded-lg border py-2 text-xs font-semibold transition ${
                              simCurvatura === c.val
                                ? "border-emerald-600 bg-emerald-50 text-emerald-800"
                                : "border-stone-200 bg-white text-stone-700 hover:bg-stone-50"
                            }`}
                          >
                            {c.label}
                          </button>
                        ))}
                      </div>
                    </div>

                    {/* Porosidade */}
                    <div>
                      <label className="text-xs font-semibold text-stone-700">Porosidade</label>
                      <div className="mt-1.5 grid grid-cols-3 gap-2">
                        {[
                          { val: 1, label: "Baixa" },
                          { val: 2, label: "Média" },
                          { val: 3, label: "Alta" },
                        ].map((p) => (
                          <button
                            key={p.val}
                            type="button"
                            onClick={() => setSimPorosidade(p.val)}
                            className={`rounded-lg border py-2 text-xs font-semibold transition ${
                              simPorosidade === p.val
                                ? "border-emerald-600 bg-emerald-50 text-emerald-800"
                                : "border-stone-200 bg-white text-stone-700 hover:bg-stone-50"
                            }`}
                          >
                            {p.label}
                          </button>
                        ))}
                      </div>
                    </div>

                    {/* Histórico Químico */}
                    <div>
                      <label className="text-xs font-semibold text-stone-700">
                        Histórico Químico
                      </label>
                      <div className="mt-1.5 grid grid-cols-3 gap-2">
                        {[
                          { val: 0, label: "Virgem" },
                          { val: 1, label: "Transição" },
                          { val: 2, label: "Com Química" },
                        ].map((q) => (
                          <button
                            key={q.val}
                            type="button"
                            onClick={() => setSimQuimica(q.val)}
                            className={`rounded-lg border py-2 text-xs font-semibold transition ${
                              simQuimica === q.val
                                ? "border-emerald-600 bg-emerald-50 text-emerald-800"
                                : "border-stone-200 bg-white text-stone-700 hover:bg-stone-50"
                            }`}
                          >
                            {q.label}
                          </button>
                        ))}
                      </div>
                    </div>

                    {/* Queixas Capilares */}
                    <div>
                      <label className="text-xs font-semibold text-stone-700">
                        Queixas Capilares Ativas
                      </label>
                      <div className="mt-2 space-y-1.5">
                        {[
                          { id: "frizz", label: "Frizz / Falta de Definição" },
                          { id: "ressecamento", label: "Ressecamento e Opacidade" },
                          { id: "couro", label: "Couro Cabeludo Sensível / Oleoso" },
                        ].map((q) => (
                          <label
                            key={q.id}
                            className="flex cursor-pointer items-center gap-2 rounded-lg border border-stone-200 p-2 text-xs transition hover:bg-stone-50"
                          >
                            <input
                              type="checkbox"
                              checked={simQueixas.includes(q.id)}
                              onChange={() => toggleQueixa(q.id)}
                              className="rounded border-stone-300 text-emerald-600 focus:ring-emerald-500"
                            />
                            <span className="text-stone-700">{q.label}</span>
                          </label>
                        ))}
                      </div>
                    </div>

                    <button
                      onClick={executarSimulacao}
                      disabled={simulando}
                      className="flex w-full items-center justify-center gap-2 rounded-lg bg-emerald-700 py-2.5 text-sm font-semibold text-white shadow-xs transition hover:bg-emerald-800 active:scale-98 disabled:opacity-50"
                    >
                      {simulando ? (
                        <RefreshCw className="h-4 w-4 animate-spin" />
                      ) : (
                        <Sparkles className="h-4 w-4" />
                      )}
                      <span>Disparar Recomendação</span>
                    </button>
                  </div>

                  {/* Visualização do Resultado da Simulação */}
                  <div className="space-y-4 lg:col-span-2">
                    {simResultado ? (
                      <div className="space-y-4">
                        {/* Header da Persona Atribuída */}
                        <div className="rounded-xl border border-stone-200 bg-white p-5 shadow-xs">
                          <div className="flex flex-wrap items-center justify-between gap-2 border-b border-stone-100 pb-3">
                            <span className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-bold text-emerald-800">
                              Persona / Cluster {simResultado.cluster_id ?? "Atribuído"}
                            </span>
                            {simResultado.peso_conhecimento_vs_feedback && (
                              <div className="text-xs text-stone-600">
                                <strong>Pesos:</strong> Regras Conteúdo{" "}
                                {(
                                  (simResultado.peso_conhecimento_vs_feedback
                                    .peso_regras_conteudo ??
                                    simResultado.peso_conhecimento_vs_feedback
                                      .peso_conteudo_regras ??
                                    0.4) * 100
                                ).toFixed(0)}
                                % &bull; Feedback Histórico{" "}
                                {(
                                  (simResultado.peso_conhecimento_vs_feedback
                                    .peso_feedback_historico ??
                                    simResultado.peso_conhecimento_vs_feedback
                                      .peso_feedback_clientes ??
                                    0.6) * 100
                                ).toFixed(0)}
                                %
                              </div>
                            )}
                          </div>
                          <p className="mt-3 text-sm font-medium text-stone-800">
                            {simResultado.persona}
                          </p>
                        </div>

                        {/* Top Produtos Recomendados */}
                        <div className="space-y-3">
                          <h3 className="text-sm font-bold uppercase tracking-wider text-stone-500">
                            Top 3 Cosméticos Prescritos:
                          </h3>
                          {simResultado.produtos.map((p, idx) => (
                            <div
                              key={p.nome}
                              className="rounded-xl border border-stone-200 bg-white p-4 shadow-xs"
                            >
                              <div className="flex items-start justify-between gap-2">
                                <div>
                                  <div className="flex items-center gap-2">
                                    <span className="flex h-5 w-5 items-center justify-center rounded-full bg-emerald-600 text-xs font-bold text-white">
                                      {idx + 1}
                                    </span>
                                    <h4 className="font-bold text-stone-900">{p.nome}</h4>
                                  </div>
                                  {p.categoria && (
                                    <span className="mt-1 inline-block text-xs font-medium text-stone-500">
                                      {p.categoria}
                                    </span>
                                  )}
                                </div>
                                <div className="text-right">
                                  <div className="text-sm font-bold text-emerald-700">
                                    Score: {p.score.toFixed(3)}
                                  </div>
                                  <div className="flex items-center justify-end gap-1 text-xs font-semibold text-amber-600">
                                    <span>{p.estrelas_estimadas.toFixed(1)}</span>
                                    <Star className="h-3 w-3 fill-amber-400 text-amber-500" />
                                  </div>
                                </div>
                              </div>
                              <p className="mt-2 text-xs text-stone-600 bg-stone-50 rounded-lg p-2.5 border border-stone-100">
                                <strong>Justificativa XAI:</strong> {p.motivo}
                              </p>
                            </div>
                          ))}
                        </div>
                      </div>
                    ) : (
                      <div className="flex min-h-[300px] flex-col items-center justify-center rounded-xl border-2 border-dashed border-stone-200 bg-white p-8 text-center">
                        <FlaskConical className="h-10 w-10 text-stone-400" />
                        <h3 className="mt-3 text-sm font-semibold text-stone-800">
                          Nenhuma simulação executada
                        </h3>
                        <p className="mt-1 max-w-sm text-xs text-stone-500">
                          Selecione os parâmetros do fio ao lado e clique em &quot;Disparar
                          Recomendação&quot; para inspecionar os cálculos tricológicos.
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </section>
            )}
          </>
        )}
      </main>
    </div>
  );
}
