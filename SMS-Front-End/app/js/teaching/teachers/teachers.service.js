angular.module('teachers')
    .factory("TeachersService",
        function($resource) {

         var restPath = 'http://localhost:8001/entities/teacher/';


         // The second param is [paramDefaults] to pass param to URL
         return $resource(restPath + ':id', {id: '@teacherId'}, {

             'getSubjects': {
                 method: 'GET',
                 url: restPath + ':id' + '/subject',
                 isArray: true
             },
             'getImparts': {
                 method: 'GET',
                 url: restPath + ':id' + '/imparts',
                 isArray: true
             },
             'update': {
                method: 'PUT'
             },
             'getClasses': {
                 method: 'GET',
                 url: restPath + ':id' + '/class',
                 isArray: true
             }

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
