--
-- Jitbit Test Queries
-- https://www.db-fiddle.com/f/3t83rr49nzg8nRbaH9TAhN/1
--
-- 1. Select employees (names) who have a bigger salary than their boss
SELECT employees.name, boss.name AS boss_name
FROM employees
LEFT JOIN employees AS boss ON boss.employee_id = employees.boss_id
WHERE employees.salary > boss.salary;

-- https://thoughtbot.com/blog/reading-an-explain-analyze-query-plan
EXPLAIN ANALYZE SELECT employees.name, boss.name AS boss_name
FROM employees
LEFT JOIN employees AS boss ON boss.employee_id = employees.boss_id
WHERE employees.salary > boss.salary;
