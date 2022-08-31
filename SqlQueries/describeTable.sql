select 
  tabname,
  colname,
  typename,
  length,
  scale,
  default,
  nulls,
  identity,
  generated,
  remarks,
  keyseq 
from 
  syscat.columns
where TABNAME = 'LABTRANS'
