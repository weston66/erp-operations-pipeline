CREATE TABLE IF NOT EXISTS work_orders (
      work_order_id    VARCHAR PRIMARY KEY,
      part_number      VARCHAR NOT NULL,
      description      VARCHAR,
      status           VARCHAR,
      priority         VARCHAR,
      qty_ordered      INT,
      qty_completed    INT,
      due_date         DATE,
      start_date       DATE,
      completed_date   DATE,
      assigned_to      VARCHAR,
      created_at       TIMESTAMP,
      updated_at       TIMESTAMP
  );

  CREATE TABLE IF NOT EXISTS bom (
      bom_id           VARCHAR PRIMARY KEY,
      parent_part      VARCHAR NOT NULL,
      child_part       VARCHAR NOT NULL,
      quantity         DECIMAL,
      unit_of_measure  VARCHAR,
      revision         VARCHAR,
      effective_date   DATE,
      created_at       TIMESTAMP,
      updated_at       TIMESTAMP
  );

  CREATE TABLE IF NOT EXISTS inventory (
      part_number      VARCHAR PRIMARY KEY,
      description      VARCHAR,
      on_hand_qty      INT,
      reorder_point    INT,
      unit_cost        DECIMAL,
      vendor_id        VARCHAR,
      lead_time_days   INT,
      updated_at       TIMESTAMP
  );

  CREATE TABLE IF NOT EXISTS vendors (
      vendor_id        VARCHAR PRIMARY KEY,
      vendor_name      VARCHAR,
      lead_time_days   INT,
      on_time_rate     DECIMAL,
      updated_at       TIMESTAMP
  );
