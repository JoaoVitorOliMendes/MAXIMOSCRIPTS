select maxuser.userid, maxuser.personid, maxuser.status, maxuser.type from maxuser
join groupuser on groupuser.userid=maxuser.userid
where groupuser.groupname in ('MAXADMIN')
	and maxuser.sysuser=0
	and maxuser.type <> 'TYPE 10'

select distinct maxuser.userid, maxuser.personid, maxuser.status, maxuser.type from maxuser
join groupuser on groupuser.userid=maxuser.userid
where groupuser.userid not in (select gu.userid from groupuser gu where groupname in ('MAXADMIN'))
	and maxuser.sysuser=0
	and maxuser.type='TYPE 10'

select maxuser.userid, maxuser.personid, maxuser.status, maxuser.type from maxuser
where maxuser.status='ACTIVE'
	and maxuser.type <> 'TYPE 10'
	and maxuser.sysuser=0

update maxuser set type='TYPE 1'
where userid not in (select gu.userid from groupuser gu where groupname in ('MAXADMIN'))
	and maxuser.sysuser=0
	and maxuser.type='TYPE 10'

update maxuser set maxuser.type='TYPE 10'
from maxuser join groupuser on groupuser.userid=maxuser.userid
where groupuser.groupname in ('MAXADMIN')
	and maxuser.sysuser=0
	and maxuser.type <> 'TYPE 10'

update maxuser set maxuser.status='INACTIVE' where maxuser.type <> 'TYPE 10' and maxuser.sysuser=0
