class GetSchemas():

    ATRACACAO_SCHEMA = {
        "IDAtracacao": "id_atracacao",
        "CDTUP": "cdtup",
        "IDBerco": "id_berco",
        "Berço": "berco",
        "Porto Atracação": "porto_atracacao",
        "Coordenadas": "coordenadas",
        "Apelido Instalação Portuária": "apelido_instalacao_portuaria",
        "Complexo Portuário": "complexo_portuario",
        "Tipo da Autoridade Portuária": "tipo_da_autoridade_portuaria",
        "Data Atracação": "data_atracacao",
        "Data Chegada": "data_chegada",
        "Data Desatracação": "data_desatracacao",
        "Data Início Operação": "data_inicio_operacao",
        "Data Término Operação": "data_termino_operacao",
        "Ano": "ano",
        "Mes": "mes",
        "Tipo de Operação": "tipo_de_operacao",
        "Tipo de Navegação da Atracação": "tipo_de_navegacao_da_atracacao",
        "Nacionalidade do Armador": "nacionalidade_do_armador",
        "FlagMCOperacaoAtracacao": "flag_mc_operacao_atracacao",
        "Terminal": "terminal",
        "Município": "municipio",
        "UF": "uf",
        "SGUF": "sguf",
        "Região Geográfica": "regiao_geografica",
        "Região Hidrográfica": "regiao_hidrografica",
        "Instalação Portuária em Rio": "instalacao_portuaria_em_rio",
        "Nº da Capitania": "numero_da_capitania",
        "Nº do IMO": "numero_do_imo"
        }

    CARGA_SCHEMA = {
        "IDCarga": "id_carga",
        "IDAtracacao": "id_atracacao",
        "Origem": "origem",
        "Destino": "destino",
        "CDMercadoria": "cd_mercadoria",
        "Tipo Operação da Carga": "tipo_operacao_da_carga",
        "Carga Geral Acondicionamento": "carga_geral_acondicionamento",
        "ConteinerEstado": "conteiner_estado",
        "Tipo Navegação": "tipo_navegacao",
        "FlagAutorizacao": "flag_autorizacao",
        "FlagCabotagem": "flag_cabotagem",
        "FlagCabotagemMovimentacao": "flag_cabotagem_movimentacao",
        "FlagConteinerTamanho": "flag_conteiner_tamanho",
        "FlagLongoCurso": "flag_longo_curso",
        "FlagMCOperacaoCarga": "flag_mc_operacao_carga",
        "FlagOffshore": "flag_offshore",
        "FlagTransporteViaInterioir": "flag_transporte_via_interior",
        "Percurso Transporte em vias Interiores": "percurso_transporte_em_vias_interiores",
        "Percurso Transporte Interiores": "percurso_transporte_interiores",
        "STNaturezaCarga": "st_natureza_carga",
        "STSH2": "stsh2",
        "STSH4": "stsh4",
        "Natureza da Carga": "natureza_da_carga",
        "Sentido": "sentido",
        "TEU": "teu",
        "QTCarga": "qt_carga",
        "VLPesoCargaBruta": "vl_peso_carga_bruta"
        }

    CARGA_CONTEINERIZADA_SCHEMA = {
        "IDCarga": "id_carga",
        "VLPesoCargaConteinerizada": "vl_peso_carga_conteinerizada",
        "CDMercadoriaConteinerizada": "cd_mercadoria_conteinerizada"
    }

    CARGA_HIDROVIA_SCHEMA = {
        "IDCarga": "id_carga",
        "Hidrovia": "hidrovia",
        "ValorMovimentado": "valor_movimentado"
        }

    CARGA_REGIAO_SCHEMA = {
        "IDCarga": "id_carga",
        "Região Hidrográfica": "regiao_hidrografica",
        "ValorMovimentado": "valor_movimentado"
    }

    CARGA_RIO_SCHEMA = {
        "IDCarga": "id_carga",
        "Rio": "rio",
        "ValorMovimentado": "valor_movimentado"
    }

    TAXA_OCUPACAO_SCHEMA = {
        "IDBerco": "id_berco",
        "DiaTaxaOcupacao": "dia_taxa_ocupacao",
        "MêsTaxaOcupacao": "mes_taxa_ocupacao",
        "AnoTaxaOcupacao": "ano_taxa_ocupacao",
        "TempoEmMinutosdias": "tempo_em_minutos_dias"
    }

    TAXA_OCUPACAO_COM_CARGA_SCHEMA ={
        "IDBerco": "id_berco",
        "DiaTaxaOcupacao": "dia_taxa_ocupacao",
        "MêsTaxaOcupacao": "mes_taxa_ocupacao",
        "AnoTaxaOcupacao": "ano_taxa_ocupacao",
        "TempoEmMinutosdiasFlagCarga": "tempo_em_minutos_dias_flag_carga"
    }

    TAXA_OCUPACAO_TO_ATRACACAO_SCHEMA = {
        "IDBerco": "id_berco",
        "DSTipoOperacaoAtracacaoTaxaOcupacao": "dstipo_operacao_atracacao_taxa_ocupacao",
        "DiaTaxaOcupacao": "dia_taxa_ocupacao",
        "MêsTaxaOcupacao": "mes_taxa_ocupacao",
        "AnoTaxaOcupacao": "ano_taxa_ocupacao",
        "TempoEmMinutosdiasTOAtracacao": "tempo_em_minutos_dias_to_atracacao"
    }

    TEMPOS_ATRACACAO_SCHEMA = {
        "IDAtracacao": "id_atracacao",
        "TEsperaAtracacao": "tespera_atracacao",
        "TEsperaInicioOp": "tespera_inicio_op",
        "TOperacao": "toperacao",
        "TEsperaDesatracacao": "tespera_desatracacao",
        "TAtracado": "tatracado",
        "TEstadia": "testadia"
    }

    TEMPOS_ATRACACAO_PARALIZACAO_SCHEMA = column_mapping = {
        "IDTemposDescontos": "id_tempos_descontos",
        "IDAtracacao": "id_atracacao",
        "DescricaoTempoDesconto": "descricao_tempo_desconto",
        "DTInicio": "dtinicio",
        "DTTermino": "dttermino"
    }


    schemas = {
        "Atracacao": ATRACACAO_SCHEMA,
        "Carga": CARGA_SCHEMA,
        "Carga_Conteinerizada": CARGA_CONTEINERIZADA_SCHEMA,
        "Carga_Hidrovia": CARGA_HIDROVIA_SCHEMA,
        "Carga_Regiao": CARGA_REGIAO_SCHEMA,
        "Carga_Rio": CARGA_RIO_SCHEMA,
        "TaxaOcupacao": TAXA_OCUPACAO_SCHEMA,
        "TaxaOcupacaoComCarga": TAXA_OCUPACAO_COM_CARGA_SCHEMA,
        "TaxaOcupacaoTOAatracacao": TAXA_OCUPACAO_TO_ATRACACAO_SCHEMA,
        "TaxaOcupacaoTOAtracacao": TAXA_OCUPACAO_TO_ATRACACAO_SCHEMA,
        "TemposAtracacao": TEMPOS_ATRACACAO_SCHEMA,
        "TemposAtracacaoParalisacao": TEMPOS_ATRACACAO_PARALIZACAO_SCHEMA,
    }