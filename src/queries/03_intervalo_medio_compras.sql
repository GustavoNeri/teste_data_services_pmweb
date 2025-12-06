/*  3 - Esta query tem o objetivo de mostrar o intervalo 
    médio entre as compras por cliente.
*/

with compra_ordenada as (
    select 
        id_cliente,
        nome,
        data_pedido,
        LAG(data_pedido) over (partition by id_cliente order by data_pedido) as data_anterior
    from pedidos pd
    join clientes cl
        on cl.id = pd.id_cliente
)
select
    id_cliente,
    nome,
    AVG(JULIANDAY(data_pedido) - JULIANDAY(data_anterior)) as intervalo_medio_dias,
    COUNT(*) as total_compras_analisadas
from compra_ordenada
where data_anterior is not null
group by id_cliente
order by intervalo_medio_dias;