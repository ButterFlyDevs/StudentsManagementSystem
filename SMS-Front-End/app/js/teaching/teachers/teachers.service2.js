angular.module('teachers')
    .factory("Post",
        function($resource) {

         return $resource('http://localhost:8001/entities/teacher/:id', {}, {
            get:    {method: 'GET'}
        });


});