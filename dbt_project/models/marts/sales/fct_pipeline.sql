with opps as (

    select * from {{ ref('stg_opportunities') }}

)

select
    opportunity_id,
    lead_id,
    account_id,
    contact_id,
    vehicle_id,
    dealer_id,
    stage,
    deal_value_eur,
    discount_pct,
    net_revenue_eur,
    close_date_key,
    sales_cycle_days,
    lost_reason,
    probability_pct,
    round(deal_value_eur * probability_pct / 100.0, 2) as weighted_pipeline_value,
    case
        when stage in ('Closed Won', 'Closed Lost') then 1
        else 0
    end as is_closed,
    case
        when stage = 'Closed Won' then 1
        else 0
    end as is_won,
    case
        when stage = 'Closed Lost' then 1
        else 0
    end as is_lost
from opps