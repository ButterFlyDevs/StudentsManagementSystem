angular.module('discipline')
    .factory("DisciplineService",
        function ($resource, globalService) {
            var restPath = 'http://'+globalService.defaultMicroServicesURL + '/disciplinarynote/';
            return $resource(restPath + ':id', {id: '@disciplinaryNoteId'}, {
                'getAll': {
                    method: 'GET',
                    url: restPath,
                    isArray: true
                }
            });
     });
