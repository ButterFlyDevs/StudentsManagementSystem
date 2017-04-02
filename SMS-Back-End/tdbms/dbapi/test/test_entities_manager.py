# -*- coding: utf-8 -*-

# How run this test:
# > pytest test_entities_manager.py  -vv -s
# > pytest --cov=entities_manager test/test_entities_manager.py  -vv -s
# > pytest --cov-report term-missing --cov=entities_manager test/test_entities_manager.py

# export PYTHONPATH="${PYTHONPATH}:/home/.../StudentsManagementSystem/SMS-Back-End/dbms/dbapi"


import sys, os
from entities_manager import EntitiesManager
from termcolor import colored
import datetime

class TestEntitiesManager:

    def setup_method(self):
        os.system('mysql -u root -p\'root\' < DBCreator.sql >/dev/null 2>&1')

    def test_1_post_method(self):

        ##################
        # STUDENT ENTITY #
        ##################

        entity = EntitiesManager.post(kind='student', data={'name': 'Juan'})

        # When we insert a entity must be returned a list with status, data and log.
        status = entity.get('status', None)
        assert status is not None and status == 1
        assert entity.get('data', None) is not None
        assert entity.get('log', 1) is None

        # Is the data received correct?
        data = entity['data']

        # The values saved plus 3 control field: [createdAt], [createdBy] and [<entity>Id]
        assert len(data) == 4

        # The control values expected have been saved?
        for item in ['createdAt', 'createdBy', 'studentId']:
            assert data.get(item, None) is not None

        # We can't save without the value 'name'.
        response = EntitiesManager.post(kind='student', data={'locality': 'UGR'})

        # Status error: 1048: Column can 't be null.
        assert response.get('status', None) == 1048
        assert response.get('data', 1) is None
        assert 'Column \'name\' cannot be null' in response.get('log', None)

        # We can't save two students with the same DNI.
        assert EntitiesManager.post(kind='student', data={'name': 'Juan', 'dni': 4545}).get('status') == 1
        response = EntitiesManager.post(kind='student', data={'name': 'Juan', 'dni': 4545})

        # Status error: 1062: Duplicate entry
        assert response.get('status', None) == 1062
        assert response.get('data', 1) is None
        assert 'Duplicate entry \'4545' in response.get('log', None)


        ##################
        # TEACHER ENTITY #
        ##################

        entity = EntitiesManager.post(kind='teacher', data={'name': 'Juan'})

        # When we insert a entity must be returned a list with status, data and log.
        status = entity.get('status', None)
        assert status is not None and status == 1
        assert entity.get('data', None) is not None
        assert entity.get('log', 1) is None

        # Is the data received correct?
        data = entity['data']

        # The values saved plus 3 control field: [createdAt], [createdBy] and [<entity>Id]
        assert len(data) == 4

        # The control values expected have been saved?
        for item in ['createdAt', 'createdBy', 'teacherId']:
            assert data.get(item, None) is not None

        # We can't save without the value 'name'.
        response = EntitiesManager.post(kind='teacher', data={'locality': 'UGR'})

        # Status error: 1048: Column can 't be null.
        assert response.get('status', None) == 1048
        assert response.get('data', 1) is None
        assert 'Column \'name\' cannot be null' in response.get('log', None)

        # We can't save two teachers with the same DNI.
        assert EntitiesManager.post(kind='teacher', data={'name': 'Juan', 'dni': 4545}).get('status') == 1
        response = EntitiesManager.post(kind='teacher', data={'name': 'Juan', 'dni': 4545})

        # Status error: 1062: Duplicate entry
        assert response.get('status', None) == 1062
        assert response.get('data', 1) is None
        assert 'Duplicate entry \'4545' in response.get('log', None)

        ##################
        # SUBJECT ENTITY #
        ##################

        entity = EntitiesManager.post(kind='subject', data={'name': 'Space Science'})

        # When we insert a entity must be returned a list with status, data and log.
        status = entity.get('status', None)
        assert status is not None and status == 1
        assert entity.get('data', None) is not None
        assert entity.get('log', 1) is None

        # Is the data received correct?
        data = entity['data']

        # The values saved plus 3 control field: [createdAt], [createdBy] and [<entity>Id]
        assert len(data) == 4

        # The control values expected have been saved?
        for item in ['createdAt', 'createdBy', 'subjectId']:
            assert data.get(item, None) is not None

        # We can't save without the value 'name'.
        response = EntitiesManager.post(kind='subject', data={'description': 'a cool subject'})

        # Status error: 1048: Column can 't be null.
        assert response.get('status', None) == 1048
        assert response.get('data', 1) is None
        assert 'Column \'name\' cannot be null' in response.get('log', None)

        # We can't save two subjects with the same name.
        response = EntitiesManager.post(kind='subject', data={'name': 'Space Science'})

        # Status error: 1062: Duplicate entry
        assert response.get('status', None) == 1062
        assert response.get('data', 1) is None
        assert 'Duplicate entry \'Space Science' in response.get('log', None)


        ##################
        # CLASS ENTITY #
        ##################

        entity = EntitiesManager.post(kind='class', data={'course': 1, 'word': 'A', 'level': 'Elementary'})

        # When we insert a entity must be returned a list with status, data and log.
        status = entity.get('status', None)
        assert status is not None and status == 1
        assert entity.get('data', None) is not None
        assert entity.get('log', 1) is None

        # Is the data received correct?
        data = entity['data']

        # The values saved plus 3 control field: [createdAt], [createdBy] and [<entity>Id]
        assert len(data) == 6

        # The control values expected have been saved?
        for item in ['createdAt', 'createdBy', 'classId']:
            assert data.get(item, None) is not None

        # We can't save without the value 'course', 'word' or 'level.
        response = EntitiesManager.post(kind='class', data={'description': 'a cool class'})
        print response
        # Status error: 1048: Column can 't be null.
        assert response.get('status', None) == 1048
        assert response.get('data', 1) is None
        assert 'Column \'course\' cannot be null' in response.get('log', None)

        # We can't save two subjects with the same name.
        response = EntitiesManager.post(kind='class', data={'course': 1, 'word': 'A', 'level': 'Elementary'})

        # Status error: 1062: Duplicate entry
        assert response.get('status', None) == 1062
        assert response.get('data', 1) is None
        assert 'Duplicate entry \'1-A-Elementary' in response.get('log', None)

    """
        for item in tests:

            entity = EntitiesManager.post(kind=item['kind'], data=item['data'])
            print colored(entity, 'yellow')

            for i in ['status', 'data', 'log']:
                assert i in entity

            for k, v in item['data'].iteritems():
                assert entity['data'][k] == v

            assert entity['data']['createdAt'].date().strftime("%d-%m-%Y %H:%M") \
                   == datetime.datetime.now().date().strftime("%d-%m-%Y %H:%M")

        # Check some errors
        entity = EntitiesManager.put(kind='cat', data={'name': u'Juan'})
        print entity
        assert entity['status'] == 1146 and "Table 'sms.cat' doesn't exist" in entity['log']

        entity = EntitiesManager.put(kind='student', data={'number': u'Juan'})
        if entity['status'] != 1054 and "Unknown column 'number'" not in entity['log']:
            assert False

        # Two teachers with the same dni can't be saved.
        original_entity = EntitiesManager.put(kind='teacher', data={'name': u'Luis', 'dni': 1234})
        assert original_entity['status'] == 1
        duplicated_entity = EntitiesManager.put(kind='teacher', data={'name': u'Manu', 'dni': 1234})
        assert duplicated_entity['status'] == 1062 and 'Duplicate entry' in duplicated_entity['log']

        # The same student is impossible:
        # Actually, because we don't have a unique identification for the student we don't use
        # any yet. So, is possible save two students if there are the same.

        # The same subject is impossible:
        entity = EntitiesManager.put(kind='subject', data={'name': u'Francés'})
        assert entity['status'] == 1062 and 'Duplicate entry' in entity['log']

        # The same class is impossible:
        entity = EntitiesManager.put(kind='class', data={'course': 1, 'word': u'B', 'level': u'ESO'})
        assert entity['status'] == 1062 and 'Duplicate entry' in entity['log']


        # The same association is impossible:
        entity = EntitiesManager.put(kind='association', data={'classId': 1, 'subjectId': 1})
        assert entity['status'] == 1062 and 'Duplicate entry' in entity['log']

        # The same impart is impossible:
        entity = EntitiesManager.put(kind='impart', data={'teacherId': 1, 'associationId': 1})
        assert entity['status'] == 1062 and 'Duplicate entry' in entity['log']

        # The same enrollment is impossible:
        entity = EntitiesManager.put(kind='enrollment', data={'studentId': 1, 'associationId': 1})
        assert entity['status'] == 1062 and 'Duplicate entry' in entity['log']

        # A association between a class with a subject that doesn't exists is impossible:
        entity = EntitiesManager.put(kind='association', data={'classId': 1, 'subjectId':2})
        errors =['foreign key constraint fails', ' REFERENCES `subject` (`subjectId`))']
        assert entity['status'] == 1452 and errors[0] in entity['log'] and errors[1] in entity['log']

        # The same but backwards.
        entity = EntitiesManager.put(kind='association', data={'classId': 2, 'subjectId': 1})
        errors = ['foreign key constraint fails', ' REFERENCES `class` (`classId`))']
        assert entity['status'] == 1452 and errors[0] in entity['log'] and errors[1] in entity['log']

        # A relation "impart" between a teacher with a association that doesn't exists is impossible:
        entity = EntitiesManager.put(kind='impart', data={'teacherId': 1, 'associationId': 24})
        errors = ['foreign key constraint fails', ' REFERENCES `association` (`associationId`))']
        assert entity['status'] == 1452 and errors[0] in entity['log'] and errors[1] in entity['log']

        # Backwards
        entity = EntitiesManager.put(kind='impart', data={'teacherId': 42, 'associationId': 1})
        errors = ['foreign key constraint fails', ' REFERENCES `teacher` (`teacherId`))']
        assert entity['status'] == 1452 and errors[0] in entity['log'] and errors[1] in entity['log']

        # A relation "enrollment" between a student with a association that doesn't exists is impossible:
        entity = EntitiesManager.put(kind='enrollment', data={'studentId': 1, 'associationId': 24})
        errors = ['foreign key constraint fails', ' REFERENCES `association` (`associationId`))']
        assert entity['status'] == 1452 and errors[0] in entity['log'] and errors[1] in entity['log']

        # Backwards
        entity = EntitiesManager.put(kind='enrollment', data={'studentId': 42, 'associationId': 1})
        errors = ['foreign key constraint fails', ' REFERENCES `student` (`studentId`))']
        assert entity['status'] == 1452 and errors[0] in entity['log'] and errors[1] in entity['log']

    def test_2_get(self):

        for item in tests:
            entity = EntitiesManager.put(kind=item['kind'], data=item['data'])
            assert entity['status'] == 1

        teachers = EntitiesManager.get(kind='teacher')['data']
        assert len(teachers) == 1
        assert teachers[0]['name'] == u'súperNombre'

        students = EntitiesManager.get(kind='student')['data']
        assert len(students) == 2
        assert students[0]['name'] == u'súperNombre'
        assert students[1]['name'] == u'Juan'

        classes = EntitiesManager.get(kind='class')['data']
        assert len(classes) == 1
        assert classes[0]['course'] == 1 and classes[0]['word'] == u'B' and classes[0]['level'] == u'ESO'

        subjects = EntitiesManager.get(kind='subject')['data']
        assert len(subjects) == 1
        assert subjects[0]['name'] == u'Francés'


        associations = EntitiesManager.get(kind='association')['data']
        assert len(associations) == 1
        assert associations[0]['classId'] == 1 and associations[0]['subjectId'] == 1

        imparts = EntitiesManager.get(kind='impart')['data']
        assert len(imparts) == 1
        assert imparts[0]['teacherId'] == 1 and imparts[0]['associationId'] == 1

        enrollments = EntitiesManager.get(kind='enrollment')['data']
        assert len(enrollments) == 1
        assert enrollments[0]['studentId'] == 1 and enrollments[0]['associationId'] == 1

        self.setup_method()  # Restart the database
        assert len(EntitiesManager.get(kind='student')['data']) == 0
        assert len(EntitiesManager.get(kind='teacher')['data']) == 0
        assert len(EntitiesManager.get(kind='class')['data']) == 0
        assert len(EntitiesManager.get(kind='subject')['data']) == 0
        assert len(EntitiesManager.get(kind='enrollment')['data']) == 0
        assert len(EntitiesManager.get(kind='impart')['data']) == 0

    def test_3_get_relateds(self):

        for item in tests:
            entity = EntitiesManager.put(kind=item['kind'], data=item['data'])
            assert entity['status'] == 1

        # TEACHERS

        # Students of a teacher.
        response = EntitiesManager.get_related(kind='teacher', entity_id=1, related_kind='student')
        assert response['status'] == 1 and len (response['data']) == 1
        assert response['data'][0]['name'] == u'súperNombre'

        # Classes of a teacher.
        response = EntitiesManager.get_related(kind='teacher', entity_id=1, related_kind='class')
        assert response['status'] == 1 and len(response['data']) == 1
        assert response['data'][0]['course'] == 1 and response['data'][0]['word'] == u'B'

        # Subject of a teacher.
        response = EntitiesManager.get_related(kind='teacher', entity_id=1, related_kind='subject')
        assert response['status'] == 1 and len(response['data']) == 1
        assert response['data'][0]['name'] == u'Francés'

        # Impart "special relations" of a teacher.
        response = EntitiesManager.get_related(kind='teacher', entity_id=1, related_kind='impart')
        assert response['status'] == 1 and len(response['data']) == 1

        assert len(response['data'][0]['classes']) == 1
        assert response['data'][0]['classes'][0]['classId'] == 1
        assert response['data'][0]['subject']['subjectId'] == 1
        assert response['data'][0]['subject']['name'] == u'Francés'

        # STUDENTS

        # Teachers of a student.
        response = EntitiesManager.get_related(kind='student', entity_id=1, related_kind='teacher')
        assert response['status'] == 1 and len(response['data']) == 1
        assert response['data'][0]['name'] == u'súperNombre'

        response = EntitiesManager.get_related(kind='student', entity_id=2, related_kind='teacher')
        assert response['status'] == 1 and len(response['data']) == 0

        # Classes of a student.
        response = EntitiesManager.get_related(kind='student', entity_id=1, related_kind='class')
        assert response['status'] == 1 and len(response['data']) == 1
        assert response['data'][0]['course'] == 1 and response['data'][0]['word'] == u'B'

        response = EntitiesManager.get_related(kind='student', entity_id=2, related_kind='class')
        assert response['status'] == 1 and len(response['data']) == 0

        # Subject of a student.
        response = EntitiesManager.get_related(kind='student', entity_id=1, related_kind='subject')
        assert response['status'] == 1 and len(response['data']) == 1
        assert response['data'][0]['name'] == u'Francés'

        response = EntitiesManager.get_related(kind='student', entity_id=2, related_kind='subject')
        assert response['status'] == 1 and len(response['data']) == 0

        # Enrollment "special relations" of a student.
        response = EntitiesManager.get_related(kind='student', entity_id=1, related_kind='enrollment')
        assert response['status'] == 1 and len(response['data']) == 1
        assert len(response['data']) == 1
        assert len(response['data'][0]['subjects']) == 1
        assert response['data'][0]['subjects'][0]['subjectId'] == 1
        assert response['data'][0]['class']['classId'] == 1
        assert response['data'][0]['class']['course'] == 1

        # CLASSES

        # Subjects "special relations" of a class.
        response = EntitiesManager.get_related(kind='class', entity_id=1, related_kind='subject')
        assert response['status'] == 1 and len(response['data']) == 1
        assert response['data'][0]['subject']['subjectName'] == u'Francés'
        assert len(response['data'][0]['teachers']) == 1
        assert response['data'][0]['teachers'][0]['teacherName'] == u'súperNombre'

        # Students of a class.
        response = EntitiesManager.get_related(kind='class', entity_id=1, related_kind='student')
        assert response['status'] == 1 and len(response['data']) == 1
        assert response['data'][0]['name'] == u'súperNombre'

        # Teachers of a class.
        response = EntitiesManager.get_related(kind='class', entity_id=1, related_kind='teacher')
        assert response['status'] == 1 and len(response['data']) == 1
        assert response['data'][0]['name'] == u'súperNombre'

        # SUBJECTS

        # Classes "special relations" of a subject.
        response = EntitiesManager.get_related(kind='subject', entity_id=1, related_kind='class')
        assert response['status'] == 1 and len(response['data']) == 1
        assert response['data'][0]['class']['course'] == 1
        assert len(response['data'][0]['teachers']) == 1
        assert response['data'][0]['teachers'][0]['name'] == u'súperNombre'

        # Students of a subject.
        response = EntitiesManager.get_related(kind='subject', entity_id=1, related_kind='student')
        assert response['status'] == 1 and len(response['data']) == 1
        assert response['data'][0]['name'] == u'súperNombre'

        # Teachers of a subject.
        response = EntitiesManager.get_related(kind='subject', entity_id=1, related_kind='teacher')
        assert response['status'] == 1 and len(response['data']) == 1
        assert response['data'][0]['name'] == u'súperNombre'

    def test_4_mod_entities(self):

        self.setup_method()

        for item in tests:
            entity = EntitiesManager.put(kind=item['kind'], data=item['data'])
            assert entity['status'] == 1

        result = EntitiesManager.update(kind='teacher', entity_id=1, data={'name': u'newName'})
        assert result['status'] == 1
        assert result['data']['name'] == u'newName'

        result = EntitiesManager.update(kind='student', entity_id=1, data={'name': u'newStudentName'})
        assert result['status'] == 1
        assert result['data']['name'] == u'newStudentName'

        result = EntitiesManager.update(kind='class', entity_id=1, data={'level': u'ESO'})
        assert result['status'] == 1
        assert result['data']['level'] == u'ESO'

        result = EntitiesManager.update(kind='subject', entity_id=1, data={'name': u'Science'})
        assert result['status'] == 1
        assert result['data']['name'] == u'Science'

        result = EntitiesManager.put(kind='subject', data={'name': 'Maths'})
        assert result['status'] == 1

        result = EntitiesManager.update(kind='association', entity_id=1, data={'subjectId': 2})
        assert result['status'] == 1
        assert result['data']['classId'] == 1 and result['data']['subjectId'] == 2

        result = EntitiesManager.put(kind='teacher', data={'name': 'Martin C.'})
        assert result['status'] == 1

        result = EntitiesManager.update(kind='impart', entity_id=1, data={'teacherId': 2})
        assert result['status'] == 1
        assert result['data']['teacherId'] == 2 and result['data']['associationId'] == 1

        result = EntitiesManager.update(kind='enrollment', entity_id=1, data={'studentId': 2})
        assert result['data']['studentId'] == 2 and result['data']['associationId'] == 1

        # Some errors:
        result = EntitiesManager.update(kind='enrollment', entity_id=1, data={'studentId': 432})
        errors = ['foreign key constraint fails', ' REFERENCES `student` (`studentId`))']
        assert result['status'] == 1452 and errors[0] in result['log'] and errors[1] in result['log']

    def test_5_del_entities(self):

        self.setup_method()

        for item in tests:
            entity = EntitiesManager.put(kind=item['kind'], data=item['data'])
            assert entity['status'] == 1

        # Is checked the special cases when we can't introduce a new item if it is repeated
        # but yes when it's deleted:

        # 1. We insert a new teacher with UNIQUE value DNI=1
        result = EntitiesManager.put(kind='teacher', data={'dni': 1})
        assert result['status'] == 1

        # 2. The same item again give an error:
        result = EntitiesManager.put(kind='teacher', data={'dni': 1})
        assert result['status'] == 1062 and 'Duplicate entry' in result['log']

        # 3. But if we delete last element inserted:
        result = EntitiesManager.delete(kind='teacher', entity_id=2)
        assert result['status'] == 1 and result['log'] == None and result['data'] == None

        # we can insert again the same item without error
        result = EntitiesManager.put(kind='teacher', data={'dni': 1})
        assert result['status'] == 1

        result = EntitiesManager.get(kind='teacher')
        assert len(result['data']) == 2

        # although we have three elements in the db
    """