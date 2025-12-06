/*  8 - Esta query tem o objetivo de identificar a sazonalidade de vendas por dia da semana
*/

select 
    case cast(strftime('%w', data_pedido) as integer)
        when 0 then 'Domingo'
        when 1 then 'Segunda-feira'
        when 2 then 'Terça-feira'
        when 3 then 'Quarta-feira'
        when 4 then 'Quinta-feira'
        when 5 then 'Sexta-feira'
        when 6 then 'Sábado'
    end as dia_semana,
    count(*) as total_pedidos,
    sum(valor_total) as valor_total_vendas,
    avg(valor_total) as ticket_medio,
    sum(quantidade) as total_itens_vendidos,
    round((count(*) * 100.0 / (select count(*) from pedidos where status_pagamento = 'CONFIRMADO')), 2) as percentual_pedidos,
    round((sum(valor_total) * 100.0 / (select sum(valor_total) from pedidos where status_pagamento = 'CONFIRMADO')), 2) as percentual_valor
from pedidos
where status_pagamento = 'CONFIRMADO'
    and data_pedido is not null
group by dia_semana
order by 
    case dia_semana
        when 'Domingo' then 0
        when 'Segunda-feira' then 1
        when 'Terça-feira' then 2
        when 'Quarta-feira' then 3
        when 'Quinta-feira' then 4
        when 'Sexta-feira' then 5
        when 'Sábado' then 6
    end;