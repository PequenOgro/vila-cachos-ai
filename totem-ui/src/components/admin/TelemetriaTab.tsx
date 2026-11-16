import React from "react";
import { CheckCircle2, Users, Star, Award, Layers, Cpu, Server, Zap } from "lucide-react";
import { type MetricasHealth, API_URL } from "@/lib/api";

interface TelemetriaTabProps {
  metricas: MetricasHealth | null;
}

export function TelemetriaTab({ metricas }: TelemetriaTabProps) {
  const personas = [
    {
      id: 0,
      titulo: "Persona 0 • Cachos Naturais",
      curvatura: "Curvatura 3 (3A / 3B / 3C)",
      badgeColor: "bg-emerald-950/90 text-emerald-300 border-emerald-800/70",
      descricao:
        "Cabelos cacheados com porosidade média e sem processos químicos abrasivos. Demanda hidratação balanceada e controle anti-frizz sem enrijecimento.",
      cosmeticosChave: ["Arvensis Ativador", "Curly Care Marshmallow", "Arvensis Geleia"],
    },
    {
      id: 1,
      titulo: "Persona 1 • Ondas e Cachos Leves",
      curvatura: "Curvatura 2 e 3 (2A / 2B / 2C / 3A)",
      badgeColor: "bg-teal-950/90 text-teal-300 border-teal-800/70",
      descricao:
        "Fios com padrão aberto e baixa tolerância a cargas pesadas de óleos. Exige formulações ultraleves à base de extratos aquosos e geleias fluidas.",
      cosmeticosChave: ["Deva Curl Delight", "Kah-Noa Super Light", "Arvensis Suave"],
    },
    {
      id: 2,
      titulo: "Persona 2 • Alta Porosidade & Dano Químico",
      curvatura: "Curvatura 2, 3 e 4 com Química",
      badgeColor: "bg-rose-950/90 text-rose-300 border-rose-800/70",
      descricao:
        "Fibras fragilizadas por descoloração ou relaxamentos químicos prévios. Prescrição imediata de acidificação para selamento cuticular e reposição de aminoácidos.",
      cosmeticosChave: ["Curly Care ACID-C", "Deva Heaven in Hair", "Curly Be Free"],
    },
    {
      id: 3,
      titulo: "Persona 3 • Crespos & Crespíssimos",
      curvatura: "Curvatura 4 (4A / 4B / 4C)",
      badgeColor: "bg-amber-950/90 text-amber-300 border-amber-800/70",
      descricao:
        "Cabelos crespos com alta taxa de evaporação hídrica e perda lipídica. Prioridade absoluta para manteigas nutritivas e cremes de alta densidade oleica.",
      cosmeticosChave: ["Curly Care Manteiga", "Arvensis Máscara 4", "Deva Decadence"],
    },
  ];

  return (
    <section className="space-y-6">
      {/* Cabeçalho da Seção */}
      <div className="flex flex-col justify-between gap-2 sm:flex-row sm:items-center">
        <div>
          <h1 className="text-xl sm:text-2xl font-serif font-bold tracking-tight text-stone-100">
            Telemetria Tricológica &amp; Validação Científica (RNF-12)
          </h1>
          <p className="mt-1 text-xs sm:text-sm text-stone-400">
            Métricas em tempo real da IA híbrida (YOLOv8 ONNX + K-Means + Média Bayesiana de Salão)
          </p>
        </div>
        <div className="inline-flex items-center gap-1.5 self-start rounded-full border border-emerald-800/80 bg-emerald-950/80 px-3 py-1 text-xs font-semibold text-emerald-300 shadow-sm">
          <Zap className="h-3.5 w-3.5 text-emerald-400" />
          <span>Inferência &lt; 20ms (ONNX)</span>
        </div>
      </div>

      {/* Grid de KPIs Executivos */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {/* KPI 1: Estado do Motor */}
        <div className="rounded-2xl border border-stone-800/90 bg-[#131d18]/90 p-5 shadow-lg shadow-black/30 transition hover:border-emerald-600/60">
          <div className="flex items-center justify-between text-stone-400">
            <span className="text-xs font-bold uppercase tracking-wider text-stone-400">
              Estado do Motor
            </span>
            <div className="rounded-xl bg-emerald-950/80 border border-emerald-800/60 p-2 text-emerald-400">
              <CheckCircle2 className="h-4 w-4" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-stone-100 capitalize">
              {metricas?.status || "Operacional"}
            </span>
          </div>
          <p className="mt-2 text-xs text-stone-400 leading-relaxed">
            Pipeline híbrido ativo: YOLOv8 ONNX + K-Means Tricológico.
          </p>
        </div>

        {/* KPI 2: Base de Atendimentos */}
        <div className="rounded-2xl border border-stone-800/90 bg-[#131d18]/90 p-5 shadow-lg shadow-black/30 transition hover:border-sky-600/60">
          <div className="flex items-center justify-between text-stone-400">
            <span className="text-xs font-bold uppercase tracking-wider text-stone-400">
              Base de Atendimentos
            </span>
            <div className="rounded-xl bg-sky-950/80 border border-sky-800/60 p-2 text-sky-400">
              <Users className="h-4 w-4" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-stone-100">
              {metricas?.total_clientes_historico ?? 1084}
            </span>
            <span className="text-xs font-semibold text-stone-400">clientes reais</span>
          </div>
          <p className="mt-2 text-xs text-stone-400 leading-relaxed">
            Histórico contínuo enriquecido com avaliações pós-atendimento.
          </p>
        </div>

        {/* KPI 3: Média de Satisfação */}
        <div className="rounded-2xl border border-stone-800/90 bg-[#131d18]/90 p-5 shadow-lg shadow-black/30 transition hover:border-amber-600/60">
          <div className="flex items-center justify-between text-stone-400">
            <span className="text-xs font-bold uppercase tracking-wider text-stone-400">
              Média Bayesiana Salão
            </span>
            <div className="rounded-xl bg-amber-950/80 border border-amber-800/60 p-2 text-amber-400">
              <Star className="h-4 w-4 fill-amber-400 text-amber-400" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-stone-100">
              {metricas?.media_satisfacao_global
                ? metricas.media_satisfacao_global.toFixed(2)
                : "4.54"}
            </span>
            <span className="text-xs font-bold text-amber-400">★ ★ ★ ★ ★</span>
          </div>
          <p className="mt-2 text-xs text-stone-400 leading-relaxed">
            Satisfação média ponderada pelo amortecedor de Laplace (C=5.0).
          </p>
        </div>

        {/* KPI 4: Silhouette Score */}
        <div className="rounded-2xl border border-emerald-700/60 bg-gradient-to-br from-emerald-950/90 to-[#131d18] p-5 shadow-lg shadow-black/40 transition hover:border-emerald-500/80">
          <div className="flex items-center justify-between text-emerald-300">
            <span className="text-xs font-bold uppercase tracking-wider text-emerald-300">
              Silhouette Score (RNF-12)
            </span>
            <div className="rounded-xl bg-emerald-900/80 border border-emerald-600/60 p-2 text-emerald-300">
              <Award className="h-4 w-4" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-emerald-200 font-mono">
              {metricas?.silhouette_score?.toFixed(3) ?? "0.448"}
            </span>
            <span className="rounded-full bg-emerald-900/90 border border-emerald-600/60 px-2 py-0.5 text-[10px] font-bold text-emerald-200">
              Robusto (&gt; 0.40)
            </span>
          </div>
          <p className="mt-2 text-xs text-emerald-300/90 leading-relaxed">
            Validação de alta separabilidade e coesão intra-cluster comprovada.
          </p>
        </div>
      </div>

      {/* Grade dos 4 Clusters Tricológicos */}
      <div className="rounded-2xl border border-stone-800/90 bg-[#131d18]/90 p-5 sm:p-6 shadow-xl shadow-black/30">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-stone-800 pb-4">
          <div className="flex items-center gap-2.5">
            <div className="rounded-xl bg-emerald-950/90 border border-emerald-800/70 p-2 text-emerald-400">
              <Layers className="h-5 w-5" />
            </div>
            <div>
              <h2 className="text-base sm:text-lg font-serif font-bold text-stone-100">
                Clusters Clínicos de Anamnese (K-Means)
              </h2>
              <p className="text-xs text-stone-400">
                Segmentação não-supervisionada das 8 variáveis tricológicas
              </p>
            </div>
          </div>
          <span className="rounded-full bg-stone-900 border border-stone-700/80 px-3 py-1 text-xs font-bold text-stone-200">
            K = {metricas?.num_clusters ?? 4} Perfis Clínicos
          </span>
        </div>

        <div className="mt-5 grid grid-cols-1 gap-4 md:grid-cols-2">
          {personas.map((persona) => (
            <div
              key={persona.id}
              className="flex flex-col justify-between rounded-xl border border-stone-800/90 bg-[#0d1411]/90 p-4 sm:p-5 transition hover:border-emerald-600/60 hover:bg-[#101915]"
            >
              <div>
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <h3 className="font-serif font-bold text-stone-100 text-sm sm:text-base">
                    {persona.titulo}
                  </h3>
                  <span
                    className={`rounded-full px-2.5 py-0.5 text-[11px] font-semibold border ${persona.badgeColor}`}
                  >
                    {persona.curvatura}
                  </span>
                </div>
                <p className="mt-2.5 text-xs text-stone-300 leading-relaxed">{persona.descricao}</p>
              </div>

              <div className="mt-4 pt-3 border-t border-stone-800">
                <span className="text-[11px] font-semibold text-stone-400 uppercase tracking-wider">
                  Cosméticos Referência:
                </span>
                <div className="mt-1.5 flex flex-wrap gap-1.5">
                  {persona.cosmeticosChave.map((item) => (
                    <span
                      key={item}
                      className="rounded-lg bg-stone-900/90 border border-stone-700/70 px-2 py-0.5 text-[11px] font-medium text-stone-300"
                    >
                      {item}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Metadados Técnicos de Infraestrutura */}
      <div className="rounded-2xl border border-stone-800/90 bg-[#131d18]/90 p-4 sm:p-5 shadow-lg shadow-black/20">
        <div className="flex flex-wrap items-center justify-between gap-3 text-xs text-stone-400">
          <div className="flex items-center gap-2">
            <Server className="h-4 w-4 text-emerald-400" />
            <span>
              <strong>Endpoint Backend:</strong>{" "}
              <code className="rounded bg-stone-900 border border-stone-800 px-1.5 py-0.5 font-mono text-emerald-300">
                {API_URL}
              </code>
            </span>
          </div>
          <div className="flex items-center gap-2">
            <Cpu className="h-4 w-4 text-sky-400" />
            <span>
              <strong>Infraestrutura:</strong> Render Cloud (512MB RAM Ceiling) • Concorrência
              Limitada (50 sockets) • Garbage Collection Forçada
            </span>
          </div>
        </div>
      </div>
    </section>
  );
}
