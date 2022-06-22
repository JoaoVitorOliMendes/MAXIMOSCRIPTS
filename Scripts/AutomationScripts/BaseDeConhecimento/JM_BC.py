# ------------------------------------------------------
# MaximoCon, Março de 2022
# Objetivo: Script para adicionar tag especial para assets criados como 
#  Conhecimentos da Base de Conhecimentos, manipula o acesso dos campos de ESCOPO
# Autor: João Vitor de Oliveira Mendes
# ------------------------------------------------------

# INIT
# Define o atributo tipo do registro ao inserir e seu solicitante
if launchPoint=='INIT':
    if onadd:
        mbo.setValue('JM_RECORDTYPE','JM_BC')
        mbo.setValue('JM_REPORTEDBY',mbo.getUserName(), mbo.NOACCESSCHECK)
    if mbo.getString("STATUS") == 'CANCEL':
        mbo.setFlag(mbo.READONLY, True)

# INIT_ITEMS & JM_TYPE
# Se o escopo for igual a Dificuldade ou Risco, seta o campo IMPACTO para Required, senao continua ReadOnly
if launchPoint == 'INIT_ITEMS' or launchPoint == 'JM_TYPE':
        
    if mbo.getString('SCOPE') == 'Dificuldade' or mbo.getString('SCOPE') == 'Risco':
        mbo.getMboValue('IMPACT').setRequired(True)
        mbo.setFieldFlag('IMPACT',mbo.READONLY, False)
    else:
        mbo.getMboValue('IMPACT').setRequired(False)
        mbo.setFieldFlag('IMPACT',mbo.READONLY, True)
        mbo.setValueNull('IMPACT', mbo.NOACCESSCHECK)
