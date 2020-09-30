CREATE TABLE aisle_tbl (
  aisle_id INT PRIMARY KEY NOT NULL,
  aisle TEXT
);

CREATE TABLE department_tbl (
  department_id INT PRIMARY KEY NOT NULL,
  department TEXT
);

CREATE TABLE product_tbl (
  product_id INT PRIMARY KEY NOT NULL,
  product_name TEXT,
  aisle_id INT NOT NULL,
  department_id INT NOT NULL,
  FOREIGN KEY (aisle_id) REFERENCES aisle_tbl(aisle_id),
  FOREIGN KEY (department_id) REFERENCES department_tbl(department_id)
);

CREATE TABLE orders_tbl (
  order_id INT PRIMARY KEY NOT NULL,
  user_id INT NOT NULL,
  eval_set TEXT,
  order_number INT,
  order_dow INT,
  order_hour_of_day INT,
  days_since_prior_order INT
);


CREATE TABLE orders_product_prior (
  id SERIAL PRIMARY KEY,
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  add_to_cart_order INT,
  reordered INT,
  FOREIGN KEY (order_id) REFERENCES orders_tbl(order_id),
  FOREIGN KEY (product_id) REFERENCES product_tbl(product_id)
);

CREATE TABLE orders_product_train (
  id SERIAL PRIMARY KEY,
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  add_to_cart_order INT,
  reordered INT,
  FOREIGN KEY (order_id) REFERENCES orders_tbl(order_id),
  FOREIGN KEY (product_id) REFERENCES product_tbl(product_id)
);

/* Alternate tables to deal with upload */

CREATE TABLE aisle2_tbl (
  aisle_id INT,
  aisle TEXT
);

CREATE TABLE department2_tbl (
  department_id INT,
  department TEXT
);

CREATE TABLE product2_tbl (
  product_id INT,
  product_name TEXT,
  aisle_id INT,
  department_id INT
);

CREATE TABLE orders2_tbl (
  order_id INT,
  user_id INT,
  eval_set TEXT,
  order_number INT,
  order_dow INT,
  order_hour_of_day INT,
  days_since_prior_order INT
);


CREATE TABLE orders_product_prior2 (
  order_id INT,
  product_id INT,
  add_to_cart_order INT,
  reordered INT
);

CREATE TABLE orders_product_train2 (
  order_id INT,
  product_id INT,
  add_to_cart_order INT,
  reordered INT
);


/* SQL ETL PROCESS */

DELETE FROM product2_tbl WHERE product_id ISNULL;
INSERT INTO product_tbl SELECT * FROM product2_tbl;
DROP TABLE product2_tbl;

DELETE FROM orders2_tbl WHERE order_id ISNULL;
INSERT INTO orders_tbl SELECT * FROM orders2_tbl;
DROP TABLE orders2_tbl;

DELETE FROM orders_product_prior2 WHERE order_id ISNULL;
INSERT INTO orders_product_prior (order_id,product_id,add_to_cart_order,reordered) SELECT * FROM orders_product_prior2;
DROP TABLE orders_product_prior2;

DELETE FROM orders_product_train2 WHERE order_id ISNULL;
INSERT INTO orders_product_train (order_id,product_id,add_to_cart_order,reordered)  SELECT * FROM orders_product_train2;
DROP TABLE orders_product_train2;
