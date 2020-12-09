--
-- Jitbit Test Queries
--
-- 5. Select employees that don't have a boss in the same department
SELECT emp.name AS emp_name, emp_dept.name AS emp_dept_name, boss.name AS boss_name, boss_dept.name AS boss_dept_name
FROM employees emp
LEFT JOIN employees AS boss ON boss.employee_id = emp.boss_id
LEFT JOIN departments AS emp_dept ON emp_dept.department_id = emp.department_id
LEFT JOIN departments AS boss_dept ON boss_dept.department_id = boss.department_id
WHERE emp.department_id != boss.department_id;
