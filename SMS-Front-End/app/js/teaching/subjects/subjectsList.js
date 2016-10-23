angular.module('subjects')
    .controller('subjectsListController',function($scope, $mdDialog, SubjectsService){

            var vm = this;

            vm.defaultAvatar = 'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcThQiJ2fHMyU37Z0NCgLVwgv46BHfuTApr973sY7mao_C8Hx_CDPrq02g'
            vm.openNewSubjectDialog = openNewSubjectDialog;

            activate();

            ///////////////////////////////////////////////////////////
            function activate() {
                console.log('Activating subjectsListController controller.')

                vm.subjectsList = SubjectsService.query({}, function(){
                    console.log(vm.subjectsList)
                }, function(){
                    console.log('Any problem found when was retrieved the subjects list.')
                })

            }

            function openNewSubjectDialog(){
                console.log('Open new Subject Dialog')

                $mdDialog.show({
                    locals: {parentScope: $scope, parentController: vm},
                    controller: 'newSubjectDialogController',
                    controllerAs: 'vm',
                    templateUrl: 'app/views/teaching/subjects/newSubjectDialog.html'
                })
                    .then(function () {

                    }, function () {

                    });
            }



});
