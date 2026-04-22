select
    feedback_id,
    case_id,
    contact_id,
    dealer_id,
    vehicle_id,
    survey_date_key,
    csat_score,
    nps_score,
    comment_text
from raw_fact_customer_feedback