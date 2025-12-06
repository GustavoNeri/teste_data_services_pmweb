/* 2 - Esta query tem o objetivo de mostrar o ticket médio do cliente por ano e mẽs.
*/

select
    id_cliente,
    nome,
    strftime('%Y', data_pedido) as ano,
    strftime('%m', data_pedido) as mes,
    AVG(valor_total)            as ticket_medio,
    COUNT(*)                    as total_compras
from pedidos pd
join clientes cl
    on cl.id = pd.id_cliente
group by id_cliente, ano, mes
order by ano, mes, nome, id_cliente ;
