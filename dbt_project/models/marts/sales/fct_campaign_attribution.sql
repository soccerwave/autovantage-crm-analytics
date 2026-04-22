with bridge as (

    select * from raw_bridge_lead_campaign

),

leads as (

    select * from {{ ref('stg_leads') }}

),

opps as (

    select * from {{ ref('stg_opportunities') }}

),

joined as (

    select
        b.campaign_id,
        l.lead_id,
        l.lead_source,
        l.region,
        l.is_converted,
        o.opportunity_id,
        o.stage,
        o.net_revenue_eur
    from bridge b
    left join leads l
        on b.lead_id = l.lead_id
    left join opps o
        on l.opportunity_id = o.opportunity_id

)

select
    campaign_id,
    count(distinct lead_id) as leads_count,
    sum(case when is_converted = true then 1 else 0 end) as converted_leads_count,
    count(distinct case when stage = 'Closed Won' then opportunity_id end) as closed_won_opps_count,
    round(sum(case when stage = 'Closed Won' then net_revenue_eur else 0 end), 2) as closed_won_revenue_eur
from joined
group by 1