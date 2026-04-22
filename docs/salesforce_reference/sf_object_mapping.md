# Salesforce Object Mapping

This project is analytically aligned to common Salesforce CRM objects, but it does not claim production Salesforce administration or real Salesforce implementation experience.

## Object Mapping

|Project Table|Salesforce Object|Notes|
|-|-|-|
|fact\_leads|Lead|Lead creation, source, qualification, and conversion logic|
|fact\_opportunities|Opportunity|Opportunity stages, pipeline progression, and win/loss logic|
|fact\_orders|Opportunity (Closed Won) / Order-like analytical subset|Analytical subset of completed sales|
|dim\_account|Account|Includes individual and corporate account logic|
|dim\_contact|Contact|Customer / prospect contact dimension|
|dim\_campaign|Campaign|Campaign metadata used for attribution|
|bridge\_lead\_campaign|CampaignMember|Represents lead-to-campaign many-to-many association|
|fact\_service\_cases|Case|Service and aftersales case handling|
|fact\_customer\_feedback|Custom feedback / survey object|Analytical feedback object for CSAT and NPS|

## Scope Clarification

This repository demonstrates:

* understanding of Salesforce-style CRM object relationships
* analytical modeling aligned to CRM workflows
* downstream analytics using Python, DuckDB, dbt, and Power BI

This repository does not claim:

* production Salesforce administration
* Salesforce security or user management
* Salesforce data pipeline ownership in a live environment
* CRM Analytics / Einstein Analytics implementation
* Apex, Flows, or production org customization

## Suggested Honest Resume Wording

* Designed an analytical CRM data model aligned to Salesforce-style objects including Lead, Opportunity, Account, Contact, Case, Campaign, and CampaignMember
* Mapped CRM object logic into a synthetic analytics environment for reporting in dbt and Power BI

