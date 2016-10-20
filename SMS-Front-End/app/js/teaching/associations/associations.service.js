angular.module('associations')
    .factory("AssociationsService",
        function($resource) {
         var restPath = 'http://localhost:8001/entities/association/';
         return $resource(restPath + ':id', {id: '@_id'}, {});
        });
