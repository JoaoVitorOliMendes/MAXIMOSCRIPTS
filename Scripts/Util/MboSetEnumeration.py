from psdi.mbo import Mbo
from psdi.mbo import MboSet
 
# Import MboSetEnumeration class
from psdi.mbo import MboSetEnumeration
 
poMbo = mbo
 
# Instantiate a MboSet of POLINE
polineMboSet = poMbo.getMboSet("POLINE")
 
# Validate if the MboSet is not null or empty
if polineMboSet is not None and not polineMboSet.notExist():
    # Instantiate MboSetEnumeration based on the MboSet
    polineMboSetEnum = MboSetEnumeration(polineMboSet)
 
    # Loop through the MboSetEnumeration until it has no more elements
    while polineMboSetEnum.hasMoreElements():
        # Instantiate the next Mbo of the MboSet
        polineMbo = polineMboSetEnum.nextMbo()
        print "Item number: ", polineMbo.getString("ITEMNUM")
