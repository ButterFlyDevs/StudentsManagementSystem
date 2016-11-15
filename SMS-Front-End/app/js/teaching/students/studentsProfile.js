angular.module('students')
    .controller('studentsProfileController', function ($scope, $resource, $state, $stateParams, $mdDialog, StudentsService, toastService, globalService) {

        var vm = this;

        vm.studentId = $stateParams.studentId

        // References to functions.
        vm.updateStudent = updateStudent;
        vm.showDeleteStudentConfirm = showDeleteStudentConfirm;
        vm.showDeleteStudentEnrollmentConfirm = showDeleteStudentEnrollmentConfirm;
        vm.openMenu = openMenu

        vm.defaultAvatar = globalService.defaultAvatar;



        vm.student = StudentsService.get({id: vm.studentId}, function () {
            console.log(vm.student)
            var parts = vm.student.birthdate.split('-');
            var tmpDateObject = new Date(parts[0], parts[1] - 1, parts[2]);
            vm.student.birthdate = tmpDateObject;


            // ### Do a copy to save process. ###
            vm.studentOriginalCopy = angular.copy(vm.student);
            $scope.studentModelHasChanged = false;
            $scope.$watch('vm.student', function (newValue, oldValue) {
                if (newValue != oldValue) {
                    $scope.studentModelHasChanged = !angular.equals(vm.student, vm.studentOriginalCopy);
                }
                compare()
            }, true);


        }, function () {
            console.log('Student not found')
            vm.student = null;
        });

        vm.studentEnrollments = StudentsService.getEnrollments({id: vm.studentId},
                function () {
                    console.log('Student Enrollments');
                    console.log(vm.studentEnrollments);

                    // ### Do a copy to save process. ###
                    vm.studentEnrollmentsOriginalCopy = angular.copy(vm.studentEnrollments);

                     $scope.studentEnrollmentsModelHasChanged = false;


                    $scope.$watch('vm.studentEnrollments', function (newValue, oldValue) {
                        if (newValue != oldValue) {
                            $scope.studentEnrollmentsModelHasChanged = !angular.equals(vm.studentEnrollments, vm.studentEnrollmentsOriginalCopy);
                        }
                        compare()
                    }, true);


                }, function (error) {
                    console.log('Get student enrollments process fail.');
                    console.log(error);
                    toastService.showToast('Error obteniendo las matrículaciones del estudiante.');
                }
        );


        activate();

        ///////////////////////////////////////////////////////////
        function activate() {
            console.log('Activating studentsProfileController controller.')

        }

        /** Delete student in server.
         * Call to server with DELETE method ($delete= DELETE) using vm.student that is
         * a instance of StudentsService.*/
        function deleteStudent() {

            vm.student.$delete(
                function(){ // Success
                    console.log('Student deleted successfully.')
                    $state.go('students')
                    toastService.showToast('Estudiante eliminado con éxito.')
                },
                function(error){ // Fail
                    console.log('Student deleted process fail.')
                    console.log(eror)
                    toastService.showToast('Error eliminando al estudiante.')
                });

        }

        /** Show the previous step to delete item, a confirm message */
        function showDeleteStudentConfirm() {

            var confirm = $mdDialog.confirm()
                .title('¿Está seguro de que quiere eliminar a este estudiante?')
                //.textContent('If you do, you will be erased from all project which you are and you can not access to app.')
                //.ariaLabel('Lucky day')
                .ok('Estoy seguro')
                .cancel('Cancelar');

            $mdDialog.show(confirm).then(function () {
                deleteStudent();
            }, function () {
                console.log('Operacion cancelada.')
            });

        };


        function deleteStudentEnrollment(subjectId, classId){

            // We need delete from data block copy the item selected:
            for (var i = 0; i < vm.studentEnrollments.length; i++)
                if (vm.studentEnrollments[i].class.classId == classId) {
                    var numSubjects = vm.studentEnrollments[i].subjects.length;
                    if (numSubjects == 1)
                        vm.studentEnrollments.splice(i, 1);
                    else{
                        var subjectIndex = -1;
                        for (var j = 0; j < numSubjects; j++)
                            if (vm.studentEnrollments[i].subjects[j].subjectId == classId)
                                subjectIndex = j;
                        vm.studentEnrollments[i].subjects.splice(subjectIndex, 1);
                    }
                }
        }

        function openMenu($mdOpenMenu, ev) {
          originatorEv = ev;
          $mdOpenMenu(ev);
        };


        function compare() {
            console.log('comparing changes ');

            if ($scope.studentModelHasChanged) {
                console.log("student Model has changed.")
            } else {
                console.log("student Model is equal.")
            }
            if ($scope.studentEnrollmentsModelHasChanged) {
                console.log("student Enrollments Model has changed.")
            } else {
                console.log("student Enrollments Model is equal.")
            }

            if ($scope.studentModelHasChanged || $scope.studentEnrollmentsModelHasChanged) {
                vm.updateButtonEnable = true;
            } else {
                vm.updateButtonEnable = false;
            }
        }

         /** Show the previous step to delete item, a confirm message */
        function showDeleteStudentEnrollmentConfirm(subjectId, classId) {

            var confirm = $mdDialog.confirm()
                .title('¿Está seguro de que quiere eliminar la relación?')
                //.textContent('If you do, you will be erased from all project which you are and you can not access to app.')
                //.ariaLabel('Lucky day')
                .ok('Estoy seguro')
                .cancel('Cancelar');

            $mdDialog.show(confirm).then(
                function () {
                    deleteStudentEntrollment(subjectId, classId);
                },
                function () {
                    console.log('Del teacher Impart relation operation canceled.')
                }
            );
        };






        /** Update student data in server.
         * Call to server with PUT method ($update = PUT) using vm.student that is
         * a instance of StudentsService.*/
        function updateStudent() {
            console.log('Calling updateStudent() function.')

            // A dirty solution to problem that does that the date is saved with a day minus.
            vm.student.birthdate.setDate(vm.student.birthdate.getDate() + 1);

            vm.student.$update(
                function () { // Success
                    console.log('Student saved successfully.')
                    toastService.showToast('Estudiante actualizado con éxito.')
                },
                function (error) { // Fail
                    console.log('Error saving student.')
                    console.log(error)
                    toastService.showToast('Error actualizando al estudiante.')
                });
        }


    })

    /** Configure date format in <md-datepicker> */
    .config(function ($mdDateLocaleProvider) {
        $mdDateLocaleProvider.formatDate = function (date) {

            // While don't find other better solution to set format DD-MM-YYYY like in Spain
            // and set default text: "Fecha de nacimiento"
            if (date == undefined) {
                console.log('undefined')
                return 'Fecha Nacimiento'
            } else {
                return moment(date).format('DD-MM-YYYY');
            }
        };
    });
