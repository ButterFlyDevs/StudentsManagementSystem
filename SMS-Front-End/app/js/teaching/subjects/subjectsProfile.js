angular.module('subjects')
    .controller('subjectsProfileController',function($scope, $resource, $stateParams, $mdDialog, SubjectsService){

            var vm = this;

            vm.subjectId = $stateParams.subjectId

            // Functions associations
            //vm.addRelation = addRelation;

            vm.defaultAvatar = 'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcThQiJ2fHMyU37Z0NCgLVwgv46BHfuTApr973sY7mao_C8Hx_CDPrq02g'


            vm.subject = SubjectsService.get({id: vm.subjectId}, function(){
                console.log(vm.subject)

            }, function(){
                console.log('Subject not found')
                vm.subject = null;
            })


            activate();

            ///////////////////////////////////////////////////////////
            function activate() {
                console.log('Activating subjectsProfileController controller.')

            }



            /**
             * Open the dialog to add a relation to this teacher.
             * The add action is done in addUserToProjectController

            function addRelation() {

                $mdDialog.show({
                    locals: {parentScope: $scope, parentController: vm},
                    controller: 'addRelationController',
                    controllerAs: 'vm',
                    templateUrl: 'app/views/teaching/utils/addRelationTemplate.html'
                })
                    .then(function () {

                    }, function () {

                    });
            }*/



});
