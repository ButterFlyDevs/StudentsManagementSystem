angular.module('associations')
    .factory("AssociationsService",
        function ($resource) {
            var restPath = 'http://localhost:8001/entities/association/';
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
