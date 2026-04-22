from pathlib import Path
import pandas as pd
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data_generation" / "data" / "raw"


def load_csv(file_name: str) -> pd.DataFrame:
    path = RAW_DIR / file_name
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return pd.read_csv(path)


def print_section(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def check(condition: bool, label: str, failures: list[str]) -> None:
    status = "PASS" if condition else "FAIL"
    print(f"{status} - {label}")
    if not condition:
        failures.append(label)


def main():
    failures = []

    print_section("LOAD FILES")
    dim_date = load_csv("dim_date.csv")
    dim_dealer = load_csv("dim_dealer.csv")
    dim_vehicle = load_csv("dim_vehicle.csv")
    dim_contact = load_csv("dim_contact.csv")
    dim_campaign = load_csv("dim_campaign.csv")
    dim_account = load_csv("dim_account.csv")
    fact_leads = load_csv("fact_leads.csv")
    fact_opportunities = load_csv("fact_opportunities.csv")
    fact_orders = load_csv("fact_orders.csv")
    fact_service_cases = load_csv("fact_service_cases.csv")
    fact_customer_feedback = load_csv("fact_customer_feedback.csv")
    bridge_lead_campaign = load_csv("bridge_lead_campaign.csv")

    print(f"RAW_DIR: {RAW_DIR}")

    print_section("ROW COUNT CHECKS")
    row_expectations = {
        "dim_date": (len(dim_date), 731),
        "dim_dealer": (len(dim_dealer), 12),
        "dim_vehicle": (len(dim_vehicle), 45),
        "dim_contact": (len(dim_contact), 5800),
        "dim_campaign": (len(dim_campaign), 30),
        "dim_account": (len(dim_account), 3200),
        "fact_service_cases": (len(fact_service_cases), 11000),
    }

    for name, (actual, expected) in row_expectations.items():
        check(actual == expected, f"{name} row count = {expected} (actual={actual})", failures)

    check(3500 <= len(fact_customer_feedback) <= 4700,
          f"fact_customer_feedback row count in reasonable range (actual={len(fact_customer_feedback)})",
          failures)

    check(2400 <= len(fact_orders) <= 3200,
          f"fact_orders row count in reasonable range (actual={len(fact_orders)})",
          failures)

    check(4500 <= len(fact_opportunities) <= 6000,
          f"fact_opportunities row count in reasonable range (actual={len(fact_opportunities)})",
          failures)

    check(8000 <= len(fact_leads) <= 17000,
          f"fact_leads row count in reasonable range (actual={len(fact_leads)})",
          failures)

    print_section("UNIQUENESS CHECKS")
    uniqueness_checks = [
        (dim_date["date_key"].nunique() == len(dim_date), "dim_date.date_key unique"),
        (dim_dealer["dealer_id"].nunique() == len(dim_dealer), "dim_dealer.dealer_id unique"),
        (dim_vehicle["vehicle_id"].nunique() == len(dim_vehicle), "dim_vehicle.vehicle_id unique"),
        (dim_contact["contact_id"].nunique() == len(dim_contact), "dim_contact.contact_id unique"),
        (dim_contact["email"].nunique() == len(dim_contact), "dim_contact.email unique"),
        (dim_campaign["campaign_id"].nunique() == len(dim_campaign), "dim_campaign.campaign_id unique"),
        (dim_account["account_id"].nunique() == len(dim_account), "dim_account.account_id unique"),
        (fact_leads["lead_id"].nunique() == len(fact_leads), "fact_leads.lead_id unique"),
        (fact_opportunities["opportunity_id"].nunique() == len(fact_opportunities), "fact_opportunities.opportunity_id unique"),
        (fact_orders["order_id"].nunique() == len(fact_orders), "fact_orders.order_id unique"),
        (fact_service_cases["case_id"].nunique() == len(fact_service_cases), "fact_service_cases.case_id unique"),
        (fact_customer_feedback["feedback_id"].nunique() == len(fact_customer_feedback), "fact_customer_feedback.feedback_id unique"),
        (bridge_lead_campaign.duplicated(subset=["lead_id", "campaign_id"]).sum() == 0, "bridge_lead_campaign pair unique"),
    ]

    for condition, label in uniqueness_checks:
        check(condition, label, failures)

    print_section("FOREIGN KEY CHECKS")
    fk_checks = [
        (fact_leads["created_date_key"].isin(dim_date["date_key"]).all(), "fact_leads.created_date_key -> dim_date"),
        (fact_leads["dealer_id"].isin(dim_dealer["dealer_id"]).all(), "fact_leads.dealer_id -> dim_dealer"),
        (fact_leads["contact_id"].isin(dim_contact["contact_id"]).all(), "fact_leads.contact_id -> dim_contact"),
        (fact_leads["vehicle_interest"].isin(dim_vehicle["vehicle_id"]).all(), "fact_leads.vehicle_interest -> dim_vehicle"),

        (fact_opportunities["account_id"].isin(dim_account["account_id"]).all(), "fact_opportunities.account_id -> dim_account"),
        (fact_opportunities["contact_id"].isin(dim_contact["contact_id"]).all(), "fact_opportunities.contact_id -> dim_contact"),
        (fact_opportunities["vehicle_id"].isin(dim_vehicle["vehicle_id"]).all(), "fact_opportunities.vehicle_id -> dim_vehicle"),
        (fact_opportunities["dealer_id"].isin(dim_dealer["dealer_id"]).all(), "fact_opportunities.dealer_id -> dim_dealer"),

        (fact_orders["opportunity_id"].isin(fact_opportunities["opportunity_id"]).all(), "fact_orders.opportunity_id -> fact_opportunities"),
        (fact_orders["account_id"].isin(dim_account["account_id"]).all(), "fact_orders.account_id -> dim_account"),
        (fact_orders["contact_id"].isin(dim_contact["contact_id"]).all(), "fact_orders.contact_id -> dim_contact"),
        (fact_orders["vehicle_id"].isin(dim_vehicle["vehicle_id"]).all(), "fact_orders.vehicle_id -> dim_vehicle"),
        (fact_orders["dealer_id"].isin(dim_dealer["dealer_id"]).all(), "fact_orders.dealer_id -> dim_dealer"),

        (fact_service_cases["account_id"].isin(dim_account["account_id"]).all(), "fact_service_cases.account_id -> dim_account"),
        (fact_service_cases["contact_id"].isin(dim_contact["contact_id"]).all(), "fact_service_cases.contact_id -> dim_contact"),
        (fact_service_cases["vehicle_id"].isin(dim_vehicle["vehicle_id"]).all(), "fact_service_cases.vehicle_id -> dim_vehicle"),
        (fact_service_cases["dealer_id"].isin(dim_dealer["dealer_id"]).all(), "fact_service_cases.dealer_id -> dim_dealer"),
        (fact_service_cases["open_date_key"].isin(dim_date["date_key"]).all(), "fact_service_cases.open_date_key -> dim_date"),

        (fact_customer_feedback["case_id"].isin(fact_service_cases["case_id"]).all(), "fact_customer_feedback.case_id -> fact_service_cases"),
        (fact_customer_feedback["contact_id"].isin(dim_contact["contact_id"]).all(), "fact_customer_feedback.contact_id -> dim_contact"),
        (fact_customer_feedback["dealer_id"].isin(dim_dealer["dealer_id"]).all(), "fact_customer_feedback.dealer_id -> dim_dealer"),
        (fact_customer_feedback["vehicle_id"].isin(dim_vehicle["vehicle_id"]).all(), "fact_customer_feedback.vehicle_id -> dim_vehicle"),

        (bridge_lead_campaign["lead_id"].isin(fact_leads["lead_id"]).all(), "bridge_lead_campaign.lead_id -> fact_leads"),
        (bridge_lead_campaign["campaign_id"].isin(dim_campaign["campaign_id"]).all(), "bridge_lead_campaign.campaign_id -> dim_campaign"),

        (dim_account["primary_contact_id"].isin(dim_contact["contact_id"]).all(), "dim_account.primary_contact_id -> dim_contact"),
    ]

    for condition, label in fk_checks:
        check(condition, label, failures)

    print_section("BUSINESS LOGIC CHECKS")

    bad_lead_1 = fact_leads[(fact_leads["is_converted"] == True) & (fact_leads["lead_status"] != "Converted")]
    bad_lead_2 = fact_leads[(fact_leads["is_converted"] == False) & (fact_leads["lead_status"] == "Converted")]
    bad_lead_3 = fact_leads[(fact_leads["lead_status"] == "Lost") & (fact_leads["lost_reason"].isna())]
    bad_lead_4 = fact_leads[(fact_leads["lead_status"] != "Lost") & (fact_leads["lost_reason"].notna())]

    check(len(bad_lead_1) == 0, "fact_leads converted flag consistent with lead_status", failures)
    check(len(bad_lead_2) == 0, "fact_leads non-converted rows are not marked Converted", failures)
    check(len(bad_lead_3) == 0, "fact_leads Lost rows have lost_reason", failures)
    check(len(bad_lead_4) == 0, "fact_leads non-Lost rows do not have lost_reason", failures)

    bad_opp_1 = fact_opportunities[(fact_opportunities["stage"] == "Closed Lost") & (fact_opportunities["lost_reason"].isna())]
    bad_opp_2 = fact_opportunities[(fact_opportunities["stage"] != "Closed Lost") & (fact_opportunities["lost_reason"].notna())]
    bad_opp_3 = fact_opportunities[
        (fact_opportunities["stage"].isin(["Closed Won", "Closed Lost"])) & (fact_opportunities["close_date_key"].isna())
    ]
    bad_opp_4 = fact_opportunities[
        (~fact_opportunities["stage"].isin(["Closed Won", "Closed Lost"])) & (fact_opportunities["close_date_key"].notna())
    ]
    calc_net = (fact_opportunities["deal_value_eur"] * (1 - fact_opportunities["discount_pct"] / 100)).round(2)

    check(len(bad_opp_1) == 0, "Closed Lost opportunities have lost_reason", failures)
    check(len(bad_opp_2) == 0, "non-Closed Lost opportunities do not have lost_reason", failures)
    check(len(bad_opp_3) == 0, "closed opportunities have close_date_key", failures)
    check(len(bad_opp_4) == 0, "open opportunities do not have close_date_key", failures)
    check(np.allclose(calc_net, fact_opportunities["net_revenue_eur"].round(2)), "fact_opportunities net_revenue formula correct", failures)

    merged_orders = fact_orders.merge(
        fact_opportunities[["opportunity_id", "stage", "close_date_key"]],
        on="opportunity_id",
        how="left"
    )
    check((merged_orders["stage"] == "Closed Won").all(), "fact_orders only from Closed Won opportunities", failures)
    check((merged_orders["order_date_key"] == merged_orders["close_date_key"]).all(), "fact_orders.order_date_key = opportunities.close_date_key", failures)

    bad_case_1 = fact_service_cases[
        fact_service_cases["close_date_key"].isna() & ~fact_service_cases["status"].isin(["Open", "In Progress"])
    ]
    bad_case_2 = fact_service_cases[
        fact_service_cases["close_date_key"].notna() & ~fact_service_cases["status"].isin(["Resolved", "Closed"])
    ]
    bad_case_3 = fact_service_cases[
        ((fact_service_cases["resolution_hours"] > fact_service_cases["sla_target_hours"]) & (fact_service_cases["is_sla_breached"] == False)) |
        ((fact_service_cases["resolution_hours"] <= fact_service_cases["sla_target_hours"]) & (fact_service_cases["is_sla_breached"] == True))
    ]

    check(len(bad_case_1) == 0, "open service cases have valid open status", failures)
    check(len(bad_case_2) == 0, "closed service cases have valid closed status", failures)
    check(len(bad_case_3) == 0, "service case SLA breach flag consistent with resolution time", failures)

    check(fact_customer_feedback["csat_score"].between(1, 5).all(), "feedback csat_score range valid", failures)
    check(fact_customer_feedback["nps_score"].between(0, 10).all(), "feedback nps_score range valid", failures)
    check(fact_customer_feedback["case_id"].nunique() == len(fact_customer_feedback), "max one feedback per case", failures)

    print_section("DISTRIBUTION / SANITY CHECKS")

    lead_conv_by_source = fact_leads.groupby("lead_source")["is_converted"].mean().sort_values(ascending=False)
    print("Lead conversion by source:")
    print(lead_conv_by_source.round(3))
    check(lead_conv_by_source.index[0] in ["Walk-in", "Referral", "Phone Inbound"],
          "top converting lead source is plausible",
          failures)

    lead_response_by_source = fact_leads.groupby("lead_source")["first_response_hours"].mean().sort_values()
    print("\nLead response time by source:")
    print(lead_response_by_source.round(2))
    check(lead_response_by_source.index[0] in ["Phone Inbound", "Walk-in"],
          "fastest lead response source is plausible",
          failures)

    service_priority_compliance = (1 - fact_service_cases.groupby("priority")["is_sla_breached"].mean()).round(3)
    print("\nSLA compliance by priority:")
    print(service_priority_compliance.sort_values(ascending=False))
    check(
        service_priority_compliance["Low"] >= service_priority_compliance["Medium"] >= service_priority_compliance["High"] >= service_priority_compliance["Critical"],
        "SLA compliance ordering by priority is logical",
        failures
    )

    feedback_join = fact_customer_feedback.merge(
        fact_service_cases[["case_id", "is_sla_breached"]],
        on="case_id",
        how="left"
    )
    csat_by_breach = feedback_join.groupby("is_sla_breached")["csat_score"].mean().round(2)
    print("\nCSAT by SLA breach:")
    print(csat_by_breach)
    check(
        (False in csat_by_breach.index) and (True in csat_by_breach.index) and (csat_by_breach[False] > csat_by_breach[True]),
        "SLA-compliant cases have higher CSAT",
        failures
    )

    print_section("FINAL SUMMARY")
    if failures:
        print("OVERALL PASS: False")
        print("\nFailed checks:")
        for item in failures:
            print(f"- {item}")
    else:
        print("OVERALL PASS: True")


if __name__ == "__main__":
    main()