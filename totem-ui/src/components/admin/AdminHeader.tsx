import React from "react";
import { Link } from "@tanstack/react-router";
import { ArrowLeft, RefreshCw, Sparkles, ShieldCheck } from "lucide-react";
import { Logo } from "@/components/totem/Logo";

interface AdminHeaderProps {
  statusTexto?: string;
  isOnline: boolean;
  recarregando: boolean;
  onRecarregar: () => void;
}

export function AdminHeader({
  statusTexto,
  isOnline,
  recarregando,
  onRecarregar,
}: AdminHeaderProps) {
  return (
    <header className="sticky top-0 z-30 border-b border-emerald-950/70 bg-[#0c1410]/95 backdrop-blur-md transition-all shadow-lg shadow-black/20">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6">
        <div className="flex items-center gap-3 md:gap-5">
          <Link
            to="/"
            className="group inline-flex items-center gap-2 rounded-xl border border-stone-800 bg-stone-900/90 px-3 py-1.5 text-xs font-semibold text-stone-200 transition hover:border-emerald-500/60 hover:bg-emerald-950/40 hover:text-emerald-300 shadow-2xs"
            title="Voltar ao Totem de Diagnóstico"
          >
            <ArrowLeft className="h-3.5 w-3.5 transition group-hover:-translate-x-0.5 text-stone-400 group-hover:text-emerald-300" />
            <span className="hidden sm:inline">Voltar ao Totem</span>
            <span className="sm:hidden">Totem</span>
          </Link>

          <div className="flex items-center gap-3 border-l border-stone-800 pl-3 md:pl-5">
            <Logo light />
            <div className="flex items-center gap-2">
              <span className="hidden items-center gap-1.5 rounded-full bg-emerald-950/80 px-2.5 py-0.5 text-[11px] font-bold text-emerald-300 border border-emerald-800/60 md:inline-flex">
                <Sparkles className="h-3 w-3 text-emerald-400" />
                Painel do Gestor Técnico
              </span>
              <span className="hidden text-[11px] font-medium text-stone-400 lg:inline">
                • Vila Cachos Tricologia &amp; IA
              </span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2.5 sm:gap-3">
          {/* Status da API */}
          <div
            className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-semibold border transition ${
              isOnline
                ? "border-emerald-800/80 bg-emerald-950/80 text-emerald-300"
                : "border-amber-800/80 bg-amber-950/80 text-amber-300"
            }`}
          >
            <span
              className={`h-2 w-2 rounded-full ${
                isOnline ? "bg-emerald-400 animate-pulse" : "bg-amber-400"
              }`}
            />
            <span className="capitalize text-[11px]">
              {statusTexto || (isOnline ? "API Conectada" : "Modo Resiliente")}
            </span>
          </div>

          {/* Botão de Recarregar */}
          <button
            onClick={onRecarregar}
            disabled={recarregando}
            aria-label="Recarregar dados"
            className="inline-flex items-center gap-1.5 rounded-xl border border-stone-800 bg-stone-900/90 px-3 py-1.5 text-xs font-semibold text-stone-200 shadow-2xs transition hover:border-emerald-600/60 hover:bg-stone-800 hover:text-white active:scale-95 disabled:opacity-50"
          >
            <RefreshCw
              className={`h-3.5 w-3.5 text-stone-400 ${recarregando ? "animate-spin text-emerald-400" : ""}`}
            />
            <span className="hidden sm:inline">
              {recarregando ? "Sincronizando..." : "Sincronizar"}
            </span>
          </button>
        </div>
      </div>
    </header>
  );
}
