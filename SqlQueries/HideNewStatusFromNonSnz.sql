select * from synonymdomain    
where domainid='LOCASSETSTATUS'
    and orgid='GEROWSNZ'
    and (
            (
                :user not in 
                (
                    select distinct userid from groupuser where UPPER(groupname) in 
                    (
                        select GROUPNAME from SITEAUTH where SITEID='SNZ-MNT'
                    )
                    and UPPER(groupname) not in 
                    (
                        select GROUPNAME from SITEAUTH where SITEID not in ('SNZ-MNT')
                    )
                )
            )
            or
            (
                (
                    :user in 
                    (
                        select distinct userid from groupuser where UPPER(groupname) in 
                        (
                            select GROUPNAME from SITEAUTH where SITEID='SNZ-MNT'
                        )
                        and UPPER(groupname) not in 
                        (
                            select GROUPNAME from SITEAUTH where SITEID not in ('SNZ-MNT')
                        )
                    )
                )
                and siteid='SNZ-MNT'
            )
        )
