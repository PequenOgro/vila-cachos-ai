import React, { useState, useMemo } from "react";
import {
  Search,
  SlidersHorizontal,
  LayoutGrid,
  TableProperties,
  Sparkles,
  Info,
  CheckCircle,
} from "lucide-react";
import { type ItemCatalogo } from "@/lib/api";
import { getImagemProduto } from "@/components/totem/product-images";
import { ProductDetailModal } from "./ProductDetailModal";

interface CatalogoTabProps {
  catalogo: ItemCatalogo[];
}

export function CatalogoTab({ catalogo }: CatalogoTabProps) {
  const [busca, setBusca] = useState("");
  const [filtroCurvatura, setFiltroCurvatura] = useState<number | null>(null);
  const [filtroMarca, setFiltroMarca] = useState<string | null>(null);
  const [modoVisualizacao, setModoVisualizacao] = useState<"grid" | "tabela">("grid");
  const [produtoSelecionado, setProdutoSelecionado] = useState<ItemCatalogo | null>(null);

  // Marcas únicas
  const marcasDisponiveis = useMemo(() => {
    const s = new Set(catalogo.map((i) => i.marca).filter(Boolean));
    return Array.from(s).sort();
  }, [catalogo]);

  // Lista filtrada
  const catalogoFiltrado = useMemo(() => {
    return catalogo.filter((item) => {
      const matchBusca =
        item.nome.toLowerCase().includes(busca.toLowerCase()) ||
        item.marca.toLowerCase().includes(busca.toLowerCase()) ||
        item.categoria.toLowerCase().includes(busca.toLowerCase());
      const matchCurv =
        filtroCurvatura === null || item.curvaturas_indicadas.includes(filtroCurvatura);
      const matchMarca =
        filtroMarca === null || item.marca.toLowerCase() === filtroMarca.toLowerCase();
      return matchBusca && matchCurv && matchMarca;
    });
  }, [catalogo, busca, filtroCurvatura, filtroMarca]);

  const marcaCores: Record<string, string> = {
    Arvensis: "bg-emerald-600 text-white",
    "Curly Care": "bg-amber-600 text-white",
    "Deva Curl": "bg-teal-600 text-white",
    "Kah-Noa": "bg-purple-600 text-white",
  };

  return (
    <section className="space-y-6">
      {/* Modal de Detalhes */}
      <ProductDetailModal
        produto={produtoSelecionado}
        onClose={() => setProdutoSelecionado(null)}
      />

      {/* Cabeçalho da Seção */}
      <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-center">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-stone-900">
            Matriz Canônica de Cosméticos &amp; Fórmulas
          </h1>
          <p className="mt-1 text-xs sm:text-sm text-stone-600">
            Acervo oficial do salão Vila Cachos (2024) com vetorização de afinidades terapêuticas
          </p>
        </div>

        {/* Alternador de Modo de Visualização */}
        <div className="flex items-center gap-1 self-start rounded-xl border border-stone-200 bg-stone-100/70 p-1">
          <button
            onClick={() => setModoVisualizacao("grid")}
            className={`flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-semibold transition ${
              modoVisualizacao === "grid"
                ? "bg-white text-emerald-800 shadow-2xs"
                : "text-stone-600 hover:text-stone-900"
            }`}
          >
            <LayoutGrid className="h-3.5 w-3.5" />
            <span>Cards</span>
          </button>
          <button
            onClick={() => setModoVisualizacao("tabela")}
            className={`flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-semibold transition ${
              modoVisualizacao === "tabela"
                ? "bg-white text-emerald-800 shadow-2xs"
                : "text-stone-600 hover:text-stone-900"
            }`}
          >
            <TableProperties className="h-3.5 w-3.5" />
            <span>Tabela</span>
          </button>
        </div>
      </div>

      {/* Painel de Métricas Rápidas do Catálogo */}
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
        <div className="rounded-xl border border-stone-200/90 bg-white p-3.5 shadow-2xs">
          <span className="text-[11px] font-bold uppercase tracking-wider text-stone-400">
            Total Cadastrado
          </span>
          <p className="mt-1 text-xl font-bold text-stone-900">{catalogo.length} cosméticos</p>
          <p className="text-[11px] text-emerald-700 font-medium">100% Acervo Oficial</p>
        </div>
        <div className="rounded-xl border border-stone-200/90 bg-white p-3.5 shadow-2xs">
          <span className="text-[11px] font-bold uppercase tracking-wider text-stone-400">
            Marcas Parceiras
          </span>
          <p className="mt-1 text-xl font-bold text-stone-900">{marcasDisponiveis.length} marcas</p>
          <p className="text-[11px] text-stone-500 font-medium">Arvensis, Curly, Deva, Kah-Noa</p>
        </div>
        <div className="rounded-xl border border-stone-200/90 bg-white p-3.5 shadow-2xs">
          <span className="text-[11px] font-bold uppercase tracking-wider text-stone-400">
            Faixa de Curvatura
          </span>
          <p className="mt-1 text-xl font-bold text-stone-900">2A até 4C</p>
          <p className="text-[11px] text-stone-500 font-medium">Ondulados, Cacheados, Crespos</p>
        </div>
        <div className="rounded-xl border border-stone-200/90 bg-white p-3.5 shadow-2xs">
          <span className="text-[11px] font-bold uppercase tracking-wider text-stone-400">
            Padrão Técnico
          </span>
          <p className="mt-1 text-xl font-bold text-emerald-800">No/Low-Poo</p>
          <p className="text-[11px] text-stone-500 font-medium">Zero sulfatos abrasivos</p>
        </div>
      </div>

      {/* Barra de Filtros e Busca */}
      <div className="rounded-2xl border border-stone-200/90 bg-white p-4 sm:p-5 shadow-xs space-y-4">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-stone-400" />
            <input
              type="text"
              placeholder="Buscar por cosmético, marca ou categoria terapêutica..."
              value={busca}
              onChange={(e) => setBusca(e.target.value)}
              className="w-full rounded-xl border border-stone-300 py-2.5 pl-9 pr-3 text-xs sm:text-sm focus:border-emerald-500 focus:outline-none focus:ring-1 focus:ring-emerald-500 transition shadow-2xs"
            />
          </div>

          {/* Filtro por Curvatura */}
          <div className="flex items-center gap-1.5 self-start sm:self-auto">
            <SlidersHorizontal className="h-4 w-4 text-stone-400 mr-1 hidden sm:block" />
            <span className="text-xs font-semibold text-stone-600 mr-1">Curvatura:</span>
            <button
              onClick={() => setFiltroCurvatura(null)}
              className={`rounded-lg px-2.5 py-1.5 text-xs font-semibold transition ${
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
                className={`rounded-lg px-2.5 py-1.5 text-xs font-semibold transition ${
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

        {/* Filtro por Marca */}
        <div className="flex flex-wrap items-center gap-1.5 border-t border-stone-100 pt-3">
          <span className="mr-1 text-xs font-semibold text-stone-500">Marca:</span>
          <button
            onClick={() => setFiltroMarca(null)}
            className={`rounded-lg px-2.5 py-1 text-xs font-semibold transition ${
              filtroMarca === null
                ? "bg-stone-900 text-white"
                : "bg-stone-100 text-stone-600 hover:bg-stone-200"
            }`}
          >
            Todas ({catalogo.length})
          </button>
          {marcasDisponiveis.map((m) => {
            const count = catalogo.filter((i) => i.marca === m).length;
            const selecionada = filtroMarca === m;
            return (
              <button
                key={m}
                onClick={() => setFiltroMarca(selecionada ? null : m)}
                className={`rounded-lg px-2.5 py-1 text-xs font-semibold transition ${
                  selecionada
                    ? "bg-emerald-700 text-white"
                    : "bg-stone-100 text-stone-600 hover:bg-stone-200"
                }`}
              >
                {m} ({count})
              </button>
            );
          })}
        </div>

        {/* Resumo de Resultados */}
        <div className="flex items-center justify-between text-xs text-stone-500 border-t border-stone-100 pt-3">
          <span>
            Exibindo <strong>{catalogoFiltrado.length}</strong> de{" "}
            <strong>{catalogo.length}</strong> cosméticos catalogados
          </span>
          {(busca || filtroCurvatura !== null || filtroMarca !== null) && (
            <button
              onClick={() => {
                setBusca("");
                setFiltroCurvatura(null);
                setFiltroMarca(null);
              }}
              className="font-semibold text-emerald-700 hover:underline"
            >
              Limpar todos os filtros
            </button>
          )}
        </div>
      </div>

      {/* MODO 1: GRID DE CARDS VISUAIS */}
      {modoVisualizacao === "grid" && (
        <div className="grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">
          {catalogoFiltrado.map((prod) => (
            <div
              key={prod.id}
              className="group flex flex-col justify-between rounded-2xl border border-stone-200/90 bg-white p-5 shadow-xs transition-all duration-200 hover:border-emerald-300 hover:shadow-md"
            >
              <div>
                <div className="flex items-start gap-3.5">
                  <div className="flex h-20 w-20 shrink-0 items-center justify-center rounded-xl border border-stone-100 bg-stone-50/80 p-2 shadow-inner group-hover:scale-102 transition-transform">
                    <img
                      src={getImagemProduto(prod.nome)}
                      alt={prod.nome}
                      className="max-h-full max-w-full object-contain"
                      loading="lazy"
                      decoding="async"
                    />
                  </div>

                  <div className="min-w-0 flex-1">
                    <div className="flex items-start justify-between gap-1">
                      <span className="rounded bg-stone-100 px-1.5 py-0.5 font-mono text-[10px] font-bold text-stone-600">
                        {prod.id}
                      </span>
                      <span className="rounded-full bg-emerald-50 px-2 py-0.5 text-[10px] font-bold text-emerald-800 line-clamp-1 border border-emerald-100">
                        {prod.categoria}
                      </span>
                    </div>

                    <h3 className="mt-1.5 text-sm font-bold leading-snug text-stone-900 line-clamp-2">
                      {prod.nome}
                    </h3>

                    <div className="mt-1 flex items-center gap-1.5">
                      <span className="text-xs font-semibold text-emerald-700">{prod.marca}</span>
                    </div>
                  </div>
                </div>

                {prod.descricao && (
                  <p className="mt-3 text-xs text-stone-600 line-clamp-2 leading-relaxed">
                    {prod.descricao}
                  </p>
                )}

                {/* Metadados Técnicos */}
                <div className="mt-4 space-y-2 border-t border-stone-100 pt-3">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-stone-500 font-medium">Curvaturas:</span>
                    <div className="flex gap-1">
                      {prod.curvaturas_indicadas.map((curv) => (
                        <span
                          key={curv}
                          className="rounded bg-stone-100 px-1.5 py-0.5 text-[10px] font-bold text-stone-700 border border-stone-200"
                        >
                          Tipo {curv}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="flex items-center justify-between text-xs">
                    <span className="text-stone-500 font-medium">Densidade / Peso:</span>
                    <span
                      className={`rounded-md px-2 py-0.5 text-[10px] font-bold capitalize ${
                        prod.peso_fio === "pesado"
                          ? "bg-amber-100 text-amber-900 border border-amber-200"
                          : prod.peso_fio === "medio"
                            ? "bg-blue-100 text-blue-900 border border-blue-200"
                            : "bg-emerald-100 text-emerald-900 border border-emerald-200"
                      }`}
                    >
                      {prod.peso_fio}
                    </span>
                  </div>
                </div>

                {/* Afinidades com Queixas Principais */}
                <div className="mt-4 border-t border-stone-100 pt-3">
                  <p className="text-[10px] font-bold uppercase tracking-wider text-stone-400">
                    Afinidade Tricológica Principal
                  </p>
                  <div className="mt-2 space-y-1.5">
                    {Object.entries(prod.afinidade_queixas)
                      .filter(([, s]) => s >= 0.5)
                      .slice(0, 3)
                      .map(([queixa, score]) => {
                        const label = queixa
                          .replace(/_/g, " ")
                          .replace("alta porosidade quimica", "Porosidade")
                          .replace("frizz falta definicao", "Frizz & Definição")
                          .replace("couro sensivel oleoso", "Couro Sensível")
                          .replace("ressecamento opacidade", "Ressecamento")
                          .replace("transicao capilar", "Transição");

                        return (
                          <div
                            key={queixa}
                            className="flex items-center justify-between text-[11px]"
                          >
                            <span className="capitalize text-stone-600 font-medium">{label}</span>
                            <div className="flex items-center gap-1.5">
                              <div className="h-1.5 w-16 overflow-hidden rounded-full bg-stone-100">
                                <div
                                  className="h-full rounded-full bg-emerald-600"
                                  style={{ width: `${score * 100}%` }}
                                />
                              </div>
                              <span className="font-mono text-[10px] font-bold text-stone-700 w-5 text-right">
                                {score.toFixed(1)}
                              </span>
                            </div>
                          </div>
                        );
                      })}
                  </div>
                </div>
              </div>

              {/* Botão de Abrir Ficha */}
              <button
                onClick={() => setProdutoSelecionado(prod)}
                className="mt-4 w-full rounded-xl border border-stone-200 bg-stone-50 py-2 text-xs font-semibold text-stone-700 transition hover:bg-stone-900 hover:text-white"
              >
                Inspecionar Ficha &amp; Afinidades
              </button>
            </div>
          ))}
        </div>
      )}

      {/* MODO 2: TABELA TÉCNICA COMPARATIVA */}
      {modoVisualizacao === "tabela" && (
        <div className="overflow-hidden rounded-2xl border border-stone-200 bg-white shadow-xs">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-stone-50 border-b border-stone-200 font-bold uppercase tracking-wider text-stone-500">
                <tr>
                  <th className="py-3 px-4">ID</th>
                  <th className="py-3 px-4">Cosmético</th>
                  <th className="py-3 px-4">Marca</th>
                  <th className="py-3 px-4">Categoria</th>
                  <th className="py-3 px-4">Curvaturas</th>
                  <th className="py-3 px-4">Peso</th>
                  <th className="py-3 px-4 text-center">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-stone-100">
                {catalogoFiltrado.map((prod) => (
                  <tr key={prod.id} className="hover:bg-stone-50/80 transition">
                    <td className="py-3 px-4 font-mono font-bold text-stone-600">{prod.id}</td>
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-2.5">
                        <img
                          src={getImagemProduto(prod.nome)}
                          alt={prod.nome}
                          className="h-8 w-8 object-contain rounded bg-stone-50 p-0.5 border"
                          loading="lazy"
                          decoding="async"
                        />
                        <span className="font-bold text-stone-900">{prod.nome}</span>
                      </div>
                    </td>
                    <td className="py-3 px-4 font-semibold text-emerald-800">{prod.marca}</td>
                    <td className="py-3 px-4 text-stone-600">
                      <span className="rounded-full bg-emerald-50 px-2 py-0.5 text-[10px] font-semibold text-emerald-900">
                        {prod.categoria}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <div className="flex gap-1">
                        {prod.curvaturas_indicadas.map((c) => (
                          <span
                            key={c}
                            className="rounded bg-stone-100 px-1.5 py-0.2 text-[10px] font-bold text-stone-700"
                          >
                            {c}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td className="py-3 px-4 capitalize font-medium text-stone-700">
                      {prod.peso_fio}
                    </td>
                    <td className="py-3 px-4 text-center">
                      <button
                        onClick={() => setProdutoSelecionado(prod)}
                        className="rounded-lg bg-stone-100 hover:bg-stone-900 hover:text-white px-2.5 py-1 font-semibold text-[11px] transition"
                      >
                        Ver Detalhes
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </section>
  );
}
