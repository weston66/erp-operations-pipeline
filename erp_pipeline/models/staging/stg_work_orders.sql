with source as (
    select * from read_parquet('../raw/work_orders/2026/03/13/work_orders.parquet')
),

renamed as (
    select
        work_order_id,
        part_number,
        description,
        status,
        priority,
        qty_ordered,
        qty_completed,
        due_date,
        start_date,
        completed_date,
        assigned_to,
        created_at,
        updated_at,
        qty_ordered - qty_completed as qty_remaining,
        case when due_date < current_date and status != 'complete' then true else false end as is_overdue
    from source
    where status != 'cancelled'
)

select * from renamed