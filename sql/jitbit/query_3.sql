--
-- Jitbit Test Queries
--
-- 3. Select departments that have less than 3 people in it
SELECT dept.name, COALESCE(dept_size.count, 0) as head_count
FROM departments dept
LEFT JOIN (
  SELECT emp.department_id AS dept_id, COUNT(emp.employee_id) AS count
  FROM employees emp
  JOIN departments d ON emp.department_id = d.department_id
  GROUP BY emp.department_id
) dept_size ON dept_size.dept_id = dept.department_id
WHERE dept_size.count < 3
  OR dept_size.count IS NULL
ORDER BY head_count;
