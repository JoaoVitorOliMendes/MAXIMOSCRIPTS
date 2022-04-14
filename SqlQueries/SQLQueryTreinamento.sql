-- 1.
-- Selecionar todos os ativos cujos os status estejam em ATIVO  ou Não Pronto  ou Operação e que não possuam prioridade menor que 2
	select assetnum, priority, status from asset where status in ('ACTIVE', 'NOT READY', 'OPERATING') and priority >= 2

-- 2.
-- Selecionar os seguintes campos na tabela de ordem de serviço:
--  a) Ordem de serviço pai , tipo de serviço, posição operacional de todos os sites sem que ocorra repetição do registro.
		select distinct parent, worktype, LOCATION from workorder where parent is not null and worktype is not null and location is not null
--  b) Ordem de serviço, ordem de serviço pai , tipo de serviço, posição operacional de todos os sites que possua tipo de
--serviço CM ou PM e posição operacional SHIPPING e o tipo de serviço não seja nulo.
	select WONUM, parent, worktype, location from workorder where worktype in ('CM', 'PM') and lower(location) = 'shipping' and parent is not null

-- 4.
-- Selecionar as descrições de ativos que contenham a palavra “bomba”  e iniciem com a letra “d”
	select description from asset where description like 'd%bomb%'

-- 5.
-- Selecionar todas as ordens de serviços cujos os status não sejam sinônimo de fechadas e canceladas.
--Observação: utilizar o operador “IN” como sub-consulta.
	select wonum, status from workorder where status not in ('CLOSE', 'CAN', 'APPR', 'COMP')

-- 6.
-- Listar distintamente todos dos itens que pertençam aos ativos.
	select distinct * from asset

-- 7.
-- Quantas OS estão com status sinônimos de cancelado? 
	select count(wonum) from workorder where status in ('CAN', 'APPR', 'CLOSE', 'COMP')

-- 8.
-- Construir  12 consultas para visualizar a quantidade de  ordens de serviço agrupada nos meses do ano atual “2022” agrupadas por status.
--Dica : Campo de data . Statusdate. 
	select count(wonum), status from workorder where year(statusdate) = '2022' and month(statusdate) = '01' group by status
	select count(wonum), status from workorder where year(statusdate) = '2022' and month(statusdate) = '02' group by status
	select count(wonum), status from workorder where year(statusdate) = '2022' and month(statusdate) = '03' group by status
	select count(wonum), status from workorder where year(statusdate) = '2022' and month(statusdate) = '04' group by status
	select count(wonum), status from workorder where year(statusdate) = '2022' and month(statusdate) = '05' group by status
	select count(wonum), status from workorder where year(statusdate) = '2022' and month(statusdate) = '06' group by status
	select count(wonum), status from workorder where year(statusdate) = '2022' and month(statusdate) = '07' group by status
	select count(wonum), status from workorder where year(statusdate) = '2022' and month(statusdate) = '08' group by status
	select count(wonum), status from workorder where year(statusdate) = '2022' and month(statusdate) = '09' group by status
	select count(wonum), status from workorder where year(statusdate) = '2022' and month(statusdate) = '10' group by status
	select count(wonum), status from workorder where year(statusdate) = '2022' and month(statusdate) = '11' group by status
	select count(wonum), status from workorder where year(statusdate) = '2022' and month(statusdate) = '12' group by status

-- 9.
-- Trazer dados de recebimento de materiais , consumo e transações de inventário  “Verificar na aplicação de inventário qual a tabela
--de transações” exibindo os seguintes campos :  item, descrição do item , quantidade , saldo , custo unitário , tipo de transação.
	select 'RECEBIMENTO' AS itemnum,description,quantity,curbal,unitcost, issuetype from matrectrans 
		union 
	select'CONSUMO' AS itemnum,description, quantity,curbal,unitcost, issuetype from matusetrans
		union 
	select 'TRANSACOES' as itemnum, null, quantity, curbal, null, transtype from invtrans

-- 10.
-- A partir da sub-consultaacima para cada linha da ordem de serviço trazer um coluna com contagem de materiais e outra com mão de obra planejada
	select workorder.wonum, workorder.description, workorder.assetnum,
	(select description from asset where asset.assetnum = workorder.assetnum and asset.siteid = workorder.siteid),location,
	(select description from locations where locations.location = workorder.location and locations.siteid = workorder.siteid),
	(select count(wonum) from wpmaterial where workorder.wonum = wpmaterial.wonum and workorder.siteid = wpmaterial.siteid) ,
	(select count(wonum) from wplabor where workorder.wonum = wplabor.wonum and workorder.siteid = wplabor.siteid) 
	from workorder

-- 11.
-- Construirduas sub-consultas:
--  a) Custo planejado de mão de obras e ja maior que 100.
--	b) Custo planejado de ferramentas seja menor que 200.
--	c) Construir uma consulta com union das três querys anteriores.
	select * from workorder where
	(select sum(linecost) from wpmaterial where wpmaterial.wonum = workorder.wonum and wpmaterial.siteid = workorder.siteid ) > 500 
		union
	select * from workorder where
	(select sum(rate * laborhrs) from wplabor where wplabor.wonum = workorder.wonum and wplabor.siteid = workorder.siteid ) > 100 
		union
	select * from workorder where
	(select sum(rate * hours * itemqty) from wptool where wptool.wonum = workorder.wonum and wptool.siteid = workorder.siteid) < 200

-- 12.
-- Elaborar uma sub-consulta no FROM usandoo union  do desafio 3 da parte de  Sub-consultas condicionada a instrução WHERE
	select tbl1.wonum, tbl1.description, tbl1.status, tbl2.wonum, tbl2.description, tbl2.status, tbl3.wonum, tbl3.description, tbl3.status 
	from
	(select wonum, description,status from workorder where (select sum(linecost) from wpmaterial where wpmaterial.wonum = workorder.wonum and wpmaterial.siteid = workorder.siteid ) > 500 ) tbl1,
	(select wonum, description,status from workorder where (select sum(rate * laborhrs) from wplabor where wplabor.wonum = workorder.wonum and wplabor.siteid = workorder.siteid ) > 100) tbl2,
	(select wonum, description,status from workorder where (select sum(rate * hours * itemqty) from wptool where wptool.wonum = workorder.wonum and wptool.siteid = workorder.siteid) < 200) tbl3