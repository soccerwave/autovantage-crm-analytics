SEED = 42

START_DATE = "2023-01-01"
END_DATE = "2024-12-31"

ROW_COUNTS = {
    "dim_date": 730,
    "dim_dealer": 12,
    "dim_vehicle": 45,
    "dim_campaign": 30,
    "dim_contact": 5800,
    "dim_account": 3200,
    "fact_leads": 16000,
    "bridge_lead_campaign": 9000,
    "fact_opportunities": 5200,
    "fact_orders": 2800,
    "fact_service_cases": 11000,
    "fact_customer_feedback": 4200,
}

REGIONS = ["North", "South", "East", "West"]

DEALERS = [
    {"dealer_id": "DLR-01", "dealer_name": "North Star Toyota", "region": "North", "brand": "Toyota"},
    {"dealer_id": "DLR-02", "dealer_name": "North Drive Volkswagen", "region": "North", "brand": "Volkswagen"},
    {"dealer_id": "DLR-03", "dealer_name": "North Elite BMW", "region": "North", "brand": "BMW"},
    {"dealer_id": "DLR-04", "dealer_name": "South Coast Toyota", "region": "South", "brand": "Toyota"},
    {"dealer_id": "DLR-05", "dealer_name": "South Motors Volkswagen", "region": "South", "brand": "Volkswagen"},
    {"dealer_id": "DLR-06", "dealer_name": "South Premium BMW", "region": "South", "brand": "BMW"},
    {"dealer_id": "DLR-07", "dealer_name": "East Point Toyota", "region": "East", "brand": "Toyota"},
    {"dealer_id": "DLR-08", "dealer_name": "East Line Volkswagen", "region": "East", "brand": "Volkswagen"},
    {"dealer_id": "DLR-09", "dealer_name": "East Gate Toyota", "region": "East", "brand": "Toyota"},
    {"dealer_id": "DLR-10", "dealer_name": "West Auto Volkswagen", "region": "West", "brand": "Volkswagen"},
    {"dealer_id": "DLR-11", "dealer_name": "West Highway Toyota", "region": "West", "brand": "Toyota"},
    {"dealer_id": "DLR-12", "dealer_name": "West Grand Volkswagen", "region": "West", "brand": "Volkswagen"},
]

TOYOTA_MODELS = [
    "Yaris", "Corolla", "Corolla Hybrid", "Camry", "C-HR",
    "RAV4", "RAV4 Hybrid", "Highlander", "Prius", "Aygo",
    "Hilux", "Land Cruiser", "Yaris Cross", "Corolla Cross", "bZ4X"
]

VOLKSWAGEN_MODELS = [
    "Polo", "Golf", "Golf GTI", "T-Roc", "T-Cross",
    "Tiguan", "Passat", "Arteon", "Taigo", "Touareg",
    "ID.3", "ID.4", "ID.5", "Touran", "Caddy",
    "Amarok", "Multivan", "Jetta", "Sharan", "Up"
]

BMW_MODELS = [
    "1 Series", "2 Series", "3 Series", "4 Series", "5 Series",
    "X1", "X3", "X5", "i4", "iX"
]

CAMPAIGN_TYPES = ["Email", "Social", "Event", "Paid Search"]

LEAD_SOURCES = [
    "Web Form",
    "Walk-in",
    "Referral",
    "Campaign",
    "Social Media",
    "Phone Inbound",
]

LEAD_STATUSES = [
    "New",
    "Working",
    "Qualified",
    "Converted",
    "Lost",
]

OPPORTUNITY_STAGES = [
    "Qualified",
    "Proposal",
    "Negotiation",
    "Closed Won",
    "Closed Lost",
]

CASE_TYPES = [
    "Warranty",
    "Maintenance",
    "Recall",
    "Damage",
    "Complaint",
]

CASE_PRIORITIES = ["Low", "Medium", "High", "Critical"]

CASE_STATUS_VALUES = ["Open", "In Progress", "Resolved", "Closed"]

BRANDS = ["Toyota", "Volkswagen", "BMW"]

CURRENCY = "EUR"

LEAD_SOURCE_CONFIG = {
    "Web Form": {
        "volume_weight": 0.35,
        "conversion_rate": 0.18,
        "response_hours_mean": 8.5,
        "response_hours_std": 4.0,
        "lost_reason_weights": {
            "No Response": 0.35,
            "Price": 0.20,
            "No Budget": 0.20,
            "Bought Elsewhere": 0.20,
            "Other": 0.05,
        },
    },
    "Walk-in": {
        "volume_weight": 0.22,
        "conversion_rate": 0.52,
        "response_hours_mean": 0.5,
        "response_hours_std": 0.3,
        "lost_reason_weights": {
            "Price": 0.30,
            "Bought Elsewhere": 0.35,
            "No Budget": 0.20,
            "No Response": 0.05,
            "Other": 0.10,
        },
    },
    "Referral": {
        "volume_weight": 0.14,
        "conversion_rate": 0.41,
        "response_hours_mean": 3.0,
        "response_hours_std": 1.5,
        "lost_reason_weights": {
            "Price": 0.20,
            "Bought Elsewhere": 0.25,
            "No Budget": 0.20,
            "No Response": 0.20,
            "Other": 0.15,
        },
    },
    "Campaign": {
        "volume_weight": 0.16,
        "conversion_rate": 0.12,
        "response_hours_mean": 24.0,
        "response_hours_std": 10.0,
        "lost_reason_weights": {
            "No Response": 0.40,
            "Price": 0.20,
            "No Budget": 0.15,
            "Bought Elsewhere": 0.15,
            "Other": 0.10,
        },
    },
    "Social Media": {
        "volume_weight": 0.08,
        "conversion_rate": 0.07,
        "response_hours_mean": 36.0,
        "response_hours_std": 12.0,
        "lost_reason_weights": {
            "No Response": 0.45,
            "Price": 0.15,
            "No Budget": 0.15,
            "Bought Elsewhere": 0.15,
            "Other": 0.10,
        },
    },
    "Phone Inbound": {
        "volume_weight": 0.05,
        "conversion_rate": 0.38,
        "response_hours_mean": 0.25,
        "response_hours_std": 0.15,
        "lost_reason_weights": {
            "Price": 0.25,
            "Bought Elsewhere": 0.30,
            "No Budget": 0.20,
            "No Response": 0.10,
            "Other": 0.15,
        },
    },
}

LEAD_LOST_REASONS = ["No Budget", "Bought Elsewhere", "No Response", "Price", "Other"]

MONTH_VOLUME_MULTIPLIERS = {
    1: 1.00,
    2: 0.98,
    3: 1.20,
    4: 1.02,
    5: 1.00,
    6: 0.97,
    7: 1.03,
    8: 0.70,
    9: 1.15,
    10: 1.00,
    11: 0.98,
    12: 0.95,
}

OPPORTUNITY_STAGE_PROBABILITY = {
    "Qualified": 25,
    "Proposal": 50,
    "Negotiation": 75,
    "Closed Won": 100,
    "Closed Lost": 0,
}

OPPORTUNITY_LOST_REASONS = [
    "Competitor",
    "Price",
    "Delay",
    "No Decision",
]

OPPORTUNITY_STAGE_WEIGHTS = {
    "from_converted_leads": {
        "Qualified": 0.10,
        "Proposal": 0.12,
        "Negotiation": 0.10,
        "Closed Won": 0.55,
        "Closed Lost": 0.13,
    },
    "direct_opps": {
        "Qualified": 0.15,
        "Proposal": 0.15,
        "Negotiation": 0.10,
        "Closed Won": 0.45,
        "Closed Lost": 0.15,
    },
}

SERVICE_CASE_TYPE_WEIGHTS = {
    "Warranty": 0.24,
    "Maintenance": 0.38,
    "Recall": 0.10,
    "Damage": 0.16,
    "Complaint": 0.12,
}

SERVICE_PRIORITY_WEIGHTS = {
    "Low": 0.32,
    "Medium": 0.38,
    "High": 0.22,
    "Critical": 0.08,
}

SLA_TARGET_HOURS = {
    "Low": 168,
    "Medium": 72,
    "High": 24,
    "Critical": 4,
}

PRIORITY_COMPLIANCE_BASE = {
    "Low": 0.92,
    "Medium": 0.84,
    "High": 0.75,
    "Critical": 0.62,
}

REGION_COMPLIANCE_ADJUSTMENT = {
    "North": 0.05,
    "East": 0.01,
    "West": -0.01,
    "South": -0.06,
}

SERVICE_MONTH_MULTIPLIERS = {
    1: 1.18,
    2: 1.00,
    3: 0.96,
    4: 0.97,
    5: 1.00,
    6: 1.02,
    7: 1.16,
    8: 0.88,
    9: 0.98,
    10: 1.00,
    11: 0.97,
    12: 0.91,
}

FEEDBACK_RESPONSE_RATE_BY_PRIORITY = {
    "Low": 0.32,
    "Medium": 0.37,
    "High": 0.45,
    "Critical": 0.50,
}

BRAND_CSAT_ADJUSTMENT = {
    "Toyota": 0.00,
    "Volkswagen": -0.05,
    "BMW": 0.10,
}

BRAND_BREACH_PENALTY = {
    "Toyota": 1.20,
    "Volkswagen": 1.25,
    "BMW": 1.45,
}

BRAND_DISCOUNT_RANGES = {
    "Toyota": (2.0, 10.0),
    "Volkswagen": (2.5, 11.5),
    "BMW": (1.0, 8.0),
}

LEAD_CAMPAIGN_ASSOCIATION_RULES = {
    "Campaign": {"attach_probability": 0.95, "max_campaigns": 2},
    "Web Form": {"attach_probability": 0.18, "max_campaigns": 1},
    "Social Media": {"attach_probability": 0.35, "max_campaigns": 2},
    "Referral": {"attach_probability": 0.08, "max_campaigns": 1},
    "Walk-in": {"attach_probability": 0.03, "max_campaigns": 1},
    "Phone Inbound": {"attach_probability": 0.05, "max_campaigns": 1},
}