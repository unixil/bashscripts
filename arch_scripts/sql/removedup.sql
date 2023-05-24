 create or replace  function remove_dup() returns integer as $$

declare
    stockdate record;
begin
    for stockdate in select tradenumber from basic.companies loop
--    	execute 'select t.date from basic.stockdaily t where t.tradenumber like ' || quote_literal(stockdate.tradenumber) ;
--	execute 'delete from basic.stockdaily where id_stockdaily in (select id_stockdaily from (select t.id_stockdaily,t.date, t.open,row_number() over (partition by date order by id_stockdaily) from basic.stockdaily t where t.tradenumber  like' || quote_literal(stockdate.tradenumber)||' order by t.date desc)s where row_number >=2)';
	execute 'delete from basic.stock5min where id_stock5min in (select id_stock5min from (select t.tradenumber,t.id_stock5min,t.date,t.time, t.open,row_number() over (partition by date, time order by id_stock5min) from basic.stock5min t where t.tradenumber  like ' || quote_literal(stockdate.tradenumber)|| ' order by t.date desc)s where row_number >=2)';

	raise notice 'hi %s',quote_ident(stockdate.tradenumber);
    end loop;
    return 1;
end;
$$ language plpgsql;
