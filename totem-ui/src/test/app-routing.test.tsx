import fs from "node:fs";
import path from "node:path";
import { QueryClient } from "@tanstack/react-query";
import { createRouter, rootRouteId } from "@tanstack/react-router";
import { afterEach, describe, expect, it, vi } from "vitest";

import { getImagemProduto } from "@/components/totem/product-images";
import { obterCatalogo } from "@/lib/api";
import { CATALOGO_OFICIAL_27 } from "@/lib/catalogo-oficial";
import { routeTree } from "@/routeTree.gen";

// Match routes without running loaders or rendering: loaders may need a server or
// network the test run lacks, and jsdom never loads the stylesheets React waits on.
describe("App routing", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("matches /, /admin, and /totem to their respective routes instead of not found", () => {
    const router = createRouter({ routeTree, context: { queryClient: new QueryClient() } });

    const rootMatch = router.matchRoutes("/");
    const adminMatch = router.matchRoutes("/admin");
    const totemMatch = router.matchRoutes("/totem");

    expect(rootMatch.at(-1)?.routeId).toBe("/");
    expect(rootMatch.at(-1)?.routeId).not.toBe(rootRouteId);

    expect(adminMatch.at(-1)?.routeId).toBe("/admin");
    expect(adminMatch.at(-1)?.routeId).not.toBe(rootRouteId);

    expect(totemMatch.at(-1)?.routeId).toBe("/totem");
    expect(totemMatch.at(-1)?.routeId).not.toBe(rootRouteId);
  });

  it("does not match an unknown route to /, /admin, or /totem", () => {
    const router = createRouter({ routeTree, context: { queryClient: new QueryClient() } });

    const unknownMatches = router.matchRoutes("/nao-existe");
    const matchedIds = unknownMatches.map((m) => m.routeId);

    expect(matchedIds).not.toContain("/");
    expect(matchedIds).not.toContain("/admin");
    expect(matchedIds).not.toContain("/totem");
  });

  it("keeps route components non-exported so @tanstack/router-plugin autoCodeSplitting stays active", () => {
    const routesDir = path.resolve(process.cwd(), "src/routes");
    const adminSrc = fs.readFileSync(path.join(routesDir, "admin.tsx"), "utf-8");
    const indexSrc = fs.readFileSync(path.join(routesDir, "index.tsx"), "utf-8");
    const totemSrc = fs.readFileSync(path.join(routesDir, "totem.tsx"), "utf-8");

    expect(adminSrc).not.toMatch(/export\s+(?:default\s+)?(?:function|const)\s+AdminPage\b/);
    expect(indexSrc).not.toMatch(/export\s+(?:default\s+)?(?:function|const)\s+Totem\b/);
    expect(totemSrc).not.toMatch(/export\s+(?:default\s+)?(?:function|const)\s+TotemRoute\b/);
  });

  it("resolves all 27 canonical products dynamically in obterCatalogo() when fetch fails", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("Network offline")));

    const catalogo = await obterCatalogo();

    expect(catalogo).toHaveLength(27);
    expect(catalogo[0]?.id).toBe("PROD_01");
    expect(catalogo[26]?.id).toBe("PROD_27");
  });

  it("maps all 27 products in CATALOGO_OFICIAL_27 to .webp assets with PROD_14, PROD_17, and PROD_21 fixes", () => {
    expect(CATALOGO_OFICIAL_27).toHaveLength(27);

    for (const produto of CATALOGO_OFICIAL_27) {
      const img = getImagemProduto(produto.nome);
      expect(img).toBeTruthy();
      expect(img).toMatch(/\.webp(\?.*)?$/);
    }

    const prod14 = CATALOGO_OFICIAL_27.find((p) => p.id === "PROD_14");
    const prod17 = CATALOGO_OFICIAL_27.find((p) => p.id === "PROD_17");
    const prod21 = CATALOGO_OFICIAL_27.find((p) => p.id === "PROD_21");

    expect(prod14).toBeDefined();
    expect(prod17).toBeDefined();
    expect(prod21).toBeDefined();

    expect(getImagemProduto(prod14!.nome)).toContain("curly-care-fix-u");
    expect(getImagemProduto(prod17!.nome)).toContain("curly-care-no-spume");
    expect(getImagemProduto(prod21!.nome)).toContain("curly-care-fix-u");
  });
});
