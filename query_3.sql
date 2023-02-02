-- Cредний балл в группе по одному предмету.
SELECT disciplines.name, groups.name, round(avg(grades.grade), 2) AS grade
FROM grades
         LEFT JOIN students ON students.id = grades.student_id
         LEFT JOIN disciplines ON disciplines.id = grades.discipline_id
         LEFT JOIN groups ON groups.id = students.group_id
WHERE disciplines.id = 2
GROUP BY groups.id
ORDER BY grade DESC;