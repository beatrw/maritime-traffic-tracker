from pyspark.sql import DataFrame
from pyspark.sql.functions import col, when, regexp_replace, sum

from fiec_plugin.logging_config import configure_logging
from fiec_plugin.spark_config import create_spark_session
from fiec_plugin.storage_paths import StoragePaths


class CargaRulesInjector:
    """Classe responsável pela ingestão de regras de negócio nos dados
    """

    def __init__(self):

        self.log = configure_logging()

    def execute(self) -> None:
        """Executa o fluxo das funções"""

        self.origin_layer = "data_lake/trusted"
        self.destination_layer = "banco_de_dados"

        self.spark = create_spark_session('business_carga_task')
        self.storage = StoragePaths()

        df_carga, df_atracacao, df_carga_conteinerizada = self._read_parquet()
        df_join = self._join_dfs(df_carga, df_atracacao, df_carga_conteinerizada)
        df_transformed = self._transform_columns(df_join)
        self._to_parquet(df_transformed)

        self._post_processing()


    def _read_parquet(self) -> DataFrame:
        """Lê todos os arquivos parquet da pasta especificada

        Returns:
            df_atracacao (DataFrame): O dataframe da tabela Atracação
            df_tempos_atracacao (DataFrame): O dataframe da tabela Tempos Atracação
        """

        self.log.info("Lendo arquivo")

        carga_path = self.storage.get_path_in_layer(self.origin_layer, "Carga")
        df_carga = self.spark.read.parquet(carga_path)

        atracacao_path = self.storage.get_path_in_layer(self.origin_layer, "Atracacao")
        df_atracaco = self.spark.read.parquet(atracacao_path)

        carga_conteinerizada_path = self.storage.get_path_in_layer(self.origin_layer, "Carga_Conteinerizada")
        df_carga_conteinerizada = self.spark.read.parquet(carga_conteinerizada_path)

        return df_carga, df_atracaco, df_carga_conteinerizada

    def _join_dfs(self, df_carga: DataFrame,
                df_atracacao: DataFrame,
                df_carga_conteinerizada: DataFrame) -> DataFrame:
        """Realiza o join entre os dfs de Carga, Atracação e Carga Conteinerizada

        Args:
            df_carga (DataFrame): O dataframe com dados de carga
            df_atracacao (DataFrame): O dataframe com dados de atracacao
            df_carga_conteinerizada (DataFrame): O dataframe com dados de carga conteinerizada

        Returns:
            df_full (DataFrame): O dataframe completo pós join
        """

        self.log.info("Realizando o join entre as tabelas")

        df_atracacao = df_atracacao.select("id_atracacao", "ano", "mes",
                                    "porto_atracacao", "sguf")

        df_full = (df_carga
                .join(df_atracacao, "id_atracacao", "left")
                .join(df_carga_conteinerizada, "id_carga", "left"))

        return df_full

    def _transform_columns(self, df: DataFrame) -> DataFrame:
        """Realiza definição do codigo de mercadoria de acordo com seu tipo de
        carga, calcula o valor liquido da carga

        Args:
            df (Dataframe): O dataframe a ser transformado

        Returns:
            df_full (DataFrame): O dataframe completo pós join
        """

        df = df.withColumn(
            "cd_mercadoria",
            when(col("carga_geral_acondicionamento") == "Conteinerizada", col("cd_mercadoria_conteinerizada"))
            .otherwise(col("cd_mercadoria"))
        )

        df = (df.withColumn("vl_peso_carga_bruta",
                regexp_replace(col("vl_peso_carga_bruta"), ",", ".")
                .cast("double"))
                .withColumn("vl_peso_carga_conteinerizada",
                regexp_replace(col("vl_peso_carga_conteinerizada"), ",", ".")
                .cast("double")))

        sum_conteinerizado = df.groupBy("id_carga").agg(
            sum("vl_peso_carga_conteinerizada").alias("soma_peso_conteinerizada")
        )

        df = df.join(sum_conteinerizado, "id_carga", "left")

        df = df.withColumn("soma_peso_conteinerizada",
                                col("soma_peso_conteinerizada").cast("double"))

        df_transformed = (df.withColumn(
            "peso_liquido_da_carga",
            when(
                col("carga_geral_acondicionamento") == "Conteinerizada",
                col("soma_peso_conteinerizada")
            ).otherwise(col("vl_peso_carga_bruta"))
        ))

        df_transformed = (df_transformed
                        .drop("cd_mercadoria_conteinerizada",
                        "soma_peso_conteinerizada", "vl_peso_carga_conteinerizada")
                        .withColumn("ano_data_inicio_operacao", col("ano"))
                        .withColumn("mes_data_inicio_operacao", col("mes")))

        return df_transformed

    def _to_parquet(self, df: DataFrame) -> None:
        """Salva o arquivo transformado em parquet.

        Args:
            df (dataframe): O dataframe pyspark final.
        """

        self.log.info("Salvando dataframe")

        file_name = "carga_fato"

        final_path = self.storage.get_path_in_layer(self.destination_layer, file_name)

        df.write.mode("overwrite") \
            .partitionBy("ano", "mes") \
            .parquet(final_path)

    def _post_processing(self) -> None:
        """Processos a serem executados ao final das transformações, como
        finalizar a session spark"""

        self.spark.stop()

        self.log.info("Extração realizada com sucesso")