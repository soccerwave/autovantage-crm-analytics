# AutoVantage CRM Analytics

End-to-end CRM analytics portfolio project for a fictional automotive dealer network, built with Python, DuckDB, dbt, and Power BI.

## Business Context

AutoVantage Group is a fictional regional automotive dealer network operating 12 dealerships across 4 regions. The network combines vehicle sales and aftersales service operations, which makes CRM performance dependent on the full customer lifecycle rather than on sales alone.

This project was built to surface operational gaps across that lifecycle: which lead sources convert efficiently, where the sales funnel loses momentum, which service operations fail SLA expectations, and how service quality affects customer satisfaction. In the generated analytical environment, lead conversion varies sharply by source (from about 7.7% for Social Media to about 51.7% for Walk-in leads), and average CSAT is materially lower for SLA-breached cases than for SLA-compliant cases (2.90 vs 4.14). These patterns are intentional and designed to make the analytics layer realistic and defensible.

## Project Objectives

- Identify which lead sources, regions, and dealers drive stronger conversion performance
- Measure pipeline quality and win-rate dynamics across the opportunity funnel
- Evaluate SLA compliance, resolution performance, and reopen behavior in aftersales service
- Analyze campaign-attributed lead quality and revenue contribution
- Connect service quality outcomes to customer satisfaction metrics such as CSAT and NPS

## Data Scale

The final implemented dataset includes:

- 12 dealerships across 4 regions
- 16,000 leads
- 5,274 opportunities
- 2,812 completed orders
- 11,000 service cases
- 4,144 customer feedback responses
- 30 campaigns

All data is synthetic and generated for portfolio purposes.

## Dashboard Preview

### Executive Overview

![Executive Overview](docs/dashboard_screenshots/page1_executive.png)

### Sales Funnel

![Sales Funnel](docs/dashboard_screenshots/page2_sales_funnel.png)

### Aftersales Service

![Aftersales Service](docs/dashboard_screenshots/page3_aftersales.png)

### Campaign Performance

![Campaign Performance](docs/dashboard_screenshots/page4_campaign.png)

### Customer Satisfaction

![Customer Satisfaction](docs/dashboard_screenshots/page5_satisfaction.png)

### Customer Journey

![Customer Journey](docs/dashboard_screenshots/page6_customer_journey.png)

## Dashboard Pages

1. Executive Overview
2. Sales Funnel
3. Aftersales Service
4. Campaign Performance
5. Customer Satisfaction
6. Customer Journey

## Tech Stack

- Python
- pandas
- Faker
- DuckDB
- dbt Core
- Power BI

## Data Model

The project uses a star-schema-style analytical model with one bridge table for lead-campaign attribution.

Core tables:

- Dimensions: date, dealer, vehicle, contact, campaign, account
- Facts: leads, opportunities, orders, service cases, customer feedback
- Bridge: lead-campaign

![ERD](docs/data_model/erd_diagram.png)

See:

- `docs/data_model/erd_diagram.png`
- `docs/data_model/erd_diagram.md`

## KPI Framework

A dedicated KPI dictionary documents KPI definitions, formulas, grain, source tables, and edge cases.

Sample KPI table:

| KPI | Formula | Primary Stakeholder |
|---|---|---|
| Total Revenue | SUM(net_revenue_eur) | CCO |
| Opportunity Win Rate | Closed Won / All Closed Opportunities | Head of Sales |
| Lead-to-Opportunity Rate | Converted Leads / Total Leads | Sales / CRM Operations |
| SLA Compliance Rate | SLA Compliant Closed Cases / Closed Service Cases | Head of Aftersales |
| CSAT Score | AVG(csat_score) | Aftersales / Customer Experience |

See:

- `KPI_DICTIONARY.md`

## Architecture

Pipeline flow:

Python synthetic data generation -> Raw CSV files -> DuckDB raw tables -> dbt staging models -> dbt mart models -> Power BI dashboard

![Architecture Diagram](docs/architecture/architecture_diagram.png)

See:

- `docs/architecture/architecture_diagram.png`
- `docs/architecture/architecture_diagram.md`

## Salesforce Alignment

This project is structurally aligned to Salesforce-style CRM objects such as Lead, Opportunity, Account, Contact, Case, Campaign, and CampaignMember. The analytical implementation is completed outside Salesforce in Python, DuckDB, dbt, and Power BI. This repository is designed to demonstrate CRM data-model understanding and analytical workflow, not production Salesforce administration or CRM Analytics delivery.

A dedicated Salesforce reference section is included in `docs/salesforce_reference/`.

## Project Structure

```text
autovantage-crm-analytics/
├── README.md
├── ASSUMPTIONS.md
├── KPI_DICTIONARY.md
├── requirements.txt
├── data_generation/
├── dbt_project/
├── dashboards/
├── docs/
└── sql/
```

## How to Run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python data_generation/generate.py
python sql/load_raw_to_duckdb.py
cd dbt_project
dbt run
dbt test
```

## Assumptions and Limitations

- All data in this project is synthetic.
- The business scenario is fictional but designed to reflect realistic CRM behavior.
- Salesforce is represented structurally, not as a production environment.
- Row counts were adjusted during development in some tables to improve analytical coverage and distribution stability.

See:

- `ASSUMPTIONS.md`

## Target Role

CRM Analyst / Business Intelligence Analyst / Salesforce-aligned Data Analyst

## Author

Hamed Fallah  
LinkedIn: https://www.linkedin.com/in/soccerwave/  
GitHub: https://github.com/soccerwave
