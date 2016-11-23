angular.module('students')
    .controller('studentsProfileController', function ($scope, moment, $q, $resource, $state, $stateParams, $mdDialog, StudentsService, AssociationsService, EnrollmentsService, toastService, globalService) {

        var vm = this
        vm.controllerName = 'studentsProfileController';

        vm.studentId = $stateParams.studentId

        // References to functions.
        vm.addRelation = addRelation;
        vm.updateStudent = updateStudent;
        vm.showDeleteStudentConfirm = showDeleteStudentConfirm;
        vm.showDeleteStudentEnrollmentConfirm = showDeleteStudentEnrollmentConfirm;


        var promises = [];
        vm.openMenu = openMenu

        vm.defaultAvatar = globalService.defaultAvatar;

        activate();





        ///////////////////////////////////////////////////////////
        function activate() {
            console.log('Activating studentsProfileController controller.');
            vm.addButtonEnable = false;
            loadData();

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


        function deleteStudentEnrollment(classId, subjectId){

            // We need delete from data block copy the item selected:
            for (var i = 0; i < vm.studentEnrollments.length; i++)
                if (vm.studentEnrollments[i].class.classId == classId) {
                    var numSubjects = vm.studentEnrollments[i].subjects.length;
                    if (numSubjects == 1)
                        vm.studentEnrollments.splice(i, 1);
                    else{
                        var subjectIndex = -1;
                        for (var j = 0; j < numSubjects; j++)
                            if (vm.studentEnrollments[i].subjects[j].subjectId == subjectId)
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

        /**
         * Open the dialog to add a relation to this student.
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


         /** Show the previous step to delete item, a confirm message */
        function showDeleteStudentEnrollmentConfirm(classId, subjectId) {

            var confirm = $mdDialog.confirm()
                .title('¿Está seguro de que quiere eliminar la relación?')
                //.textContent('If you do, you will be erased from all project which you are and you can not access to app.')
                //.ariaLabel('Lucky day')
                .ok('Estoy seguro')
                .cancel('Cancelar');

            $mdDialog.show(confirm).then(
                function () {
                    console.log('Try')
                    deleteStudentEnrollment(classId, subjectId);
                },
                function () {
                    console.log('Del student Enrollment relation operation canceled.')
                }
            );
        };






        /** Update student data in server.
         * Call to server with PUT method ($update = PUT) using vm.student that is
         * a instance of StudentsService.*/
        function updateStudent() {
            console.log('Calling updateStudent() function.')

            if($scope.studentModelHasChanged){ // We update student data.
                // A dirty solution to problem that does that the date is saved with a day minus.
                vm.student.birthdate.setDate(vm.student.birthdate.getDate() + 1);

                var deferred = $q.defer();

                var promise = vm.student.$update(
                    function () { // Success
                        deferred.resolve('Success updating the student with vm.student.$update.');
                    },
                    function (error) { // Fail
                        deferred.reject('Error updating the student with vm.student.$update, error: ' + error)
                    });
                promises.push(deferred.promise)
            }


            if ($scope.studentEnrollmentsModelHasChanged) { // We update the teacher imparts info.
                // Algorithm that compare both data blocks and save or delete accordingly.
                processDiferences(vm.studentEnrollmentsOriginalCopy, vm.studentEnrollments)
            }


            $q.all(promises).then(
                function (value) {
                    console.log('Resolving all promises, SUCCESS,  value: ')
                    console.log(value);
                    toastService.showToast('Estudiante actualizado con éxito.');

                    // It reloaded all data to avoid problems.
                    // How wait to exit from teacher.$update
                    loadData();

                    promises = [];

                }, function (reason) {
                    console.log('Resolving all promises, FAIL, reason: ')
                    console.log(reason);
                    toastService.showToast('Error actualizando el estudiante.');
                }
            )

        }


        function delEnrollment(enrollmentId){
            console.log('Deleting enrollment relation ' + enrollmentId)

            var deferred = $q.defer();

            EnrollmentsService.delete({id: enrollmentId},
                function () {
                    deferred.resolve('Success deleting the enrollment relation with EnrollmentService.$delete');
                },
                function (error) {
                    deferred.reject('Error deleting the the enrollment relation with EnrollmentService.$delete, error: ' + error)
                });

            promises.push(deferred.promise)
        }





        /**
        * @ngdoc function
        * @name module.name#doSomething
        * @methodOf module.name
        * @description Does the thing
        * @param {string=} [foo='bar'] This is a parameter that does nothing, it is
                                       optional and defaults to 'bar'
        * @returns {undefined} It doesn't return
        */
         function newEnrollment(classId, subjectId) {

                var deferred = $q.defer();

                // This function will decide if it need create a new A
                // relation before to create new I relation with the teacher related.

                var exists = false;
                var index = -1;
                for (var i = 0; i < vm.associationsList.length; i++)
                    if (vm.associationsList[i].classId == classId &&
                        vm.associationsList[i].subjectId == subjectId) {
                        exists = true;
                        index = i;
                    }

                if (exists) { //We need create only a new Enrollment relation.

                    console.log('Creating a new Enrollment relation');
                    var newEnrollment = new EnrollmentsService({
                        data: {
                            associationId: vm.associationsList[index].associationId,
                            studentId: vm.studentId
                        }
                    });
                    newEnrollment.$save(
                        function () { // Success
                            deferred.resolve('Success saving the enrollment relation with newEnrollment.$save');
                        },
                        function (error) { // Fail
                            deferred.reject('Error saving the the enrollment relation with newEnrollment.$save, error: ' + error)
                        });
                    promises.push(deferred.promise)

                } else { // We need create a new Association relation and before a new Enrollment relation.
                    console.log('Creating a new Association relation and Enrollment relation.');

                    var nestedDeferred = $q.defer();

                    var newAssociation = new AssociationsService({data: {classId: classId, subjectId: subjectId}});
                    newAssociation.$save(
                        function () { // Success
                            deferred.resolve('Success saving the association relation with AssociationsService $save');

                            // Now we save the enrollment relation with this associationId

                            var newEnrollment = new EnrollmentsService({
                                data: {
                                    associationId: newAssociation.associationId,
                                    studentId: vm.studentId
                                }
                            })
                            newEnrollment.$save(
                                function () { // Success
                                    nestedDeferred.resolve('Success saving the enrollment relation with EnrollmentsService $save');
                                },
                                function (error) { // Fail
                                   nestedDeferred.reject('Error saving the the enrollment relation with EnrollmentsService $save, error: ' + error)
                                })
                        },
                        function (error) { // Fail
                            deferred.reject('Error saving the the association relation with AssociationsService $save, error: ' + error)
                        });
                    promises.push(deferred.promise)
                    promises.push(nestedDeferred.promise)

                }

            }

        function processDiferences(original, modified) {

            // Deleted review
            if (original.length !== 0)
                for (var i = 0; i < original.length; i++) {
                    var index = -1;
                    for (var j = 0; j < modified.length; j++)
                        if (modified[j].class.classId == original[i].class.classId)
                            index = j;
                    if (index == -1)
                        for (var c = 0; c < original[i].subjects.length; c++)
                            delEnrollment(original[i].subjects[c].enrollmentId);
                    else
                        for (var c2 = 0; c2 < original[i].subjects.length; c2++) {
                            var indexC = -1;
                            for (var d = 0; d < modified[index].subjects.length; d++)
                                if (original[i].subjects[c2].subjectId == modified[index].subjects[d].subjectId)
                                    indexC = d;
                            if (indexC == -1)
                                delEnrollment(original[i].subjects[c2].enrollmentId);
                        }

                }

            // Created item review
            if (modified.lenght !== 0)
                for (var a = 0; a < modified.length; a++) {
                    var index3 = -1;
                    for (var b = 0; b < original.length; b++)
                        if (original[b].class.classId == modified[a].class.classId)
                            index3 = b;
                    if (index3 == -1)
                        for (var h = 0; h < modified[a].subjects.length; h++)
                            newEnrollment(modified[a].subjects[h].subjectId, modified[a].class.classId);
                    else
                        for (var m = 0; m < modified[a].subjects.length; m++) {
                            var index4 = -1;
                            for (var n = 0; n < original[index3].subjects.length; n++)
                                if (original[index3].subjects[n].subjectId == modified[a].subjects[m].subjectId)
                                    index4 = n;
                            if (index4 == -1)
                                newEnrollment(modified[a].subjects[m].subjectId, modified[a].class.classId);
                        }
                }
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
