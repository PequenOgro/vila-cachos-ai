import React, { useRef, useState } from "react";
import { diagnosticarImagem, type DiagnosticoImagem } from "@/lib/api";
import { type FormAnamnese, Titulo, Opcao, Onda } from "./AnamneseShared";

interface PassoCurvaturaProps {
  form: FormAnamnese;
  setForm: (f: FormAnamnese) => void;
}

/**
 * =====================================================================
 * ETAPA 1 DA ANAMNESE: IDENTIFICAÇÃO DA CURVATURA
 * =====================================================================
 * Permite ao usuário escolher a curvatura de forma manual (2: Ondulado,
 * 3: Cacheado, 4: Crespo) OU utilizar o modelo de Visão Computacional (YOLO)
 * para inferência instantânea via foto/câmera do dispositivo.
 * Implementa o padrão Human-in-the-Loop com botão "Aplicar diagnóstico".
 */
export function PassoCurvatura({ form, setForm }: PassoCurvaturaProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [analisando, setAnalisando] = useState(false);
  const [diag, setDiag] = useState<DiagnosticoImagem | null>(null);
  const [erroRede, setErroRede] = useState<string | null>(null);

  /**
   * Envia o arquivo de imagem para /diagnostico/imagem.
   * Se a IA identificar que não há cabelo, exibe aviso amigável sem inventar diagnósticos falsos.
   */
  const onFile = async (f?: File) => {
    if (!f) return;
    setPreview(URL.createObjectURL(f));
    setDiag(null);
    setErroRede(null);
    setAnalisando(true);

    try {
      const d = await diagnosticarImagem(f);
      setDiag(d);
    } catch {
      setErroRede(
        "Não foi possível conectar ao servidor de visão computacional. Você pode tirar outra foto ou selecionar sua curvatura manualmente nos botões abaixo.",
      );
    } finally {
      setAnalisando(false);
    }
  };

  /**
   * Aplica a sugestão da IA no formulário apenas se cabelo válido foi detectado.
   */
  const aplicarDiagnosticoIA = () => {
    if (!diag || diag.cabelo_detectado === false || !diag.curvatura_detectada) return;
    setForm({
      ...form,
      curvatura: diag.curvatura_detectada,
      porosidade: diag.porosidade_aparente || 2,
      queixas:
        diag.frizz_detectado && !form.queixas.includes("frizz")
          ? [...form.queixas, "frizz"]
          : form.queixas,
    });
  };

  return (
    <>
      <Titulo t="Qual é a sua curvatura?" s="Envie uma foto da mecha ou escolha manualmente." />

      {/* Card de Visão Computacional com Câmera/Upload */}
      <div className="mb-6 grid gap-6 rounded-3xl bg-primary p-6 text-primary-foreground shadow-soft md:grid-cols-[180px_1fr]">
        <button
          onClick={() => inputRef.current?.click()}
          className="relative flex aspect-square items-center justify-center overflow-hidden rounded-2xl border-2 border-dashed border-primary-foreground/50 bg-sage-soft transition hover:border-primary-foreground active:scale-95"
          aria-label="Tirar ou enviar foto da mecha"
        >
          {preview ? (
            <img src={preview} alt="Foto da mecha enviada" className="h-full w-full object-cover" />
          ) : (
            <span className="px-4 text-center text-sm font-medium">📷 Tirar ou enviar foto</span>
          )}
          {analisando && <span className="absolute inset-0 animate-pulse bg-primary/60" />}
        </button>

        <input
          ref={inputRef}
          type="file"
          accept="image/*"
          capture="environment"
          className="hidden"
          onChange={(e) => onFile(e.target.files?.[0])}
        />

        <div className="flex flex-col justify-center">
          <p className="text-xs uppercase tracking-[0.25em] text-primary-foreground/70">
            Visão computacional
          </p>

          {!diag && !analisando && !erroRede && (
            <p className="mt-2 font-serif text-2xl font-light">
              Deixe a IA ler sua mecha em milissegundos.
            </p>
          )}

          {analisando && (
            <p className="mt-2 font-serif text-2xl font-light">Analisando sua mecha com IA…</p>
          )}

          {/* Cenário: Erro de Conexão com a API */}
          {erroRede && !analisando && (
            <div className="mt-2 space-y-2 rounded-2xl border border-amber-300/40 bg-amber-500/20 p-4 text-amber-50">
              <p className="text-sm font-semibold">⚠️ Conexão offline com o modelo</p>
              <p className="text-xs text-amber-100/90 leading-relaxed">{erroRede}</p>
            </div>
          )}

          {/* Cenário: Foto Sem Cabelo / Anúncio / Careca */}
          {diag && diag.cabelo_detectado === false && (
            <div className="mt-2 space-y-3 rounded-2xl border border-amber-300/40 bg-amber-500/20 p-4 text-amber-50">
              <div className="flex items-center gap-2">
                <span className="text-xl">⚠️</span>
                <p className="font-serif text-lg font-semibold">Nenhum cabelo detectado na foto</p>
              </div>
              <p className="text-xs text-amber-100/90 leading-relaxed">
                {diag.mensagem_alerta ||
                  "Não identificamos fios ou mechas de cabelo na foto enviada. Envie uma foto aproximada dos fios ou selecione sua curvatura abaixo."}
              </p>
              <div className="pt-1">
                <button
                  type="button"
                  onClick={() => inputRef.current?.click()}
                  className="text-xs font-semibold underline underline-offset-4 hover:opacity-80 transition"
                >
                  📷 Tirar outra foto da mecha
                </button>
              </div>
            </div>
          )}

          {/* Cenário: Mechas e Cachos Detectados com Sucesso */}
          {diag && diag.cabelo_detectado !== false && diag.curvatura_detectada && (
            <div className="mt-2 space-y-3">
              <p className="font-serif text-2xl">{diag.curvatura_label}</p>
              <div className="flex flex-wrap gap-2 text-sm">
                <span className="rounded-full bg-primary-foreground/15 px-3 py-1">
                  Confiança {Math.round(diag.confianca_curvatura * 100)}%
                </span>
                <span className="rounded-full bg-primary-foreground/15 px-3 py-1">
                  Frizz {diag.frizz_detectado ? "presente" : "baixo"}
                </span>
                <span className="rounded-full bg-primary-foreground/15 px-3 py-1">
                  Porosidade{" "}
                  {["baixa", "média", "alta"][(diag.porosidade_aparente || 2) - 1] ?? "média"}
                </span>
                <span className="rounded-full bg-primary-foreground/15 px-3 py-1">
                  {diag.tempo_inferencia_ms.toFixed(1)} ms
                </span>
              </div>
              <button
                type="button"
                onClick={aplicarDiagnosticoIA}
                className="min-h-12 rounded-full bg-primary-foreground px-6 font-semibold text-primary transition hover:bg-primary-foreground/90 active:scale-95"
              >
                Aplicar diagnóstico
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Seleção Manual de Curvaturas */}
      <div className="grid gap-4 md:grid-cols-3">
        {[
          [2, "Ondulado", "Tipo 2 — ondas em S, leves e soltas."],
          [3, "Cacheado", "Tipo 3 — cachos definidos em espiral."],
          [4, "Crespo", "Tipo 4 — fios em zigue-zague, muito volume."],
        ].map(([val, tit, desc]) => (
          <Opcao
            key={val}
            ativo={form.curvatura === val}
            onClick={() => setForm({ ...form, curvatura: val as number })}
            titulo={tit as string}
            desc={desc as string}
            icone={<Onda voltas={val as number} />}
          />
        ))}
      </div>
    </>
  );
}
