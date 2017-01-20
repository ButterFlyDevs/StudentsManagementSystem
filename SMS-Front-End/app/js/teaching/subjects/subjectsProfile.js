angular.module('subjects')
    .controller('subjectsProfileController', function ($scope, $resource, $q, $state, $stateParams, $mdDialog, SubjectsService, EnrollmentsService, ClassesService, AssociationsService, ImpartsService, toastService) {

        var vm = this;

        vm.controllerName = 'subjectsProfileController';

        vm.subjectId = $stateParams.subjectId;
        vm.updateButtonEnable = false; // To control when the update button could be enabled.

        // References to functions.
        vm.updateSubject = updateSubject;
        vm.showDeleteSubjectConfirm = showDeleteSubjectConfirm;

        vm.showDeleteSubjectClassImpartConfirm = showDeleteSubjectClassImpartConfirm;
        vm.showDeleteClassConfirm = showDeleteClassConfirm;
        vm.showDeleteStudentConfirm = showDeleteStudentConfirm

        vm.showDeleteTeacherFromClassConfirm = showDeleteTeacherFromClassConfirm;

        vm.addRelation = addRelation;

        vm.loadStudents = loadStudents;
        vm.loadTeaching = loadTeaching;
        vm.loadReports = loadReports;



        vm.modValues = modValues;
        vm.cancelModValues = cancelModValues;

        vm.defaultAvatar = 'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcThQiJ2fHMyU37Z0NCgLVwgv46BHfuTApr973sY7mao_C8Hx_CDPrq02g'

        // An array of promises from calls.
        var promises = [];

        activate();

        ///////////////////////////////////////////////////////////
        function activate() {
            console.log('Activating subjectsProfileController controller.')
            loadData()


        }


        /**
         * Load only the teaching info about this class.
         */
        function loadTeaching() {
            vm.subjectTeaching = SubjectsService.getTeaching({id: vm.subjectId},
                function () {
                    console.log('Subject Teaching Data Block');
                    console.log(vm.subjectTeaching);
                }, function (error) {
                    console.log('Get subject teaching process fail.');
                    console.log(error);
                    toastService.showToast('Error obteniendo las asignaturas que se imparten en la clase.')
                }
            );
        }

        function loadReports() {
            vm.subjectReport = SubjectsService.getReport({id: vm.subjectId},
                function () {
                    console.log('Subject Report Data Block');
                    console.log(vm.subjectReport);
                    if (vm.subjectReport.report_log != null) {
                        vm.chartConfig['series'][0]['data'][0]['y'] = vm.subjectReport['students']['gender_percentage']['M']
                        vm.chartConfig['series'][0]['data'][1]['y'] = vm.subjectReport['students']['gender_percentage']['F'];
                        console.log(vm.chartConfig);
                    }

                }, function (error) {
                    console.log('Get class report process fail.');
                    console.log(error);
                    toastService.showToast('Error obteniendo los reports de la asingatura.')
                })
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

            loadTeaching();

        }

        function modValues() {
            vm.editValuesEnabled = true;
        }

        function cancelModValues() {
            vm.editValuesEnabled = false;

            vm.subject = angular.copy(vm.subjectOriginalCopy);


        }

        function compare() {
            if ($scope.subjectModelHasChanged || $scope.subjectClassesModelHasChanged) {
                vm.updateButtonEnable = true;
            } else {
                vm.updateButtonEnable = false;
            }
        }


        /**
         * Which actually delete the class selected related with the subject in the view.
         * @param associationId The id of association that represent the link between the class and the subject.
         * This come from subjectTeaching data block.
         */
        function deleteClass(associationId) {

            AssociationsService.delete({id: associationId},
                function () { // Success
                    loadTeaching(); // Reload the specific section.
                    toastService.showToast('Relación eliminada con éxito.')
                },
                function (error) { // Fail
                    console.log('Class deleted process fail.');
                    console.log(error)
                    toastService.showToast('Error eliminando la relación.')
                });

        }

        /**
         * Show the floating dialog to ask user if it actually want to delete the relation.
         * @param associationId The id of the association that come from subjectTeaching data block.
         */
        function showDeleteClassConfirm(associationId) {
            var confirm = $mdDialog.confirm()
                .title('¿Está seguro de que quiere eliminar esta grupo?')
                .textContent('Si lo hace, también eliminará las matrículas de los estudiantes matriculados a esta.')
                .ok('Estoy seguro')
                .cancel('Cancelar');

            $mdDialog.show(confirm).then(function () {
                deleteClass(associationId);
            }, function () {
                console.log('Operacion cancelada.')
            });

        }


        function deleteTeacherFromClass(impartId) {

            ImpartsService.delete({id: impartId},
                function () { // Success
                    console.log('Class deleted successfully.');
                    loadTeaching(); // Reload the specific section.
                    toastService.showToast('Relación eliminada con éxito.')
                },
                function (error) { // Fail
                    console.log('Class deleted process fail.');
                    console.log(error)
                    toastService.showToast('Error eliminando la relación.')
                });

        }

        function showDeleteTeacherFromClassConfirm(impartId) {
            var confirm = $mdDialog.confirm()
                .title('¿Está seguro de que quiere que este profesor deje de impartir la asingatura en esta clase?')
                .ok('Estoy seguro')
                .cancel('Cancelar');

            $mdDialog.show(confirm).then(function () {
                deleteTeacherFromClass(impartId);
            }, function () {
                console.log('Operacion cancelada.')
            });

        }


        /**
         * Load the list of students
         * @param associationId
         */
        function loadStudents(associationId) {

            console.log('loadStudents associationId')
            console.log(associationId)

            if (!associationId) {

                // We want all students that is related with this subject, independently of the class from which come.

                vm.subjectStudents = SubjectsService.getStudents({id: vm.subjectId},
                    function () {
                        console.log('Subject Students');
                        console.log(vm.subjectStudents);
                    },
                    function (error) {
                        console.log('Get subject students process fail.');
                        console.log(error);
                        toastService.showToast('Error obteniendo los alumnos matriculados.');
                    }
                );
            }
            else {
                vm.subjectStudents = AssociationsService.getStudents({id: associationId},
                    function () {
                        console.log('Subject Students');
                        console.log(vm.subjectStudents);
                    },
                    function (error) {
                        console.log('Get Class- subject students process fail.');
                        console.log(error);
                        toastService.showToast('Error obteniendo los alumnos matriculados en este grupo.');
                    }
                );
            }
        }


        function deleteStudent(enrollmentId, kind) {
            console.log('Deleting student from class.');
            console.log(enrollmentId);
            console.log(kind);

            if (kind == 'enrollment')
                EnrollmentsService.delete({id: enrollmentId},
                    function () { // Success
                        loadStudents(vm.associationIdSelected); // Reload the specific section.
                        toastService.showToast('Relación eliminada con éxito.')
                    },
                    function (error) { // Fail
                        console.log('Relation deleted process fail.');
                        console.log(error)
                        toastService.showToast('Error eliminando la relación.')
                    });
            else if (kind == 'student') {

                SubjectsService.nested_delete({id: vm.subjectId, a: 'student', b: enrollmentId}, //nested_kind_plus_id Because the behaviour of $resource we pass the nested element this way.
                    function () { // Success
                        loadStudents(vm.associationIdSelected); // Reload the specific section.
                        toastService.showToast('Relación múltiple eliminada con éxito.')
                    },
                    function (error) { // Fail
                        console.log('Multiple relation deleted process fail.');
                        console.log(error)
                        toastService.showToast('Error eliminando la relación múltiple.')
                    });
            }
        }

        /** Show the previous step to delete item, a confirm message */
        function showDeleteStudentConfirm(enrollmentId, kind) {

            var message = ''
            console.log(vm.associationIdSelected);
            if (vm.associationIdSelected)
                message = '¿Está seguro de querer eliminar al estudiante de la asignatura?'
            else
                message = '¿Está seguro de querer eliminar al estudiante de TODAS las asignaturas de esta clase?'

            var confirm = $mdDialog.confirm()
                .title(message)
                .ok('Estoy seguro')
                .cancel('Cancelar');

            $mdDialog.show(confirm).then(function () {
                deleteStudent(enrollmentId, kind);
            }, function () {
                console.log('Operacion cancelada.')
            });

        };


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


        /** Show the previous step to delete item (method just above): a confirm message */
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
            console.log('Calling updateSubject() function.');
            vm.subject.$update(
                function () { // Success
                    console.log('Subject updated successfully.')
                    toastService.showToast('Asignatura actualizada con éxito.')
                    vm.editValuesEnabled = false;
                    vm.updateButtonEnable = false;
                },
                function (error) { // Fail
                    console.log('Error updating the subject.')
                    console.log(error)
                    toastService.showToast('Error actualizando la asignatura.')
                });

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

        vm.chartConfig = {
            xAxis: {
                type: 'category'
            },
            title: {
                text: 'Porcentaje por género.'
            },
            yAxis: {
                allowDecimals: false,
                title: {
                    text: 'Porcentaje'
                }
            },
            tooltip: {
                headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}%</b> of total<br/>'
            },
            legend: {enabled: false},
            plotOptions: {
                series: {
                    borderWidth: 0,
                    dataLabels: {
                        enabled: true,
                        format: '{point.y:.1f}%'
                    }
                }
            },
            series: [{
                name: 'Genero',
                colorByPoint: true,
                type: 'column',
                data: [
                    {name: 'Chicos', y: 0},
                    {name: 'Chicas', y: 1}]
            }]
        };


    });
