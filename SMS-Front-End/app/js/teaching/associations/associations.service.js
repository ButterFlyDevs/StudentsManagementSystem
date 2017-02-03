angular.module('associations')
    .factory("AssociationsService",
        function ($resource, globalService) {
            var restPath = 'http://'+globalService.defaultMicroServicesURL+'/entities/association/';
            return $resource(restPath + ':id', {id: '@_id'}, {

                'delete': {
                    method: 'DELETE',
                    url: restPath + ':id' + '?action=dd' // Delete dependencies also by default.
                },
                'getStudents': {
                    method: 'GET',
                    url: restPath + ':id' + '/student',
                    isArray: true
                }
            });
        });
