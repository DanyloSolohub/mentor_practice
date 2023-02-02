-- список курсів, які відвідує студент.
SELECT students.fullname, disciplines.name
FROM grades
         LEFT JOIN students ON students.id = grades.student_id
         LEFT JOIN disciplines ON disciplines.id = grades.discipline_id
WHERE grades.student_id = 1
GROUP BY disciplines.name;