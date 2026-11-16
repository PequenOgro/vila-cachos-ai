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
    <header className="sticky top-0 z-30 border-b border-stone-200/80 bg-white/95 backdrop-blur-md transition-all shadow-xs">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6">
        <div className="flex items-center gap-3 md:gap-5">
          <Link
            to="/"
            className="group inline-flex items-center gap-2 rounded-xl border border-stone-200 bg-stone-50 px-3 py-1.5 text-xs font-semibold text-stone-700 transition hover:border-emerald-300 hover:bg-white hover:text-emerald-800 shadow-2xs"
            title="Voltar ao Totem de Diagnóstico"
          >
            <ArrowLeft className="h-3.5 w-3.5 transition group-hover:-translate-x-0.5" />
            <span className="hidden sm:inline">Voltar ao Totem</span>
            <span className="sm:hidden">Totem</span>
          </Link>

          <div className="flex items-center gap-3 border-l border-stone-200 pl-3 md:pl-5">
            <Logo />
            <div className="flex items-center gap-2">
              <span className="hidden items-center gap-1 rounded-full bg-emerald-50 px-2.5 py-0.5 text-[11px] font-bold text-emerald-800 border border-emerald-200/60 md:inline-flex">
                <Sparkles className="h-3 w-3 text-emerald-600" />
                Painel do Gestor Técnico
              </span>
              <span className="hidden text-[11px] font-medium text-stone-400 lg:inline">
                • Vila Cachos Tricologia & IA
              </span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2.5 sm:gap-3">
          {/* Status da API */}
          <div
            className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-semibold border transition ${
              isOnline
                ? "border-emerald-200 bg-emerald-50/80 text-emerald-800"
                : "border-amber-200 bg-amber-50/80 text-amber-800"
            }`}
          >
            <span
              className={`h-2 w-2 rounded-full ${
                isOnline ? "bg-emerald-500 animate-pulse" : "bg-amber-500"
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
            className="inline-flex items-center gap-1.5 rounded-xl border border-stone-200 bg-white px-3 py-1.5 text-xs font-semibold text-stone-700 shadow-2xs transition hover:border-emerald-300 hover:bg-stone-50 active:scale-95 disabled:opacity-50"
          >
            <RefreshCw
              className={`h-3.5 w-3.5 text-stone-500 ${recarregando ? "animate-spin text-emerald-600" : ""}`}
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
