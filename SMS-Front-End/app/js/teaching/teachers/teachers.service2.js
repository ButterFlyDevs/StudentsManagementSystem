angular.module('teachers')
    .factory("Post",
        function($resource) {

         return $resource('http://jsonplaceholder.typicode.com/users', {}, {
            get:    {method: 'GET'}
        });


});