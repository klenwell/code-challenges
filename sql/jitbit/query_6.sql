--
-- Jitbit Test Queries
--
-- 6. Select all departments along with the total salary there
SELECT dept.name, COALESCE(dept_expense.total_salary, 0) AS dept_salary
FROM departments dept
LEFT JOIN (
  SELECT emp.department_id AS dept_id, SUM(emp.salary) AS total_salary
  FROM employees emp
  JOIN departments d ON emp.department_id = d.department_id
  GROUP BY emp.department_id
) dept_expense ON dept_expense.dept_id = dept.department_id
ORDER BY dept_salary DESC;
