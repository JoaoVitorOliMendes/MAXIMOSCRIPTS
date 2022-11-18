srStatusSet = mbo.getMboSet("$TKSTATUS$","TKSTATUS"," ticketid = :ticketid ")
srStatusSet.setOrderBy("changedate desc")
srStatusSet.reset()
