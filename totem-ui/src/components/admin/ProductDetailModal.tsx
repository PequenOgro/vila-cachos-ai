import React, { useEffect } from "react";
import { X, Droplets, Scale } from "lucide-react";
import { type ItemCatalogo } from "@/lib/api";
import { getImagemProduto } from "@/components/totem/product-images";

interface ProductDetailModalProps {
  produto: ItemCatalogo | null;
  onClose: () => void;
}

export function ProductDetailModal({ produto, onClose }: ProductDetailModalProps) {
  // Fecha com a tecla ESC e trava o scroll da página de fundo enquanto o modal estiver aberto
  useEffect(() => {
    if (!produto) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        onClose();
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    const originalOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      document.body.style.overflow = originalOverflow;
    };
  }, [produto, onClose]);

  if (!produto) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-produto-titulo"
      onClick={onClose}
      className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 bg-black/85 backdrop-blur-md transition-opacity cursor-pointer animate-fadeIn"
    >
      {/* Caixa de conteúdo do Modal */}
      <div
        className="relative max-h-[90vh] w-full max-w-xl overflow-y-auto rounded-3xl bg-[#131d18] border border-stone-700/80 p-6 shadow-2xl transition-all sm:p-8 text-stone-100 cursor-default animate-scaleUp"
        onClick={(e) => e.stopPropagation()}
      >
        <button
          onClick={onClose}
          aria-label="Fechar detalhes"
          className="absolute right-5 top-5 rounded-full bg-stone-900 border border-stone-700 p-2 text-stone-400 transition hover:bg-stone-800 hover:text-white"
        >
          <X className="h-4 w-4" />
        </button>

        <div className="flex flex-col items-center sm:flex-row sm:items-start gap-5">
          <div className="flex h-28 w-28 shrink-0 items-center justify-center rounded-2xl border border-stone-800 bg-[#0d1411] p-2 shadow-inner">
            <img
              src={getImagemProduto(produto.nome)}
              alt={produto.nome}
              width={112}
              height={112}
              className="max-h-full max-w-full object-contain"
              loading="lazy"
              decoding="async"
            />
          </div>

          <div className="min-w-0 flex-1 text-center sm:text-left">
            <div className="flex flex-wrap items-center justify-center sm:justify-start gap-2">
              <span className="rounded-md bg-stone-900 border border-stone-700 px-2 py-0.5 font-mono text-xs font-bold text-stone-300">
                {produto.id}
              </span>
              <span className="rounded-full bg-emerald-950/90 border border-emerald-800/80 px-2.5 py-0.5 text-xs font-semibold text-emerald-300">
                {produto.categoria}
              </span>
            </div>
            <h3
              id="modal-produto-titulo"
              className="mt-2 font-serif text-lg font-bold text-stone-100 leading-snug"
            >
              {produto.nome}
            </h3>
            <p className="text-xs font-semibold text-amber-400">{produto.marca}</p>
          </div>
        </div>

        <div className="mt-5 space-y-4">
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-stone-400">
              Descrição Oficial do Salão
            </h4>
            <p className="mt-1 text-xs sm:text-sm text-stone-300 leading-relaxed bg-[#0d1411] rounded-xl p-3 border border-stone-800">
              {produto.descricao}
            </p>
          </div>

          {/* Ficha Técnica */}
          <div className="grid grid-cols-2 gap-3">
            <div className="rounded-xl border border-stone-800 bg-[#0d1411] p-3">
              <div className="flex items-center gap-1.5 text-xs text-stone-400 font-medium">
                <Droplets className="h-3.5 w-3.5 text-sky-400" />
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
                          ? "bg-emerald-600 text-white shadow-xs"
                          : "bg-stone-900 border border-stone-800 text-stone-500"
                      }`}
                    >
                      Tipo {c}
                    </span>
                  );
                })}
              </div>
            </div>

            <div className="rounded-xl border border-stone-800 bg-[#0d1411] p-3">
              <div className="flex items-center gap-1.5 text-xs text-stone-400 font-medium">
                <Scale className="h-3.5 w-3.5 text-amber-400" />
                <span>Peso no Fio:</span>
              </div>
              <p className="mt-2 text-xs font-bold capitalize text-stone-200">{produto.peso_fio}</p>
            </div>
          </div>

          {/* Matriz de Afinidade Terapêutica */}
          <div>
            <div className="flex items-center justify-between">
              <h4 className="text-xs font-bold uppercase tracking-wider text-stone-400">
                Afinidade Terapêutica (0 a 1.0)
              </h4>
              <span className="text-[11px] font-medium text-emerald-400">
                Pesos do Motor Heurístico
              </span>
            </div>

            <div className="mt-2 space-y-2 rounded-2xl border border-stone-800 bg-[#0d1411] p-3.5">
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
                    <span className="text-stone-300 capitalize font-medium">{label}</span>
                    <div className="flex items-center gap-2">
                      <div className="h-2 w-24 overflow-hidden rounded-full bg-stone-900 border border-stone-800">
                        <div
                          className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-teal-400 transition-all duration-500"
                          style={{ width: `${score * 100}%` }}
                        />
                      </div>
                      <span className="font-mono text-xs font-bold text-stone-200 w-7 text-right">
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
            className="rounded-xl bg-emerald-700 hover:bg-emerald-600 px-5 py-2 text-xs font-semibold text-white transition shadow-md shadow-emerald-950/50"
          >
            Fechar Detalhes
          </button>
        </div>
      </div>
    </div>
  );
}
