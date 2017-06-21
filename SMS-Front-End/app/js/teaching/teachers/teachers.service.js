angular.module('teachers')
    .factory("TeachersService",
        function ($resource, globalService) {

            var restPath = 'http://'+globalService.defaultMicroServicesURL+'/entities/teacher/';


            // The second param is [paramDefaults] to pass param to URL
            return $resource(restPath + ':id', {id: '@teacherId'}, {

                'getSubjects': {
                    method: 'GET',
                    url: restPath + ':id' + '/subject',
                    isArray: true
                },
                'getImparts': {
                    method: 'GET',
                    url: restPath + ':id' + '/teaching',
                    isArray: true
                },
                'update': {
                    method: 'PUT'
                },
                'getReport': {
                    method: 'GET',
                    url: restPath + ':id' + '/report'
                },
                'delete': {
                    method: 'DELETE',
                    url: restPath + ':id' + '?action=dd' // Delete dependencies also.
                },
                'getTeaching': {
                    method: 'GET',
                    url: restPath + ':id' + '/teaching',
                    isArray: true
                },
                'getClasses': {
                    method: 'GET',
                    url: restPath + ':id' + '/class',
                    isArray: true
                },
                'getStudents': {
                    method: 'GET',
                    url: restPath + ':id' + '/student',
                    isArray: true
                },
                'getStudentsFromSubject': {
                    method: 'GET',
                    url: restPath + ':id' + '/subject/' + ':idSubject' + '/student',
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
