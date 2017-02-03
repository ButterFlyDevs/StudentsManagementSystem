angular.module('imparts')
    .factory("ImpartsService",
        function($resource, globalService) {

         var restPath = 'http://'+globalService.defaultMicroServicesURL+'/entities/impart/';

         return $resource(restPath + ':id');

        });
