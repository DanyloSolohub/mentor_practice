--  оцінки студентів у окремій групі з певного предмета.
SELECT disciplines.name, groups.name, students.fullname, grades.date_of, grades.grade
FROM grades
LEFT JOIN students ON students.id = grades.student_id
LEFT JOIN disciplines ON disciplines.id = grades.discipline_id
LEFT JOIN groups ON groups.id = students.group_id
WHERE disciplines.id = 2 AND groups.id = 1;