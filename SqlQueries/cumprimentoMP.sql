select Months.month, COALESCE(wapprCount.Nume_os, 0) as wapprCount, COALESCE(apprCount.Nume_os, 0)
as apprCount, COALESCE(ROUND((100/CAST((wapprCount.Nume_os + apprCount.Nume_os) as Float) * apprCount.Nume_os), 2), 0) as percentage
from (  
        select 1 as MONTH union 
        select 2 as MONTH union 
        select 3 as MONTH union 
        select 4 as MONTH union 
        select 5 as MONTH union 
        select 6 as MONTH union 
        select 7 as MONTH union 
        select 8 as MONTH union 
        select 9 as MONTH union 
        select 10 as MONTH union 
        select 11 as MONTH union 
        select 12 as MONTH 
    ) Months 
left outer join  
    ( 
        select COALESCE(COUNT(wonum),0) AS Nume_os, month(reportdate) as month 
        from workorder 
        where pmnum is not null 
            and status in ( 
                    select value 
                    from synonymdomain 
                    where domainid = 'WOSTATUS' 
                        and lower(maxvalue) like 'w%'
                        and year(reportdate) = '2021'
                ) 
        group by month(reportdate) 
    ) wapprCount 
on Months.month = wapprCount.month 
left outer join  
    ( 
        select COALESCE(COUNT(wonum),0) AS Nume_os, month(reportdate) as month 
        from workorder 
        where pmnum is not null 
            and status in ( 
                    select value 
                    from synonymdomain 
                    where domainid = 'WOSTATUS' 
                        and lower(maxvalue) in ('appr' , 'inprg', 'comp', 'close')
                        and year(reportdate) = '2021'
                ) 
        group by month(reportdate) 
    ) apprCount 
on Months.month = apprCount.month;
