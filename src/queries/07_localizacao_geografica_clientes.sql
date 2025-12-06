/*  7 - Esta query tem o objetivo de analisar as vendas
    por localização geográfica dos clientes.
*/

with vendas_por_localizacao as (
    select 
        c.uf,
        c.cidade,
        c.id as id_cliente,
        c.nome,
        p.valor_total,
        p.quantidade,
        p.data_pedido,
        p.departamento,
        p.id_pedido
    from clientes c
    join pedidos p on c.id = p.id_cliente
    where c.uf is not null 
        and c.uf != ''
        and p.status_pagamento = 'CONFIRMADO'
),
analise_uf as (
    select 
        uf,
        count(distinct id_cliente) as total_clientes,
        count(*) as total_pedidos,
        sum(quantidade) as total_itens_vendidos,
        sum(valor_total) as valor_total_vendas,
        avg(valor_total) as ticket_medio_uf,
        count(distinct departamento) as departamentos_ativos
    from vendas_por_localizacao
    group by uf
),
analise_cidade as (
    select 
        uf,
        cidade,
        count(distinct id_cliente) as total_clientes_cidade,
        count(*) as total_pedidos_cidade,
        sum(valor_total) as valor_total_cidade,
        avg(valor_total) as ticket_medio_cidade
    from vendas_por_localizacao
    where cidade is not null and cidade != ''
    group by uf, cidade
),
top_cidades_por_uf as (
    select 
        uf,
        cidade,
        valor_total_cidade,
        row_number() over (partition by uf order by valor_total_cidade desc) as ranking_cidade
    from analise_cidade
)
select 
    a.uf,
    a.total_clientes,
    a.total_pedidos,
    a.total_itens_vendidos,
    a.valor_total_vendas,
    a.ticket_medio_uf,
    a.departamentos_ativos,
    t.cidade as cidade_maior_venda,
    t.valor_total_cidade as valor_top_cidade,
    round((a.valor_total_vendas * 100.0 / (select sum(valor_total_vendas) from analise_uf)), 2) as percentual_vendas_uf,
    round((a.total_pedidos * 100.0 / (select sum(total_pedidos) from analise_uf)), 2) as percentual_pedidos_uf,
    round((cast(a.total_clientes as float) / a.total_pedidos), 2) as clientes_por_pedido,
    rank() over (order by a.valor_total_vendas desc) as ranking_geral_vendas,
    rank() over (order by a.total_pedidos desc) as ranking_geral_pedidos
from analise_uf a
left join top_cidades_por_uf t on a.uf = t.uf and t.ranking_cidade = 1
order by a.valor_total_vendas desc, a.total_pedidos desc;