angular.module('students')
    .controller('studentsProfileController', function ($scope, moment, $q, $resource, $state, $stateParams, $mdDialog, StudentsService, AssociationsService, EnrollmentsService, toastService, globalService) {

        var vm = this

        vm.controllerName = 'studentsProfileController';
        vm.studentId = $stateParams.studentId;

        // Default img to users without it
        vm.defaultAvatar = globalService.defaultAvatar;

        // To control the loading spinner.
        vm.dataIsReady = false;
        vm.teacherDataIsReady = false;
        vm.teachingDataIsReady = false;

        // References to functions.
        vm.addRelation = addRelation;
        vm.updateStudent = updateStudent;
        vm.showDeleteStudentConfirm = showDeleteStudentConfirm;
        vm.showDeleteEnrollmentConfirm = showDeleteEnrollmentConfirm;
        vm.showDeleteClassConfirm = showDeleteClassConfirm;

        vm.loadTeachers = loadTeachers;
        vm.loadTeaching = loadTeaching;

        // Vars to control entity values edition.
        vm.editValuesEnabled = false;
        vm.updateButtonEnable = false;
        // Functions references to control entity values edition.
        vm.modValues = modValues;
        vm.cancelModValues = cancelModValues;

        var promises = [];
        vm.openMenu = openMenu;


        activate();


        ///////////////////////////////////////////////////////////
        function activate() {
            console.log('Activating studentsProfileController controller.');
            vm.addButtonEnable = false;
            loadData();

        }

        /**
         * Load only the teaching info about this student.
         */
        function loadTeaching() {
            vm.teachingDataIsReady = false;
            vm.studentTeaching = StudentsService.getTeaching({id: vm.studentId},
                function () {
                    vm.dataIsReady = true;
                    vm.teachingDataIsReady = true;
                }, function (error) {
                    console.log('Get stduent teaching process fail.');
                    console.log(error);
                    toastService.showToast('Error obteniendo los datos de docencia del estudiante.')
                }
            );
        }

        function loadData() {
            vm.student = StudentsService.get({id: vm.studentId}, function () {
                console.log(vm.student)
                var parts = vm.student.birthdate.split('-');
                var tmpDateObject = new Date(parts[0], parts[1] - 1, parts[2]);
                vm.student.birthdate = tmpDateObject;


                // ### Do a copy to save process. ###
                vm.studentOriginalCopy = angular.copy(vm.student);
                $scope.studentModelHasChanged = false;
                $scope.$watch('vm.student', function (newValue, oldValue) {

                    $scope.studentModelHasChanged = !angular.equals(vm.student, vm.studentOriginalCopy);
                    if ($scope.studentModelHasChanged)
                        vm.updateButtonEnable = true;
                    else
                        vm.updateButtonEnable = false;
                }, true);


            }, function () {
                console.log('Student not found')
                vm.student = null;
            });

            loadTeaching();
        }

        function modValues() { vm.editValuesEnabled = true; }
        function cancelModValues() { vm.editValuesEnabled = false; vm.student = angular.copy(vm.studentOriginalCopy); }

        /** Delete student in server.
         * Call to server with DELETE method ($delete= DELETE) using vm.student that is
         * a instance of StudentsService.*/
        function deleteStudent() {

            vm.student.$delete(
                function () { // Success
                    console.log('Student deleted successfully.');
                    $state.go('students');
                    toastService.showToast('Estudiante eliminado con éxito.');
                },
                function (error) { // Fail
                    console.log('Student deleted process fail.');
                    console.log(error);
                    toastService.showToast('Error eliminando al estudiante.');
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


        function deleteClass(teachingItem) {

            var promises = [];
            var deferred = $q.defer();

            for (var i = 0; i < teachingItem.subjects.length; i++) {
                EnrollmentsService.delete({id: teachingItem.subjects[i].enrollmentId},
                    function () {
                        deferred.resolve('Success deleting the enrollment relation with EnrollmentsService.$delete');
                    },
                    function (error) {
                        deferred.reject('Error deleting the the enrollment relation with EnrollmentsService.$delete, error: ' + error)
                    });
                promises.push(deferred.promise);
            }


            $q.all(promises).then(
                function (value) {
                    console.log('Resolving all promises, SUCCESS,  value: ')
                    console.log(value);
                    toastService.showToast('Desmatriculacion de grupo completo realizada con exito.');

                    loadTeaching();

                }, function (reason) {
                    console.log('Resolving all promises, FAIL, reason: ')
                    console.log(reason);
                    toastService.showToast('Error realizando la desmatriculacion al grupo completo.');
                }
            );

        }
        function showDeleteClassConfirm(teachingItem) {
            var confirm = $mdDialog.confirm()
                .title('¿Está seguro de que quiere desmatricular al alumno de este grupo?')
                .textContent('Esto hará que se desmatricule de todas las asignaturas en la estuviera.')
                .ok('Estoy seguro')
                .cancel('Cancelar');

            $mdDialog.show(confirm).then(function () {
                deleteClass(teachingItem);
            }, function () {
                console.log('Operacion cancelada.')
            });

        }

        function openMenu($mdOpenMenu, ev) { originatorEv = ev; $mdOpenMenu(ev);};

        /*
         * Open the dialog to add a relation to this class.
         * The add action is done in addRelationController in addRelation.js
         */
        function addRelation(itemTypeToAdd, secondaryItem) {

            $mdDialog.show({
                locals: {
                    parentScope: $scope,
                    parentController: vm,
                    itemTypeToAdd: itemTypeToAdd,
                    secondaryItem: secondaryItem
                },
                // We use the same basic controller.
                controller: 'addRelationController',
                controllerAs: 'vm',
                templateUrl: 'app/views/teaching/utils/addRelationTemplate.html'
            }).then(function () { }, function () {});
        }

        function loadTeachers() {

            vm.teacherDataIsReady = false;
            vm.studentTeachers = StudentsService.getTeachers({id: vm.studentId},
                function () {
                    vm.teacherDataIsReady = true;
                },
                function (error) {
                    console.log('Get student teachers process fail.');
                    console.log(error);
                    toastService.showToast('Error obteniendo los profesores del estudiante.');
                }
            );
        }

        /**
         * Delete the relation between a student and an associationb (class-subject). This
         * relation is Enrollment.
         * @param subject Object in studentTeaching that has inside id of enrollment to delete.
         */
        function deleteEnrollment(subject) {

            EnrollmentsService.delete({id: subject.enrollmentId},
                function () { // Success
                    console.log('Enrollment relation deleted successfully.')
                    toastService.showToast('Matricula eliminada con éxito.')
                    loadTeaching();
                },
                function (error) { // Fail
                    console.log('Enrollment deleted process fail.')
                    console.log(error)
                    toastService.showToast('Error eliminando la matricula.')
                });

        }

        /** Show the previous step to delete a enrollment item related with the student, a confirm message */
        function showDeleteEnrollmentConfirm(subject) {

            var confirm = $mdDialog.confirm()
                .title('¿Está seguro de que quiere desmatricular al estudiante?')
                //.textContent('Si lo hace todos los alumnos quedarán ')
                //.ariaLabel('Lucky day')
                .ok('Estoy seguro')
                .cancel('Cancelar');

            $mdDialog.show(confirm).then(function () {
                deleteEnrollment(subject);
            }, function () {
                console.log('Operacion cancelada.')
            });

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
                    console.log('Student updated successfully.')
                    toastService.showToast('Estudiante actualizado con éxito.')
                    vm.editValuesEnabled = false;
                    vm.updateButtonEnable = false;
                },
                function (error) { // Fail
                    console.log('Error updating student.')
                    console.log(error)
                    toastService.showToast('Error actualizando el estudiante.')
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
