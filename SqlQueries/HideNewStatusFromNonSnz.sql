select * from synonymdomain where
domainid = 'LOCASSETSTATUS'
    and
    (
        (
            'SNZ_TECH_MNT' not in
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
                    'SNZ_TECH_MNT' in
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
                    'SNZ_TECH_MNT' in
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

domainid = 'LOCASSETSTATUS' and(('SNZ_TECH_MNT' not in(select userid from groupuser where(UPPER(groupname) like 'SNZ%MNT' and userid not in(select userid from groupuser where UPPER(groupname) not in ('MAXEVERYONE', 'MAXADMIN', 'MAXDEFLTREG') and UPPER(groupname) not like 'SNZ%MNT'))or(UPPER(groupname) like 'SNZ%FM' and userid not in(select userid from groupuser where UPPER(groupname) not in ('MAXEVERYONE', 'MAXADMIN', 'MAXDEFLTREG') and UPPER(groupname) not like 'SNZ%FM'))))or((('SNZ_TECH_MNT' in(select userid from groupuser where UPPER(groupname) like 'SNZ%MNT' and userid not in(select userid from groupuser where UPPER(groupname) not in ('MAXEVERYONE', 'MAXADMIN', 'MAXDEFLTREG') and UPPER(groupname) not like 'SNZ%MNT')))and orgid = 'GEROWSNZ' and siteid = 'SNZ-MNT')or(('SNZ_TECH_MNT' in(select userid from groupuser where UPPER(groupname) like 'SNZ%FM' and userid not in(select userid from groupuser where UPPER(groupname) not in ('MAXEVERYONE', 'MAXADMIN', 'MAXDEFLTREG') and UPPER(groupname) not like 'SNZ%FM')))and orgid = 'GEROWSNZ' and siteid = 'SNZ-FM')))
