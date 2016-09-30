

angular.module('teachers')
    .controller('teachersListController',function($scope, Calculator, $resource, Post){

            var vm = this;
            vm.text='hi';

            activate();

            ///////////////////////////////////////////////////////////
            function activate() {
                console.log('Activating teachersListController controller.')

                console.log(Calculator.square(4));

                /*
                var user = Post.get( function(){
                    console.log(user);
                }, function(){
                    console.log(user);
                }  )

                console.log(user);
                */

                /*

                Post.get()
                .then(function (response) {
                    console.log(response)
                })
                .then(function (response) {
                    // (avoid putting a [then] inside another [then] unless you need to)
                    console.log("A: response", response);
                    console.log("response.data", response.data);
                    return response.data;
                });
                */


                var teacher = $resource('http://localhost:8001/entities/teacher/:id');

                teacher.get({id: 1}).$promise.then(function(teacher) {
                   // success
                   $scope.teacher = teacher;

                }, function(errResponse) {
                   // fail
                   console.log('fail')
                   console.log(errResponse)
                });







            }

});

//angular.module('teachers').controller('teachersListController', ['$scope', function($scope) {}]);
