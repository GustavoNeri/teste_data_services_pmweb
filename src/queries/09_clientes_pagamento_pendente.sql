/*  9 - Esta query tem o objetivo de identificar clientes com pagamentos 
    não confirmados e verificar se podem receber emails para campanhas 
    de recuperação de vendas.
*/

with clientes_pagamentos_status as (
    select 
        c.id as id_cliente,
        c.nome,
        c.email,
        c.uf,
        c.cidade,
        c.permissao_recebe_email,
        p.id_pedido,
        p.data_pedido,
        p.valor_total,
        p.status_pagamento,
        p.meio_pagamento,
        p.parcelas,
        p.departamento,
        case 
            when upper(p.status_pagamento) in ('CONFIRMADO') then 'confirmado'
            when upper(p.status_pagamento) in ('PENDENTE') then 'pendente'
            when upper(p.status_pagamento) in ('CANCELADO') then 'cancelado'
            else 'outros'
        end as status_categorizado
    from clientes c
    join pedidos p on c.id = p.id_cliente
    where c.email is not null 
        and c.email != ''
),
resumo_por_cliente as (
    select 
        id_cliente,
        nome,
        email,
        uf,
        cidade,
        permissao_recebe_email,
        count(case when status_categorizado = 'confirmado' then 1 end) as pedidos_confirmados,
        count(case when status_categorizado = 'pendente' then 1 end) as pedidos_pendentes,
        count(case when status_categorizado = 'cancelado' then 1 end) as pedidos_cancelados,
        count(case when status_categorizado = 'outros' then 1 end) as pedidos_outros,
        count(*) as total_pedidos,
        sum(case when status_categorizado = 'pendente' then valor_total else 0 end) as valor_pendente,
        sum(case when status_categorizado = 'cancelado' then valor_total else 0 end) as valor_cancelado,
        sum(valor_total) as valor_total_historico,
        min(data_pedido) as primeira_compra,
        max(data_pedido) as ultima_compra,
        group_concat(distinct meio_pagamento) as meios_pagamento_usados,
        group_concat(distinct departamento) as departamentos_comprados
    from clientes_pagamentos_status
    group by id_cliente, nome, email, uf, cidade, permissao_recebe_email
),
clientes_com_problemas as (
    select 
        *,
        case 
            when pedidos_pendentes > 0 then 'tem_pendencias'
            when pedidos_cancelados > 0 then 'tem_cancelamentos'
            else 'sem_problemas'
        end as tipo_problema,
        case 
            when valor_pendente >= 1000 or valor_cancelado >= 2000 then 'alta_prioridade'
            when valor_pendente >= 500 or valor_cancelado >= 1000 then 'media_prioridade'
            else 'baixa_prioridade'
        end as nivel_prioridade,
        case 
            when permissao_recebe_email = 1 then 'pode_receber_emails'
            else 'nao_pode_receber_emails'
        end as status_email
    from resumo_por_cliente
    where pedidos_pendentes > 0 
        or pedidos_cancelados > 0 
)
select 
    id_cliente,
    nome,
    email,
    uf,
    cidade,
    status_email,
    permissao_recebe_email as flag_recebe_email,
    tipo_problema,
    nivel_prioridade,
    pedidos_confirmados,
    pedidos_pendentes,
    pedidos_cancelados,
    pedidos_outros,
    total_pedidos,
    round(valor_pendente, 2) as valor_pendente,
    round(valor_cancelado, 2) as valor_cancelado,
    round(valor_total_historico, 2) as valor_total_historico,
    round((pedidos_pendentes * 100.0 / nullif(total_pedidos, 0)), 2) as percentual_pendentes,
    round((pedidos_cancelados * 100.0 / nullif(total_pedidos, 0)), 2) as percentual_cancelados,
    primeira_compra,
    ultima_compra,
    meios_pagamento_usados,
    departamentos_comprados,
    case 
        when status_email = 'pode_receber_emails' and pedidos_pendentes > 0 then 
            'enviar email de lembrete de pagamento'
        when status_email = 'pode_receber_emails' and pedidos_cancelados > 0 then 
            'enviar email de recuperação com oferta especial'
        when status_email = 'nao_pode_receber_emails' and pedidos_pendentes > 0 then 
            'tentar contato telefônico ou sms'
        when status_email = 'nao_pode_receber_emails' and pedidos_cancelados > 0 then 
            'oferecer cupom de desconto via sms/app'
        else 'avaliar contato direto'
    end as acao_recomendada,
    case 
        when nivel_prioridade = 'alta_prioridade' and status_email = 'pode_receber_emails' then 'campanha_urgente_email'
        when nivel_prioridade = 'alta_prioridade' and status_email = 'nao_pode_receber_emails' then 'campanha_urgente_outros'
        when nivel_prioridade = 'media_prioridade' and status_email = 'pode_receber_emails' then 'campanha_regular_email'
        when nivel_prioridade = 'media_prioridade' and status_email = 'nao_pode_receber_emails' then 'campanha_regular_outros'
        else 'campanha_baixa_prioridade'
    end as segmento_campanha
from clientes_com_problemas
order by 
    case nivel_prioridade
        when 'alta_prioridade' then 1
        when 'media_prioridade' then 2
        when 'baixa_prioridade' then 3
    end,
    valor_pendente desc,
    valor_cancelado desc;