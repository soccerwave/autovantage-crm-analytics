# Assumptions

## Project-wide Assumptions

* All datasets in this project are synthetic and generated for portfolio purposes.
* The business scenario is fictional but based on realistic automotive CRM patterns.
* Currency is EUR.
* The time window covers 2023-01-01 to 2024-12-31.
* The dealer network includes 12 dealerships across 4 regions.

## Data Generation Assumptions

* Lead behavior varies by source, including conversion rate and response time.
* Service case behavior varies by priority, SLA target, and region.
* Customer feedback is generated only for responded closed cases.
* Campaign attribution is simplified using a bridge table between leads and campaigns.
* Some row counts were adjusted during development from the original planning blueprint to support broader dashboard coverage and more stable distributions. Final implemented row counts should be interpreted as the source of truth for this repository.

## CRM / Salesforce Alignment Assumptions

* The project is aligned to Salesforce-style object logic, not to a real production Salesforce org.
* Lead, Opportunity, Account, Contact, Case, Campaign, and CampaignMember concepts are represented analytically.
* No production Salesforce administration, integration, security, or CRM Analytics implementation is claimed.

## Limitations

* This project does not use real customer data.
* Attribution logic is simplified and does not represent full production-grade first-touch / last-touch / multi-touch methodology.
* Some lifecycle relationships are simplified to keep the portfolio project interpretable and maintainable.
* Dashboard insights demonstrate analytical workflow and modeling capability, not real business performance.

