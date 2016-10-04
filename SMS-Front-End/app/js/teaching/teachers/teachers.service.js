angular.module('teachers')
    .factory("Post",
        function($resource) {

         return $resource('http://localhost:8002/entities/teacher/'+ ':id', {
            id: '@_id'
        });

        /* Default behaviour:

            { 'get':    {method:'GET'},
            'save':   {method:'POST'},
            'query':  {method:'GET', isArray:true},
            'remove': {method:'DELETE'},
            'delete': {method:'DELETE'} };

         */

});