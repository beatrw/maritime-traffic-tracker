from datetime import date
from fiec_plugin.logging_config import configure_logging


class CalculateParams:
    """Classe responsável por calcular os três últimos anos."""

    def __init__(self):
        self.log = configure_logging()

    def execute(self) -> list:
        """Executa o fluxo das funções"""
        data = self._calculate_year()

        return data

    def _calculate_year(self) -> list:
        years = []
        yesterday_year = date.today().year
        for year in range(3):
            last_year = yesterday_year - year - 1
            years.append([last_year])
        return years
