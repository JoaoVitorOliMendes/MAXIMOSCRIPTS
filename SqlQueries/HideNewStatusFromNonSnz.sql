select * from synonymdomain where
domainid = 'LOCASSETSTATUS'
    and
    (
        (
            :user not in
            (
                select userid from groupuser where
                (
                    UPPER(groupname) like 'SNZ%MNT'
                    and userid not in
                    (
                        select userid from groupuser where UPPER(groupname) not in ('MAXEVERYONE', 'MAXADMIN', 'MAXDEFLTREG')
                        and UPPER(groupname) not like 'SNZ%MNT'
                    )
                )
                or
                (
                    UPPER(groupname) like 'SNZ%FM'
                    and userid not in
                    (
                        select userid from groupuser where UPPER(groupname) not in ('MAXEVERYONE', 'MAXADMIN', 'MAXDEFLTREG')
                        and UPPER(groupname) not like 'SNZ%FM'
                    )
                )
            )
        )
        or
        (
            (
                (
                    :user in
                    (
                        select userid from groupuser where UPPER(groupname) like 'SNZ%MNT'
                        and userid not in
                        (
                            select userid from groupuser where UPPER(groupname) not in ('MAXEVERYONE', 'MAXADMIN', 'MAXDEFLTREG')
                            and UPPER(groupname) not like 'SNZ%MNT'
                        )
                    )
                )
                and orgid = 'GEROWSNZ'
                and siteid = 'SNZ-MNT'
            )
            or
            (
                (
                    :user in
                    (
                        select userid from groupuser where UPPER(groupname) like 'SNZ%FM'
                        and userid not in
                        (
                            select userid from groupuser where UPPER(groupname) not in ('MAXEVERYONE', 'MAXADMIN', 'MAXDEFLTREG')
                            and UPPER(groupname) not like 'SNZ%FM'
                        )
                    )
                )
                and orgid = 'GEROWSNZ'
                and siteid = 'SNZ-FM'
            )
        )
    )

domainid = 'LOCASSETSTATUS' and((:user not in(select userid from groupuser where(UPPER(groupname) like 'SNZ%MNT' and userid not in(select userid from groupuser where UPPER(groupname) not in ('MAXEVERYONE', 'MAXADMIN', 'MAXDEFLTREG') and UPPER(groupname) not like 'SNZ%MNT'))or(UPPER(groupname) like 'SNZ%FM' and userid not in(select userid from groupuser where UPPER(groupname) not in ('MAXEVERYONE', 'MAXADMIN', 'MAXDEFLTREG') and UPPER(groupname) not like 'SNZ%FM'))))or(((:user in(select userid from groupuser where UPPER(groupname) like 'SNZ%MNT' and userid not in(select userid from groupuser where UPPER(groupname) not in ('MAXEVERYONE', 'MAXADMIN', 'MAXDEFLTREG') and UPPER(groupname) not like 'SNZ%MNT')))and orgid = 'GEROWSNZ' and siteid = 'SNZ-MNT')or((:user in(select userid from groupuser where UPPER(groupname) like 'SNZ%FM' and userid not in(select userid from groupuser where UPPER(groupname) not in ('MAXEVERYONE', 'MAXADMIN', 'MAXDEFLTREG') and UPPER(groupname) not like 'SNZ%FM')))and orgid = 'GEROWSNZ' and siteid = 'SNZ-FM')))
