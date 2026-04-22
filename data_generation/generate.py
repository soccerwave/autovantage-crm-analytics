from pathlib import Path

from config import (
    START_DATE,
    END_DATE,
    DEALERS,
    TOYOTA_MODELS,
    VOLKSWAGEN_MODELS,
    BMW_MODELS,
    ROW_COUNTS,
    SEED,
    LEAD_SOURCE_CONFIG,
    MONTH_VOLUME_MULTIPLIERS,
    OPPORTUNITY_STAGE_PROBABILITY,
    OPPORTUNITY_STAGE_WEIGHTS,
    BRAND_DISCOUNT_RANGES,
    SERVICE_CASE_TYPE_WEIGHTS,
    SERVICE_PRIORITY_WEIGHTS,
    SLA_TARGET_HOURS,
    PRIORITY_COMPLIANCE_BASE,
    REGION_COMPLIANCE_ADJUSTMENT,
    SERVICE_MONTH_MULTIPLIERS,
    FEEDBACK_RESPONSE_RATE_BY_PRIORITY,
    BRAND_CSAT_ADJUSTMENT,
    BRAND_BREACH_PENALTY,
    LEAD_CAMPAIGN_ASSOCIATION_RULES,
)
from generators.bridge_lead_campaign import generate_bridge_lead_campaign
from generators.dim_date import generate_dim_date
from generators.dim_dealer import generate_dim_dealer
from generators.dim_vehicle import generate_dim_vehicle
from generators.dim_contact import generate_dim_contact
from generators.dim_campaign import generate_dim_campaign
from generators.dim_account import generate_dim_account
from generators.fact_leads import generate_fact_leads
from generators.fact_opportunities import generate_fact_opportunities
from generators.fact_orders import generate_fact_orders
from generators.fact_service_cases import generate_fact_service_cases
from generators.fact_customer_feedback import generate_fact_customer_feedback


def save_csv(df, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


def main():
    raw_dir = Path(__file__).resolve().parent / "data" / "raw"

    dim_date = generate_dim_date(START_DATE, END_DATE)
    dim_dealer = generate_dim_dealer(DEALERS)
    dim_vehicle = generate_dim_vehicle(
        TOYOTA_MODELS,
        VOLKSWAGEN_MODELS,
        BMW_MODELS,
    )
    dim_contact = generate_dim_contact(
        row_count=ROW_COUNTS["dim_contact"],
        seed=SEED,
    )
    dim_campaign = generate_dim_campaign(seed=SEED)
    dim_account = generate_dim_account(
        contacts_df=dim_contact,
        row_count=ROW_COUNTS["dim_account"],
        seed=SEED,
    )

    fact_leads = generate_fact_leads(
        row_count=ROW_COUNTS["fact_leads"],
        seed=SEED,
        dim_date=dim_date,
        dim_dealer=dim_dealer,
        dim_vehicle=dim_vehicle,
        dim_contact=dim_contact,
        lead_source_config=LEAD_SOURCE_CONFIG,
        month_volume_multipliers=MONTH_VOLUME_MULTIPLIERS,
    )

    converted_leads_count = int(fact_leads["is_converted"].sum())

    target_opportunities = int(converted_leads_count / 0.85)

    fact_opportunities = generate_fact_opportunities(
        target_row_count=target_opportunities,
        seed=SEED,
        fact_leads=fact_leads,
        dim_account=dim_account,
        dim_contact=dim_contact,
        dim_vehicle=dim_vehicle,
        dim_dealer=dim_dealer,
        dim_date=dim_date,
        stage_probability_map=OPPORTUNITY_STAGE_PROBABILITY,
        stage_weight_groups=OPPORTUNITY_STAGE_WEIGHTS,
        brand_discount_ranges=BRAND_DISCOUNT_RANGES,
    )

    lead_to_opp = (
        fact_opportunities.dropna(subset=["lead_id"])[["lead_id", "opportunity_id"]]
        .drop_duplicates(subset=["lead_id"])
    )

    fact_leads = fact_leads.merge(
        lead_to_opp,
        on="lead_id",
        how="left",
        suffixes=("", "_new"),
    )
    fact_leads["opportunity_id"] = fact_leads["opportunity_id_new"].combine_first(
        fact_leads["opportunity_id"]
    )
    fact_leads = fact_leads.drop(columns=["opportunity_id_new"])

    fact_orders = generate_fact_orders(fact_opportunities=fact_opportunities)

    fact_service_cases = generate_fact_service_cases(
        row_count=ROW_COUNTS["fact_service_cases"],
        seed=SEED,
        dim_date=dim_date,
        dim_dealer=dim_dealer,
        dim_vehicle=dim_vehicle,
        dim_contact=dim_contact,
        dim_account=dim_account,
        service_case_type_weights=SERVICE_CASE_TYPE_WEIGHTS,
        service_priority_weights=SERVICE_PRIORITY_WEIGHTS,
        sla_target_hours=SLA_TARGET_HOURS,
        priority_compliance_base=PRIORITY_COMPLIANCE_BASE,
        region_compliance_adjustment=REGION_COMPLIANCE_ADJUSTMENT,
        service_month_multipliers=SERVICE_MONTH_MULTIPLIERS,
    )

    fact_customer_feedback = generate_fact_customer_feedback(
        seed=SEED,
        fact_service_cases=fact_service_cases,
        dim_vehicle=dim_vehicle,
        response_rate_by_priority=FEEDBACK_RESPONSE_RATE_BY_PRIORITY,
        brand_csat_adjustment=BRAND_CSAT_ADJUSTMENT,
        brand_breach_penalty=BRAND_BREACH_PENALTY,
    )

    bridge_lead_campaign = generate_bridge_lead_campaign(
        fact_leads=fact_leads,
        dim_campaign=dim_campaign,
        seed=SEED,
        association_rules=LEAD_CAMPAIGN_ASSOCIATION_RULES,
    )

    save_csv(dim_date, raw_dir / "dim_date.csv")
    save_csv(dim_dealer, raw_dir / "dim_dealer.csv")
    save_csv(dim_vehicle, raw_dir / "dim_vehicle.csv")
    save_csv(dim_contact, raw_dir / "dim_contact.csv")
    save_csv(dim_campaign, raw_dir / "dim_campaign.csv")
    save_csv(dim_account, raw_dir / "dim_account.csv")
    save_csv(fact_leads, raw_dir / "fact_leads.csv")
    save_csv(fact_opportunities, raw_dir / "fact_opportunities.csv")
    save_csv(fact_orders, raw_dir / "fact_orders.csv")
    save_csv(fact_service_cases, raw_dir / "fact_service_cases.csv")
    save_csv(fact_customer_feedback, raw_dir / "fact_customer_feedback.csv")
    save_csv(bridge_lead_campaign, raw_dir / "bridge_lead_campaign.csv")

    print("Generated dim_date:", dim_date.shape)
    print("Generated dim_dealer:", dim_dealer.shape)
    print("Generated dim_vehicle:", dim_vehicle.shape)
    print("Generated dim_contact:", dim_contact.shape)
    print("Generated dim_campaign:", dim_campaign.shape)
    print("Generated dim_account:", dim_account.shape)
    print("Converted leads count:", converted_leads_count)
    print("Calculated target opportunities:", target_opportunities)
    print("Generated fact_leads:", fact_leads.shape)
    print("Generated fact_opportunities:", fact_opportunities.shape)
    print("Generated fact_orders:", fact_orders.shape)
    print("Generated fact_service_cases:", fact_service_cases.shape)
    print("Generated fact_customer_feedback:", fact_customer_feedback.shape)
    print("Generated bridge_lead_campaign:", bridge_lead_campaign.shape)


if __name__ == "__main__":
    main()