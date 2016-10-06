#!/bin/bash

# Provides a way to insert content to database automatically to ApiRest testing.

PORT=8001

mysql -u root -p'root' < dbapi/DBCreator.sql


# It inserted three teachers
curl -H "Content-Type: application/json" -X POST -d '{"data": {"name": "María"} }' localhost:${PORT}/entities/teacher
curl -H "Content-Type: application/json" -X POST -d '{"data": {"name": "Juan"} }' localhost:${PORT}/entities/teacher
curl -H "Content-Type: application/json" -X POST -d '{"data": {"name": "Lucía"} }' localhost:${PORT}/entities/teacher

# It inserted three students
curl -H "Content-Type: application/json" -X POST -d '{"data": {"name": "Ramón"} }' localhost:${PORT}/entities/student
curl -H "Content-Type: application/json" -X POST -d '{"data": {"name": "Esteban"} }' localhost:${PORT}/entities/student
curl -H "Content-Type: application/json" -X POST -d '{"data": {"name": "Carmen"} }' localhost:${PORT}/entities/student

# It inserted three subjects
curl -H "Content-Type: application/json" -X POST -d '{"data": {"name": "Spanish"} }' localhost:${PORT}/entities/subject
curl -H "Content-Type: application/json" -X POST -d '{"data": {"name": "French"} }' localhost:${PORT}/entities/subject
curl -H "Content-Type: application/json" -X POST -d '{"data": {"name": "Science"} }' localhost:${PORT}/entities/subject

# It inserted three classes
curl -H "Content-Type: application/json" -X POST -d '{"data": {"course": 1, "word": "A", "level": "ESO"} }' localhost:${PORT}/entities/class
curl -H "Content-Type: application/json" -X POST -d '{"data": {"course": 1, "word": "B", "level": "ESO"} }' localhost:${PORT}/entities/class
curl -H "Content-Type: application/json" -X POST -d '{"data": {"course": 1, "word": "C", "level": "ESO"} }' localhost:${PORT}/entities/class


# It inserted three relations between subject and class
curl -H "Content-Type: application/json" -X POST -d '{"data": {"classId": 1, "subjectId": 1} }' localhost:${PORT}/entities/association
curl -H "Content-Type: application/json" -X POST -d '{"data": {"classId": 2, "subjectId": 2} }' localhost:${PORT}/entities/association
curl -H "Content-Type: application/json" -X POST -d '{"data": {"classId": 3, "subjectId": 3} }' localhost:${PORT}/entities/association

# It inserted three relations between teachers and associations
curl -H "Content-Type: application/json" -X POST -d '{"data": {"teacherId": 1, "associationId": 1} }' localhost:${PORT}/entities/impart
curl -H "Content-Type: application/json" -X POST -d '{"data": {"teacherId": 2, "associationId": 2} }' localhost:${PORT}/entities/impart
curl -H "Content-Type: application/json" -X POST -d '{"data": {"teacherId": 3, "associationId": 3} }' localhost:${PORT}/entities/impart

# It inserted three relations between students and associations

# A student 1 is enrolled in one, two and three associations
curl -H "Content-Type: application/json" -X POST -d '{"data": {"studentId": 1, "associationId": 1} }' localhost:${PORT}/entities/enrollment
curl -H "Content-Type: application/json" -X POST -d '{"data": {"studentId": 1, "associationId": 2} }' localhost:${PORT}/entities/enrollment
curl -H "Content-Type: application/json" -X POST -d '{"data": {"studentId": 1, "associationId": 3} }' localhost:${PORT}/entities/enrollment

curl -H "Content-Type: application/json" -X POST -d '{"data": {"studentId": 2, "associationId": 2} }' localhost:${PORT}/entities/enrollment
curl -H "Content-Type: application/json" -X POST -d '{"data": {"studentId": 3, "associationId": 3} }' localhost:${PORT}/entities/enrollment

