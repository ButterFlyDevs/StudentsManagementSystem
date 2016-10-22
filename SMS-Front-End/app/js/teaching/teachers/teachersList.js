

angular.module('teachers')
    .controller('teachersListController',function($scope, $mdDialog, TeachersService){

            var vm = this;
            vm.text='hiteach';

            vm.defaultAvatar = 'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcThQiJ2fHMyU37Z0NCgLVwgv46BHfuTApr973sY7mao_C8Hx_CDPrq02g'
            vm.openNewTeacherDialog = openNewTeacherDialog;


            activate();

            ///////////////////////////////////////////////////////////
            function activate() {
                console.log('Activating teachersListController controller.')

                vm.teachersList = TeachersService.query({}, function(){
                    console.log(vm.teachersList)
                }, function(){
                    console.log('Any problem found when was retrieved the teachers list.')
                })

            }

            function openNewTeacherDialog(){
                console.log('Open new Teacher Dialog')

                $mdDialog.show({
                    locals: {parentScope: $scope, parentController: vm},
                    controller: 'newTeacherDialogController',
                    controllerAs: 'vm',
                    templateUrl: 'app/views/teaching/teachers/newTeacherDialog.html'
                })
                    .then(function () {

                    }, function () {

                    });
            }



});

//angular.module('teachers').controller('teachersListController', ['$scope', function($scope) {}]);
