angular.module('classes')
    .factory("ClassesService",
        function($resource) {

         var restPath = 'http://localhost:8001/entities/class/';

         return $resource(restPath + ':id', {id: '@_id'}, {
             'getSubjects': {
                 method: 'GET',
                 url: restPath + ':id' + '/subject',
                 isArray: true
             }});

        });
