from pyspark.sql import DataFrame
from pyspark.sql.functions import col, round, to_timestamp, regexp_replace

from fiec_plugin.logging_config import configure_logging
from fiec_plugin.spark_config import create_spark_session
from fiec_plugin.storage_paths import StoragePaths


class AtracacaoRulesInjector:
    """Classe responsável pela ingestão de regras de negócio nos dados
    """

    def __init__(self):

        self.log = configure_logging()

    def execute(self) -> None:
        """Executa o fluxo das funções"""

        self.origin_layer = "data_lake/trusted"
        self.destination_layer = "banco_de_dados"

        self.spark = create_spark_session('business_atracacao_task')
        self.storage = StoragePaths()

        df_atracacao, df_tempos_atracacao = self._read_parquet()
        df_join = self._join_dfs(df_atracacao, df_tempos_atracacao)
        df_formatted = self._format_columns(df_join)
        self._to_parquet(df_formatted)

        self._post_processing()


    def _read_parquet(self) -> DataFrame:
        """Lê todos os arquivos parquet da pasta especificada

        Returns:
            df_atracacao (DataFrame): O dataframe da tabela Atracação
            df_tempos_atracacao (DataFrame): O dataframe da tabela Tempos Atracação
        """

        self.log.info("Lendo arquivo")

        atracacao_path = self.storage.get_path_in_layer(self.origin_layer, "Atracacao")
        df_atracacao = self.spark.read.parquet(atracacao_path)

        tempos_atracacao_path = self.storage.get_path_in_layer(self.origin_layer, "TemposAtracacao")
        df_tempos_atracacao = self.spark.read.parquet(tempos_atracacao_path)

        return df_atracacao, df_tempos_atracacao

    def _join_dfs(self, df_atracacao: DataFrame,
                df_tempos_atracacao: DataFrame) -> DataFrame:
        """Realiza o join entre os dfs de Atracação e de Tempos Atracação

        Args:
            df_atracacao (DataFrame): O dataframe com dados de atracação
            df_tempos_atracacao (DataFrame): O dataframe com dados de tempo de atracação

        Returns:
            df_full (DataFrame): O dataframe completo pós join
        """

        self.log.info("Realizando o join entre as tabelas")

        df_full = df_atracacao.join(
            df_tempos_atracacao,
            "id_atracacao",
            "left"
        ).drop("coordenadas",
            "regiao_hidrografica",
            "instalacao_portuaria_em_rio")

        return df_full

    def _format_columns(self, df: DataFrame) -> DataFrame:
        """Realiza a formatação de tipos de colunas e ajustes de colunas de
        particionamento

        Args:
            df (Dataframe): O dataframe a ser formatado

        Returns:
            df_full (DataFrame): O dataframe completo pós join
        """

        self.log.info("Formatando colunas")

        float_cols = ["tespera_atracacao", "tespera_inicio_op", "toperacao",
                    "tespera_desatracacao", "tatracado", "testadia"]

        for coluna in float_cols:
            df = df.withColumn(
                coluna,
                    round(regexp_replace(col(coluna), ",", ".").cast("float"), 3))


        date_cols = ["data_atracacao", "data_chegada", "data_desatracacao",
                    "data_inicio_operacao", "data_termino_operacao"]

        for column in date_cols:
            df = df.withColumn(
                column,
                to_timestamp(col(column),
                'dd/MM/yyyy HH:mm:ss')
            )

        df_formatted = df.withColumn("ano_data_inicio_operacao", col("ano"))\
                    .withColumn("mes_data_inicio_operacao", col("mes"))

        return df_formatted

    def _to_parquet(self, df: DataFrame) -> None:
        """Salva o arquivo transformado em parquet.

        Args:
            df (dataframe): O dataframe pyspark final.
        """

        self.log.info("Salvando dataframe")

        file_name = "atracacao_fato"

        final_path = self.storage.get_path_in_layer(self.destination_layer, file_name)

        df.write.mode("overwrite") \
            .partitionBy("ano", "mes") \
            .parquet(final_path)

    def _post_processing(self) -> None:
        """Processos a serem executados ao final das transformações, como
        finalizar a session spark"""

        self.spark.stop()

        self.log.info("Extração realizada com sucesso")