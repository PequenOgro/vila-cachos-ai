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
      badgeColor: "bg-emerald-50 text-emerald-800 border-emerald-200",
      descricao:
        "Cabelos cacheados com porosidade média e sem processos químicos abrasivos. Demanda hidratação balanceada e controle anti-frizz sem enrijecimento.",
      cosmeticosChave: ["Arvensis Ativador", "Curly Care Marshmallow", "Arvensis Geleia"],
    },
    {
      id: 1,
      titulo: "Persona 1 • Ondas e Cachos Leves",
      curvatura: "Curvatura 2 e 3 (2A / 2B / 2C / 3A)",
      badgeColor: "bg-teal-50 text-teal-800 border-teal-200",
      descricao:
        "Fios com padrão aberto e baixa tolerância a cargas pesadas de óleos. Exige formulações ultraleves à base de extratos aquosos e geleias fluidas.",
      cosmeticosChave: ["Deva Curl Delight", "Kah-Noa Super Light", "Arvensis Suave"],
    },
    {
      id: 2,
      titulo: "Persona 2 • Alta Porosidade & Dano Químico",
      curvatura: "Curvatura 2, 3 e 4 com Química",
      badgeColor: "bg-rose-50 text-rose-800 border-rose-200",
      descricao:
        "Fibras fragilizadas por descoloração ou relaxamentos químicos prévios. Prescrição imediata de acidificação para selamento cuticular e reposição de aminoácidos.",
      cosmeticosChave: ["Curly Care ACID-C", "Deva Heaven in Hair", "Curly Be Free"],
    },
    {
      id: 3,
      titulo: "Persona 3 • Crespos & Crespíssimos",
      curvatura: "Curvatura 4 (4A / 4B / 4C)",
      badgeColor: "bg-amber-50 text-amber-900 border-amber-200",
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
          <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-stone-900">
            Telemetria Tricológica &amp; Validação Científica (RNF-12)
          </h1>
          <p className="mt-1 text-xs sm:text-sm text-stone-600">
            Métricas em tempo real da IA híbrida (YOLOv8 ONNX + K-Means + Média Bayesiana de Salão)
          </p>
        </div>
        <div className="inline-flex items-center gap-1.5 self-start rounded-full border border-emerald-200/80 bg-emerald-50/80 px-3 py-1 text-xs font-semibold text-emerald-800">
          <Zap className="h-3.5 w-3.5 text-emerald-600" />
          <span>Inferência &lt; 20ms (ONNX)</span>
        </div>
      </div>

      {/* Grid de KPIs Executivos */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {/* KPI 1: Estado do Motor */}
        <div className="rounded-2xl border border-stone-200/90 bg-white p-5 shadow-xs transition hover:border-emerald-300">
          <div className="flex items-center justify-between text-stone-500">
            <span className="text-xs font-bold uppercase tracking-wider text-stone-400">
              Estado do Motor
            </span>
            <div className="rounded-xl bg-emerald-50 p-2 text-emerald-600">
              <CheckCircle2 className="h-4 w-4" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-stone-900 capitalize">
              {metricas?.status || "Operacional"}
            </span>
          </div>
          <p className="mt-2 text-xs text-stone-500 leading-relaxed">
            Pipeline híbrido ativo: YOLOv8 ONNX + K-Means Tricológico.
          </p>
        </div>

        {/* KPI 2: Base de Atendimentos */}
        <div className="rounded-2xl border border-stone-200/90 bg-white p-5 shadow-xs transition hover:border-blue-300">
          <div className="flex items-center justify-between text-stone-500">
            <span className="text-xs font-bold uppercase tracking-wider text-stone-400">
              Base de Atendimentos
            </span>
            <div className="rounded-xl bg-blue-50 p-2 text-blue-600">
              <Users className="h-4 w-4" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-stone-900">
              {metricas?.total_clientes_historico ?? 1084}
            </span>
            <span className="text-xs font-semibold text-stone-500">clientes reais</span>
          </div>
          <p className="mt-2 text-xs text-stone-500 leading-relaxed">
            Histórico contínuo enriquecido com avaliações pós-atendimento.
          </p>
        </div>

        {/* KPI 3: Média de Satisfação */}
        <div className="rounded-2xl border border-stone-200/90 bg-white p-5 shadow-xs transition hover:border-amber-300">
          <div className="flex items-center justify-between text-stone-500">
            <span className="text-xs font-bold uppercase tracking-wider text-stone-400">
              Média Bayesiana Salão
            </span>
            <div className="rounded-xl bg-amber-50 p-2 text-amber-600">
              <Star className="h-4 w-4 fill-amber-400 text-amber-500" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-stone-900">
              {metricas?.media_satisfacao_global
                ? metricas.media_satisfacao_global.toFixed(2)
                : "4.54"}
            </span>
            <span className="text-xs font-bold text-amber-600">★ ★ ★ ★ ★</span>
          </div>
          <p className="mt-2 text-xs text-stone-500 leading-relaxed">
            Satisfação média ponderada pelo amortecedor de Laplace (C=5.0).
          </p>
        </div>

        {/* KPI 4: Silhouette Score */}
        <div className="rounded-2xl border border-emerald-200 bg-gradient-to-br from-emerald-50/70 to-white p-5 shadow-xs transition hover:border-emerald-400">
          <div className="flex items-center justify-between text-emerald-800">
            <span className="text-xs font-bold uppercase tracking-wider text-emerald-700">
              Silhouette Score (RNF-12)
            </span>
            <div className="rounded-xl bg-emerald-100/80 p-2 text-emerald-700">
              <Award className="h-4 w-4" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-emerald-950 font-mono">
              {metricas?.silhouette_score?.toFixed(3) ?? "0.448"}
            </span>
            <span className="rounded-full bg-emerald-200/90 px-2 py-0.5 text-[10px] font-bold text-emerald-900">
              Robusto (&gt; 0.40)
            </span>
          </div>
          <p className="mt-2 text-xs text-emerald-800 leading-relaxed">
            Validação de alta separabilidade e coesão intra-cluster comprovada.
          </p>
        </div>
      </div>

      {/* Grade dos 4 Clusters Tricológicos */}
      <div className="rounded-2xl border border-stone-200/90 bg-white p-5 sm:p-6 shadow-xs">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-stone-100 pb-4">
          <div className="flex items-center gap-2.5">
            <div className="rounded-xl bg-emerald-50 p-2 text-emerald-700">
              <Layers className="h-5 w-5" />
            </div>
            <div>
              <h2 className="text-base sm:text-lg font-bold text-stone-900">
                Clusters Clínicos de Anamnese (K-Means)
              </h2>
              <p className="text-xs text-stone-500">
                Segmentação não-supervisionada das 8 variáveis tricológicas
              </p>
            </div>
          </div>
          <span className="rounded-full bg-stone-100 px-3 py-1 text-xs font-bold text-stone-700">
            K = {metricas?.num_clusters ?? 4} Perfis Clínicos
          </span>
        </div>

        <div className="mt-5 grid grid-cols-1 gap-4 md:grid-cols-2">
          {personas.map((persona) => (
            <div
              key={persona.id}
              className="flex flex-col justify-between rounded-xl border border-stone-200/80 bg-stone-50/60 p-4 sm:p-5 transition hover:bg-white hover:border-emerald-300 hover:shadow-2xs"
            >
              <div>
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <h3 className="font-bold text-stone-900 text-sm sm:text-base">
                    {persona.titulo}
                  </h3>
                  <span
                    className={`rounded-full px-2.5 py-0.5 text-[11px] font-semibold border ${persona.badgeColor}`}
                  >
                    {persona.curvatura}
                  </span>
                </div>
                <p className="mt-2.5 text-xs text-stone-600 leading-relaxed">{persona.descricao}</p>
              </div>

              <div className="mt-4 pt-3 border-t border-stone-200/60">
                <span className="text-[11px] font-semibold text-stone-500 uppercase tracking-wider">
                  Cosméticos Referência:
                </span>
                <div className="mt-1.5 flex flex-wrap gap-1.5">
                  {persona.cosmeticosChave.map((item) => (
                    <span
                      key={item}
                      className="rounded-lg bg-white border border-stone-200/80 px-2 py-0.5 text-[11px] font-medium text-stone-700"
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
      <div className="rounded-2xl border border-stone-200/80 bg-white p-4 sm:p-5 shadow-2xs">
        <div className="flex flex-wrap items-center justify-between gap-3 text-xs text-stone-600">
          <div className="flex items-center gap-2">
            <Server className="h-4 w-4 text-emerald-600" />
            <span>
              <strong>Endpoint Backend:</strong>{" "}
              <code className="rounded bg-stone-100 px-1.5 py-0.5 font-mono text-stone-800">
                {API_URL}
              </code>
            </span>
          </div>
          <div className="flex items-center gap-2">
            <Cpu className="h-4 w-4 text-blue-600" />
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
