/*  4- Esta query tem o objetivo de classificar os clientes de 
    acordo com o valor de compras mensal (tiers).
*/

with valor_mensal as (
    select
        id_cliente,
        nome,
        strftime('%Y', data_pedido) as ano,
        strftime('%m', data_pedido) as mes,
        SUM(valor_total)          as valor_total
    from pedidos pd
    join clientes cl
        on cl.id = pd.id_cliente
    group by id_cliente, ano, mes
)
select 
    id_cliente,
    nome,
    ano,
    mes,
    valor_total,
    case
        when valor_total <= 1000 then 'Básico'
        when valor_total <= 2000 then 'Prata'
        when valor_total <= 5000 then 'Ouro'
        else 'Super'
    end as tier
from valor_mensal
order by ano, mes, nome, id_cliente ;