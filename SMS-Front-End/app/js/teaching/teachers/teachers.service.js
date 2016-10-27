angular.module('teachers')
    .factory("TeachersService",
        function($resource) {

         var restPath = 'http://localhost:8001/entities/teacher/';

         return $resource(restPath + ':id', {id: '@_id'}, {
             'getSubjects': {
                 method: 'GET',
                 url: restPath + ':id' + '/subject',
                 isArray: true
             },
             'getClasses': {
                 method: 'GET',
                 url: restPath + ':id' + '/class',
                 isArray: true
             },
             'update': {
                 method: 'PUT' // this method issues a PUT request
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
