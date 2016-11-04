angular.module('subjects')
    .controller('subjectsProfileController',function($scope, $resource, $state, $stateParams, $mdDialog, SubjectsService, toastService){

            var vm = this;

            vm.subjectId = $stateParams.subjectId

            // Functions associations
            //vm.addRelation = addRelation;

            vm.updateSubject = updateSubject;
            vm.showDeleteSubjectConfirm = showDeleteSubjectConfirm


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


            function deleteSubject(){

                vm.subject.$delete(function(){
                            console.log('Subject deleted successfully.')
                            $state.go('subjects')
                            toastService.showToast('Asignatura eliminada.')

                        },
                        function(){
                            console.log('Subject deleted process fail.')
                        });

            }

            function showDeleteSubjectConfirm() {

                var confirm = $mdDialog.confirm()
                .title('¿Está seguro de que quiere eliminar esta asignatura?')
                //.textContent('If you do, you will be erased from all project which you are and you can not access to app.')
                //.ariaLabel('Lucky day')
                .ok('Estoy seguro')
                .cancel('Cancelar');

                $mdDialog.show(confirm).then(function () {
                    deleteSubject();
                    }, function () {
                        console.log('Operacion cancelada.')
                });

            };


            function updateSubject(){

                 vm.subject.$update(function(){
                    console.log('Subject saved successfully.')
                    }, function(error){
                        console.log('Error saving subject.')
                        console.log(error)
                    });

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
