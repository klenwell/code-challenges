--
-- Jitbit Test Queries
--
-- 2. Select employees who have the biggest salary in their departments
-- Source https://stackoverflow.com/a/612268/1093087
SELECT emp.name, dept_max.dept_name, emp.salary
FROM employees emp
INNER JOIN (
  SELECT d.department_id AS dept_id, d.name AS dept_name, MAX(salary) AS max_salary
  FROM employees e
  JOIN departments d ON d.department_id = e.department_id
  GROUP BY dept_id, dept_name
) dept_max ON emp.department_id = dept_max.dept_id AND emp.salary = dept_max.max_salary;
