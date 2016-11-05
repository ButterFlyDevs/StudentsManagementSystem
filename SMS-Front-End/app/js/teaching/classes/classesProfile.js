angular.module('classes')
    .controller('classesProfileController', function ($scope, $resource, $state, $stateParams, $mdDialog, ClassesService, toastService) {

        var vm = this;

        vm.classId = $stateParams.classId

        console.log(vm.classId)

        // References to functions.
        vm.updateClass = updateClass;
        vm.showDeleteClassConfirm = showDeleteClassConfirm
        //vm.addRelation = addRelation;

        vm.defaultAvatar = 'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcThQiJ2fHMyU37Z0NCgLVwgv46BHfuTApr973sY7mao_C8Hx_CDPrq02g'


        vm.class = ClassesService.get({id: vm.classId}, function () {
            console.log(vm.class)

        }, function () {
            console.log('Class not found')
            vm.student = null;
        })


        activate();

        ///////////////////////////////////////////////////////////
        function activate() {
            console.log('Activating classesProfileController controller.')

        }

        /** Delete class in server.
         * Call to server with DELETE method ($delete= DELETE) using vm.class that is
         * a instance of ClassesService.*/
        function deleteClass() {

            vm.class.$delete(
                function(){ // Success
                    console.log('Class deleted successfully.')
                    $state.go('classes')
                    toastService.showToast('Clase eliminada con éxito.')
                },
                function(error){ // Fail
                    console.log('Class deleted process fail.')
                    console.log(error)
                    toastService.showToast('Error eliminando la clase.')
                });

        }

        /** Show the previous step to delete item, a confirm message */
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


        /** Update class data in server.
         * Call to server with PUT method ($update = PUT) using vm.class that is
         * a instance of ClassesService.*/
        function updateClass() {
            console.log('Calling updateClass() function.')
            vm.class.$update(
                function () { // Success
                    console.log('Class updated successfully.')
                    toastService.showToast('Clase actualizada con éxito.')
                },
                function (error) { // Fail
                    console.log('Error updating class.')
                    console.log(error)
                    toastService.showToast('Error actualizando la clase.')
                });
        }


    });
