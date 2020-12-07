---
--- Schema
---
CREATE TABLE departments (
  department_id serial PRIMARY KEY,
  name VARCHAR ( 50 ) NOT NULL
);

CREATE TABLE employees (
  employee_id serial PRIMARY KEY,
  department_id INT,
  boss_id INT,
  name VARCHAR ( 50 ) NOT NULL,
  salary REAL,
  FOREIGN KEY (boss_id)
      REFERENCES employees (employee_id),
  FOREIGN KEY (department_id)
      REFERENCES departments (department_id)
);


--
-- Inserts
--
-- Departments
INSERT INTO departments (department_id, name) VALUES (1, 'Executive');
INSERT INTO departments (department_id, name) VALUES (2, 'Ride Operations');
INSERT INTO departments (department_id, name) VALUES (3, 'Vending');
INSERT INTO departments (department_id, name) VALUES (4, 'Guest Services');

-- Executive Employees
INSERT INTO employees (employee_id, department_id, boss_id, name, salary) VALUES (1, 1, NULL, 'Walt', 10000000);

-- Ride Operations Employees
INSERT INTO employees (employee_id, department_id, boss_id, name, salary) VALUES (2, 2, 1, 'Suzanne', 40000);
INSERT INTO employees (employee_id, department_id, boss_id, name, salary) VALUES (3, 2, 2, 'Jack', 50000);
INSERT INTO employees (employee_id, department_id, boss_id, name, salary) VALUES (4, 2, 2, 'Melissa', 45000);
INSERT INTO employees (employee_id, department_id, boss_id, name, salary) VALUES (5, 2, 2, 'Norman', 30000);
INSERT INTO employees (employee_id, department_id, boss_id, name, salary) VALUES (6, 2, 2, 'Ryan', 33000);

-- Vending Employees
INSERT INTO employees (employee_id, department_id, boss_id, name, salary) VALUES (7, 3, 1, 'Debbie', 60000);
INSERT INTO employees (employee_id, department_id, boss_id, name, salary) VALUES (8, 3, 7, 'Timothy', 35000);

-- Guest Services Employees
-- None
