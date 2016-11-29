angular.module('subjects')
    .controller('subjectsProfileController', function ($scope, $resource, $q, $state, $stateParams, $mdDialog, SubjectsService, AssociationsService, ImpartsService, toastService) {

        var vm = this;

        vm.controllerName = 'subjectsProfileController';

        vm.subjectId = $stateParams.subjectId;
        vm.updateButtonEnable = false; // To control when the update button could be enabled.

        // References to functions.
        vm.updateSubject = updateSubject;
        vm.showDeleteSubjectConfirm = showDeleteSubjectConfirm;

        vm.showDeleteSubjectClassImpartConfirm = showDeleteSubjectClassImpartConfirm;
        vm.showDeleteClassConfirm = showDeleteClassConfirm;

        vm.addRelation = addRelation;

        vm.defaultAvatar = 'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcThQiJ2fHMyU37Z0NCgLVwgv46BHfuTApr973sY7mao_C8Hx_CDPrq02g'

        // An array of promises from calls.
        var promises = [];

        activate();

        ///////////////////////////////////////////////////////////
        function activate() {
            console.log('Activating subjectsProfileController controller.')
            loadData()


        }

        function loadData() {
            vm.subject = SubjectsService.get({id: vm.subjectId}, function () {
                console.log(vm.subject)

                // ### Do a copy to save process. ###
                vm.subjectOriginalCopy = angular.copy(vm.subject);

                $scope.subjectModelHasChanged = false;

                $scope.$watch('vm.subject', function (newValue, oldValue) {
                    if (newValue != oldValue) {
                        $scope.subjectModelHasChanged = !angular.equals(vm.subject, vm.subjectOriginalCopy);
                    }
                    compare();
                }, true);


            }, function (error) {
                console.log('Get subject process fail.');
                console.log(error);
                // Here we don't use toastService because in the view will appear a message.
                vm.subject = null;  //Maybe useful.
            });

            vm.subjectClasses = SubjectsService.getClasses({id: vm.subjectId},
                function () {
                    console.log('Subject Classes');
                    console.log(vm.subjectClasses);

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


        function deleteClass(classId) {

            console.log('deleteTeacherFromClass');
            console.log(vm.subjectClasses);
            // We need delete from data block copy the item selected:
            for (var i = 0; i < vm.subjectClasses.length; i++)
                if (vm.subjectClasses[i].class.classId == classId)
                    vm.subjectClasses.splice(i, 1);
            console.log(vm.subjectClasses);
        }

        /** Show the previous step to delete item, a confirm message */
        function showDeleteSubjectConfirm() {

            var confirm = $mdDialog.confirm()
                .title('¿Está seguro de que quiere eliminar esta asignatura?')
                .textContent('Si lo hace, eliminará todas las relaciones existentes con profesores y alumnos.')
                //.ariaLabel('Lucky day')
                .ok('Estoy seguro')
                .cancel('Cancelar');

            $mdDialog.show(confirm).then(function () {
                deleteSubject();
            }, function () {
                console.log('Operacion cancelada.')
            });

        };


        function showDeleteClassConfirm(classId) {
            var confirm = $mdDialog.confirm()
                .title('¿Está seguro de que quiere dejar de impartir esta asignatura en este grupo?')
                //.textContent('If you do, you will be erased from all project which you are and you can not access to app.')
                //.ariaLabel('Lucky day')
                .ok('Estoy seguro')
                .cancel('Cancelar');

            $mdDialog.show(confirm).then(function () {
                deleteClass(classId);
            }, function () {
                console.log('Operacion cancelada.')
            });

        }


        // We delete a teacher from a class
        function deleteTeacherFromClass(classId, teacherId) {

            console.log('deleteTeacherFromClass');
            console.log(vm.subjectClasses);
            // We need delete from data block copy the item selected:
            for (var i = 0; i < vm.subjectClasses.length; i++)
                if (vm.subjectClasses[i].class.classId == classId) {
                    var classIndex = -1;
                    for (var j = 0; j < vm.subjectClasses[i].teachers.length; j++)
                        if (vm.subjectClasses[i].teachers[j].teacherId == teacherId)
                            classIndex = j;
                    vm.subjectClasses[i].teachers.splice(classIndex, 1);
                    if (vm.subjectClasses[i].teachers.length == 0) {
                        delete vm.subjectClasses[i].teachers;
                    }

                }


            console.log(vm.subjectClasses);
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
                    deleteTeacherFromClass(classId, teacherId);
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

            // We check if the CHANGES are in the SUBJECT-MODEL and in this case we add this call to
            // queue.
            if ($scope.subjectModelHasChanged) {

                var deferred = $q.defer();

                var promise = vm.subject.$update(
                    function () { // Success
                        deferred.resolve('Success updating the subject with vm.subject.$update.');
                    },
                    function (error) { // Fail
                        deferred.reject('Error updating the subject with vm.subject.$update, error: ' + error)
                    });
                promises.push(deferred.promise)
            }


            if ($scope.subjectClassesModelHasChanged) { // We update the teacher imparts info.

                // Algorithm that compare both data blocks and save or delete accordingly.
                processDiferences(vm.subjectClassesOriginalCopy, vm.subjectClasses)

            }


            // After check the models and put the calls in the queue we process this queue:
            $q.all(promises).then(
                function (value) {
                    console.log('Resolving all promises, SUCCESS,  value: ')
                    console.log(value);
                    toastService.showToast('Asignatura actualizado con éxito.');

                    // It reloaded all data to avoid problems.
                    // How wait to exit from teacher.$update
                    loadData();

                    promises = [];

                }, function (reason) {
                    console.log('Resolving all promises, FAIL, reason: ')
                    console.log(reason);
                    toastService.showToast('Error actualizando la asignatura.');
                }
            )
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

        function delAssociation(associationId) {
            console.log('Deleting association relation ' + associationId)

            var deferred = $q.defer();

            AssociationsService.delete({id: associationId},
                function () {
                    deferred.resolve('Success deleting the association relation with AssociationService.$delete');
                },
                function (error) {
                    deferred.reject('Error deleting the the association relation with AssociaitonService.$delete, error: ' + error)
                });

            promises.push(deferred.promise)
        }


        // Esta función será la que crea la relación entre la asignatura y las nuevas clases, tengan o no profesores. en el proceso de GUARDADO.
        function newClass(classId, teachersIds) {

            console.log('Creating newClass relation:')
            console.log('classId: ' + classId)
            console.log('teacherIds: ' + teachersIds)

            // If the class has teachers inside
            if (classId && teachersIds) {

                var deferred = $q.defer();

                //Creamos un vector de referencias anidadas:
                var nestedsDeferreds = [];
                var indices = [];
                for (var i = 0; i < teachersIds.length; i++) {
                    nestedsDeferreds.push($q.defer());
                    indices.push(i);
                }
                console.log(nestedsDeferreds)

                function prueba() {
                    console.log('Hola soy una funcion.');
                }

                var newAssociation = new AssociationsService({data: {classId: classId, subjectId: vm.subjectId}});
                newAssociation.$save(
                    function () { // Success
                        deferred.resolve('Success saving the association relation with AssociationsService $save');

                        for (var a = 0; a < teachersIds.length; a++) {

                            console.log('AQUIIIIII')
                            console.log(a)

                            // Now we save the impart with this associationId
                            var newImpart = new ImpartsService({
                                data: {
                                    associationId: newAssociation.associationId,
                                    teacherId: teachersIds[a]
                                }
                            })

                            newImpart.$save(
                                function (a) { // Success
                                    console.log(nestedsDeferreds);
                                    console.log(a);
                                    console.log('success, got data: ', a);
                                    nestedsDeferreds[a].resolve('Success saving the impart relation with ImpartService $save');

                                },
                                function (error) { // Fail
                                    nestedsDeferreds[a].reject('Error saving the the impart relation with ImpartService $save, error: ' + error)
                                })

                        }

                    },
                    function (error) { // Fail
                        deferred.reject('Error saving the the association relation with AssociationsService $save, error: ' + error)
                    });
                promises.push(deferred.promise);
                for (var i = 0; i < teachersIds.length; i++)
                    promises.push(nestedsDeferreds[i].promise)


            } else if (classId && teachersIds == undefined) { // The class hasn't teachers inside, only a association relation is needed to create.
                var deferred = $q.defer();
                var newAssociation = new AssociationsService({data: {classId: classId, subjectId: vm.subjectId}});
                newAssociation.$save(
                    function () { // Success
                        deferred.resolve('Success saving the association relation with AssociationsService $save');
                    },
                    function (error) { // Fail
                        deferred.reject('Error saving the the association relation with AssociationsService $save, error: ' + error)
                    });
                promises.push(deferred.promise);
            }

        }

        //ASOCIATION - TEACHER
        function newImpart(associationId, teacherId) {

            var deferred = $q.defer();

            console.log('Creating newImpart relation:');
            console.log('associationdId: ' + associationId);
            console.log('teacherId: ' + teacherId);


                console.log('Creating a new Imparts relation');
                var newImpart = new ImpartsService({
                    data: {
                        associationId: associationId,
                        teacherId: teacherId
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

        }


        // Función que procesa los bloques de datos y realiza las llamadas a las funciones que realmente modifican datos.
        function processDiferences(original, modified) {
            console.log('ProcessDiferences')
            console.log(original)
            console.log(modified)

            // DELETED REVIEW, in this case unlike teachersProfile of studentProfile is  possible delImpart and delAssociation.

            if (original.length != 0)

                for (var i = 0; i < original.length; i++) {
                    var index = -1;
                    for (var j = 0; j < modified.length; j++)
                        if (modified[j].class.classId == original[i].class.classId)
                            index = j;
                    if (index == -1) {
                        // If the item have teachers list.
                        if (original[i].teachers !== undefined)
                            for (var c = 0; c < original[i].teachers.length; c++)
                                delImpart(original[i].teachers[c].impartId)
                        // In any case the association between subject and class is deleted:
                        delAssociation(original[i].class.associationId);
                    }
                    else

                    // Que pasa cuando alguno o ambos no tienen teachers.


                    //Ninguno de los dos tiene profesores
                    if (original[i].teachers == undefined && modified[index].teachers == undefined) {
                        console.log('Ninguno de los dos tiene profesores, no se hace nada.')
                    } else {

                        if (original[i].teachers !== undefined) {
                            for (var c2 = 0; c2 < original[i].teachers.length; c2++) {
                                var indexC = -1;
                                for (var d = 0; d < modified[index].teachers.length; d++)
                                    if (original[i].teachers[c2].teacherId == modified[index].teachers[d].teacherId)
                                        indexC = d;
                                if (indexC == -1)
                                // We delete the relation between the teacher with subject-class
                                    delImpart(original[i].teachers[c2].impartId)
                            }
                        }


                    }


                    // HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE //


                }


            // CREATE REVIEW, in this case unlike teachersProfile of studentProfile is  possible newImpart and newAssociation.

            if (modified.lenght !== 0)


                for (var a = 0; a < modified.length; a++) {
                    console.log('working with ' + a)
                    var index3 = -1;
                    // Search if the class exists
                    for (var b = 0; b < original.length; b++)
                        if (original[b].class.classId == modified[a].class.classId)
                            index3 = b;

                    console.log(index3);
                    //If not exists THE CLASS has been created:
                    if (index3 == -1) {
                        console.log('creating the class');

                        // If there aren't teachers:
                        if (modified[a].teachers == undefined) {

                            newClass(modified[a].class.classId)
                            //newAssociation(modified[a].class.classId, vm.subjectId);
                        } else {  // If there are:

                            teachersIds = [];
                            for (var h = 0; h < modified[a].teachers.length; h++)
                                //If a association is needed to be created would be decission to newImpart
                                //newImpart(modified[a].class.classId, modified[a].teachers[h].teacherId);
                                teachersIds.push(modified[a].teachers[h].teacherId)

                            //
                            newClass(modified[a].class.classId, teachersIds)
                        }

                        //If exists, we need only add a new teacher if this case appear.
                    } else {
                        //If the block teachers in original doesn't exists we created one.
                        if (original[index3].teachers == undefined) {
                            original[index3].teachers = [];
                        }

                        for (var m = 0; m < modified[a].teachers.length; m++) {


                            var index4 = -1;
                            for (var n = 0; n < original[index3].teachers.length; n++)
                                if (original[index3].teachers[n].teacherId == modified[a].teachers[m].teacherId)
                                    index4 = n;
                            if (index4 == -1)
                                newImpart(modified[a].class.associationId, modified[a].teachers[m].teacherId);


                        }
                    }
                }


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
