angular.module('marks')
    .factory("MarksService",
        function ($resource, globalService) {

            var restPath = 'http://'+globalService.defaultMicroServicesURL + '/mark/';

            // The second param is [paramDefaults] to pass param to URL
            return $resource(restPath + ':id', {id: '@markId'}, {

                'getAll': {
                    method: 'GET',
                    url: restPath,
                    isArray: true
                },
                'update': {method: 'PUT'},
                'getBase': {
                    method: 'GET',
                    url: restPath + 'base/' + ':id'
                },
                'getByEnrollmentId':{
                    method: 'GET',
                    url: restPath.slice(0, -1) + '?enrollmentId=' + ':enrollmentId'
                }
            });
     });
