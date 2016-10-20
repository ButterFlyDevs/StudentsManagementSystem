angular.module('imparts')
    .factory("ImpartsService",
        function($resource) {
         console.log('here')
         var restPath = 'http://localhost:8001/entities/impart';
         return $resource(restPath + ':id');
        });
