angular.module('subjects')
    .controller('subjectsProfileController', function ($scope, $resource, $state, $stateParams, $mdDialog, SubjectsService, toastService) {

        var vm = this;

        vm.controllerName = 'subjectsProfileController';

        vm.subjectId = $stateParams.subjectId

        // References to functions.
        vm.updateSubject = updateSubject;
        vm.showDeleteSubjectConfirm = showDeleteSubjectConfirm

        vm.showDeleteSubjectClassImpartConfirm = showDeleteSubjectClassImpartConfirm

        vm.addRelation = addRelation;

        vm.defaultAvatar = 'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcThQiJ2fHMyU37Z0NCgLVwgv46BHfuTApr973sY7mao_C8Hx_CDPrq02g'


        activate();

        ///////////////////////////////////////////////////////////
        function activate() {
            console.log('Activating subjectsProfileController controller.')
            loadData()

        }

        function loadData() {
            vm.subject = SubjectsService.get({id: vm.subjectId}, function () {
                console.log(vm.subject)

            }, function () {
                console.log('Subject not found')
                vm.subject = null;
            })

            vm.subjectClasses = SubjectsService.getClasses({id: vm.subjectId},
                function () {
                    console.log('Subject Classes')
                    console.log(vm.subjectClasses)

                    // ### Do a copy to save process. ###
                    vm.subjectClassesOriginalCopy = angular.copy(vm.subjectClasses);

                    $scope.subjectClassesModelHasChanged = false;

                    $scope.$watch('vm.subjectClasses', function (newValue, oldValue) {
                        if (newValue != oldValue) {
                            $scope.subjectClassesModelHasChanged = !angular.equals(vm.subjectClasses, vm.subjectClassesOriginalCopy);
                        }
                        compare()
                    }, true);

                }, function (error) {
                    console.log('Get subject classes process fail.')
                    console.log(error)
                    toastService.showToast('Error obteniendo las clases donde se imparte la asignatura.')
                }
            )

        }

        function compare() {
            if ($scope.subjectModelHasChanged || $scope.subjectClassesModelHasChanged) {
                vm.updateButtonEnable = true;
            } else {
                vm.updateButtonEnable = false;
            }
        }



        /** Delete subject in server.
         * Call to server with DELETE method ($delete= DELETE) using vm.subject that is
         * a instance of SubjectsService.*/
        function deleteSubject() {

            vm.subject.$delete(
                function () { // Success
                    console.log('Subject deleted successfully.')
                    $state.go('subjects')
                    toastService.showToast('Asignatura eliminada con éxito.')
                },
                function (error) { // Fail
                    console.log('Subject deleted process fail.')
                    console.log(error)
                    toastService.showToast('Error eliminando la asignatura.')
                });

        }

        /** Show the previous step to delete item, a confirm message */
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


        function deleteSubjectClassImpart(classId, teacherId){

            // We need delete from data block copy the item selected:
            for (var i = 0; i < vm.subjectClasses.length; i++)
                if (vm.subjectClasses[i].class.classId == classId) {
                    var numTeachers = vm.subjectClasses[i].teachers.length;
                    if (numTeachers == 1)
                        vm.subjectClasses.splice(i, 1);
                    else{
                        var classIndex = -1;
                        for (var j = 0; j < numTeachers; j++)
                            if (vm.subjectClasses[i].teachers[j].teacherId == teacherId)
                                classIndex = j;
                        vm.subjectClasses[i].teachers.splice(classIndex, 1);
                    }
                }
        }


        /** Show the previous step to delete item, a confirm message */
        function showDeleteSubjectClassImpartConfirm(classId, teacherId) {

            var confirm = $mdDialog.confirm()
                .title('¿Está seguro de que quiere eliminar al profesor de la asignatura?')
                //.textContent('If you do, you will be erased from all project which you are and you can not access to app.')
                //.ariaLabel('Lucky day')
                .ok('Estoy seguro')
                .cancel('Cancelar');

            $mdDialog.show(confirm).then(
                function () {
                    deleteSubjectClassImpart(classId, teacherId);
                },
                function () {
                    console.log('Del teacher from class relation operation canceled.')
                }
            );
        };





        /** Update subject data in server.
         * Call to server with PUT method ($update = PUT) using vm.subject that is
         * a instance of SubjectsService.*/
        function updateSubject() {
            console.log('Calling updateSubject() function.')
            vm.subject.$update(
                function () { // Success
                    console.log('Subject saved successfully.')
                    toastService.showToast('Asignatura actualizada con éxito.')
                },
                function (error) { // Fail
                    console.log('Error saving subject.')
                    console.log(error)
                    toastService.showToast('Error actualizando la asignatura.')
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
