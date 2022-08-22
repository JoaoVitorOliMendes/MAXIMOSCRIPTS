select userid, GROUPNAME from groupuser
where
    (
        UPPER(groupname) in ('SNZ_METH_MNT', 'SNZ_METH_FM','SNZ_TECH_FM','SNZ_TECH_MNT', 'NTS_ADMIN_MNT')
    )
    and UPPER(userid) not in
    (
        select UPPER(userid) from groupuser
        where UPPER(groupname) not in ('SNZ_METH_MNT', 'SNZ_METH_FM','SNZ_TECH_FM','SNZ_TECH_MNT', 'NTS_ADMIN_MNT', 'MAXEVERYONE', 'MAXDEFLTREG')
    )
