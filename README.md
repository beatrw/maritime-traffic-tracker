# Maritime Traffic Tracker Project

Projeto em um ambiente **airflow+docker** que consome dados da ANTAQ (Agência Nacional de
Transportes Aquáticos), transformando-os e persistindo-os em um Data Lake, seguindo a arquitetura de camadas
camadas: landing, trusted e business.

Na pasta de documentação estão todas as instruções sobre como configurar o ambiente Docker, bem como sessões separadas para cada módulo do projeto, detalhando a arquitetura, as escolhas feitas e ideias para monitoramento e alertas.


A seguir, as repostas para perguntas:

1 - Autoavaliação:

- Ferramentas de visualização de dados (Power BI, Qlik Sense e outros): 4
- Manipulação e tratamento de dados com Python: 6
- Manipulação e tratamento de dados com Pyspark: 6
- Desenvolvimento de data workflows em Ambiente Azure com databricks: 6
- Desenvolvimento de data workflows com Airflow: 6
- Manipulação de bases de dados NoSQL: 6
- Web crawling e web scraping para mineração de dados: 6
- Construção de APIs: REST, SOAP e Microservices: 4

2-a:
Considerando os dados disponíveis na fonta, a recomendação seria armazená-los inicialmente em um Data Lake NoSQL. Isso se deve ao fato de que a informação bruta extraída está em formato de arquivos txt zipados, os quais são adequados para armazenamento em um formato de arquivo ou json. O Data Lake NoSQL permite a retenção de grandes volumes de dados não estruturados ou semi-estruturados, como json, sem a necessidade de uma estrutura rígida. Isso facilita a ingestão de dados no formato original, sem precisar de um modelo de dados pré-definido.

Após o processamento e a transformação dos dados, quando estiverem prontos para análise ou consumo por clientes, é recomendado movê-los para um banco de dados SQL. A estrutura SQL é ideal para dados estruturados, permitindo consultas complexas, além de garantir maior consistência e integridade dos dados. Essa mudança de armazenamento entre o Data Lake (para dados brutos) e o banco SQL (para dados estruturados e prontos para consumo) é alinhada com a arquitetura medallion ou de camadas, que usamos no projeto, onde organizamos os dados em diferentes camadas: dados brutos, dados tratados e dados prontos para análise.

2-c:
Considerando que foi pedido dados dos 3 últimos anos = 2022-2024, a seguir se
encontra a query para dados de 2022 e 2024:

```shell
SELECT
    CASE
        WHEN uf = 'CE' THEN 'Ceará'
        WHEN regiao_geografica = 'Nordeste' THEN 'Nordeste'
        WHEN cdtup LIKE 'BR%' THEN 'Brasil'
        ELSE 'Outros'
    END AS Localidade,
    "mes_data_inicio_operacao" AS Mês,
    "ano_data_inicio_operacao" AS Ano,
    COUNT(*) AS "Número de Atracações",
    (COUNT(*) -
        (SELECT COUNT(*)
         FROM atracacao_fato
         WHERE "mes_data_inicio_operacao" = "mes_data_inicio_operacao"
         AND "ano_data_inicio_operacao" = "ano_data_inicio_operacao" - 1
         AND (uf = 'CE' OR regiao_geografica = 'Nordeste' OR cdtup LIKE 'BR%')) 
    ) AS "Variação do Número de Atracações",
    AVG(EXTRACT(EPOCH FROM ("data_inicio_operação" - "data_atracacao")) / 3600) AS "Tempo de Espera Médio (horas)",
    AVG(EXTRACT(EPOCH FROM ("data_desatracacao" - "data_inicio_peracao")) / 3600) AS "Tempo Atracado Médio (horas)"
FROM
    atracacao_fato
WHERE
    ("ano_data_inicio_operacao" IN (2022, 2024))
    AND (uf = 'CE' OR regiao_geografica = 'Nordeste' OR cdtup LIKE 'BR%')
GROUP BY
    Localidade, "mes_data_inicio_operacao", "ano_data_inicio_operacao"
ORDER BY
    Localidade, "mes_data_inicio_operacao", "ano_data_inicio_operacao";
```
