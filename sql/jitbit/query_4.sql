--
-- Jitbit Test Queries
--
-- 4. Select all departments along with the number of people there (tricky - people often do an "inner join" leaving out empty departments)
SELECT dept.name, COALESCE(dept_size.count, 0) AS size
FROM departments dept
LEFT JOIN (
  SELECT emp.department_id AS dept_id, COUNT(emp.employee_id) AS count
  FROM employees emp
  JOIN departments d ON emp.department_id = d.department_id
  GROUP BY emp.department_id
) dept_size ON dept_size.dept_id = dept.department_id
ORDER BY size DESC;
