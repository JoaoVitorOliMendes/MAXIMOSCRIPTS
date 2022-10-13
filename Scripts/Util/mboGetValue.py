wonum = mbo.getMboValue("WONUM").getCurrentValue().asString()

wonum = mbo.getMboValue("WONUM").getPreviousValue().asString()

wonum = mbo.getDatabaseValue("WONUM")
wonum = mbo.getMboValue("WONUM").getInitialValue().asString()

mbo.isModified("WONUM")
