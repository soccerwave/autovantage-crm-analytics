# KPI Dictionary

## Executive KPIs

### 1\) Total Revenue (Net)

* Definition: Total realized net revenue from completed vehicle sales.
* Formula: SUM(net\_revenue\_eur)
* Grain: Order
* Source: fact\_orders
* Edge cases: Includes only completed sales. Open and lost opportunities are excluded. Revenue is measured after discount.

### 2\) Average Deal Value

* Definition: Average net revenue per completed order.
* Formula: SUM(net\_revenue\_eur) / COUNT(order\_id)
* Grain: Order
* Source: fact\_orders
* Edge cases: Calculated only on completed orders.

### 3\) Opportunity Win Rate

* Definition: Share of closed opportunities that ended as Closed Won.
* Formula: Closed Won Opportunities / (Closed Won Opportunities + Closed Lost Opportunities)
* Grain: Opportunity
* Source: fct\_pipeline
* Edge cases: Open opportunities must be excluded from the denominator.

### 4\) Weighted Pipeline Value

* Definition: Expected pipeline value weighted by stage probability.
* Formula: SUM(weighted\_pipeline\_value)
* Grain: Opportunity
* Source: fct\_pipeline
* Edge cases: Closed Lost contributes 0. Closed Won contributes full value.

## Sales Funnel KPIs

### 5\) Total Leads

* Definition: Number of generated leads.
* Formula: COUNT(lead\_id)
* Grain: Lead
* Source: fact\_leads / stg\_leads
* Edge cases: One row per lead.

### 6\) Lead-to-Opportunity Rate

* Definition: Share of leads that converted into opportunities.
* Formula: Converted Leads / Total Leads
* Grain: Lead
* Source: fact\_leads / fct\_sales\_funnel
* Edge cases: Uses the converted lead logic in the synthetic CRM model.

### 7\) Lost Lead Rate

* Definition: Share of leads ending in Lost status.
* Formula: Lost Leads / Total Leads
* Grain: Lead
* Source: fct\_sales\_funnel
* Edge cases: Only lead\_status = 'Lost' counts as lost.

### 8\) Average First Response Time

* Definition: Average time between lead creation and first response.
* Formula: AVG(first\_response\_hours)
* Grain: Lead
* Source: fact\_leads / fct\_sales\_funnel
* Edge cases: Sensitive to lead source mix.

### 9\) Average Lead Age at Close/Loss

* Definition: Average number of days before lead close or loss.
* Formula: AVG(age\_at\_close\_days)
* Grain: Lead
* Source: fact\_leads / fct\_sales\_funnel
* Edge cases: Open leads may still have lower age values.

### 10\) Sales Cycle Length

* Definition: Average number of days from opportunity creation to close.
* Formula: AVG(sales\_cycle\_days)
* Grain: Opportunity
* Source: fct\_pipeline
* Edge cases: Best interpreted on closed opportunities only.

### 11\) Closed Lost Rate

* Definition: Share of closed opportunities that ended as Closed Lost.
* Formula: Closed Lost Opportunities / (Closed Won Opportunities + Closed Lost Opportunities)
* Grain: Opportunity
* Source: fct\_pipeline
* Edge cases: Open opportunities are excluded from the denominator.

## Campaign KPIs

### 12\) Campaign Leads Count

* Definition: Number of distinct leads associated with a campaign.
* Formula: COUNT(DISTINCT lead\_id)
* Grain: Campaign
* Source: fct\_campaign\_attribution
* Edge cases: Based on bridge\_lead\_campaign logic.

### 13\) Campaign Converted Leads

* Definition: Number of campaign-linked leads that converted.
* Formula: SUM(converted\_leads\_count)
* Grain: Campaign
* Source: fct\_campaign\_attribution
* Edge cases: Depends on the current bridge-table attribution rule.

### 14\) Campaign Closed Won Opportunities

* Definition: Number of campaign-attributed opportunities that ended as Closed Won.
* Formula: COUNT(DISTINCT opportunity\_id), filtered to stage = 'Closed Won'
* Grain: Campaign
* Source: fct\_campaign\_attribution
* Edge cases: Attribution is simplified and not a production multi-touch model.

### 15\) Campaign Revenue

* Definition: Revenue from Closed Won opportunities linked to campaign-attributed leads.
* Formula: SUM(closed\_won\_revenue\_eur)
* Grain: Campaign
* Source: fct\_campaign\_attribution
* Edge cases: Revenue attribution is simplified for portfolio purposes.

## Service / Aftersales KPIs

### 16\) Total Service Cases

* Definition: Number of service cases opened.
* Formula: COUNT(case\_id)
* Grain: Service case
* Source: fact\_service\_cases / fct\_case\_resolution
* Edge cases: One row per case.

### 17\) SLA Compliance Rate

* Definition: Share of closed service cases resolved within SLA threshold.
* Formula: SLA Compliant Closed Cases / Closed Service Cases
* Grain: Closed service case
* Source: fct\_case\_resolution
* Edge cases: Open cases should be excluded from the denominator.

### 18\) SLA Breach Rate

* Definition: Share of closed service cases resolved after SLA threshold.
* Formula: SLA Breached Closed Cases / Closed Service Cases
* Grain: Closed service case
* Source: fct\_case\_resolution
* Edge cases: Complement of SLA Compliance Rate on closed cases.

### 19\) Average Resolution Time

* Definition: Average time to resolve service cases.
* Formula: AVG(resolution\_hours)
* Grain: Service case
* Source: fct\_case\_resolution
* Edge cases: Most interpretable when segmented by priority and case type; open cases should be treated carefully if included.

### 20\) Reopen Rate

* Definition: Share of service cases reopened after first resolution.
* Formula: Reopened Cases / Total Cases
* Grain: Service case
* Source: fact\_service\_cases / fct\_case\_resolution
* Edge cases: Warranty and Complaint cases tend to drive this metric.

### 21\) First-Time Fix Rate

* Definition: Share of service cases resolved without reopening.
* Formula: 1 - Reopen Rate
* Grain: Service case
* Source: fct\_case\_resolution
* Edge cases: Proxy metric based on reopen flag.

## Customer Satisfaction KPIs

### 22\) CSAT Score

* Definition: Average customer satisfaction score on a 1–5 scale.
* Formula: AVG(csat\_score)
* Grain: Feedback response
* Source: fact\_customer\_feedback
* Edge cases: Includes only responded surveys.

### 23\) NPS

* Definition: Net Promoter Score derived from 0–10 survey responses.
* Formula: % Promoters (9–10) - % Detractors (0–6)
* Grain: Feedback response
* Source: fact\_customer\_feedback
* Edge cases: Passives (7–8) are excluded from the formula.

### 24\) Survey Response Rate

* Definition: Share of closed service cases that received survey feedback.
* Formula: Feedback Responses / Closed Service Cases
* Grain: Closed service case
* Source: fact\_customer\_feedback + fact\_service\_cases
* Edge cases: Low response rates can bias satisfaction analysis.

### 25\) Detractor Rate

* Definition: Share of feedback responses with NPS score 0–6.
* Formula: Detractors / Total Responses
* Grain: Feedback response
* Source: fact\_customer\_feedback
* Edge cases: Should be reviewed alongside total response count.

### 26\) CSAT Gap by SLA Status

* Definition: Difference in average CSAT between SLA-compliant and SLA-breached cases.
* Formula: AVG(CSAT for compliant cases) - AVG(CSAT for breached cases)
* Grain: Feedback response
* Source: fact\_customer\_feedback + fact\_service\_cases
* Edge cases: This is one of the key analytical storylines in the project and depends on feedback response coverage.

