conKey = ""
con = ""
s = ""

try:
    conKey = mbo.getThisMboSet().getUserInfo().getConnectionKey();
    con = mbo.getThisMboSet().getMboServer().getDBConnection(conKey)
    s = con.createStatement()
    val = "update asset set description = 'Update Parent Description' where assetnum = '" + mbo.getString("parent") + "' and siteid = '" + mbo.getString("siteid") + "'"
    rs = s.execute(val)
    con.commit()
finally:
    if s != "":
        s.close()
    if conKey != "" and con != "":
        mbo.getThisMboSet().getMboServer().freeDBConnection(conKey)
