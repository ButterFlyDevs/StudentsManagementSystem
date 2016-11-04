angular.module('classes')
    .controller('classesProfileController',function($scope, $resource, $state, $stateParams, $mdDialog, ClassesService, toastService){

            var vm = this;

            vm.classId = $stateParams.classId

            console.log(vm.classId)

            // Functions associations

            vm.updateClass = updateClass;
            vm.showDeleteClassConfirm = showDeleteClassConfirm


            //vm.addRelation = addRelation;

            vm.defaultAvatar = 'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcThQiJ2fHMyU37Z0NCgLVwgv46BHfuTApr973sY7mao_C8Hx_CDPrq02g'


            vm.class = ClassesService.get({id: vm.classId}, function(){
                console.log(vm.class)

            }, function(){
                console.log('Class not found')
                vm.student = null;
            })


            activate();

            ///////////////////////////////////////////////////////////
            function activate() {
                console.log('Activating classesProfileController controller.')

            }

            function deleteClass(){

                vm.class.$delete(function(){
                            console.log('Class deleted successfully.')
                            $state.go('classes')
                            toastService.showToast('Grupo eliminada.')

                        },
                        function(){
                            console.log('Class deleted process fail.')
                        });

            }

            function showDeleteClassConfirm() {

                var confirm = $mdDialog.confirm()
                .title('¿Está seguro de que quiere eliminar este grupo?')
                //.textContent('Si lo hace todos los alumnos quedarán ')
                //.ariaLabel('Lucky day')
                .ok('Estoy seguro')
                .cancel('Cancelar');

                $mdDialog.show(confirm).then(function () {
                    deleteClass();
                    }, function () {
                        console.log('Operacion cancelada.')
                });

            };



            function updateClass(){

                 vm.class.$update(function(){
                    console.log('Class saved successfully.')
                    }, function(error){
                        console.log('Error saving class.')
                        console.log(error)
                    });

            }



});
