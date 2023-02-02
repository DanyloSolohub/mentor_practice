-- список студентів у певній групі.
SELECT students.id, students.fullname, groups.name
FROM students
LEFT JOIN groups ON groups.id = students.group_id
WHERE groups.id = 1;