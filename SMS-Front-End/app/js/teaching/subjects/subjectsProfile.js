angular.module('subjects')
    .controller('subjectsProfileController', function ($scope, $resource, $q, $state, $stateParams, $mdDialog, SubjectsService, EnrollmentsService, ClassesService, AssociationsService, ImpartsService, toastService, globalService) {

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

        vm.defaultAvatar = globalService.defaultAvatar;

        // To control the loading spinner.
        vm.dataIsReady = false;
        vm.studentDataIsReady = false;
        vm.teachingDataIsReady = false;


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
            vm.teachingDataIsReady = false;
            vm.subjectTeaching = SubjectsService.getTeaching({id: vm.subjectId},
                function () {
                    vm.dataIsReady = true;
                    vm.teachingDataIsReady = true;
                    console.log(vm.subjectTeaching);
                }, function (error) {
                    console.log('Get subject teaching process fail.');
                    console.log(error);
                    toastService.showToast('Error obteniendo las asignaturas que se imparten en la clase.')
                });
        }

        /**
         * Load the list of students
         * @param associationId
         */
        function loadStudents(associationId) {

            vm.studentDataIsReady = false;

            if (!associationId) {

                // We want all students that is related with this subject, independently of the class from which come.

                vm.subjectStudents = SubjectsService.getStudents({id: vm.subjectId},
                    function () {
                        vm.studentDataIsReady = true;
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
                        vm.studentDataIsReady = true;
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

        function loadReports() {
            vm.subjectReport = SubjectsService.getReport({id: vm.subjectId},
                function () {
                    console.log('Subject Report Data Block');
                    console.log(vm.subjectReport);
                    //if (vm.subjectReport.report_log != null) {
                    vm.chartConfig['series'][0]['data'][0]['y'] = vm.subjectReport['students']['gender_percentage']['M']
                    vm.chartConfig['series'][0]['data'][1]['y'] = vm.subjectReport['students']['gender_percentage']['F'];
                    //}

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

                // To make possible the changes detections pre-saved item to avoid or allow the save action.
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

        /**
         * Enable all fields to can change attributes of item.
         */
        function modValues() {
            vm.editValuesEnabled = true;
        }

        /**
         * Cancel all mods over the subject attributes.
         */
        function cancelModValues() {
            // Do all fields not editables.
            vm.editValuesEnabled = false;
            // Back to previous state without new request:
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

                    // ### Do a copy to save process. ###
                    vm.subjectOriginalCopy = angular.copy(vm.subject);
                },
                function (error) { // Fail
                    console.log('Error updating the subject.')
                    console.log(error)
                    toastService.showToast('Error actualizando la asignatura.')
                });

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
                text: 'Genero',
                align: 'center',
                verticalAlign: 'middle',
                y: 60
            },
            credits: {
                enabled: false
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
            exporting: {
                enabled: false
            },
            plotOptions: {
                pie: {
                    dataLabels: {
                        enabled: true,
                        distance: -50,
                        style: {
                            fontWeight: 'bold',
                            color: 'white'
                        }
                    },
                    startAngle: -90,
                    endAngle: 90,
                    center: ['50%', '75%']
                }
            },
            colors: ['#5EA6DD', '#F09FFF'],
            series: [{
                name: 'Genero',
                colorByPoint: true,
                type: 'pie',
                innerSize: '50%',
                data: [
                    {name: 'Chicos', y: 0},
                    {name: 'Chicas', y: 0}]
            }]
        };


    });
