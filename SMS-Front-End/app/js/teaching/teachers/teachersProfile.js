angular.module('teachers')
    .controller('teachersProfileController', function ($scope, moment, $q, $resource, $state, $stateParams, $mdDialog, TeachersService, AssociationsService, ImpartsService, toastService, globalService) {

        var vm = this;

        vm.controllerName = 'teachersProfileController';

        vm.teacherId = $stateParams.teacherId
        vm.updateButtonEnable = false; // To control when the update button could be enabled.
        vm.associationsList = null;


        vm.formUpdated = formUpdated


        // References to functions.
        vm.addRelation = addRelation;
        vm.updateTeacher = updateTeacher;

        vm.showDeleteClassConfirm = showDeleteClassConfirm;
        vm.showDeleteSubjectConfirm = showDeleteSubjectConfirm;
        vm.showDeleteTeacherConfirm = showDeleteTeacherConfirm;
        vm.showDeleteTeacherImpartConfirm = showDeleteTeacherImpartConfirm;


        vm.loadStudents = loadStudents;
        vm.loadTeaching = loadTeaching;
        //vm.loadReports = loadReports;

        // Vars to control entity values edition.
        vm.editValuesEnabled = false;
        vm.updateButtonEnable = false;
        // Functions references to control entity values edition.
        vm.modValues = modValues;
        vm.cancelModValues = cancelModValues;

        vm.defaultAvatar = globalService.defaultAvatar;

        // An array of promises from calls.
        var promises = [];


        activate();

        ///////////////////////////////////////////////////////////////////
        function activate() {
            console.log('Activating teachersProfileController controller.');
            vm.addButtonEnable = false;
            loadData();
        }


        /**
         * Load only the teaching info about this teacher.
         */
        function loadTeaching() {
            vm.teacherTeaching = TeachersService.getTeaching({id: vm.teacherId},
                function () {
                    console.log('Teacher Teaching Data Block');
                    console.log(vm.teacherTeaching);
                }, function (error) {
                    console.log('Get teacher teaching process fail.');
                    console.log(error);
                    toastService.showToast('Error obteniendo los datos de docencia del profesor.')
                }
            );
        }

        function loadData() {
            vm.teacher = TeachersService.get({id: vm.teacherId}, function () {
                console.log(vm.teacher)

                // We need change time data from string to JavaScript date object.

                // Thu Oct  6 00:00:00 2016
                console.log(vm.teacher.birthdate);
                //tmpDateObject.setTime(Date.parse( vm.teacher.birthdate ));


                var parts = vm.teacher.birthdate.split('-');
                var tmpDateObject = new Date(parts[0], parts[1] - 1, parts[2]);

                vm.teacher.birthdate = tmpDateObject;

                //Date 2016-10-05T22:00:00.000Z teachersProfile.js:26:17
                console.log(vm.teacher.birthdate);


                // ### Do a copy to save process. ###

                vm.teacherOriginalCopy = angular.copy(vm.teacher);

                $scope.teacherModelHasChanged = false;

                $scope.$watch('vm.teacher', function (newValue, oldValue) {
                    $scope.teacherModelHasChanged = !angular.equals(vm.class, vm.teacherOriginalCopy);
                    if ($scope.teacherModelHasChanged)
                        vm.updateButtonEnable = true;
                    else
                        vm.updateButtonEnable = false;
                }, true);



            }, function (error) {
                console.log('Get teacher process fail.')
                console.log(error)
                // Here we don't use toastService because in the view will appear a message.
                vm.teacher = null;
            })


            vm.teacherImparts = TeachersService.getImparts({id: vm.teacherId},
                function () {
                    console.log('Teachers imparts')
                    console.log(vm.teacherImparts)

                    // ### Do a copy to save process. ###
                    vm.teacherImpartsOriginalCopy = angular.copy(vm.teacherImparts);

                    $scope.teacherImpartsModelHasChanged = false;

                    $scope.$watch('vm.teacherImparts', function (newValue, oldValue) {
                        if (newValue != oldValue) {
                            $scope.teacherImpartsModelHasChanged = !angular.equals(vm.teacherImparts, vm.teacherImpartsOriginalCopy);
                        }
                        compare()
                    }, true);

                }, function (error) {
                    console.log('Get teacher imparts process fail.')
                    console.log(error)
                    toastService.showToast('Error obteniendo la docencia del profesor.')
                }
            )

            loadTeaching();

        }

        function formUpdated() {
            console.log('formUpdated')
        }

        function compare() {
            console.log('comparing changes ');

            if ($scope.teacherModelHasChanged) {
                console.log("teacher Model has changed.")
            } else {
                console.log("teacher Model is equal.")
            }
            if ($scope.teacherImpartsModelHasChanged) {
                console.log("teacher Imparts Model has changed.")
            } else {
                console.log("teacher Imparts Model is equal.")
            }

            if ($scope.teacherModelHasChanged || $scope.teacherImpartsModelHasChanged) {
                vm.updateButtonEnable = true;
            } else {
                vm.updateButtonEnable = false;
            }
        }

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
            })
                .then(function () {

                }, function () {

                });
        }


        /** Delete teacher in server.
         * Call to server with DELETE method ($delete= DELETE) using vm.teacher that is
         * a instance of TeachersService.*/
        function deleteUser() {

            vm.teacher.$delete(
                function () { // Success
                    console.log('Teacher deleted successfully.')
                    $state.go('teachers')
                    toastService.showToast('Profesor eliminado con éxito.')
                },
                function (error) { // Fail
                    console.log('Teacher deleted process fail.')
                    console.log(error)
                    toastService.showToast('Error eliminando al profesor.')
                });

        }

        function deleteTeacherImpart(subjectId, classId) {

            // We need delete from data block copy the item selected:
            for (var i = 0; i < vm.teacherImparts.length; i++)
                if (vm.teacherImparts[i].subject.subjectId == subjectId) {
                    var numClasses = vm.teacherImparts[i].classes.length;
                    if (numClasses == 1)
                        vm.teacherImparts.splice(i, 1);
                    else {
                        var classIndex = -1;
                        for (var j = 0; j < numClasses; j++)
                            if (vm.teacherImparts[i].classes[j].classId == classId)
                                classIndex = j;
                        vm.teacherImparts[i].classes.splice(classIndex, 1);
                    }
                }
        }

        /** Show the previous step to delete item, a confirm message */
        function showDeleteTeacherConfirm() {

            var confirm = $mdDialog.confirm()
                .title('¿Está seguro de que quiere eliminar a este usuario?')
                //.textContent('If you do, you will be erased from all project which you are and you can not access to app.')
                //.ariaLabel('Lucky day')
                .ok('Estoy seguro')
                .cancel('Cancelar');

            $mdDialog.show(confirm).then(
                function () {
                    deleteUser();
                },
                function () {
                    console.log('Del teacher operation canceled.')
                }
            );
        };

        /** Show the previous step to delete item, a confirm message */
        function showDeleteTeacherImpartConfirm(subjectId, classId) {

            var confirm = $mdDialog.confirm()
                .title('¿Está seguro de que quiere eliminar la relación?')
                //.textContent('If you do, you will be erased from all project which you are and you can not access to app.')
                //.ariaLabel('Lucky day')
                .ok('Estoy seguro')
                .cancel('Cancelar');

            $mdDialog.show(confirm).then(
                function () {
                    deleteTeacherImpart(subjectId, classId);
                },
                function () {
                    console.log('Del teacher Impart relation operation canceled.')
                }
            );
        };


        /** Delete class related with a the subject that the teacher impart, is a impart entity.
         * Call to server with DELETE method ($delete= DELETE) using vm.class that is
         * a instance of ClassesService.*/
        function deleteClass(impartId) {

            ImpartsService.delete({id: impartId},
                function () { // Success
                    console.log('Impart relation deleted successfully.')
                    toastService.showToast('Relación imparte eliminada con éxito.')
                    loadTeaching();
                },
                function (error) { // Fail
                    console.log('Impart deleted process fail.')
                    console.log(error)
                    toastService.showToast('Error eliminando la relación imparte.')
                });

        }

        /** Show the previous step to delete item, a confirm message */
        function showDeleteClassConfirm(impartId) {

            var confirm = $mdDialog.confirm()
                .title('¿Está seguro de que quiere eliminar este grupo?')
                //.textContent('Si lo hace todos los alumnos quedarán ')
                //.ariaLabel('Lucky day')
                .ok('Estoy seguro')
                .cancel('Cancelar');

            $mdDialog.show(confirm).then(function () {
                deleteClass(impartId);
            }, function () {
                console.log('Operacion cancelada.')
            });

        };


        function deleteSubject(teachingItem) {

            // We have a lot of class where the teacher impart this subject, so we look at in teachingItem
            // which are this classes and which are the impartId identificator to delete this in a list of deletions.

            var promises = [];
            var deferred = $q.defer();

            for (var i = 0; i < teachingItem.classes.length; i++) {
                ImpartsService.delete({id: teachingItem.classes[i].impartId},
                    function () {
                        deferred.resolve('Success deleting the impart relation with ImpartService.$delete');
                    },
                    function (error) {
                        deferred.reject('Error deleting the the impart relation with ImpartService.$delete, error: ' + error)
                    });
                promises.push(deferred.promise);
            }


            $q.all(promises).then(
                function (value) {
                    console.log('Resolving all promises, SUCCESS,  value: ')
                    console.log(value);
                    toastService.showToast('Asignatura eliminada con exito.');

                    loadTeaching();

                }, function (reason) {
                    console.log('Resolving all promises, FAIL, reason: ')
                    console.log(reason);
                    toastService.showToast('Error eliminando la asignatura.');
                }
            );

        }

        function showDeleteSubjectConfirm(teachingItem) {
            var confirm = $mdDialog.confirm()
                .title('¿Está seguro de que quiere eliminar esta asignatura? Si lo hace, también eliminará las matrículas' +
                    'de los estudiantes matriculados a esta.')
                //.textContent('Si lo hace todos los alumnos quedarán ')
                //.ariaLabel('Lucky day')
                .ok('Estoy seguro')
                .cancel('Cancelar');

            $mdDialog.show(confirm).then(function () {
                deleteSubject(teachingItem);
            }, function () {
                console.log('Operacion cancelada.')
            });

        }


        /** Update teacher data in server.
         * Call to server with PUT method ($update = PUT) using vm.teacher that is
         * a instance of TeachersService.*/
        function updateTeacher() {
            console.log('Calling updateTeacher() function.')
            // A dirty solution to problem that does that the date is saved with a day minus.
            vm.teacher.birthdate.setDate(vm.teacher.birthdate.getDate() + 1);

            vm.teacher.$update(
                function () { // Success
                    console.log('Teacher updated successfully.')
                    toastService.showToast('Profesor actualizado con éxito.')
                    vm.editValuesEnabled = false;
                    vm.updateButtonEnable = false;
                },
                function (error) { // Fail
                    console.log('Error updating teacher.')
                    console.log(error)
                    toastService.showToast('Error actualizando el profesor.')
                });


        }

        function modValues() {
            vm.editValuesEnabled = true;
        }

        function cancelModValues() {
            vm.editValuesEnabled = false;
            vm.teacher = angular.copy(vm.teacherOriginalCopy);
        }

        /**
         * Load the list of students
         * @param associationId
         */
        function loadStudents(subjectId, classId) {


            // To show the classes of the subject we charge the list of it when the subjectId is passed
            if (subjectId) {

                for (var a = 0; a < vm.teacherTeaching.length; a++) {
                    if (vm.teacherTeaching[a].subject.subjectId == subjectId) {
                        vm.classes = vm.teacherTeaching[a].classes
                    }
                }

                console.log('CLASSES')
                console.log(vm.classes)

            }


            console.log('loadStudents subjectId')
            console.log(subjectId)

            if (!subjectId && !classId) {

                console.log('No hay ni asignaturas ni clases');

                // We want all students that is related with this class, independently of the subject from which come.

                vm.teacherStudents = TeachersService.getStudents({id: vm.teacherId},
                    function () {
                        console.log('Teacher Students');
                        console.log(vm.teacherStudents);
                    },
                    function (error) {
                        console.log('Get teacher students process fail.');
                        console.log(error);
                        toastService.showToast('Error obteniendo los alumnos a los que da clase el profesor.');
                    }
                );
            }
            if (subjectId && !classId) {
                console.log('Solo la clase');
                vm.teacherStudents = TeachersService.getStudentsFromSubject({id: vm.teacherId, idSubject: subjectId},
                    function () {
                        console.log('Teacher Students from subject call sucess.');
                        console.log(vm.teacherStudents);
                    },
                    function (error) {
                        console.log('Get teacher students from subject process fail.');
                        console.log(error);
                        toastService.showToast('Error obteniendo los alumnos a los que da clase el profesor para la asignatura.');
                    }
                );
            }
        }


        function delImpart(impartId) {
            console.log('Deleting impart relation ' + impartId)

            var deferred = $q.defer();

            ImpartsService.delete({id: impartId},
                function () {
                    deferred.resolve('Success deleting the impart relation with ImpartService.$delete');
                },
                function (error) {
                    deferred.reject('Error deleting the the impart relation with ImpartService.$delete, error: ' + error)
                });

            promises.push(deferred.promise)
        }

        function newImpart(classId, subjectId) {

            var deferred = $q.defer();

            // This function will decide if it need create a new A
            // relation before to create new I relation with the teacher related.

            console.log('Creating new impart relation:')
            console.log('classId: ' + classId)
            console.log('subjectId: ' + subjectId)

            var exists = false;
            var index = -1;
            for (var i = 0; i < vm.associationsList.length; i++)
                if (vm.associationsList[i].classId == classId &&
                    vm.associationsList[i].subjectId == subjectId) {
                    exists = true;
                    index = i;
                }

            if (exists) { //We need create only a new Imparts relation.

                console.log('Creating a new Imparts relation');
                var newImpart = new ImpartsService({
                    data: {
                        associationId: vm.associationsList[index].associationId,
                        teacherId: vm.teacherId
                    }
                });
                newImpart.$save(
                    function () { // Success
                        deferred.resolve('Success saving the impart relation with newImpart.$save');
                    },
                    function (error) { // Fail
                        deferred.reject('Error saving the the impart relation with newImpart.$save, error: ' + error)
                    });
                promises.push(deferred.promise)

            } else { // We need create a new Association relation and before a new Imparts relation.
                console.log('Creating a new Association relation and Imparts relation.');

                var nestedDeferred = $q.defer();

                var newAssociation = new AssociationsService({data: {classId: classId, subjectId: subjectId}});
                newAssociation.$save(
                    function () { // Success
                        deferred.resolve('Success saving the association relation with AssociationsService $save');

                        // Now we save the impart with this associationId

                        var newImpart = new ImpartsService({
                            data: {
                                associationId: newAssociation.associationId,
                                teacherId: vm.teacherId
                            }
                        })
                        newImpart.$save(
                            function () { // Success
                                nestedDeferred.resolve('Success saving the impart relation with ImpartService $save');
                            },
                            function (error) { // Fail
                                nestedDeferred.reject('Error saving the the impart relation with ImpartService $save, error: ' + error)
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
            // console.log(original)
            // console.log(modified)

            // Deleted review

            if (original.length !== 0)
                for (var i = 0; i < original.length; i++) {
                    var index = -1;
                    for (var j = 0; j < modified.length; j++)
                        if (modified[j].subject.subjectId == original[i].subject.subjectId)
                            index = j;
                    if (index == -1)
                        for (var c = 0; c < original[i].classes.length; c++)
                            delImpart(original[i].classes[c].impartId)
                    else
                        for (var c2 = 0; c2 < original[i].classes.length; c2++) {
                            var indexC = -1;
                            for (var d = 0; d < modified[index].classes.length; d++)
                                if (original[i].classes[c2].classId == modified[index].classes[d].classId)
                                    indexC = d;
                            if (indexC == -1)
                                delImpart(original[i].classes[c2].impartId)
                        }

                }

            // Created item review

            if (modified.lenght !== 0)
                for (var a = 0; a < modified.length; a++) {
                    var index3 = -1;
                    for (var b = 0; b < original.length; b++)
                        if (original[b].subject.subjectId == modified[a].subject.subjectId)
                            index3 = b;
                    if (index3 == -1)
                        for (var h = 0; h < modified[a].classes.length; h++)
                            newImpart(modified[a].classes[h].classId, modified[a].subject.subjectId);
                    else
                        for (var m = 0; m < modified[a].classes.length; m++) {
                            var index4 = -1;
                            for (var n = 0; n < original[index3].classes.length; n++)
                                if (original[index3].classes[n].classId == modified[a].classes[m].classId)
                                    index4 = n;
                            if (index4 == -1)
                                newImpart(modified[a].classes[m].classId, modified[a].subject.subjectId);
                        }
                }

        }


    })

    /** Configure date format in <md-datepicker> */
    .config(function ($mdDateLocaleProvider) {
        $mdDateLocaleProvider.formatDate = function (date) {

            // While don't find other better solution to set format DD-MM-YYYY like in Spain
            // and set default text: "Fecha de nacimiento" .
            if (date == undefined) {
                console.log('undefined')
                return 'Fecha Nacimiento'
            } else {
                return moment(date).format('DD-MM-YYYY');
            }
        };
    });