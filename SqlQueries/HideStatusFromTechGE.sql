--Conditional experession
:&USERNAME& not in (select userid from groupuser where UPPER(groupname) like 'SNZ_TECH%')
--Lookup where clause
:USER not in (select userid from groupuser where UPPER(groupname) like 'SNZ_TECH%')
