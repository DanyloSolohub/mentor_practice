-- Знайти середній бал на потоці (по всій таблиці grades)
SELECT round(avg(grade),2) AS avg_grade
FROM grades;