angular.module('discipline')
    .factory("disciplineService",
        function ($resource, globalService) {
            var restPath = 'http://'+globalService.defaultMicroServicesURL + '/disciplinarynotes/';
            return $resource(restPath + ':id', {id: '@acId'}, {
                'getAll': {
                    method: 'GET',
                    url: restPath,
                    isArray: true
                }
            });
     });
