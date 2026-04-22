select
    case_id,
    contact_id,
    account_id,
    vehicle_id,
    dealer_id,
    open_date_key,
    close_date_key,
    case_type,
    priority,
    sla_target_hours,
    resolution_hours,
    is_sla_breached,
    is_reopened,
    reopen_count,
    related_case_id,
    status
from raw_fact_service_cases