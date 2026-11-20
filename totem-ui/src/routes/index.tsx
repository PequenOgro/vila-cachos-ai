import { createFileRoute } from "@tanstack/react-router";
import { TotemFlow } from "@/components/totem/TotemFlow";

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

function Totem() {
  return <TotemFlow />;
}
