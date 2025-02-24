from pyspark.sql import DataFrame
from pyspark.sql.functions import col
from functools import reduce


from fiec_plugin.logging_config import configure_logging
from fiec_plugin.spark_config import create_spark_session
from fiec_plugin.storage_paths import StoragePaths

from maritime_traffic_tracker.tools.schemas import GetSchemas

class DataTrasformer:
    """Classe responsável por realizar a transformação dos dados
    """

    def __init__(self):

        self.log = configure_logging()

    def execute(self) -> None:
        """Executa o fluxo das funções"""

        self.origin_layer = "data_lake/landing"
        self.destination_layer = "data_lake/trusted"

        self.spark = create_spark_session("transform_task")
        self.storage = StoragePaths()

        path_list = self.storage.get_file_list_in_layer(self.origin_layer)
        for path in path_list:
            self.log.info(f"Processando {path}")
            df_full = self._read_parquet(path)
            df_renamed = self._rename_columns(path, df_full)
            self._to_parquet(path, df_renamed)

        self._post_processing()


    def _read_parquet(self, path: str) -> DataFrame:
        """Lê todos os arquivos parquet da pasta e junta-os

        Args:
            path (Str): O repositório dentro do Data Lake

        Returns:
            df_full (DataFrame): O dataframe completo
        """

        file_list = self.storage.get_file_list_paths_in_layer(f"{self.origin_layer}/{path}")
        dfs_list = [self.spark.read.parquet(file) \
                    for file in file_list]

        df_full = reduce(lambda df1, df2: df1\
                    .unionByName(df2,allowMissingColumns=True), dfs_list)

        return df_full

    def _rename_columns(self, path: str, df: DataFrame) -> DataFrame:
        """Renomeia as colunas do dataframe, de acordo com seu schema

        Args:
            path (Str): O repositório dentro do Data Lake
            df (DataFrame): O dataframe a ser renomeado

        Returns:
            df_renamed (DataFrame): O dataframe renomeado
        """

        schema = GetSchemas.schemas[path]

        try:
            df_renamed = df.select([col(column).alias(schema[column]) for column in  schema])
        except Exception as err:
            raise Exception(f'Falha ao aplicar o Schema na trusted: {err}')

        return df_renamed

    def _to_parquet(self, path: str, df: DataFrame) -> None:
        """Salva o arquivo transformado em parquet.

        Args:
            df (dataframe): O dataframe pyspark final.
        """

        self.log.info(f"Salvando {path}")

        final_path = self.storage.get_path_in_layer(self.destination_layer, path)

        df.write.mode("overwrite")\
            .parquet(final_path)

    def _post_processing(self) -> None:
        """Processos a serem executados ao final das transformações, como
        finalizar a session spark"""

        self.spark.stop()

        self.log.info("Extração realizada com sucesso")
