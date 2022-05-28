# ------------------------------------------------------
# MaximoCon, Março de 2022
# Objetivo: Script para checar se o tipo de conhecimento = "ATIVO"
# Autor: João Vitor de Oliveira Mendes
# ------------------------------------------------------

evalresult=False

# JM_ASSETNUM_HID
# Define se o campo JM_TYPE será exibido ou não na tela conforme o Escopo do registro.
if launchPoint == 'JM_ASSETNUM_HID':
    if mbo.getString('JM_TYPE') == 'ATIVO':
        evalresult = True
