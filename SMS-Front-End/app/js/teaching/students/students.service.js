angular.module('students')
    .factory("StudentsService",
        function ($resource, globalService) {

            var restPath = 'http://'+globalService.defaultMicroServicesURL+'/entities/student/';

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
                'delete': {
                    method: 'DELETE',
                    url: restPath + ':id' + '?action=dd' // Delete dependencies also.
                },
                'getTeaching': {
                    method: 'GET',
                    url: restPath + ':id' + '/teaching',
                    isArray: true
                },
                'getClasses': {
                    method: 'GET',
                    url: restPath + ':id' + '/class',
                    isArray: true
                },
                'getTeachers': {
                    method: 'GET',
                    url: restPath + ':id' + '/teacher',
                    isArray: true
                }
            });
        });
