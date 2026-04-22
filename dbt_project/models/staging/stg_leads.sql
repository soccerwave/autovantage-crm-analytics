select
    lead_id,
    created_date_key,
    dealer_id,
    contact_id,
    lead_source,
    lead_status,
    vehicle_interest as vehicle_id,
    assigned_to_rep,
    first_response_hours,
    is_converted,
    converted_date_key,
    opportunity_id,
    lost_reason,
    age_at_close_days,
    region
from raw_fact_leads