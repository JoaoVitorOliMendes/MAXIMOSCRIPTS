select * from synonymdomain
where domainid = 'LOCASSETSTATUS'
    and
    (
        (
            :user not in 
            (
                select userid from groupuser where UPPER(groupname) like 'SNZ%MNT' and userid not in 
                (
                    select userid from groupuser where UPPER(groupname) not in 
                    ('SNZ_METH_MNT', 'SNZ_TECH_MNT', 'SNZ_ADMIN_MNT','MAXEVERYONE', 'MAXADMIN', 'MAXDEFLTREG')
                )
            )
        )
        or
        (
            (
                :user in
                (
                    select userid from groupuser where UPPER(groupname) like 'SNZ%MNT' and userid not in 
                    (
                        select userid from groupuser where UPPER(groupname) not in 
                        ('SNZ_METH_MNT', 'SNZ_TECH_MNT', 'SNZ_ADMIN_MNT','MAXEVERYONE', 'MAXADMIN', 'MAXDEFLTREG')
                    )
                )
            )
            and orgid = 'GEROWSNZ'
            and siteid = 'SNZ-MNT'
        )
    )

domainid = 'LOCASSETSTATUS' and((:user not in (select userid from groupuser where UPPER(groupname) like 'SNZ%MNT' and userid not in (select userid from groupuser where UPPER(groupname) not in ('MAXEVERYONE', 'MAXADMIN', 'MAXDEFLTREG') AND UPPER(groupname) not like 'SNZ%MNT')))or((:user in(select userid from groupuser where UPPER(groupname) like 'SNZ%MNT' and userid not in (select userid from groupuser where UPPER(groupname) not in ('MAXEVERYONE', 'MAXADMIN', 'MAXDEFLTREG') AND UPPER(groupname) not like 'SNZ%MNT')))and orgid = 'GEROWSNZ'and siteid = 'SNZ-MNT'))
