-- Оцінки студентів у певній групі з певного предмета на останньому занятті.
SELECT disciplines.name, groups.name, students.fullname, grades.date_of, grades.grade
FROM grades
         LEFT JOIN students ON students.id = grades.student_id
         LEFT JOIN disciplines ON disciplines.id = grades.discipline_id
         LEFT JOIN groups ON groups.id = students.group_id
WHERE disciplines.id = 1
  AND groups.id = 2
  AND grades.date_of = (SELECT MAX(g.date_of)
                        FROM grades AS g
                                 LEFT JOIN students ON students.id = g.student_id
                                 LEFT JOIN groups ON groups.id = students.group_id
                        WHERE g.discipline_id = 1
                          AND g.id = 2)
order BY grades.date_of DESC