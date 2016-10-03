

angular.module('teachers')
    .controller('teachersListController',function($scope, $http, Calculator, $resource, Post){

            var vm = this;
            vm.text='hi';

            activate();

            ///////////////////////////////////////////////////////////
            function activate() {
                console.log('Activating teachersListController controller.')

                console.log(Calculator.square(4));







                /*
                var postUsers = $http.get('http://localhost:8001/entities/teacher/1')
                postUsers.then(function(result) {
                    vm.users = result.data;
                    console.log(vm.users);
                });
                */

                /*
                // var postUsers = $http.get('http://localhost:8002/entities/teacher')
                var postUsers = $http.get('http://jsonplaceholder.typicode.com/users')
                postUsers.then(function(result) {
                    vm.users = result.data;
                    console.log(result.data)
                    console.log(result.status)
                    console.log(result.headers)
                    console.log(result.config)
                    console.log(vm.users);
                });
                console.log(postUsers);
                */

                var postUsers = $http.get('http://localhost:8002/entities/teacher')
                //var postUsers = $http.get('http://jsonplaceholder.typicode.com/users')
                postUsers.then(function(result) {
                    vm.users = result.data;
                    console.log(result.data)
                    console.log(result.status)
                    console.log(result.headers)
                    console.log(result.config)
                    console.log(vm.users);
                });
                console.log(postUsers);






                /*

                var teacher = $resource('http://localhost:8001/entities/teacher/:id');

                teacher.get({id: 1}).$promise.then(function(response) {
                   // success
                   $scope.teacher = response.data.teacher;

                }, function(errResponse) {
                   // fail
                   console.log('fail')
                   console.log(errResponse)
                });

                */





            }

});

//angular.module('teachers').controller('teachersListController', ['$scope', function($scope) {}]);
