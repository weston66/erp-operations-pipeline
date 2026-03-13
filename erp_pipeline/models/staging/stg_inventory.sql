with source as (
    select * from read_parquet('../raw/inventory/2026/03/13/inventory.parquet')
),

renamed as (
    select
        part_number,
        description,
        on_hand_qty,
        reorder_point,
        unit_cost,
        vendor_id,
        lead_time_days,
        updated_at,
        on_hand_qty - reorder_point as stock_buffer,
        case when on_hand_qty < reorder_point then true else false end as is_at_risk
    from source
)

select * from renamed