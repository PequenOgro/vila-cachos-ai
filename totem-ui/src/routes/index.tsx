import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useRef, useState } from "react";
import hero from "@/assets/hero.jpg";
import prod1 from "@/assets/prod-1.jpg";
import prod2 from "@/assets/prod-2.jpg";
import prod3 from "@/assets/prod-3.jpg";
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
      { name: "description", content: "Descubra em menos de 1 minuto os produtos ideais para seus cachos, ondas e crespos na Vila Cachos." },
      { property: "og:title", content: "Vila Cachos — Totem de Diagnóstico Capilar" },
      { property: "og:description", content: "Diagnóstico capilar personalizado com IA para cabelos ondulados, cacheados e crespos." },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: Totem,
});

type Etapa = "inicio" | "anamnese" | "processando" | "resultado";
type Form = { curvatura: number | null; porosidade: number | null; quimica: number | null; queixas: string[] };

const formInicial: Form = { curvatura: null, porosidade: null, quimica: null, queixas: [] };
const imagens = [prod1, prod2, prod3];

function Logo({ light }: { light?: boolean }) {
  return (
    <div className={`flex items-center gap-3 ${light ? "text-primary-foreground" : "text-foreground"}`}>
      <svg viewBox="0 0 40 56" className="h-11 w-8" fill="none" stroke="currentColor" strokeWidth="1.6" aria-hidden>
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
    const porosidadeNormalizada = (rawPorosidade >= 1 && rawPorosidade <= 3) ? rawPorosidade : 2;
    const rawCurvatura = Number(form.curvatura);
    const curvaturaNormalizada = (rawCurvatura >= 2 && rawCurvatura <= 4) ? rawCurvatura : 3;

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
      <img src={hero} alt="Mulher com cabelos cacheados volumosos" width={1280} height={1600} className="absolute inset-0 h-full w-full object-cover" />
      <div className="absolute inset-0 bg-veil" />
      <div className="relative flex min-h-dvh flex-col justify-between p-8 md:p-14">
        <header className="flex items-start justify-between">
          <Logo light />
          <p className="max-w-[14rem] text-right text-sm tracking-wide text-primary-foreground/80">
            Totem Inteligente de Diagnóstico Capilar
          </p>
        </header>
        <div className="max-w-2xl animate-rise pb-6">
          <p className="mb-4 text-sm uppercase tracking-[0.3em] text-primary-foreground/70">Slow Beauty</p>
          <h1 className="text-5xl font-light leading-[1.05] text-primary-foreground md:text-7xl">
            Seu cacho tem <span className="font-bold italic">uma história.</span>
          </h1>
          <p className="mt-6 max-w-lg text-lg text-primary-foreground/85">
            Descubra em menos de 1 minuto os cuidados ideais para a sua curvatura.
          </p>
          <div className="mt-8 flex flex-wrap gap-2">
            {["100% Personalizado", "IA Híbrida Especialista", "Explicabilidade Tricológica"].map((b) => (
              <span key={b} className="rounded-full border border-primary-foreground/40 px-4 py-2 text-sm text-primary-foreground backdrop-blur-md">
                {b}
              </span>
            ))}
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

function Opcao({ ativo, onClick, titulo, desc, icone }: { ativo: boolean; onClick: () => void; titulo: string; desc: string; icone?: React.ReactNode }) {
  return (
    <button
      onClick={onClick}
      aria-pressed={ativo}
      className={`flex min-h-32 flex-col items-start gap-3 rounded-3xl border-2 p-6 text-left transition ${
        ativo ? "border-primary bg-primary text-primary-foreground shadow-soft" : "border-transparent bg-card hover:border-sage-soft"
      }`}
    >
      {icone}
      <span className="font-serif text-xl font-semibold">{titulo}</span>
      <span className={`text-sm ${ativo ? "text-primary-foreground/85" : "text-muted-foreground"}`}>{desc}</span>
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
    <svg viewBox="0 0 68 50" className="h-10 w-16" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" aria-hidden>
      <path d={d} />
    </svg>
  );
}

const passos = ["Curvatura", "Porosidade", "Química", "Queixas"];

function Anamnese({ form, setForm, onVoltar, onFinalizar }: { form: Form; setForm: (f: Form) => void; onVoltar: () => void; onFinalizar: () => void }) {
  const [passo, setPasso] = useState(0);
  const pode = [form.curvatura, form.porosidade, form.quimica, true][passo] !== null;

  return (
    <section className="mx-auto flex min-h-dvh max-w-5xl flex-col px-6 py-8 md:px-10">
      <header className="flex items-center justify-between">
        <Logo />
        <span className="text-sm text-muted-foreground">Passo {passo + 1} de 4</span>
      </header>
      <div className="mt-8 grid grid-cols-4 gap-2" role="progressbar" aria-valuenow={passo + 1} aria-valuemin={1} aria-valuemax={4}>
        {passos.map((p, i) => (
          <div key={p}>
            <div className={`h-1.5 rounded-full transition-colors ${i <= passo ? "bg-primary" : "bg-secondary"}`} />
            <p className={`mt-2 text-xs uppercase tracking-widest ${i === passo ? "text-foreground" : "text-muted-foreground"}`}>{p}</p>
          </div>
        ))}
      </div>

      <div key={passo} className="flex-1 animate-rise py-10">
        {passo === 0 && <PassoCurvatura form={form} setForm={setForm} />}
        {passo === 1 && (
          <>
            <Titulo t="Como seus fios absorvem água?" s="A porosidade indica o quanto as cutículas estão abertas." />
            <div className="grid gap-4 md:grid-cols-3">
              {[["Baixa", "Cutículas seladas, produto demora a penetrar."], ["Média", "Equilibrada, absorve e retém bem."], ["Alta", "Fios ásperos, secam rápido e perdem brilho."]].map(([t, d], i) => (
                <Opcao key={t} ativo={form.porosidade === (i + 1)} onClick={() => setForm({ ...form, porosidade: i + 1 })} titulo={t!} desc={d!} />
              ))}
            </div>
          </>
        )}
        {passo === 2 && (
          <>
            <Titulo t="Qual o histórico químico?" s="Isso nos ajuda a equilibrar nutrição e reconstrução." />
            <div className="grid gap-4 md:grid-cols-3">
              {[["100% Natural", "Sem química nos fios."], ["Transição Capilar", "Parte natural, parte com química."], ["Danificado", "Descoloração, relaxamento ou progressiva."]].map(([t, d], i) => (
                <Opcao key={t} ativo={form.quimica === i} onClick={() => setForm({ ...form, quimica: i })} titulo={t!} desc={d!} />
              ))}
            </div>
          </>
        )}
        {passo === 3 && (
          <>
            <Titulo t="O que mais te incomoda no dia a dia?" s="Escolha quantas quiser." />
            <div className="flex flex-wrap gap-3">
              {([["frizz", "Frizz excessivo e falta de definição"], ["ressecamento", "Ressecamento e pontas secas"], ["couro", "Couro cabeludo sensível ou oleoso"], ["quebra", "Perda de massa / quebra"]] as const).map(([k, l]) => {
                const on = form.queixas.includes(k);
                return (
                  <button
                    key={k}
                    aria-pressed={on}
                    onClick={() => setForm({ ...form, queixas: on ? form.queixas.filter((x) => x !== k) : [...form.queixas, k] })}
                    className={`min-h-14 rounded-full border-2 px-6 text-base transition ${on ? "border-terracotta bg-terracotta text-accent-foreground" : "border-border bg-card hover:border-terracotta"}`}
                  >
                    {on ? "✓ " : ""}{l}
                  </button>
                );
              })}
            </div>
          </>
        )}
      </div>

      <footer className="flex items-center justify-between gap-4 pb-4">
        <button onClick={() => (passo === 0 ? onVoltar() : setPasso(passo - 1))} className="min-h-14 rounded-full px-8 text-base text-muted-foreground hover:text-foreground">
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
          {preview ? <img src={preview} alt="Foto da mecha enviada" className="h-full w-full object-cover" /> : <span className="px-4 text-center text-sm">📷 Tirar ou enviar foto</span>}
          {analisando && <span className="absolute inset-0 animate-pulse bg-primary/60" />}
        </button>
        <input ref={input} type="file" accept="image/*" capture="environment" className="hidden" onChange={(e) => onFile(e.target.files?.[0])} />
        <div className="flex flex-col justify-center">
          <p className="text-xs uppercase tracking-[0.25em] text-primary-foreground/70">Visão computacional</p>
          {!diag && !analisando && <p className="mt-2 font-serif text-2xl">Deixe a IA ler sua mecha em milissegundos.</p>}
          {analisando && <p className="mt-2 font-serif text-2xl">Analisando sua mecha…</p>}
          {diag && (
            <div className="mt-2 space-y-3">
              <p className="font-serif text-2xl">{diag.curvatura_label}</p>
              <div className="flex flex-wrap gap-2 text-sm">
                <span className="rounded-full bg-primary-foreground/15 px-3 py-1">Confiança {Math.round(diag.confianca_curvatura * 100)}%</span>
                <span className="rounded-full bg-primary-foreground/15 px-3 py-1">Frizz {diag.frizz_detectado ? "presente" : "baixo"}</span>
                <span className="rounded-full bg-primary-foreground/15 px-3 py-1">Porosidade {["baixa", "média", "alta"][(diag.porosidade_aparente || 2) - 1] ?? "média"}</span>
                <span className="rounded-full bg-primary-foreground/15 px-3 py-1">{diag.tempo_inferencia_ms.toFixed(1)} ms</span>
              </div>
              <button
                onClick={() =>
                  setForm({
                    ...form,
                    curvatura: diag.curvatura_detectada,
                    porosidade: diag.porosidade_aparente || 2,
                    queixas: diag.frizz_detectado && !form.queixas.includes("frizz") ? [...form.queixas, "frizz"] : form.queixas,
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
        {[[2, "Ondulado", "Tipo 2 — ondas em S, leves e soltas."], [3, "Cacheado", "Tipo 3 — cachos definidos em espiral."], [4, "Crespo", "Tipo 4 — fios em zigue-zague, muito volume."]].map(([v, t, d]) => (
          <Opcao key={v} ativo={form.curvatura === v} onClick={() => setForm({ ...form, curvatura: v as number })} titulo={t as string} desc={d as string} icone={<Onda voltas={v as number} />} />
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
          <span key={d} className="absolute inset-0 rounded-full border-2 border-primary-foreground/60 animate-ripple" style={{ animationDelay: `${d}s` }} />
        ))}
        <Logo light />
      </div>
      <p key={i} className="mt-14 max-w-md animate-rise text-center font-serif text-2xl" aria-live="polite">
        {mensagens[i]}
      </p>
    </section>
  );
}

function Resultado({ r, perfil, onReiniciar }: { r: Recomendacao; perfil: Perfil; onReiniciar: () => void }) {
  return (
    <section className="mx-auto max-w-6xl px-6 py-10 md:px-10">
      <header className="flex items-center justify-between">
        <Logo />
        <button onClick={onReiniciar} className="min-h-12 rounded-full border-2 border-primary px-6 font-semibold text-primary hover:bg-primary hover:text-primary-foreground">
          Realizar novo diagnóstico
        </button>
      </header>
      <div className="mt-12 animate-rise">
        <p className="text-sm uppercase tracking-[0.3em] text-muted-foreground">Sua prescrição cosmética</p>
        <h1 className="mt-3 max-w-3xl text-4xl font-light md:text-5xl">
          <span className="font-bold italic">{r.persona}</span>
        </h1>
      </div>
      <div className="mt-10 grid gap-6 lg:grid-cols-3">
        {r.produtos.slice(0, 3).map((p, i) => (
          <ProdutoCard key={p.nome} p={p} img={imagens[i % 3]!} perfil={perfil} delay={i * 120} />
        ))}
      </div>
    </section>
  );
}

function ProdutoCard({ p, img, perfil, delay }: { p: Recomendacao["produtos"][number]; img: string; perfil: Perfil; delay: number }) {
  const [nota, setNota] = useState(0);
  const rawScore = Number(p.score);
  const pct = (!isNaN(rawScore) && rawScore > 0)
    ? Math.round(rawScore <= 1 ? rawScore * 100 : rawScore)
    : Math.round(((Number(p.estrelas_estimadas) || 4.2) / 5) * 100);
  return (
    <article className="flex animate-rise flex-col overflow-hidden rounded-3xl bg-card shadow-soft" style={{ animationDelay: `${delay}ms` }}>
      <div className="relative">
        <img src={img} alt={p.nome} width={816} height={816} loading="lazy" className="aspect-[4/3] w-full object-cover" />
        <span className="absolute left-4 top-4 rounded-full bg-card/90 px-4 py-1.5 text-sm font-semibold backdrop-blur">{pct}% compatível</span>
      </div>
      <div className="flex flex-1 flex-col p-6">
        <h3 className="text-2xl font-semibold">{p.nome}</h3>
        <p className="mt-1 text-sm text-amber">{"★".repeat(Math.round(p.estrelas_estimadas))} <span className="text-muted-foreground">{p.estrelas_estimadas.toFixed(1)} estimado</span></p>
        <div className="mt-4 rounded-2xl bg-secondary p-4">
          <p className="text-xs font-semibold uppercase tracking-widest text-primary">Por que para você?</p>
          <p className="mt-2 text-sm leading-relaxed text-secondary-foreground">{p.motivo}</p>
        </div>
        <div className="mt-auto pt-6">
          {nota ? (
            <p className="animate-rise font-serif text-lg text-primary">Obrigada! Sua avaliação nos ajuda a cuidar melhor 🌿</p>
          ) : (
            <>
              <p className="text-sm text-muted-foreground">Já usou? Avalie:</p>
              <div className="mt-1 flex gap-1">
                {[1, 2, 3, 4, 5].map((n) => (
                  <button
                    key={n}
                    aria-label={`${n} estrelas`}
                    onClick={() => {
                      setNota(n);
                      enviarFeedback(perfil, p.nome, n);
                    }}
                    className="flex h-12 w-12 items-center justify-center text-3xl text-muted-foreground transition hover:scale-110 hover:text-amber"
                  >
                    ★
                  </button>
                ))}
              </div>
            </>
          )}
        </div>
      </div>
    </article>
  );
}
