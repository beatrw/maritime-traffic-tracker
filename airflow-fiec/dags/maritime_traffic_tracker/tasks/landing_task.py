import requests
import zipfile
import io
import re
import os

from fiec_plugin.spark_config import create_spark_session
from fiec_plugin.storage_paths import StoragePaths
from fiec_plugin.logging_config import configure_logging

class DataExtractor:
    """Classe responsável por extrair dados da ANTAQ e salvá-los em um Data Lake
    local"""

    def __init__(self):
        self.log = configure_logging()

    def execute(self, *args) -> None:
        """Executa o fluxo das funções"""

        self.spark = create_spark_session("landing_task")
        self.storage = StoragePaths()

        self.year = args[0]
        self.destination_layer = "data_lake/landing"

        data = self._extract()
        self._process_zip(data)
        self._post_processing()


    def _extract(self) -> str:
        """Extrai dados da ANTAQ

        Returns:
        response.content (str): Conteúdo da requisição HTTP
        """

        self.log.info(f"Iniciando extração de dados {self.year}")

        url = f"https://web3.antaq.gov.br/ea/txt/{self.year}.zip"

        session = requests.Session()
        response = session.get(url)

        if response.status_code == 200:
            self.log.info("Arquivos capturados com sucesso.")
        else:
            raise Exception(f"Erro ao fazer o download: {response.status_code}")

        return response.content

    def _process_zip(self, data: str) -> None:
        """Extrai os arquivos zipados e salva-os no storage.

        Args:
            data (str): O conteúdo da requisição HTTP da extração dos arquivos.
        """

        self.log.info("Deszipando")
        with zipfile.ZipFile(io.BytesIO(data)) as zip_ref:
            for file_name in zip_ref.namelist():
                if file_name.endswith('.txt'):

                    path = re.sub(r'^\d+|\.txt$', '', file_name)
                    self.log.info(f"Processando arquivo: {file_name}")

                    with zip_ref.open(file_name) as file:
                        linhas = file.read().decode("utf-8").splitlines()

                        temp_txt_path = self.storage.get_path_in_layer(
                            self.destination_layer,
                            f"{path}/{file_name}"
                        )

                        self.log.info(f"Salvando arquivo .txt em: {temp_txt_path}")
                        temp_dir = os.path.dirname(temp_txt_path)
                        if not os.path.exists(temp_dir):
                            os.makedirs(temp_dir)

                        with open(temp_txt_path, 'w', encoding='utf-8') as temp_file:
                            for linha in linhas:
                                temp_file.write(linha + '\n')

                    df = self.spark.read.option("delimiter", ";").option("header", "true").csv(temp_txt_path)

                    final_path = self.storage.get_path_in_layer(
                        self.destination_layer,
                        f"{path}/{file_name.replace('.txt', '')}"
                    )

                    self.log.info(f"Salvando arquivo em: {final_path}")

                    df.write.mode("overwrite").parquet(final_path)

                    if os.path.exists(temp_txt_path):
                        os.remove(temp_txt_path)

    def _post_processing(self) -> None:
        """Processos a serem executados ao final das transformações, como
        finalizar a session spark"""

        self.spark.stop()

        self.log.info("Extração realizada com sucesso")
