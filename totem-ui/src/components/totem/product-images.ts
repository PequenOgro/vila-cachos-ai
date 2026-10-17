/**
 * =====================================================================
 * MAPEAMENTO DE IMAGENS OFICIAIS DOS COSMÉTICOS (VILA CACHOS)
 * =====================================================================
 * Este módulo centraliza os assets gráficos dos produtos cosméticos
 * cadastrados no acervo da Vila Cachos. Assegura resolução transparente
 * e fallback resiliente caso o nome retornado pela API varie ligeiramente.
 */

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

/**
 * Retorna o asset visual oficial correspondente ao nome do cosmético.
 * Utiliza correspondência semântica por substring em lowercase.
 *
 * @param nome Nome do cosmético retornado pelo motor de recomendação.
 * @returns Caminho do asset compilado pelo Vite.
 */
export function getImagemProduto(nome: string): string {
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
