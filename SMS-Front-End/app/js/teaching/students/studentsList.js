

angular.module('students')
    .controller('studentsListController',function($scope, $mdDialog, StudentsService){

            var vm = this;

            vm.defaultAvatar = 'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcThQiJ2fHMyU37Z0NCgLVwgv46BHfuTApr973sY7mao_C8Hx_CDPrq02g'
            vm.openNewStudentDialog = openNewStudentDialog;

            activate();

            ///////////////////////////////////////////////////////////
            function activate() {
                console.log('Activating studentsListController controller.')

                vm.studentsList = StudentsService.query({}, function(){
                    console.log(vm.studentsList)
                }, function(){
                    console.log('Any problem found when was retrieved the student list.')
                })

            }

            function openNewStudentDialog(){
                console.log('Open new Student Dialog')

                $mdDialog.show({
                    locals: {parentScope: $scope, parentController: vm},
                    controller: 'newStudentDialogController',
                    controllerAs: 'vm',
                    templateUrl: 'app/views/teaching/students/newStudentDialog.html'
                })
                    .then(function () {

                    }, function () {

                    });
            }



});

//angular.module('teachers').controller('teachersListController', ['$scope', function($scope) {}]);
