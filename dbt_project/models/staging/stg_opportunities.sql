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
    probability_pct
from raw_fact_opportunities