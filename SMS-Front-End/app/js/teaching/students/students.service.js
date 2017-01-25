angular.module('students')
    .factory("StudentsService",
        function ($resource) {

            var restPath = 'http://localhost:8001/entities/student/';

            return $resource(restPath + ':id', {id: '@studentId'}, {
                'getSubjects': {
                    method: 'GET',
                    url: restPath + ':id' + '/subject',
                    isArray: true
                },
                'getEnrollments': {
                    method: 'GET',
                    url: restPath + ':id' + '/enrollment',
                    isArray: true
                },
                'update': {method: 'PUT'},
                'getTeaching': {
                    method: 'GET',
                    url: restPath + ':id' + '/teaching',
                    isArray: true
                },
                'getClasses': {
                    method: 'GET',
                    url: restPath + ':id' + '/class',
                    isArray: true
                }
            });
        });
