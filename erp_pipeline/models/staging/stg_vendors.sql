with source as (
    select * from read_parquet('../raw/vendors/2026/03/13/vendors.parquet')
),

renamed as (
    select
        vendor_id,
        vendor_name,
        lead_time_days,
        on_time_rate,
        updated_at,
        case when on_time_rate < 0.75 then true else false end as is_underperforming
    from source
)

select * from renamed