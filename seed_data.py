import random                                                                                                             
from datetime import datetime, timedelta                                                                                  
import psycopg2                                                                                                           
from faker import Faker                                     

fake = Faker()

# --- Connection ---
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="erp_dev",
    user="erp_user",
    password="erp_pass"
)
cur = conn.cursor()

# --- Clear existing data ---
cur.execute("TRUNCATE work_orders, bom, inventory, vendors RESTART IDENTITY CASCADE;")

# --- Vendors ---
print("Seeding vendors...")
vendor_ids = []
for _ in range(20):
    vendor_id = fake.unique.bothify(text="VND-####")
    vendor_ids.append(vendor_id)
    cur.execute("""
        INSERT INTO vendors (vendor_id, vendor_name, lead_time_days, on_time_rate, updated_at)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        vendor_id,
        fake.company(),
        random.randint(3, 45),
        round(random.uniform(0.60, 0.99), 2),
        fake.date_time_between(start_date="-90d", end_date="now")
    ))

# --- Inventory ---
print("Seeding inventory...")
part_numbers = []
for _ in range(100):
    part_number = fake.unique.bothify(text="PRT-######")
    part_numbers.append(part_number)
    cur.execute("""
        INSERT INTO inventory (part_number, description, on_hand_qty, reorder_point, unit_cost, vendor_id, lead_time_days,
updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        part_number,
        fake.bs().title(),
        random.randint(0, 500),
        random.randint(10, 100),
        round(random.uniform(1.50, 9999.99), 2),
        random.choice(vendor_ids),
        random.randint(3, 45),
        fake.date_time_between(start_date="-90d", end_date="now")
    ))

# --- BOM ---
print("Seeding BOM...")
bom_id_counter = 1
for parent in random.sample(part_numbers, 40):
    children = random.sample([p for p in part_numbers if p != parent], random.randint(2, 6))
    for child in children:
        cur.execute("""
            INSERT INTO bom (bom_id, parent_part, child_part, quantity, unit_of_measure, revision, effective_date,
created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            f"BOM-{bom_id_counter:04d}",
            parent,
            child,
            round(random.uniform(1, 20), 2),
            random.choice(["EA", "FT", "LB", "M", "KG"]),
            random.choice(["A", "B", "C", "D"]),
            fake.date_between(start_date="-2y", end_date="today"),
            fake.date_time_between(start_date="-2y", end_date="-90d"),
            fake.date_time_between(start_date="-90d", end_date="now")
        ))
        bom_id_counter += 1

# --- Work Orders ---
print("Seeding work orders...")
statuses = ["open", "in_progress", "complete", "cancelled"]
priorities = ["critical", "high", "medium", "low"]

for i in range(500):
    status = random.choice(statuses)
    start_date = fake.date_between(start_date="-6m", end_date="today")
    due_date = start_date + timedelta(days=random.randint(3, 60))
    completed_date = due_date + timedelta(days=random.randint(-5, 10)) if status == "complete" else None
    qty_ordered = random.randint(1, 200)
    qty_completed = qty_ordered if status == "complete" else random.randint(0, qty_ordered)

    cur.execute("""
        INSERT INTO work_orders (work_order_id, part_number, description, status, priority, qty_ordered, qty_completed,
due_date, start_date, completed_date, assigned_to, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        f"WO-{i+1:05d}",
        random.choice(part_numbers),
        fake.bs().title(),
        status,
        random.choice(priorities),
        qty_ordered,
        qty_completed,
        due_date,
        start_date,
        completed_date,
        fake.name(),
        fake.date_time_between(start_date="-6m", end_date="-90d"),
        fake.date_time_between(start_date="-90d", end_date="now")
    ))

conn.commit()
cur.close()
conn.close()
print("Done. Database seeded.")