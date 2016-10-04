angular.module('teachers')
    .factory("TeachersService",
        function($resource) {

         return $resource('http://localhost:8001/entities/teacher/'+ ':id', {
            id: '@_id'
        });

        /* Default behaviour:

            { 'get':    {method:'GET'},
            'save':   {method:'POST'},
            'query':  {method:'GET', isArray:true},
            'remove': {method:'DELETE'},
            'delete': {method:'DELETE'} };

            Examples of use:
            var teacherList = Post.query({}, function(){
                    console.log(teacherList)
                })

            var singleTeacher = Post.get({id: 2}, function(){
                console.log(singleTeacher)
            })



         */

});