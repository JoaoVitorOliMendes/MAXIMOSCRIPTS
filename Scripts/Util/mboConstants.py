from psdi.mbo import MboConstants
mbo.setValue("DESCRIPTION","My description",MboConstants.NOACCESSCHECK)

mbo.setValue("DESCRIPTION","My description",mbo.NOACCESSCHECK)

mbo.setValue("DESCRIPTION","My description",mbo.NOACCESSCHECK|mbo.NOVALIDATION)

###   NOACCESSCHECK - Suppress access control checks (Lookups/Domain restrictions)
###  	NOVALIDATION - Used to suppress validation of a field
###   NOACTION - Used to suppress action of a field
### 	NOVALIDATION_AND_NOACTION - Used to suppress validation and action
