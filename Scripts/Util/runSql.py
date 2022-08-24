conKey = ""
con = ""
s = ""

try:
    conKey = mbo.getThisMboSet().getUserInfo().getConnectionKey();
    con = mbo.getThisMboSet().getMboServer().getDBConnection(conKey)
    s = con.createStatement()
    val = "update asset set description = 'Update Parent Description' where assetnum = '" + mbo.getString("parent") + "' and siteid = '" + mbo.getString("siteid") + "'"
    rs = s.execute(val)
    # If executing a select
    #val = 'select xxxx from workorder'
    #rs = s.executeQuery(val)
    #while rs.next():
    #   service.error('',str(rs.getString('WONUM')))
    con.commit()
finally:
    if s != "":
        s.close()
    if conKey != "" and con != "":
        mbo.getThisMboSet().getMboServer().freeDBConnection(conKey)
