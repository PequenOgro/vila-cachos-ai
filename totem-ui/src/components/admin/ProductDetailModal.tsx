import React from "react";
import { X, Sparkles, Droplets, CheckCircle, Scale } from "lucide-react";
import { type ItemCatalogo } from "@/lib/api";
import { getImagemProduto } from "@/components/totem/product-images";

interface ProductDetailModalProps {
  produto: ItemCatalogo | null;
  onClose: () => void;
}

export function ProductDetailModal({ produto, onClose }: ProductDetailModalProps) {
  if (!produto) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      className="fixed inset-0 z-50 flex items-center justify-center bg-stone-900/60 p-4 backdrop-blur-xs animate-fadeIn"
      onClick={onClose}
    >
      <div
        className="relative max-h-[90vh] w-full max-w-xl overflow-y-auto rounded-3xl bg-white p-6 shadow-2xl transition-all sm:p-8"
        onClick={(e) => e.stopPropagation()}
      >
        <button
          onClick={onClose}
          aria-label="Fechar detalhes"
          className="absolute right-5 top-5 rounded-full bg-stone-100 p-2 text-stone-500 transition hover:bg-stone-200 hover:text-stone-800"
        >
          <X className="h-4 w-4" />
        </button>

        <div className="flex flex-col items-center sm:flex-row sm:items-start gap-5">
          <div className="flex h-28 w-28 shrink-0 items-center justify-center rounded-2xl border border-stone-200/80 bg-stone-50 p-2 shadow-inner">
            <img
              src={getImagemProduto(produto.nome)}
              alt={produto.nome}
              className="max-h-full max-w-full object-contain"
              loading="lazy"
              decoding="async"
            />
          </div>

          <div className="min-w-0 flex-1 text-center sm:text-left">
            <div className="flex flex-wrap items-center justify-center sm:justify-start gap-2">
              <span className="rounded-md bg-stone-100 px-2 py-0.5 font-mono text-xs font-bold text-stone-600">
                {produto.id}
              </span>
              <span className="rounded-full bg-emerald-100/80 px-2.5 py-0.5 text-xs font-semibold text-emerald-800">
                {produto.categoria}
              </span>
            </div>
            <h3 className="mt-2 text-lg font-bold text-stone-900 leading-snug">{produto.nome}</h3>
            <p className="text-xs font-semibold text-emerald-700">{produto.marca}</p>
          </div>
        </div>

        <div className="mt-5 space-y-4">
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-stone-400">
              Descrição Oficial do Salão
            </h4>
            <p className="mt-1 text-xs sm:text-sm text-stone-700 leading-relaxed bg-stone-50 rounded-xl p-3 border border-stone-100">
              {produto.descricao}
            </p>
          </div>

          {/* Ficha Técnica */}
          <div className="grid grid-cols-2 gap-3">
            <div className="rounded-xl border border-stone-100 bg-stone-50/70 p-3">
              <div className="flex items-center gap-1.5 text-xs text-stone-500 font-medium">
                <Droplets className="h-3.5 w-3.5 text-blue-600" />
                <span>Curvaturas Indicadas:</span>
              </div>
              <div className="mt-2 flex gap-1.5">
                {[2, 3, 4].map((c) => {
                  const indicado = produto.curvaturas_indicadas.includes(c);
                  return (
                    <span
                      key={c}
                      className={`rounded-lg px-2 py-0.5 text-xs font-bold ${
                        indicado
                          ? "bg-emerald-600 text-white shadow-2xs"
                          : "bg-stone-200/60 text-stone-400"
                      }`}
                    >
                      Tipo {c}
                    </span>
                  );
                })}
              </div>
            </div>

            <div className="rounded-xl border border-stone-100 bg-stone-50/70 p-3">
              <div className="flex items-center gap-1.5 text-xs text-stone-500 font-medium">
                <Scale className="h-3.5 w-3.5 text-amber-600" />
                <span>Peso no Fio:</span>
              </div>
              <p className="mt-2 text-xs font-bold capitalize text-stone-800">{produto.peso_fio}</p>
            </div>
          </div>

          {/* Matriz de Afinidade Terapêutica */}
          <div>
            <div className="flex items-center justify-between">
              <h4 className="text-xs font-bold uppercase tracking-wider text-stone-400">
                Afinidade Terapêutica (0 a 1.0)
              </h4>
              <span className="text-[11px] font-medium text-emerald-700">
                Pesos do Motor Heurístico
              </span>
            </div>

            <div className="mt-2 space-y-2 rounded-2xl border border-stone-100 bg-stone-50/50 p-3.5">
              {Object.entries(produto.afinidade_queixas).map(([queixa, score]) => {
                const label = queixa
                  .replace(/_/g, " ")
                  .replace("alta porosidade quimica", "Porosidade / Dano Químico")
                  .replace("frizz falta definicao", "Frizz / Falta de Definição")
                  .replace("couro sensivel oleoso", "Couro Cabeludo Sensível")
                  .replace("ressecamento opacidade", "Ressecamento e Opacidade")
                  .replace("transicao capilar", "Transição Capilar");

                return (
                  <div key={queixa} className="flex items-center justify-between text-xs">
                    <span className="text-stone-700 capitalize font-medium">{label}</span>
                    <div className="flex items-center gap-2">
                      <div className="h-2 w-24 overflow-hidden rounded-full bg-stone-200">
                        <div
                          className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-emerald-700 transition-all duration-500"
                          style={{ width: `${score * 100}%` }}
                        />
                      </div>
                      <span className="font-mono text-xs font-bold text-stone-800 w-7 text-right">
                        {score.toFixed(1)}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        <div className="mt-6 flex justify-end">
          <button
            onClick={onClose}
            className="rounded-xl bg-stone-900 px-5 py-2 text-xs font-semibold text-white transition hover:bg-stone-800"
          >
            Fechar Detalhes
          </button>
        </div>
      </div>
    </div>
  );
}
