angular.module('enrollments')
    .factory("EnrollmentsService",
        function($resource, globalService) {

         var restPath = 'http://'+globalService.defaultMicroServicesURL+'/entities/enrollment/';

         return $resource(restPath + ':id', {}, {
                 'multiple_save': {
                     method: 'POST', isArray: true
                 }
             }
             );

        });
