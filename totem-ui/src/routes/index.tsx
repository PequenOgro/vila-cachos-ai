import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { recomendacaoDemo, recomendar, type Perfil, type Recomendacao } from "@/lib/api";
import { Inicio } from "@/components/totem/Inicio";
import { Anamnese } from "@/components/totem/Anamnese";
import { Processando } from "@/components/totem/Processando";
import { Resultado } from "@/components/totem/Resultado";
import { type FormAnamnese } from "@/components/totem/AnamneseShared";

/**
 * =====================================================================
 * CONFIGURAÇÃO DA ROTA RAIZ (TOTEM VILA CACHOS)
 * =====================================================================
 * Configura metadados de SEO, Open Graph e vincula o componente Totem.
 */
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
function Totem() {
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
    </main>
  );
}
