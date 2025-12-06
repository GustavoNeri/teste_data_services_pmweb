/*  6 - Esta query tem o objetivo de analisar o comportamento de compra
    por faixa etária dos clientes.
*/

with idade_clientes as (
    select 
        c.id as id_cliente,
        c.nome,
        c.uf,
        c.cidade,
        cast(
            (julianday('now') - julianday(
                case 
                    when c.data_nascimento like '__/__/____' 
                    then substr(c.data_nascimento, 7, 4) || '-' || 
                         substr(c.data_nascimento, 4, 2) || '-' || 
                         substr(c.data_nascimento, 1, 2)
                    else c.data_nascimento
                end
            )) / 365.25 as integer
        ) as idade,
        p.valor_total,
        p.quantidade,
        p.data_pedido
    from clientes c
    join pedidos p on c.id = p.id_cliente
    where c.data_nascimento is not null 
        and c.data_nascimento != ''
        and p.status_pagamento = 'CONFIRMADO'
),
faixa_etaria as (
    select 
        *,
        case 
            when idade between 18 and 25 then '18-25 (Jovens)'
            when idade between 26 and 35 then '26-35 (Adultos jovens)'
            when idade between 36 and 45 then '36-45 (Adultos)'
            when idade between 46 and 55 then '46-55 (<eia idade)'
            when idade between 56 and 65 then '56-65 (Pré-aposentadoria)'
            when idade > 65 then '66+ (Aposentados)'
            else 'Menor de 18'
        end as faixa_etaria
    from idade_clientes
    where idade >= 18
)
select 
    faixa_etaria,
    count(distinct id_cliente) as total_clientes,
    count(*) as total_pedidos,
    sum(quantidade) as total_itens_vendidos,
    sum(valor_total) as valor_total_vendas,
    avg(valor_total) as ticket_medio,
    avg(quantidade) as media_itens_por_pedido,
    round((sum(valor_total) * 100.0 / (select sum(valor_total) from faixa_etaria)), 2) as percentual_valor,
    round((count(*) * 100.0 / (select count(*) from faixa_etaria)), 2) as percentual_pedidos
from faixa_etaria
group by faixa_etaria
order by 
    case faixa_etaria
        when '18-25 (Jovens)' then 1
        when '26-35 (Adultos jovens)' then 2
        when '36-45 (Adultos)' then 3
        when '46-55 (Meia idade)' then 4
        when '56-65 (Pré-aposentadoria)' then 5
        when '66+ (Aposentados)' then 6
        else 7
    end;