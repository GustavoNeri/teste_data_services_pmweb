/* 2 - Esta query tem o objetivo de mostrar o ticket médio do cliente por ano e mẽs.
*/

select
    id_cliente,
    strftime('%Y', data_pedido) as ano,
    strftime('%m', data_pedido) as mes,
    AVG(valor_total)            as ticket_medio,
    COUNT(*)                    as total_compras
from pedidos
group by id_cliente, ano, mes
order by ano, mes, id_cliente ;
