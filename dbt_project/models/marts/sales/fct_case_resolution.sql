with cases as (

    select * from {{ ref('stg_service_cases') }}

)

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
    status,
    case
        when is_sla_breached = false then 1
        else 0
    end as is_sla_compliant,
    case
        when is_reopened = true then 1
        else 0
    end as reopen_flag
from cases