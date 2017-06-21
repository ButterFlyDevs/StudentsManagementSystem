angular.module('teachers')
    .controller('teachersProfileController', function ($scope, moment, $q, $resource, $state, $stateParams, $mdDialog, TeachersService, AssociationsService, ImpartsService, toastService, globalService) {

        var vm = this;

        vm.controllerName = 'teachersProfileController';

        vm.teacherId = $stateParams.teacherId;

        vm.defaultAvatar = globalService.defaultAvatar;

        // To control the loading spinner.
        vm.dataIsReady = false;
        vm.studentDataIsReady = false;
        vm.teachingDataIsReady = false;

        vm.updateButtonEnable = false; // To control when the update button could be enabled.
        vm.associationsList = null;


        // References to functions.
        vm.addRelation = addRelation;
        vm.updateTeacher = updateTeacher;

        vm.showDeleteClassConfirm = showDeleteClassConfirm;
        vm.showDeleteSubjectConfirm = showDeleteSubjectConfirm;
        vm.showDeleteTeacherConfirm = showDeleteTeacherConfirm;


        vm.loadStudents = loadStudents;
        vm.loadTeaching = loadTeaching;
        vm.loadReports = loadReports;

        // Vars to control entity values edition.
        vm.editValuesEnabled = false;
        vm.updateButtonEnable = false;
        // Functions references to control entity values edition.
        vm.modValues = modValues;
        vm.cancelModValues = cancelModValues;



        // An array of promises from calls.
        var promises = [];

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
            vm.teachingDataIsReady = false;
            vm.teacherTeaching = TeachersService.getTeaching({id: vm.teacherId},
                function () {
                    vm.dataIsReady = true;
                    vm.teachingDataIsReady = true;
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
                    $scope.teacherModelHasChanged = !angular.equals(vm.teacher, vm.teacherOriginalCopy);
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

            loadTeaching();

        }


        /**
         * Load the list of students
         * @param associationId
         */
        function loadStudents(subjectId, classId) {

            vm.studentDataIsReady = false;

            // To show the classes of the subject we charge the list of it when the subjectId is passed
            if (subjectId)
                for (var a = 0; a < vm.teacherTeaching.length; a++)
                    if (vm.teacherTeaching[a].subject.subjectId == subjectId)
                        vm.classes = vm.teacherTeaching[a].classes

            if (!subjectId && !classId) {
                // We want all students that is related with this class, independently of the subject from which come.
                vm.teacherStudents = TeachersService.getStudents({id: vm.teacherId},
                    function () {
                        vm.studentDataIsReady = true;
                    },
                    function (error) {
                        console.log('Get teacher students process fail.');
                        console.log(error);
                        toastService.showToast('Error obteniendo los alumnos a los que da clase el profesor.');
                    }
                );
            }
            if (subjectId && !classId) {
                vm.teacherStudents = TeachersService.getStudentsFromSubject({id: vm.teacherId, idSubject: subjectId},
                    function () {
                        vm.studentDataIsReady = true;
                    },
                    function (error) {
                        console.log('Get teacher students from subject process fail.');
                        console.log(error);
                        toastService.showToast('Error obteniendo los alumnos a los que da clase el profesor para la asignatura.');
                    }
                );
            }
        }


        function loadReports() {
            vm.teacherReport = TeachersService.getReport({id: vm.teacherId},
                function () {
                    console.log('Teacher Report Data Block');
                    console.log(vm.teacherReport);
                    if (vm.teacherReport.report_log != null) {
                        vm.chartConfig['series'][0]['data'][0]['y'] = vm.teacherReport['students']['gender_percentage']['M']
                        vm.chartConfig['series'][0]['data'][1]['y'] = vm.teacherReport['students']['gender_percentage']['F'];
                    }

                }, function (error) {
                    console.log('Get teacher report process fail.');
                    console.log(error);
                    toastService.showToast('Error obteniendo los reports del profesor.')
                })
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
        function deleteTeacher() {

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
                    deleteTeacher();
                },
                function () {
                    console.log('Del teacher operation canceled.')
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

        function modValues() { vm.editValuesEnabled = true;}
        function cancelModValues() { vm.editValuesEnabled = false; vm.teacher = angular.copy(vm.teacherOriginalCopy);}



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