select * from synonymdomain
where domainid = 'WOSTATUS'
    and orgid = 'GEROWSNZ'
    and
    (
        (
            :user not in 
            (
                select userid from groupuser where UPPER(groupname) like 'SNZ_TECH%' and userid not in 
                (
                    select userid from groupuser where UPPER(groupname) not in 
                    ('SNZ_TECH_MNT', 'SNZ_TECH_FM', 'MAXEVERYONE', 'MAXADMIN', 'MAXDEFLTREG')
                )
            )
        )
        or
        (
            (
                :user in
                (
                    select userid from groupuser where UPPER(groupname) like 'SNZ_TECH%' and userid not in
                    (
                        select userid from groupuser where UPPER(groupname) not in
                        ('SNZ_TECH_MNT', 'SNZ_TECH_FM', 'MAXEVERYONE', 'MAXADMIN', 'MAXDEFLTREG')
                    )
                )
            )
            and value not in ('WORKCOMP', 'QUOCAN', 'QUOMAKE', 'QUOPEN', 'QUOSENT', 'QUOVALID')
        )
    )
