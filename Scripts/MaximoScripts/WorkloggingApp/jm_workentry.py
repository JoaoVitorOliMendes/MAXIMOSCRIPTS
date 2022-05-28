# ------------------------------------------------------
# MaximoCon, 2022-05-23 15:02:47-0300
# Objetivo: Script to manipulate JM_WORKENTRY in JM_WORKLOGGING app
# Autor: João Vitor de Oliveira Mendes
# ------------------------------------------------------


if launchPoint == 'INIT' and onadd:
    service.error('aaaaa','canAddOrDelete')
    mbo.setValue('JM_WORKNUMBER',mbo.getOwner().getString('JM_WORKNUMBER'), mbo.NOACCESSCHECK)

