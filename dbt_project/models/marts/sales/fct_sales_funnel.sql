with leads as (

    select * from {{ ref('stg_leads') }}

),

aggregated as (

    select
        lead_source,
        region,
        count(*) as total_leads,
        sum(case when lead_status in ('Qualified', 'Converted') then 1 else 0 end) as qualified_leads,
        sum(case when lead_status = 'Converted' then 1 else 0 end) as converted_leads,
        sum(case when lead_status = 'Lost' then 1 else 0 end) as lost_leads,
        avg(first_response_hours) as avg_first_response_hours,
        avg(age_at_close_days) as avg_age_at_close_days
    from leads
    group by 1, 2

)

select
    lead_source,
    region,
    total_leads,
    qualified_leads,
    converted_leads,
    lost_leads,
    round(avg_first_response_hours, 2) as avg_first_response_hours,
    round(avg_age_at_close_days, 2) as avg_age_at_close_days,
    round(converted_leads * 1.0 / nullif(total_leads, 0), 4) as lead_to_conversion_rate,
    round(lost_leads * 1.0 / nullif(total_leads, 0), 4) as lost_rate
from aggregated