-- ============================================================
-- Electronic Campaigns Efficiency Dashboard
-- SQL Server Views & KPI Queries
-- Author: Abdelrahman Elmogy
-- ============================================================


-- ─────────────────────────────────────────
-- VIEW 1: Campaign Summary KPIs
-- ─────────────────────────────────────────
CREATE OR ALTER VIEW vw_CampaignKPIs AS
SELECT
    campaign_id,
    campaign_name,
    channel,
    segment,
    status,
    start_date,
    end_date,
    total_contacts,
    delivered,
    responded,
    converted,
    ROUND(CAST(delivered  AS FLOAT) / NULLIF(total_contacts, 0), 4) AS delivery_rate,
    ROUND(CAST(responded  AS FLOAT) / NULLIF(delivered,      0), 4) AS response_rate,
    ROUND(CAST(converted  AS FLOAT) / NULLIF(responded,      0), 4) AS conversion_rate,
    total_cost,
    recovery_amount,
    ROUND((recovery_amount - total_cost) / NULLIF(total_cost, 0) * 100, 2) AS campaign_roi,
    ROUND(total_cost / NULLIF(total_contacts, 0), 2) AS cost_per_contact
FROM dbo.Campaigns;
GO


-- ─────────────────────────────────────────
-- VIEW 2: Channel Performance Summary
-- ─────────────────────────────────────────
CREATE OR ALTER VIEW vw_ChannelPerformance AS
SELECT
    channel,
    COUNT(*)                                                        AS total_campaigns,
    SUM(total_contacts)                                             AS total_contacts,
    SUM(delivered)                                                  AS total_delivered,
    SUM(responded)                                                  AS total_responded,
    SUM(converted)                                                  AS total_converted,
    ROUND(AVG(CAST(delivered  AS FLOAT) / NULLIF(total_contacts,0)),4) AS avg_delivery_rate,
    ROUND(AVG(CAST(responded  AS FLOAT) / NULLIF(delivered,     0)),4) AS avg_response_rate,
    ROUND(AVG(CAST(converted  AS FLOAT) / NULLIF(responded,     0)),4) AS avg_conversion_rate,
    SUM(total_cost)                                                 AS total_cost,
    SUM(recovery_amount)                                            AS total_recovered,
    ROUND(SUM(recovery_amount - total_cost) / NULLIF(SUM(total_cost),0) * 100, 2) AS overall_roi
FROM dbo.Campaigns
GROUP BY channel;
GO


-- ─────────────────────────────────────────
-- VIEW 3: Best Time to Contact
-- ─────────────────────────────────────────
CREATE OR ALTER VIEW vw_BestContactHours AS
SELECT
    channel,
    DATEPART(HOUR, contact_time)         AS contact_hour,
    COUNT(*)                             AS total_contacts,
    SUM(responded)                       AS total_responses,
    ROUND(
        CAST(SUM(responded) AS FLOAT) / NULLIF(COUNT(*), 0), 4
    )                                    AS response_rate
FROM dbo.Contacts
GROUP BY channel, DATEPART(HOUR, contact_time);
GO


-- ─────────────────────────────────────────
-- KPI QUERIES
-- ─────────────────────────────────────────

-- Q1: Top 10 campaigns by ROI
SELECT TOP 10
    campaign_id,
    campaign_name,
    channel,
    segment,
    campaign_roi,
    recovery_amount,
    total_cost
FROM vw_CampaignKPIs
ORDER BY campaign_roi DESC;


-- Q2: Monthly recovery trend per channel
SELECT
    FORMAT(start_date, 'yyyy-MM')   AS campaign_month,
    channel,
    SUM(recovery_amount)            AS total_recovered,
    SUM(total_cost)                 AS total_cost,
    ROUND(
        SUM(recovery_amount - total_cost) / NULLIF(SUM(total_cost),0) * 100, 2
    )                               AS monthly_roi
FROM dbo.Campaigns
GROUP BY FORMAT(start_date, 'yyyy-MM'), channel
ORDER BY campaign_month, channel;


-- Q3: Segment performance comparison
SELECT
    segment,
    channel,
    COUNT(*)                        AS campaigns,
    ROUND(AVG(response_rate),4)     AS avg_response_rate,
    ROUND(AVG(conversion_rate),4)   AS avg_conversion_rate,
    ROUND(AVG(campaign_roi),2)      AS avg_roi
FROM vw_CampaignKPIs
GROUP BY segment, channel
ORDER BY segment, avg_roi DESC;


-- Q4: Cost efficiency per channel
SELECT
    channel,
    ROUND(AVG(cost_per_contact), 2)  AS avg_cost_per_contact,
    ROUND(AVG(conversion_rate),  4)  AS avg_conversion_rate,
    ROUND(
        AVG(recovery_amount) / NULLIF(AVG(total_cost), 0), 2
    )                                AS recovery_per_cost_ratio
FROM vw_CampaignKPIs
GROUP BY channel
ORDER BY recovery_per_cost_ratio DESC;
