/*  5- Esta query tem o objetivo de comparar o percentual 
    entre 2019 e 2020 para os segmentos som e papelaria.
*/

with vendas_segmento as (
    select
        departamento,
        strftime('%Y', data_pedido) as ano,
        SUM(valor_total)            as total_vendas,
        COUNT(*)                    as qtd_pedidos
    from pedidos
    where departamento in ('Som', 'Papelaria')
        and strftime('%Y', data_pedido) in ('2019', '2020')
    group by departamento, ano
),
comparativo as (
    select 
        departamento,
        ano,
        total_vendas,
        LAG(total_vendas) over (partition by departamento order by ano) as total_anterior
    from vendas_segmento
)
select 
    departamento,
    ano,
    total_vendas,
    total_anterior,
    case
        when total_anterior is null then null
        else ROUND(((total_vendas - total_anterior) * 100 / total_anterior), 2)
    end as variacao_percentual
from comparativo
order by departamento, ano;