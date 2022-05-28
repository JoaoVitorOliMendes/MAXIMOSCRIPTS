# ------------------------------------------------------
# MaximoCon, Março de 2022
# Objetivo: Script da Base de Conhecimento para tornar obrigatorio o campo ATIVO 
#  RELACIONADO quando o escopo = "ATIVO", além de adicionar valor a tag especial 
#  JM_RECORDTYPE
# Autor: João Vitor de Oliveira Mendes
# ------------------------------------------------------

# ADD
# Define o atributo tipo do registro ao inserir
if launchPoint=='ADD' and onadd:
    mbo.setValue('JM_RECORDTYPE','BC')

# JM_TYPE
# Determina acesso e valor do campo Ativo Relacionado (SUASINICIAIS_ASSETNUM) com Base no Escopo (SUASINICIAIS_TYPE)
if launchPoint in ['JM_TYPE','ADD']:
    if mbo.getString('JM_TYPE') == 'ATIVO':
        mbo.getMboValue('JM_ASSETNUM').setRequired(True)
    else:
        mbo.getMboValue('JM_ASSETNUM').setRequired(False)
        mbo.setValueNull('JM_ASSETNUM', mbo.NOACCESSCHECK)
