/* 2 - Esta query tem o objetivo de mostrar o ticket médio do cliente por ano e mẽs.
*/

select
    cod_cliente,
    nome,
    strftime('%Y', dt_pedido) as ano,
    strftime('%m', dt_pedido) as mes,
    AVG(valor_total)            as ticket_medio,
    COUNT(*)                    as total_compras
from pedidos pd
join clientes cl
    on cl.id = pd.cod_cliente
group by cod_cliente, ano, mes
order by ano, mes, nome, cod_cliente ;
