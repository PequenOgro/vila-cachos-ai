import React, { useState } from "react";
import { Sparkles, RefreshCw, FlaskConical, Star, CheckCircle2, TrendingUp } from "lucide-react";
import { recomendar, type Perfil, type Recomendacao } from "@/lib/api";
import { getImagemProduto } from "@/components/totem/product-images";

export function SimuladorTab() {
  const [curvatura, setCurvatura] = useState<number>(3);
  const [porosidade, setPorosidade] = useState<number>(2);
  const [quimica, setQuimica] = useState<number>(0);
  const [queixas, setQueixas] = useState<string[]>(["frizz"]);
  const [resultado, setResultado] = useState<Recomendacao | null>(null);
  const [simulando, setSimulando] = useState(false);

  const toggleQueixa = (q: string) => {
    setQueixas((prev) => (prev.includes(q) ? prev.filter((item) => item !== q) : [...prev, q]));
  };

  const dispararSimulacao = async () => {
    setSimulando(true);
    try {
      const perfilSimulado: Perfil = {
        curvatura,
        porosidade,
        dano_quimico: quimica === 2 ? 1 : 0,
        transicao_capilar: quimica === 1 ? 1 : 0,
        alta_porosidade_quimica: quimica === 2 && porosidade === 3 ? 1 : 0,
        frizz_falta_definicao: queixas.includes("frizz") ? 1 : 0,
        ressecamento_opacidade: queixas.includes("ressecamento") ? 1 : 0,
        couro_sensivel_oleoso: queixas.includes("couro") ? 1 : 0,
      };
      const res = await recomendar(perfilSimulado);
      setResultado(res);
    } catch (err) {
      console.error("[Simulador] Erro na simulação:", err);
    } finally {
      setSimulando(false);
    }
  };

  return (
    <section className="space-y-6">
      <div>
        <h1 className="text-xl sm:text-2xl font-serif font-bold tracking-tight text-stone-100">
          Simulador &amp; Auditoria Tricológica em Tempo Real
        </h1>
        <p className="mt-1 text-xs sm:text-sm text-stone-400">
          Audite o motor de IA híbrido inspecionando os pesos da combinação convexa e a
          explicabilidade (XAI)
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        {/* Painel de Parâmetros do Fio (5 colunas) */}
        <div className="space-y-5 rounded-2xl border border-stone-800/90 bg-[#131d18]/90 p-5 shadow-xl shadow-black/30 lg:col-span-5">
          <div className="flex items-center gap-2 border-b border-stone-800 pb-3">
            <FlaskConical className="h-4 w-4 text-emerald-400" />
            <h2 className="text-sm font-bold uppercase tracking-wider text-stone-300">
              Parâmetros do Fio &amp; Anamnese
            </h2>
          </div>

          {/* Curvatura */}
          <div>
            <label className="text-xs font-semibold text-stone-300">
              Curvatura Capilar (Walker)
            </label>
            <div className="mt-2 grid grid-cols-3 gap-2">
              {[
                { val: 2, label: "2 • Ondulado" },
                { val: 3, label: "3 • Cacheado" },
                { val: 4, label: "4 • Crespo" },
              ].map((c) => (
                <button
                  key={c.val}
                  type="button"
                  onClick={() => setCurvatura(c.val)}
                  className={`rounded-xl border py-2.5 text-xs font-bold transition shadow-xs ${
                    curvatura === c.val
                      ? "border-emerald-600 bg-emerald-950 text-emerald-200"
                      : "border-stone-800 bg-stone-900/90 text-stone-400 hover:text-stone-200 hover:bg-stone-800"
                  }`}
                >
                  {c.label}
                </button>
              ))}
            </div>
          </div>

          {/* Porosidade */}
          <div>
            <label className="text-xs font-semibold text-stone-300">Grau de Porosidade</label>
            <div className="mt-2 grid grid-cols-3 gap-2">
              {[
                { val: 1, label: "Baixa" },
                { val: 2, label: "Média" },
                { val: 3, label: "Alta" },
              ].map((p) => (
                <button
                  key={p.val}
                  type="button"
                  onClick={() => setPorosidade(p.val)}
                  className={`rounded-xl border py-2.5 text-xs font-bold transition shadow-xs ${
                    porosidade === p.val
                      ? "border-emerald-600 bg-emerald-950 text-emerald-200"
                      : "border-stone-800 bg-stone-900/90 text-stone-400 hover:text-stone-200 hover:bg-stone-800"
                  }`}
                >
                  {p.label}
                </button>
              ))}
            </div>
          </div>

          {/* Histórico Químico */}
          <div>
            <label className="text-xs font-semibold text-stone-300">Histórico Químico</label>
            <div className="mt-2 grid grid-cols-3 gap-2">
              {[
                { val: 0, label: "100% Natural" },
                { val: 1, label: "Transição" },
                { val: 2, label: "Com Química" },
              ].map((q) => (
                <button
                  key={q.val}
                  type="button"
                  onClick={() => setQuimica(q.val)}
                  className={`rounded-xl border py-2.5 text-xs font-bold transition shadow-xs ${
                    quimica === q.val
                      ? "border-emerald-600 bg-emerald-950 text-emerald-200"
                      : "border-stone-800 bg-stone-900/90 text-stone-400 hover:text-stone-200 hover:bg-stone-800"
                  }`}
                >
                  {q.label}
                </button>
              ))}
            </div>
          </div>

          {/* Queixas Capilares */}
          <div>
            <label className="text-xs font-semibold text-stone-300">Queixas Relatadas</label>
            <div className="mt-2 space-y-2">
              {[
                { id: "frizz", label: "Frizz & Falta de Definição" },
                { id: "ressecamento", label: "Ressecamento & Pontas Secas" },
                { id: "couro", label: "Couro Cabeludo Sensível / Oleoso" },
              ].map((q) => (
                <label
                  key={q.id}
                  className="flex cursor-pointer items-center gap-2.5 rounded-xl border border-stone-800 bg-stone-900/80 p-2.5 text-xs font-medium text-stone-300 transition hover:bg-stone-800/80 hover:border-emerald-800/60"
                >
                  <input
                    type="checkbox"
                    checked={queixas.includes(q.id)}
                    onChange={() => toggleQueixa(q.id)}
                    className="rounded border-stone-700 bg-stone-800 text-emerald-500 focus:ring-emerald-500 h-4 w-4"
                  />
                  <span>{q.label}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Botão de Disparo */}
          <button
            onClick={dispararSimulacao}
            disabled={simulando}
            className="flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 py-3 text-sm font-bold text-white shadow-lg shadow-emerald-950/50 transition hover:from-emerald-500 hover:to-teal-500 active:scale-98 disabled:opacity-50"
          >
            {simulando ? (
              <RefreshCw className="h-4 w-4 animate-spin text-white" />
            ) : (
              <Sparkles className="h-4 w-4 text-white" />
            )}
            <span>{simulando ? "Calculando..." : "Disparar Recomendação"}</span>
          </button>
        </div>

        {/* Painel do Resultado da Recomendação (7 colunas) */}
        <div className="space-y-4 lg:col-span-7">
          {resultado ? (
            <div className="space-y-4">
              {/* Header da Persona Atribuída */}
              <div className="rounded-2xl border border-emerald-900/80 bg-[#131d18]/90 p-5 shadow-xl shadow-black/30">
                <div className="flex flex-wrap items-center justify-between gap-2 border-b border-stone-800 pb-3">
                  <span className="rounded-full bg-emerald-950 border border-emerald-700/80 px-3 py-1 text-xs font-bold text-emerald-300">
                    Cluster Clínico #{resultado.cluster_id ?? 0}
                  </span>
                  {resultado.peso_conhecimento_vs_feedback && (
                    <div className="text-xs text-stone-400 font-medium">
                      <strong className="text-stone-300">Equilíbrio Híbrido:</strong> Matriz
                      Especialista{" "}
                      {(
                        (resultado.peso_conhecimento_vs_feedback.peso_regras_conteudo ??
                          resultado.peso_conhecimento_vs_feedback.peso_conteudo_regras ??
                          0.65) * 100
                      ).toFixed(0)}
                      % • Feedback de Salão{" "}
                      {(
                        (resultado.peso_conhecimento_vs_feedback.peso_feedback_historico ??
                          resultado.peso_conhecimento_vs_feedback.peso_feedback_clientes ??
                          0.35) * 100
                      ).toFixed(0)}
                      %
                    </div>
                  )}
                </div>
                <h3 className="mt-3 font-serif text-lg font-bold text-stone-100">
                  {resultado.persona}
                </h3>
              </div>

              {/* Top 3 Cosméticos Prescritos */}
              <div className="space-y-3">
                <h4 className="text-xs font-bold uppercase tracking-wider text-stone-400">
                  Top 3 Cosméticos Prescritos com Justificativa XAI:
                </h4>

                {resultado.produtos.map((p, idx) => (
                  <div
                    key={p.nome}
                    className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 rounded-2xl border border-stone-800/90 bg-[#131d18]/90 p-4 shadow-xl shadow-black/30 transition hover:border-emerald-700/70"
                  >
                    <div className="flex items-start gap-3">
                      <div className="relative flex h-16 w-16 shrink-0 items-center justify-center rounded-xl border border-stone-800 bg-[#0d1411] p-1.5 shadow-inner">
                        <span className="absolute -top-1.5 -left-1.5 flex h-5 w-5 items-center justify-center rounded-full bg-emerald-600 text-[10px] font-bold text-white shadow-xs">
                          {idx + 1}
                        </span>
                        <img
                          src={getImagemProduto(p.nome)}
                          alt={p.nome}
                          className="max-h-full max-w-full object-contain"
                          loading="lazy"
                          decoding="async"
                        />
                      </div>

                      <div className="min-w-0">
                        <h5 className="font-serif font-bold text-stone-100 text-sm">{p.nome}</h5>
                        {p.categoria && (
                          <span className="rounded-full bg-emerald-950/80 border border-emerald-800/60 px-2 py-0.5 text-[10px] font-semibold text-emerald-300">
                            {p.categoria}
                          </span>
                        )}
                        <p className="mt-2 text-xs text-stone-300 bg-[#0d1411] rounded-lg p-2.5 border border-stone-800/80 leading-relaxed">
                          <strong className="text-emerald-400">Justificativa XAI:</strong>{" "}
                          {p.motivo}
                        </p>
                      </div>
                    </div>

                    <div className="flex sm:flex-col items-center sm:items-end justify-between border-t sm:border-t-0 pt-2 sm:pt-0 border-stone-800">
                      <span className="text-sm font-bold text-emerald-400">
                        Score: {p.score.toFixed(3)}
                      </span>
                      <div className="flex items-center gap-1 text-xs font-bold text-amber-400">
                        <span>{p.estrelas_estimadas.toFixed(1)}</span>
                        <Star className="h-3.5 w-3.5 fill-amber-400 text-amber-400" />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="flex min-h-[360px] flex-col items-center justify-center rounded-2xl border-2 border-dashed border-stone-800 bg-[#131d18]/50 p-8 text-center">
              <FlaskConical className="h-10 w-10 text-stone-600" />
              <h4 className="mt-3 font-serif text-sm font-bold text-stone-200">
                Nenhuma auditoria disparada
              </h4>
              <p className="mt-1 max-w-sm text-xs text-stone-500 leading-relaxed">
                Configure os parâmetros do fio ao lado e clique em &quot;Disparar Recomendação&quot;
                para auditar a prescrição em tempo de execução.
              </p>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
