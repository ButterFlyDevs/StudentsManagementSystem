angular.module('classes')
    .controller('classesProfileController', function ($scope, $resource, $state, $stateParams, $mdDialog, ClassesService, toastService) {

        var vm = this;

        // Vars:
        vm.controllerName = 'classesProfileController';
        vm.classId = $stateParams.classId;
        vm.updateButtonEnable = false; // To control when the update button could be enabled.
        vm.defaultAvatar = 'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcThQiJ2fHMyU37Z0NCgLVwgv46BHfuTApr973sY7mao_C8Hx_CDPrq02g'

        // References to functions.
        vm.updateClass = updateClass;
        vm.showDeleteClassConfirm = showDeleteClassConfirm;
        vm.addRelation = addRelation;




        activate();

        ///////////////////////////////////////////////////////////
        function activate() {
            console.log('Activating classesProfileController controller.')
            loadData();

        }


        function loadData() {

            // Retrieve all data from this class
            vm.class = ClassesService.get({id: vm.classId}, function () {
                console.log(vm.class);

                // ### Do a copy to save process. ###
                vm.classOriginalCopy = angular.copy(vm.class);

                $scope.classModelHasChanged = false;
                $scope.$watch('vm.class', function (newValue, oldValue) {
                    if (newValue != oldValue) {
                        $scope.classModelHasChanged = !angular.equals(vm.class, vm.classOriginalCopy);
                    }
                    compare();
                }, true);


            }, function (error) {
                console.log('Get class process fail.');
                console.log(error);
                vm.class = null;
            });


            vm.classStudents = ClassesService.getStudents({id: vm.classId},
                function(){
                    console.log('Class Students');
                    console.log(vm.classStudents);
                },
                function (error) {
                    console.log('Get class students process fail.');
                    console.log(error);
                    toastService.showToast('Error obteniendo los alumnos inscritos a este grupo.');
                }
            );


            vm.classSubjects = ClassesService.getSubjects({id: vm.classId},
                function () {
                    console.log('Class Subjects');
                    console.log(vm.classSubjects);

                    // ### Do a copy to save process. ###
                    vm.classSubjectsOriginalCopy = angular.copy(vm.classSubjects);

                    $scope.classSubjectsModelHasChanged = false;

                    $scope.$watch('vm.classSubjects', function (newValue, oldValue) {
                        if (newValue != oldValue) {
                            $scope.classSubjectsModelHasChanged = !angular.equals(vm.classSubjects, vm.classSubjectsOriginalCopy);
                        }
                        compare()
                    }, true);

                }, function (error) {
                    console.log('Get class subjects process fail.')
                    console.log(error)
                    toastService.showToast('Error obteniendo las asignaturas que se imparten en la clase.')
                }
            )

        }

        function compare() {
            if ($scope.classModelHasChanged || $scope.classSubjectsModelHasChanged) {
                vm.updateButtonEnable = true;
            } else {
                vm.updateButtonEnable = false;
            }
        }

        /** Delete class in server.
         * Call to server with DELETE method ($delete= DELETE) using vm.class that is
         * a instance of ClassesService.*/
        function deleteClass() {

            vm.class.$delete(
                function () { // Success
                    console.log('Class deleted successfully.')
                    $state.go('classes')
                    toastService.showToast('Clase eliminada con éxito.')
                },
                function (error) { // Fail
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


        /*
         * Open the dialog to add a relation to this teacher.
         * The add action is done in addUserToProjectController
         */
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
        }

    });
