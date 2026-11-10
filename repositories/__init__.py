"""
Camada de Repositórios (Persistência e Acesso a Dados).
Clean Architecture - DIP (Dependency Inversion Principle).
"""

from .feedback_repository import FeedbackRepository, CsvFeedbackRepository

__all__ = ["FeedbackRepository", "CsvFeedbackRepository"]
