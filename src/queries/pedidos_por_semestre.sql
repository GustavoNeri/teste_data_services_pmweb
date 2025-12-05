/*  1 - Esta query tem o objetivo de mostrar a quantidade de pedidos parcelados por cliente por semestre.
*/

select
    id_cliente,
    strftime('%Y', data_pedido) as ano,
    case 
        when cast(strftime('%m', data_pedido) as integer) <= 6 then 1
        else 2
    end         as semestre,
    COUNT(*)    as qtd_pedidos
from pedidos
where parcelas > 1
group by id_cliente, ano, semestre
order by ano, semestre, id_cliente;
