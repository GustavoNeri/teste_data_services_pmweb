/*  1 - Esta query tem o objetivo de mostrar a quantidade de pedidos parcelados por cliente por semestre.
*/

select
    cod_cliente,
    nome,
    strftime('%Y', dt_pedido) as ano,
    case 
        when cast(strftime('%m', dt_pedido) as integer) <= 6 then 1
        else 2
    end         as semestre,
    COUNT(*)    as qtd_pedidos
from pedidos pd
join clientes cl
    on cl.id = pd.cod_cliente
where qtd_parcelas > 1
group by cod_cliente, ano, semestre
order by ano, semestre, nome, cod_cliente;
