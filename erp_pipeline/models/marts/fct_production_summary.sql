with work_orders as (
    select * from {{ ref('stg_work_orders') }}
),

inventory as (
    select * from {{ ref('stg_inventory') }}
),

summary as (
    select
        current_date as report_date,

        -- work order counts
        count(*) as total_open_orders,
        count(case when priority = 'critical' then 1 end) as critical_orders,
        count(case when is_overdue then 1 end) as overdue_orders,

        -- schedule attainment
        count(case when status = 'complete' and completed_date <= due_date then 1 end) as completed_on_time,
        (completed_on_time / total_open_orders) as on_time_percent,
        count(case when status = 'complete' then 1 end) as total_completed,
        round(
            count(case when status = 'complete' and completed_date <= due_date then 1 end) * 100.0
            / nullif(count(case when status = 'complete' then 1 end), 0),
        2) as schedule_attainment_pct,

        -- parts at risk
        (select count(*) from inventory where is_at_risk) as parts_at_risk_count

    from work_orders
)

select * from summary