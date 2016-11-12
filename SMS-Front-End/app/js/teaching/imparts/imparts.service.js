angular.module('imparts')
    .factory("ImpartsService",
        function($resource) {

         var restPath = 'http://localhost:8001/entities/impart/';

         return $resource(restPath + ':id');

        });
