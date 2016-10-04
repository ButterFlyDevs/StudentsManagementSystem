

angular.module('teachers')
    .controller('teachersListController',function($scope, Post){

            var vm = this;
            vm.text='hi';

            activate();

            ///////////////////////////////////////////////////////////
            function activate() {
                console.log('Activating teachersListController controller.')

                var teacherList = Post.query({}, function(){
                    console.log(teacherList)
                })

                var singleTeacher = Post.get({id: 2}, function(){
                    console.log(singleTeacher)
                })

            }

});

//angular.module('teachers').controller('teachersListController', ['$scope', function($scope) {}]);
