import { Suspense, lazy, useState, useEffect } from "react";
import { recomendacaoDemo, recomendar, type Perfil, type Recomendacao } from "@/lib/api";
import { Inicio } from "@/components/totem/Inicio";
import { type FormAnamnese } from "@/components/totem/AnamneseShared";

const Anamnese = lazy(() =>
  import("@/components/totem/Anamnese").then((m) => ({ default: m.Anamnese })),
);
const Processando = lazy(() =>
  import("@/components/totem/Processando").then((m) => ({ default: m.Processando })),
);
const Resultado = lazy(() =>
  import("@/components/totem/Resultado").then((m) => ({ default: m.Resultado })),
);

function TotemStageFallback() {
  return (
    <div className="flex min-h-dvh items-center justify-center bg-background p-8 text-center font-serif text-muted-foreground">
      Carregando diagnóstico capilar…
    </div>
  );
}

/** Estados possíveis da máquina de estados do totem */
type Etapa = "inicio" | "anamnese" | "processando" | "resultado";

/** Estado inicial limpo do formulário */
const FORM_INICIAL: FormAnamnese = {
  curvatura: null,
  porosidade: null,
  quimica: null,
  queixas: [],
};

/**
 * =====================================================================
 * CONTROLADOR PRINCIPAL DO TOTEM (MÁQUINA DE ESTADOS)
 * =====================================================================
 * Responsabilidade Única (SRP):
 * Gerenciar a transição de fluxo (Início -> Anamnese -> Processando -> Resultado),
 * converter as respostas do formulário no vetor tricológico de 8 dimensões
 * e orquestrar a chamada ao motor híbrido de recomendação.
 */
export function TotemFlow() {
  const [etapa, setEtapa] = useState<Etapa>("inicio");
  const [form, setForm] = useState<FormAnamnese>(FORM_INICIAL);
  const [resultado, setResultado] = useState<Recomendacao | null>(null);
  const [perfil, setPerfil] = useState<Perfil | null>(null);

  /**
   * Reseta todo o estado para permitir que uma nova cliente inicie seu diagnóstico.
   */
  const reiniciar = () => {
    setForm(FORM_INICIAL);
    setResultado(null);
    setPerfil(null);
    setEtapa("inicio");
  };

  /**
   * RNF-06 (UML Sequência Pág. 1 - Exceção E1):
   * Como o totem touch opera em espaço público, se houver inatividade por 15 minutos,
   * a sessão temporária é destruída por segurança e o sistema retorna à tela inicial.
   */
  useEffect(() => {
    if (etapa === "inicio") return;

    const TEMPO_INATIVIDADE_MS = 15 * 60 * 1000; // 15 minutos
    let timer: ReturnType<typeof setTimeout>;

    const resetTimer = () => {
      clearTimeout(timer);
      timer = setTimeout(() => {
        reiniciar();
      }, TEMPO_INATIVIDADE_MS);
    };

    const eventos = ["mousedown", "mousemove", "keydown", "scroll", "touchstart", "click"];
    eventos.forEach((evento) => window.addEventListener(evento, resetTimer));

    resetTimer();

    return () => {
      clearTimeout(timer);
      eventos.forEach((evento) => window.removeEventListener(evento, resetTimer));
    };
  }, [etapa]);

  /**
   * Normaliza os dados do formulário e consulta a API de recomendação.
   * Cria o vetor de 8 dimensões:
   * [curvatura, porosidade, dano_quimico, transicao, alta_porosidade_quimica, frizz, ressecamento, couro]
   */
  const finalizarAnamnese = async () => {
    const rawPorosidade = Number(form.porosidade);
    const porosidadeNormalizada = rawPorosidade >= 1 && rawPorosidade <= 3 ? rawPorosidade : 2;
    const rawCurvatura = Number(form.curvatura);
    const curvaturaNormalizada = rawCurvatura >= 2 && rawCurvatura <= 4 ? rawCurvatura : 3;
    const queixas = form.queixas || [];

    // Vetor de entrada tricológico
    const perfilCapilar: Perfil = {
      curvatura: curvaturaNormalizada,
      porosidade: porosidadeNormalizada,
      dano_quimico: form.quimica === 2 ? 1 : 0,
      transicao_capilar: form.quimica === 1 ? 1 : 0,
      alta_porosidade_quimica: form.quimica === 2 && porosidadeNormalizada === 3 ? 1 : 0,
      frizz_falta_definicao: queixas.includes("frizz") ? 1 : 0,
      ressecamento_opacidade: queixas.includes("ressecamento") ? 1 : 0,
      couro_sensivel_oleoso: queixas.includes("couro") ? 1 : 0,
    };

    setPerfil(perfilCapilar);
    setEtapa("processando");

    // Pré-aquece o chunk de Resultado enquanto a animação de processamento roda
    void import("@/components/totem/Resultado");

    // Executa a requisição assíncrona garantindo um tempo mínimo de exibição para UX
    const [resposta] = await Promise.all([
      recomendar(perfilCapilar).catch(() => recomendacaoDemo(perfilCapilar)),
      new Promise((res) => setTimeout(res, 3800)),
    ]);

    setResultado(resposta.produtos.length ? resposta : recomendacaoDemo(perfilCapilar));
    setEtapa("resultado");
  };

  return (
    <main className="min-h-dvh bg-background">
      {etapa === "inicio" && <Inicio onStart={() => setEtapa("anamnese")} />}

      {etapa !== "inicio" && (
        <Suspense fallback={<TotemStageFallback />}>
          {etapa === "anamnese" && (
            <Anamnese
              form={form}
              setForm={setForm}
              onVoltar={reiniciar}
              onFinalizar={finalizarAnamnese}
            />
          )}

          {etapa === "processando" && <Processando />}

          {etapa === "resultado" && resultado && perfil && (
            <Resultado r={resultado} perfil={perfil} onReiniciar={reiniciar} />
          )}
        </Suspense>
      )}
    </main>
  );
}
