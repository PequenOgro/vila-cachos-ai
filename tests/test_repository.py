"""
test_repository.py
Testes unitários para o repositório de feedback (Clean Architecture - DIP).
"""

import os
import sys
import tempfile
import unittest
import pandas as pd

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from repositories.feedback_repository import FeedbackRepository, CsvFeedbackRepository


class TestFeedbackRepository(unittest.TestCase):
    def test_csv_feedback_repository_lifecycle(self):
        # Cria arquivo temporário para teste isolado
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # 1. Instancia o repositório
            repo = CsvFeedbackRepository(csv_path=tmp_path)
            self.assertIsInstance(repo, FeedbackRepository)

            # 2. Carrega histórico inicial
            df = repo.obter_historico()
            self.assertIsInstance(df, pd.DataFrame)
            initial_count = repo.obter_total_avaliacoes()
            self.assertGreaterEqual(initial_count, 0)

            # 3. Salva novo feedback
            perfil = {
                "curvatura": 3,
                "porosidade": 2,
                "dano_quimico": 0,
                "ressecamento_opacidade": 1,
                "alta_porosidade_quimica": 0,
                "frizz_falta_definicao": 1,
                "transicao_capilar": 0,
                "couro_sensivel_oleoso": 0
            }
            repo.salvar_feedback(
                perfil_cliente=perfil,
                nome_produto="Curly Care ACID-C (Acidificante Antiporosidade)",
                nota_satisfacao=5,
                cluster_id=1
            )

            # 4. Valida persistência
            self.assertEqual(repo.obter_total_avaliacoes(), initial_count + 1)
            df_apos = repo.obter_historico()
            self.assertEqual(len(df_apos), initial_count + 1)
            self.assertIn("nota_satisfacao", df_apos.columns)
            self.assertGreater(repo.obter_media_global(), 0.0)

        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


if __name__ == "__main__":
    unittest.main()
