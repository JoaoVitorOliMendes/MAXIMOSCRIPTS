--Conditional experession
:&USERNAME& not in (select userid from groupuser where UPPER(groupname) like 'SNZ_TECH%')
