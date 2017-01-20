angular.module('subjects')
    .factory("SubjectsService",
        function ($resource) {

            var restPath = 'http://localhost:8001/entities/subject/';

            return $resource(restPath + ':id', {id: '@subjectId'}, {
                'getTeachers': {
                    method: 'GET',
                    url: restPath + ':id' + '/teacher',
                    isArray: true
                },
                'getReport': {
                    method: 'GET',
                    url: restPath + ':id' + '/report'
                },
                'update': {method: 'PUT'},
                'delete': {
                    method: 'DELETE',
                    url: restPath + ':id' + '?action=dd' // Delete dependencies also.
                },
                'nested_delete': {
                    method: 'DELETE',
                    url: restPath + ':id/:a/:b'  // Example: /entities/subject/1/student/1
                },
                'getTeaching': {
                    method: 'GET',
                    url: restPath + ':id' + '/teaching',
                    isArray: true
                },
                'getStudents': {
                    method: 'GET',
                    url: restPath + ':id' + '/student',
                    isArray: true
                },
            });

        });
