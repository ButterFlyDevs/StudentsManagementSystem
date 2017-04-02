angular.module('attendanceControls')
    .controller('attendanceControlController', function ($scope, moment, $q, $resource, $state, $stateParams, $mdDialog, toastService, globalService, attendanceControlsService) {

            var vm = this;

            // Param url passed to load an existing ac
            vm.acId = $stateParams.acId;

            // Param url passed to CREATE a new Attendance Control
            vm.associationId = $stateParams.associationId;

            vm.action = null;

            if (vm.associationId)
                vm.action = 'new';
            else
                vm.action = 'loaded';

            vm.defaultAvatar = globalService.defaultAvatar;

            // Functions:
            vm.changeAssistanceForStudent = changeAssistanceForStudent;
            vm.changeUniformForStudent = changeUniformForStudent;
            vm.checkIfDelayIsEnabled = checkIfDelayIsEnabled;
            vm.checkIfJustifiedDelayIsEnabled = checkIfJustifiedDelayIsEnabled;

            // To control the loading spinner.
            vm.dataIsReady = false;

            vm.delayList = ['5', '10', '15', '20', '30', '45'];

            activate();


            ///////////////////////////////////////////////////////////////////
            function activate() {
                console.log('Activating attendanceControlController controller.');

                // We want charge base to do the AC
                if (vm.action == 'new') {
                    vm.acBase = new attendanceControlsService();
                    // Using $ like prefix to use own methods
                    vm.acBase.$getBase({id: vm.associationId},
                        function () {
                            console.log('Attendance Control Base Data Block received:');

                            for (var i = 0; i < vm.acBase.students.length; i++)
                                vm.acBase.students[i].control = vm.acBase.control;

                            vm.dataIsReady = true;


                        }, function (error) {
                            console.log('Get ac base process fail.', error);
                            toastService.showToast('Error obteniendo la base para el control de asistencia.')
                        });
                }
                // We want to see a existing ac.
                if(vm.action == 'loaded'){

                    vm.ac = attendanceControlsService.get({id: vm.acId},
                        function () {
                            console.log('Attendance Control Base Data Block received:');
                            vm.dataIsReady = true;
                            vm.acBase = vm.ac;
                        }, function (error) {
                            console.log('Get ac base process fail.', error);
                            toastService.showToast('Error obteniendo la base para el control de asistencia.')
                        })
                }
            }


            function checkIfDelayIsEnabled(delayValue) {
                if (delayValue == null)
                    return false;
                else
                    return true;
            }

            function checkIfJustifiedDelayIsEnabled(delayValue) {
                if (delayValue == null)
                    return false;
                else
                    return true;
            }


            vm.changeDelay = function changeDelay(studentId, delay) {

                if (delay == 'Sin retraso') {
                    delay = 0;
                }
                for (var a = 0; a < vm.acBase.students.length; a++) {
                    if (vm.acBase.students[a].studentId == studentId) {
                        vm.acBase.students[a].control.delay = delay;
                        if (delay != 0)
                            vm.acBase.students[a].control.justifiedDelay = 0;
                        else
                            vm.acBase.students[a].control.justifiedDelay = null;
                    }
                }
            };

            vm.changeJustifiedDelay = function changeJustifiedDelay(studentId) {
                for (var a = 0; a < vm.acBase.students.length; a++) {
                    if (vm.acBase.students[a].studentId == studentId) {
                        if (vm.acBase.students[a].control.justifiedDelay == true) {
                            vm.acBase.students[a].control.justifiedDelay = false;
                        } else {
                            vm.acBase.students[a].control.justifiedDelay = true;
                        }
                    }
                }
            };

            function changeUniformForStudent(studentId) {
                for (var a = 0; a < vm.acBase.students.length; a++) {
                    if (vm.acBase.students[a].studentId == studentId) {
                        if (vm.acBase.students[a].control.uniform == true) {
                            vm.acBase.students[a].control.uniform = false;
                        } else {
                            vm.acBase.students[a].control.uniform = true;
                        }
                    }
                }
            };

            function changeAssistanceForStudent(studentId) {

                for (var a = 0; a < vm.acBase.students.length; a++) {
                    if (vm.acBase.students[a].studentId == studentId)
                        if (vm.acBase.students[a].control.assistance == true) {
                            // Set the student to fault.
                            vm.acBase.students[a].control.assistance = false;
                            // It changed to null the rest of values:
                            vm.acBase.students[a].control.delay = null;
                            vm.acBase.students[a].control.justifiedDelay = false;
                            vm.acBase.students[a].control.uniform = null;


                        } else {
                            vm.acBase.students[a].control.assistance = true;
                            vm.acBase.students[a].control.delay = 0;
                            vm.acBase.students[a].control.justifiedDelay = null;
                            vm.acBase.students[a].control.uniform = true;
                        }

                }

            }

            vm.saveCA = function saveCA() {

                console.log('Saving CA');
                // First we adjust the data block to correct input format to the server.
                vm.acBase.association.classId = vm.acBase.association.class.classId;
                delete vm.acBase.association.class;
                vm.acBase.association.subjectId = vm.acBase.association.subject.subjectId;
                delete vm.acBase.association.subject;
                delete vm.acBase.control;

                vm.acBase.teacherId = vm.acBase.teachers[0].teacherId;
                delete vm.acBase.teachers;

                vm.acBase.$save(
                    function () { // Success
                        console.log('ac saved successfully');
                        $state.go('attendanceControls');
                        toastService.showToast('Control de asistencia realizado con éxito.');
                    },
                    function (error) { // Fail
                        toastService.showToast('Error al enviar control de asistencia.');
                        console.log('Error while ac was saved.', error);
                    });
            }

        }
    );