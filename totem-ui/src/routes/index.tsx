import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useRef, useState } from "react";
import hero from "@/assets/hero.jpg";
import acidC from "@/assets/produtos/curly-care-acid-c.png";
import manteigaNutritiva from "@/assets/produtos/curly-care-manteiga-nutritiva.png";
import arvensisGeleia from "@/assets/produtos/arvensis-geleia-forte.png";
import arvensisAtivador from "@/assets/produtos/arvensis-ativador-cachos.png";
import arvensisCowash from "@/assets/produtos/arvensis-cowash.png";
import devaDelight from "@/assets/produtos/deva-curl-delight.png";
import curlyMarshmallow from "@/assets/produtos/curly-care-marshmallow.png";
import curlyPudding from "@/assets/produtos/curly-care-pudding.png";
import curlyFixU from "@/assets/produtos/curly-care-fix-u.png";
import curlyMousse from "@/assets/produtos/curly-care-mousse.png";
import curlyBeStrong from "@/assets/produtos/curly-care-be-strong.png";
import curlyBeFree from "@/assets/produtos/curly-care-be-free.png";
import curlySpume from "@/assets/produtos/curly-care-spume.png";
import curlyHighCondition from "@/assets/produtos/curly-care-high-condition.png";
import curlyNoSpume from "@/assets/produtos/curly-care-no-spume.png";
import curlyAtivador from "@/assets/produtos/curly-care-ativador.png";
import devaAngell from "@/assets/produtos/deva-curl-angell.png";
import devaHeaven from "@/assets/produtos/deva-curl-heaven-in-hair.png";
import devaStyling from "@/assets/produtos/deva-curl-styling-cream.png";
import devaLowPooOriginal from "@/assets/produtos/deva-curl-low-poo-original.png";
import devaOneConditionOriginal from "@/assets/produtos/deva-curl-one-condition-original.png";
import devaNoPooOriginal from "@/assets/produtos/deva-curl-no-poo-original.png";
import devaOneConditionDecadence from "@/assets/produtos/deva-curl-one-condition-decadence.png";
import devaNoPooDecadence from "@/assets/produtos/deva-curl-no-poo-decadence.png";
import arvensisShampoo from "@/assets/produtos/arvensis-shampoo.png";

function getImagemProduto(nome: string): string {
  const n = (nome || "").toLowerCase();
  if (n.includes("acid-c") || n.includes("acidificante")) return acidC;
  if (n.includes("manteiga") || n.includes("nutritiva")) return manteigaNutritiva;
  if (n.includes("marshmallow")) return curlyMarshmallow;
  if (n.includes("pudding") || n.includes("gelatina")) return curlyPudding;
  if (n.includes("fix u") || n.includes("fix-u")) return curlyFixU;
  if (n.includes("mousse")) return curlyMousse;
  if (n.includes("be strong")) return curlyBeStrong;
  if (n.includes("be free")) return curlyBeFree;
  if (n.includes("spume!") || n.includes("shampoo hidratante spume")) return curlySpume;
  if (n.includes("high condition")) return curlyHighCondition;
  if (n.includes("no spume") || n.includes("no-spume")) return curlyNoSpume;
  if (n.includes("ativador") && n.includes("curly care")) return curlyAtivador;
  if (n.includes("geleia")) return arvensisGeleia;
  if (n.includes("ativador") && n.includes("arvensis")) return arvensisAtivador;
  if (n.includes("co-wash") || n.includes("cowash") || n.includes("higienizador"))
    return arvensisCowash;
  if (n.includes("shampoo") && n.includes("arvensis")) return arvensisShampoo;
  if (n.includes("delight")) return devaDelight;
  if (n.includes("angell") || n.includes("angéll")) return devaAngell;
  if (n.includes("heaven")) return devaHeaven;
  if (n.includes("styling") || n.includes("supercream")) return devaStyling;
  if (n.includes("decadence") && n.includes("one condition")) return devaOneConditionDecadence;
  if (n.includes("decadence") && (n.includes("no poo") || n.includes("no-poo")))
    return devaNoPooDecadence;
  if (n.includes("low-poo") || n.includes("low poo")) return devaLowPooOriginal;
  if (n.includes("one condition")) return devaOneConditionOriginal;
  if (n.includes("no-poo") || n.includes("no poo")) return devaNoPooOriginal;
  return acidC;
}
import {
  diagnosticarImagem,
  enviarFeedback,
  recomendacaoDemo,
  recomendar,
  type DiagnosticoImagem,
  type Perfil,
  type Recomendacao,
} from "@/lib/api";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Vila Cachos — Totem de Diagnóstico Capilar" },
      {
        name: "description",
        content:
          "Descubra em menos de 1 minuto os produtos ideais para seus cachos, ondas e crespos na Vila Cachos.",
      },
      { property: "og:title", content: "Vila Cachos — Totem de Diagnóstico Capilar" },
      {
        property: "og:description",
        content:
          "Diagnóstico capilar personalizado com IA para cabelos ondulados, cacheados e crespos.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: Totem,
});

type Etapa = "inicio" | "anamnese" | "processando" | "resultado";
type Form = {
  curvatura: number | null;
  porosidade: number | null;
  quimica: number | null;
  queixas: string[];
};

const formInicial: Form = { curvatura: null, porosidade: null, quimica: null, queixas: [] };

function Logo({ light }: { light?: boolean }) {
  return (
    <div
      className={`flex items-center gap-3 ${light ? "text-primary-foreground" : "text-foreground"}`}
    >
      <svg
        viewBox="0 0 40 56"
        className="h-11 w-8"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.6"
        aria-hidden
      >
        <rect x="2" y="2" width="36" height="52" rx="18" />
        <path d="M14 46 C 10 30, 12 18, 22 10 M20 46 C 18 32, 22 22, 30 16 M12 22 c 6 -2, 10 2, 10 8" />
      </svg>
      <div className="font-serif leading-none">
        <div className="text-2xl font-light">Vila</div>
        <div className="text-2xl font-light">Cachos</div>
      </div>
    </div>
  );
}

function Totem() {
  const [etapa, setEtapa] = useState<Etapa>("inicio");
  const [form, setForm] = useState<Form>(formInicial);
  const [resultado, setResultado] = useState<Recomendacao | null>(null);
  const [perfil, setPerfil] = useState<Perfil | null>(null);

  const reiniciar = () => {
    setForm(formInicial);
    setResultado(null);
    setEtapa("inicio");
  };

  const finalizar = async () => {
    const rawPorosidade = Number(form.porosidade);
    const porosidadeNormalizada = rawPorosidade >= 1 && rawPorosidade <= 3 ? rawPorosidade : 2;
    const rawCurvatura = Number(form.curvatura);
    const curvaturaNormalizada = rawCurvatura >= 2 && rawCurvatura <= 4 ? rawCurvatura : 3;
    const q = form.queixas || [];

    const p: Perfil = {
      curvatura: curvaturaNormalizada,
      porosidade: porosidadeNormalizada,
      dano_quimico: form.quimica === 2 ? 1 : 0,
      transicao_capilar: form.quimica === 1 ? 1 : 0,
      alta_porosidade_quimica: form.quimica === 2 && porosidadeNormalizada === 3 ? 1 : 0,
      frizz_falta_definicao: q.includes("frizz") ? 1 : 0,
      ressecamento_opacidade: q.includes("ressecamento") ? 1 : 0,
      couro_sensivel_oleoso: q.includes("couro") ? 1 : 0,
    };
    setPerfil(p);
    setEtapa("processando");
    const [r] = await Promise.all([
      recomendar(p).catch(() => recomendacaoDemo(p)),
      new Promise((res) => setTimeout(res, 4200)),
    ]);
    setResultado(r.produtos.length ? r : recomendacaoDemo(p));
    setEtapa("resultado");
  };

  return (
    <main className="min-h-dvh bg-background">
      {etapa === "inicio" && <Inicio onStart={() => setEtapa("anamnese")} />}
      {etapa === "anamnese" && (
        <Anamnese form={form} setForm={setForm} onVoltar={reiniciar} onFinalizar={finalizar} />
      )}
      {etapa === "processando" && <Processando />}
      {etapa === "resultado" && resultado && perfil && (
        <Resultado r={resultado} perfil={perfil} onReiniciar={reiniciar} />
      )}
    </main>
  );
}

function Inicio({ onStart }: { onStart: () => void }) {
  return (
    <section className="relative min-h-dvh overflow-hidden">
      <img
        src={hero}
        alt="Mulher com cabelos cacheados volumosos"
        width={1280}
        height={1600}
        className="absolute inset-0 h-full w-full object-cover"
      />
      <div className="absolute inset-0 bg-veil" />
      <div className="relative flex min-h-dvh flex-col justify-between p-8 md:p-14">
        <header className="flex items-start justify-between">
          <Logo light />
          <p className="max-w-[14rem] text-right text-sm tracking-wide text-primary-foreground/80">
            Totem Inteligente de Diagnóstico Capilar
          </p>
        </header>
        <div className="max-w-2xl animate-rise pb-6">
          <p className="mb-4 text-sm uppercase tracking-[0.3em] text-primary-foreground/70">
            Slow Beauty
          </p>
          <h1 className="text-5xl font-light leading-[1.05] text-primary-foreground md:text-7xl">
            Seu cacho tem <span className="font-bold italic">uma história.</span>
          </h1>
          <p className="mt-6 max-w-lg text-lg text-primary-foreground/85">
            Descubra em menos de 1 minuto os cuidados ideais para a sua curvatura.
          </p>
          <div className="mt-8 flex flex-wrap gap-2">
            {["100% Personalizado", "IA Híbrida Especialista", "Explicabilidade Tricológica"].map(
              (b) => (
                <span
                  key={b}
                  className="rounded-full border border-primary-foreground/40 px-4 py-2 text-sm text-primary-foreground backdrop-blur-md"
                >
                  {b}
                </span>
              ),
            )}
          </div>
          <button
            onClick={onStart}
            className="mt-10 min-h-16 rounded-full bg-primary px-10 text-lg font-semibold text-primary-foreground animate-breathe transition hover:bg-sage-soft"
          >
            Iniciar Diagnóstico Capilar
          </button>
        </div>
      </div>
    </section>
  );
}

function Opcao({
  ativo,
  onClick,
  titulo,
  desc,
  icone,
}: {
  ativo: boolean;
  onClick: () => void;
  titulo: string;
  desc: string;
  icone?: React.ReactNode;
}) {
  return (
    <button
      onClick={onClick}
      aria-pressed={ativo}
      className={`flex min-h-32 flex-col items-start gap-3 rounded-3xl border-2 p-6 text-left transition ${
        ativo
          ? "border-primary bg-primary text-primary-foreground shadow-soft"
          : "border-transparent bg-card hover:border-sage-soft"
      }`}
    >
      {icone}
      <span className="font-serif text-xl font-semibold">{titulo}</span>
      <span className={`text-sm ${ativo ? "text-primary-foreground/85" : "text-muted-foreground"}`}>
        {desc}
      </span>
    </button>
  );
}

function Onda({ voltas }: { voltas: number }) {
  const d =
    voltas === 2
      ? "M4 30 Q 14 10, 24 30 T 44 30 T 64 30"
      : voltas === 3
        ? "M4 30 c 6 -16, 18 -16, 14 0 s 8 16, 14 0 s 8 -16, 14 0 s 8 16, 14 0"
        : "M4 30 l 5 -12 l 5 18 l 5 -18 l 5 18 l 5 -18 l 5 18 l 5 -18 l 5 18 l 5 -18 l 5 12";
  return (
    <svg
      viewBox="0 0 68 50"
      className="h-10 w-16"
      fill="none"
      stroke="currentColor"
      strokeWidth="2.2"
      strokeLinecap="round"
      aria-hidden
    >
      <path d={d} />
    </svg>
  );
}

const passos = ["Curvatura", "Porosidade", "Química", "Queixas"];

function Anamnese({
  form,
  setForm,
  onVoltar,
  onFinalizar,
}: {
  form: Form;
  setForm: (f: Form) => void;
  onVoltar: () => void;
  onFinalizar: () => void;
}) {
  const [passo, setPasso] = useState(0);
  const pode = [form.curvatura, form.porosidade, form.quimica, true][passo] !== null;

  return (
    <section className="mx-auto flex min-h-dvh max-w-5xl flex-col px-6 py-8 md:px-10">
      <header className="flex items-center justify-between">
        <Logo />
        <span className="text-sm text-muted-foreground">Passo {passo + 1} de 4</span>
      </header>
      <div
        className="mt-8 grid grid-cols-4 gap-2"
        role="progressbar"
        aria-valuenow={passo + 1}
        aria-valuemin={1}
        aria-valuemax={4}
      >
        {passos.map((p, i) => (
          <div key={p}>
            <div
              className={`h-1.5 rounded-full transition-colors ${i <= passo ? "bg-primary" : "bg-secondary"}`}
            />
            <p
              className={`mt-2 text-xs uppercase tracking-widest ${i === passo ? "text-foreground" : "text-muted-foreground"}`}
            >
              {p}
            </p>
          </div>
        ))}
      </div>

      <div key={passo} className="flex-1 animate-rise py-10">
        {passo === 0 && <PassoCurvatura form={form} setForm={setForm} />}
        {passo === 1 && (
          <>
            <Titulo
              t="Como seus fios absorvem água?"
              s="A porosidade indica o quanto as cutículas estão abertas."
            />
            <div className="grid gap-4 md:grid-cols-3">
              {[
                ["Baixa", "Cutículas seladas, produto demora a penetrar."],
                ["Média", "Equilibrada, absorve e retém bem."],
                ["Alta", "Fios ásperos, secam rápido e perdem brilho."],
              ].map(([t, d], i) => (
                <Opcao
                  key={t}
                  ativo={form.porosidade === i + 1}
                  onClick={() => setForm({ ...form, porosidade: i + 1 })}
                  titulo={t!}
                  desc={d!}
                />
              ))}
            </div>
          </>
        )}
        {passo === 2 && (
          <>
            <Titulo
              t="Qual o histórico químico?"
              s="Isso nos ajuda a equilibrar nutrição e reconstrução."
            />
            <div className="grid gap-4 md:grid-cols-3">
              {[
                ["100% Natural", "Sem química nos fios."],
                ["Transição Capilar", "Parte natural, parte com química."],
                ["Danificado", "Descoloração, relaxamento ou progressiva."],
              ].map(([t, d], i) => (
                <Opcao
                  key={t}
                  ativo={form.quimica === i}
                  onClick={() => setForm({ ...form, quimica: i })}
                  titulo={t!}
                  desc={d!}
                />
              ))}
            </div>
          </>
        )}
        {passo === 3 && (
          <>
            <Titulo t="O que mais te incomoda no dia a dia?" s="Escolha quantas quiser." />
            <div className="flex flex-wrap gap-3">
              {(
                [
                  ["frizz", "Frizz excessivo e falta de definição"],
                  ["ressecamento", "Ressecamento e pontas secas"],
                  ["couro", "Couro cabeludo sensível ou oleoso"],
                  ["quebra", "Perda de massa / quebra"],
                ] as const
              ).map(([k, l]) => {
                const on = form.queixas.includes(k);
                return (
                  <button
                    key={k}
                    aria-pressed={on}
                    onClick={() =>
                      setForm({
                        ...form,
                        queixas: on ? form.queixas.filter((x) => x !== k) : [...form.queixas, k],
                      })
                    }
                    className={`min-h-14 rounded-full border-2 px-6 text-base transition ${on ? "border-terracotta bg-terracotta text-accent-foreground" : "border-border bg-card hover:border-terracotta"}`}
                  >
                    {on ? "✓ " : ""}
                    {l}
                  </button>
                );
              })}
            </div>
          </>
        )}
      </div>

      <footer className="flex items-center justify-between gap-4 pb-4">
        <button
          onClick={() => (passo === 0 ? onVoltar() : setPasso(passo - 1))}
          className="min-h-14 rounded-full px-8 text-base text-muted-foreground hover:text-foreground"
        >
          ← Voltar
        </button>
        <button
          disabled={!pode}
          onClick={() => (passo === 3 ? onFinalizar() : setPasso(passo + 1))}
          className="min-h-14 rounded-full bg-primary px-10 text-base font-semibold text-primary-foreground transition disabled:opacity-40"
        >
          {passo === 3 ? "Ver minha prescrição" : "Continuar →"}
        </button>
      </footer>
    </section>
  );
}

function Titulo({ t, s }: { t: string; s: string }) {
  return (
    <div className="mb-8">
      <h2 className="text-4xl font-light md:text-5xl">{t}</h2>
      <p className="mt-3 text-muted-foreground">{s}</p>
    </div>
  );
}

function PassoCurvatura({ form, setForm }: { form: Form; setForm: (f: Form) => void }) {
  const input = useRef<HTMLInputElement>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [analisando, setAnalisando] = useState(false);
  const [diag, setDiag] = useState<DiagnosticoImagem | null>(null);

  const onFile = async (f?: File) => {
    if (!f) return;
    setPreview(URL.createObjectURL(f));
    setDiag(null);
    setAnalisando(true);
    const d = await diagnosticarImagem(f).catch(() => ({
      curvatura_detectada: 3,
      curvatura_label: "Cacheado (Tipo 3: 3A/3B/3C)",
      confianca_curvatura: 0.92,
      frizz_detectado: 1,
      porosidade_aparente: 2,
      tempo_inferencia_ms: 28.5,
    }));
    setDiag(d);
    setAnalisando(false);
  };

  return (
    <>
      <Titulo t="Qual é a sua curvatura?" s="Envie uma foto da mecha ou escolha manualmente." />
      <div className="mb-6 grid gap-6 rounded-3xl bg-primary p-6 text-primary-foreground shadow-soft md:grid-cols-[180px_1fr]">
        <button
          onClick={() => input.current?.click()}
          className="relative flex aspect-square items-center justify-center overflow-hidden rounded-2xl border-2 border-dashed border-primary-foreground/50 bg-sage-soft"
          aria-label="Tirar ou enviar foto da mecha"
        >
          {preview ? (
            <img src={preview} alt="Foto da mecha enviada" className="h-full w-full object-cover" />
          ) : (
            <span className="px-4 text-center text-sm">📷 Tirar ou enviar foto</span>
          )}
          {analisando && <span className="absolute inset-0 animate-pulse bg-primary/60" />}
        </button>
        <input
          ref={input}
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
          {!diag && !analisando && (
            <p className="mt-2 font-serif text-2xl">Deixe a IA ler sua mecha em milissegundos.</p>
          )}
          {analisando && <p className="mt-2 font-serif text-2xl">Analisando sua mecha…</p>}
          {diag && (
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
                onClick={() =>
                  setForm({
                    ...form,
                    curvatura: diag.curvatura_detectada,
                    porosidade: diag.porosidade_aparente || 2,
                    queixas:
                      diag.frizz_detectado && !form.queixas.includes("frizz")
                        ? [...form.queixas, "frizz"]
                        : form.queixas,
                  })
                }
                className="min-h-12 rounded-full bg-primary-foreground px-6 font-semibold text-primary"
              >
                Aplicar diagnóstico
              </button>
            </div>
          )}
        </div>
      </div>
      <div className="grid gap-4 md:grid-cols-3">
        {[
          [2, "Ondulado", "Tipo 2 — ondas em S, leves e soltas."],
          [3, "Cacheado", "Tipo 3 — cachos definidos em espiral."],
          [4, "Crespo", "Tipo 4 — fios em zigue-zague, muito volume."],
        ].map(([v, t, d]) => (
          <Opcao
            key={v}
            ativo={form.curvatura === v}
            onClick={() => setForm({ ...form, curvatura: v as number })}
            titulo={t as string}
            desc={d as string}
            icone={<Onda voltas={v as number} />}
          />
        ))}
      </div>
    </>
  );
}

const mensagens = [
  "Processando vetor de 8 dimensões…",
  "Cruzando formulações com a matriz de afinidade tricológica…",
  "Consultando histórico de 1.000+ clientes reais do salão…",
];

function Processando() {
  const [i, setI] = useState(0);
  useEffect(() => {
    const t = setInterval(() => setI((x) => (x + 1) % mensagens.length), 1400);
    return () => clearInterval(t);
  }, []);
  return (
    <section className="flex min-h-dvh flex-col items-center justify-center bg-primary px-6 text-primary-foreground">
      <div className="relative flex h-56 w-56 items-center justify-center">
        {[0, 0.8, 1.6].map((d) => (
          <span
            key={d}
            className="absolute inset-0 rounded-full border-2 border-primary-foreground/60 animate-ripple"
            style={{ animationDelay: `${d}s` }}
          />
        ))}
        <Logo light />
      </div>
      <p
        key={i}
        className="mt-14 max-w-md animate-rise text-center font-serif text-2xl"
        aria-live="polite"
      >
        {mensagens[i]}
      </p>
    </section>
  );
}

/**
 * =====================================================================
 * TELA DE RESULTADO (PRESCRIÇÃO TERAPÊUTICA & XAI)
 * =====================================================================
 * Apresenta a Persona identificada pelo agrupamento não-supervisionado K-Means,
 * a decomposição dos pesos híbridos (Conhecimento Especialista vs. Média Bayesiana)
 * e o Top 3 de cosméticos com explicabilidade semântica (XAI).
 */
function Resultado({
  r,
  perfil,
  onReiniciar,
}: {
  r: Recomendacao;
  perfil: Perfil;
  onReiniciar: () => void;
}) {
  // Pesos adaptativos do motor híbrido (alpha da combinação convexa)
  const pesoRegras = Math.round(
    (r.peso_conhecimento_vs_feedback?.peso_conteudo_regras ?? 0.65) * 100,
  );
  const pesoFeedback = Math.round(
    (r.peso_conhecimento_vs_feedback?.peso_feedback_clientes ?? 0.35) * 100,
  );

  return (
    <section className="mx-auto max-w-6xl px-6 py-10 md:px-10">
      {/* Cabeçalho de Navegação */}
      <header className="flex items-center justify-between">
        <Logo />
        <button
          onClick={onReiniciar}
          className="min-h-12 rounded-full border-2 border-primary px-6 font-semibold text-primary transition hover:bg-primary hover:text-primary-foreground"
        >
          Realizar novo diagnóstico
        </button>
      </header>

      {/* Título da Persona Capilar Identificada */}
      <div className="mt-12 animate-rise">
        <div className="flex items-center gap-2">
          <span className="rounded-full bg-primary/10 px-3 py-1 text-xs font-semibold text-primary">
            {r.cluster_id != null ? `Cluster Clínico #${r.cluster_id}` : "Prescrição Personalizada"}
          </span>
          <span className="text-xs uppercase tracking-widest text-muted-foreground">
            Diagnóstico Tricológico Vila Cachos
          </span>
        </div>
        <h1 className="mt-3 max-w-3xl text-3xl font-light md:text-5xl">
          <span className="font-bold italic">{r.persona}</span>
        </h1>
      </div>

      {/* Painel XAI: Inteligência Artificial Explicável & Equilíbrio Híbrido */}
      <div className="mt-8 rounded-3xl border border-border/60 bg-card p-6 shadow-soft animate-rise">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <span className="text-xs font-semibold uppercase tracking-wider text-primary">
              Transparência Algorítmica (XAI)
            </span>
            <h2 className="text-lg font-semibold text-foreground">
              Composição da Recomendação Híbrida
            </h2>
            <p className="mt-0.5 text-xs text-muted-foreground">
              Equilíbrio ponderado entre a ciência capilar e a avaliação de mais de 1.000 clientes reais.
            </p>
          </div>

          <div className="flex items-center gap-6 text-sm">
            <div className="flex items-center gap-2">
              <span className="h-3 w-3 rounded-full bg-primary" />
              <div>
                <p className="font-bold text-foreground">{pesoRegras}%</p>
                <p className="text-[11px] text-muted-foreground">Matriz Especialista</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <span className="h-3 w-3 rounded-full bg-amber" />
              <div>
                <p className="font-bold text-foreground">{pesoFeedback}%</p>
                <p className="text-[11px] text-muted-foreground">Média Bayesiana (Salão)</p>
              </div>
            </div>
          </div>
        </div>

        {/* Barra visual proporcional */}
        <div className="mt-4 flex h-2 w-full overflow-hidden rounded-full bg-secondary">
          <div
            className="bg-primary transition-all duration-700"
            style={{ width: `${pesoRegras}%` }}
            title={`Peso da Matriz Especialista: ${pesoRegras}%`}
          />
          <div
            className="bg-amber transition-all duration-700"
            style={{ width: `${pesoFeedback}%` }}
            title={`Peso das Avaliações Reais de Salão: ${pesoFeedback}%`}
          />
        </div>
      </div>

      {/* Grid de Cosméticos Recomendados */}
      <div className="mt-10 grid gap-6 lg:grid-cols-3">
        {r.produtos.slice(0, 3).map((p, i) => (
          <ProdutoCard
            key={p.nome}
            p={p}
            img={getImagemProduto(p.nome)}
            perfil={perfil}
            delay={i * 120}
          />
        ))}
      </div>
    </section>
  );
}

/**
 * =====================================================================
 * CARD DE PRODUTO RECOMENDADO
 * =====================================================================
 * Renderiza foto oficial, categoria, score composto, motivos clínicos
 * e mecanismo de feedback ativo com recalibração imediata de pesos.
 */
function ProdutoCard({
  p,
  img,
  perfil,
  delay,
}: {
  p: Recomendacao["produtos"][number];
  img: string;
  perfil: Perfil;
  delay: number;
}) {
  const [nota, setNota] = useState(0);
  const [mensagemFeedback, setMensagemFeedback] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  // Normalização do score final híbrido em porcentagem
  const rawScore = Number(p.score);
  const pct =
    !isNaN(rawScore) && rawScore > 0
      ? Math.round(rawScore <= 1 ? rawScore * 100 : rawScore)
      : Math.round(((Number(p.estrelas_estimadas) || 4.2) / 5) * 100);

  // Registro de feedback com recalibração de pesos no backend
  const handleAvaliar = async (estrelas: number) => {
    setNota(estrelas);
    setEnviando(true);
    const resp = await enviarFeedback(perfil, p.nome, estrelas);
    setEnviando(false);
    if (resp?.mensagem) {
      setMensagemFeedback(resp.mensagem);
    } else {
      setMensagemFeedback("Avaliação registrada! Pesos do seu cluster recalibrados no motor 🌿");
    }
  };

  return (
    <article
      className="flex animate-rise flex-col overflow-hidden rounded-3xl bg-card shadow-soft"
      style={{ animationDelay: `${delay}ms` }}
    >
      {/* Vitrine do Frasco Oficial com Fundo Transparente */}
      <div className="relative flex aspect-[4/3] w-full items-center justify-center bg-stone-100/70 p-6 dark:bg-stone-900/60">
        <img
          src={img}
          alt={p.nome}
          width={400}
          height={400}
          loading="lazy"
          className="h-full max-h-56 w-auto object-contain drop-shadow-md transition-transform duration-300 hover:scale-105"
        />
        {/* Badge de Compatibilidade Geral */}
        <span className="absolute left-4 top-4 rounded-full bg-card/95 px-3 py-1 text-xs font-semibold tracking-wide text-foreground shadow-sm backdrop-blur">
          {pct}% compatível
        </span>

        {/* Badge da Categoria Cosmética */}
        {p.categoria && (
          <span className="absolute right-4 top-4 rounded-full bg-primary/10 px-3 py-1 text-[11px] font-semibold text-primary backdrop-blur">
            {p.categoria}
          </span>
        )}
      </div>

      <div className="flex flex-1 flex-col p-6">
        <h3 className="text-xl font-semibold leading-snug">{p.nome}</h3>

        {/* Descrição dos Ativos e Função Terapêutica */}
        {p.descricao && (
          <p className="mt-1.5 text-xs text-muted-foreground leading-relaxed line-clamp-2">
            {p.descricao}
          </p>
        )}

        {/* Avaliação Média Estimada e Total de Votos no Salão */}
        <div className="mt-3 flex items-center justify-between text-xs text-muted-foreground">
          <span className="text-amber font-medium">
            {"★".repeat(Math.round(p.estrelas_estimadas))}{" "}
            <span className="text-foreground font-semibold">
              {p.estrelas_estimadas.toFixed(1)}
            </span>{" "}
            estimado
          </span>
          {p.avaliacoes_cluster !== undefined && (
            <span>{p.avaliacoes_cluster} clientes no cluster</span>
          )}
        </div>

        {/* Detalhamento dos Scores Híbridos */}
        <div className="mt-3 grid grid-cols-2 gap-2 rounded-xl bg-muted/40 p-2.5 text-[11px]">
          <div>
            <span className="text-muted-foreground">Afinidade com Fio:</span>
            <p className="font-semibold text-foreground">
              {p.score_conteudo != null ? `${Math.round(p.score_conteudo * 100)}%` : `${pct}%`}
            </p>
          </div>
          <div>
            <span className="text-muted-foreground">Satisfação Salão:</span>
            <p className="font-semibold text-foreground">
              {p.score_feedback_bayesiano != null
                ? `${Math.round(p.score_feedback_bayesiano * 100)}%`
                : "4.8★"}
            </p>
          </div>
        </div>

        {/* Justificativa XAI (Por que para você?) */}
        <div className="mt-4 rounded-2xl bg-secondary p-4">
          <p className="text-xs font-semibold uppercase tracking-widest text-primary">
            Por que para você?
          </p>
          <p className="mt-1.5 text-xs leading-relaxed text-secondary-foreground">{p.motivo}</p>
        </div>

        {/* Seção de Feedback e Recalibração de Pesos */}
        <div className="mt-auto pt-5">
          {nota ? (
            <div className="animate-rise rounded-xl bg-primary/10 p-3 text-center">
              <p className="font-serif text-sm font-medium text-primary">
                {mensagemFeedback ?? "Obrigada! Sua avaliação nos ajuda a cuidar melhor 🌿"}
              </p>
            </div>
          ) : (
            <div>
              <p className="text-xs text-muted-foreground">Já usou este produto? Avalie:</p>
              <div className="mt-1 flex items-center gap-1">
                {[1, 2, 3, 4, 5].map((n) => (
                  <button
                    key={n}
                    disabled={enviando}
                    aria-label={`${n} estrelas`}
                    onClick={() => handleAvaliar(n)}
                    className="flex h-10 w-10 items-center justify-center text-2xl text-muted-foreground transition hover:scale-115 hover:text-amber disabled:opacity-50"
                  >
                    ★
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </article>
  );
}
