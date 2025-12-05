/*  3 - Esta query tem o objetivo de mostrar o intervalo 
    médio entre as compras por cliente.
*/

with compra_ordenada as (
    select 
        cod_cliente,
        nome,
        dt_pedido,
        LAG(dt_pedido) over (partition by cod_cliente order by dt_pedido) as data_anterior
    from pedidos pd
    join clientes cl
        on cl.id = pd.cod_cliente
)
select
    cod_cliente,
    nome,
    AVG(JULIANDAY(dt_pedido) - JULIANDAY(data_anterior)) as intervalo_medio_dias,
    COUNT(*) as total_compras_analisadas
from compra_ordenada
where data_anterior is not null
group by cod_cliente
order by intervalo_medio_dias;