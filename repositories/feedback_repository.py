"""
feedback_repository.py
Contrato abstrato e implementação concreta de persistência de feedbacks e dados históricos.

Padrões aplicados:
- Clean Architecture: Isolamento da camada de persistência.
- Dependency Inversion Principle (DIP): Motores e Controladores dependem da interface abstrata FeedbackRepository.
"""

from abc import ABC, abstractmethod
import os
import sys
import threading
import pandas as pd
from typing import Dict, Any, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)


def sanitizar_campo_csv(valor: Any) -> Any:
    """
    Previne CSV Formula Injection (OWASP A03).
    Se uma string começar com caracteres executáveis por planilhas ('=', '+', '-', '@', '\t', '\r'),
    neutraliza adicionando um apóstrofo (') seguro no início.
    """
    if isinstance(valor, str):
        v = valor.strip()
        if v and v[0] in ("=", "+", "-", "@", "\t", "\r"):
            return f"'{v}"
        return v
    return valor


class FeedbackRepository(ABC):
    """Interface abstrata para armazenamento e recuperação de feedbacks e histórico de clientes."""

    @abstractmethod
    def obter_historico(self) -> pd.DataFrame:
        """Retorna o DataFrame histórico de clientes e avaliações."""
        pass

    @abstractmethod
    def salvar_feedback(
        self,
        perfil_cliente: Dict[str, Any],
        nome_produto: str,
        nota_satisfacao: int,
        cluster_id: int
    ) -> None:
        """Persiste um novo feedback pós-atendimento."""
        pass

    @abstractmethod
    def obter_total_avaliacoes(self) -> int:
        """Retorna o número total de registros no histórico."""
        pass

    @abstractmethod
    def obter_media_global(self) -> float:
        """Retorna a média global de satisfação das avaliações."""
        pass


class CsvFeedbackRepository(FeedbackRepository):
    """
    Implementação concreta baseada em arquivo CSV para persistência analítica.
    Permite fácil transição futura para bancos relacionais (PostgreSQL/SQLite) sem impactar o domínio.
    """

    def __init__(self, csv_path: Optional[str] = None):
        if csv_path:
            self.csv_path = csv_path
        else:
            # Resolução padrão: data/dataset_historico_vila_cachos.csv ou fallback raiz
            data_dir = os.path.join(BASE_DIR, "data")
            caminho_preferencial = os.path.join(data_dir, "dataset_historico_vila_cachos.csv")
            caminho_raiz = os.path.join(BASE_DIR, "dataset_historico_vila_cachos.csv")

            if os.path.exists(caminho_preferencial):
                self.csv_path = caminho_preferencial
            elif os.path.exists(caminho_raiz):
                self.csv_path = caminho_raiz
            else:
                os.makedirs(data_dir, exist_ok=True)
                self.csv_path = caminho_preferencial

        self._lock = threading.Lock()
        self._df_cache: Optional[pd.DataFrame] = None
        self._carregar_ou_inicializar()

    def _carregar_ou_inicializar(self) -> None:
        """Carrega a base do disco ou gera o dataset causal inicial se não existir."""
        with self._lock:
            if os.path.exists(self.csv_path) and os.path.getsize(self.csv_path) > 0:
                self._df_cache = pd.read_csv(self.csv_path)
            else:
                try:
                    from generate_dataset import gerar_dataset_causal
                    df_inicial = gerar_dataset_causal(num_clientes=1000, seed=42)
                except Exception:
                    # Estrutura mínima se o gerador não estiver disponível
                    cols = [
                        'curvatura', 'porosidade', 'dano_quimico',
                        'ressecamento_opacidade', 'alta_porosidade_quimica',
                        'frizz_falta_definicao', 'transicao_capilar',
                        'couro_sensivel_oleoso', 'produto_recomendado',
                        'nota_satisfacao', 'cluster'
                    ]
                    df_inicial = pd.DataFrame(columns=cols)

                os.makedirs(os.path.dirname(os.path.abspath(self.csv_path)), exist_ok=True)
                df_inicial.to_csv(self.csv_path, index=False, encoding="utf-8")
                self._df_cache = df_inicial

    def obter_historico(self) -> pd.DataFrame:
        with self._lock:
            if self._df_cache is None:
                self._carregar_ou_inicializar()
            return self._df_cache.copy()

    def salvar_feedback(
        self,
        perfil_cliente: Dict[str, Any],
        nome_produto: str,
        nota_satisfacao: int,
        cluster_id: int
    ) -> None:
        # Sanitização contra CSV Injection em campos de texto
        novo_registro = {k: sanitizar_campo_csv(v) for k, v in perfil_cliente.items()}
        novo_registro["produto_recomendado"] = sanitizar_campo_csv(nome_produto)
        novo_registro["nota_satisfacao"] = int(nota_satisfacao)
        novo_registro["cluster"] = int(cluster_id)

        df_novo = pd.DataFrame([novo_registro])

        with self._lock:
            if self._df_cache is None or self._df_cache.empty:
                self._df_cache = df_novo
            else:
                self._df_cache = pd.concat([self._df_cache, df_novo], ignore_index=True)

            os.makedirs(os.path.dirname(os.path.abspath(self.csv_path)), exist_ok=True)
            self._df_cache.to_csv(self.csv_path, index=False, encoding="utf-8")

    def obter_total_avaliacoes(self) -> int:
        if self._df_cache is None:
            return 0
        return len(self._df_cache)

    def obter_media_global(self) -> float:
        if self._df_cache is None or "nota_satisfacao" not in self._df_cache.columns or self._df_cache.empty:
            return 3.5
        media = float(self._df_cache["nota_satisfacao"].mean())
        return round(media, 4)
