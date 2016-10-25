angular.module('classes')
    .controller('classesListController',function($scope, $mdDialog, ClassesService){

            var vm = this;

            vm.defaultAvatar = 'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcThQiJ2fHMyU37Z0NCgLVwgv46BHfuTApr973sY7mao_C8Hx_CDPrq02g'
            vm.openNewClassDialog = openNewClassDialog;

            activate();

            ///////////////////////////////////////////////////////////
            function activate() {
                console.log('Activating classesListController controller.')

                vm.classesList = ClassesService.query({}, function(){
                    console.log(vm.classesList)
                }, function(){
                    console.log('Any problem found when was retrieved the classes list.')
                })

            }

            function openNewClassDialog(){
                console.log('Open new Class Dialog')

                $mdDialog.show({
                    locals: {parentScope: $scope, parentController: vm},
                    controller: 'newClassDialogController',
                    controllerAs: 'vm',
                    templateUrl: 'app/views/teaching/classes/newClassDialog.html'
                })
                    .then(function () {

                    }, function () {

                    });
            }



});
