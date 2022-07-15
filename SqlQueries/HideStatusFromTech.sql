select * from synonymdomain
where domainid = 'WOSTATUS'
    and orgid = 'GEROWSNZ'
    and
        (
            (
                :&USERNAME& not in (select userid from groupuser where UPPER(groupname) like 'SNZ_TECH%')
            )
            or
            (
                (:&USERNAME& in (select userid from groupuser where UPPER(groupname) like 'SNZ_TECH%'))
                and
                value not in ('WORKCOMP', 'QUOCAN', 'QUOMAKE', 'QUOPEN', 'QUOSENT', 'QUOVALID')
            )
        )
