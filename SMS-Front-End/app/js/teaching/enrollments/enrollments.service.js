angular.module('enrollments')
    .factory("EnrollmentsService",
        function($resource) {

         var restPath = 'http://localhost:8001/entities/enrollment/';

         return $resource(restPath + ':id', {}, {
                 'multiple_save': {
                     method: 'POST', isArray: true
                 }
             }
             );

        });
