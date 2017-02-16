angular.module('attendanceControls')
    .controller('attendanceControlController', function ($scope, moment, $q, $resource, $state, $stateParams, $mdDialog, toastService, globalService, attendanceControlsService) {

            var vm = this;

            // vm.teacherId = $stateParams.teacherId;

            vm.defaultAvatar = globalService.defaultAvatar;

            // Functions:
            vm.changeAssistanceForStudent = changeAssistanceForStudent;
            vm.changeUniformForStudent = changeUniformForStudent;
            vm.checkIfDelayIsEnabled = checkIfDelayIsEnabled;
            vm.checkIfJustifiedDelayIsEnabled = checkIfJustifiedDelayIsEnabled;
            vm.changeDelayForStudent = changeDelayForStudent;

            // To control the loading spinner.
            vm.dataIsReady = false;

            vm.delayList = ['5', '10', '15', '20', '30', '45'];

            activate();

            ///////////////////////////////////////////////////////////////////
            function activate() {
                console.log('Activating attendanceControlController controller.');

                vm.acBase = attendanceControlsService.getBase({id: 5629499534213120},
                    function () {
                        console.log('Attendance Control Base Data Block');
                        console.log(vm.acBase);
                        vm.dataIsReady = true;

                    }, function (error) {
                        console.log('Get ac base process fail.');
                        console.log(error);
                        toastService.showToast('Error obteniendo la base para el control de asistencia.')
                    })

            }

            function changeDelayForStudent(studentId) {
                console.log('DELAY CHANGED')
            }

            function checkIfDelayIsEnabled(delayValue) {
                console.log('checkIfDelayIsEnable')

                if (delayValue == null)
                    return false;
                else
                    return true;

            }

            function checkIfJustifiedDelayIsEnabled(delayValue) {
                console.log('checkIfJustifiedDelayIsEnable')

                if (delayValue == null)
                    return false;
                else
                    return true;

            }


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
            }

            function changeAssistanceForStudent(studentId) {
                console.log('changing');
                console.log(studentId);


                for (var a = 0; a < vm.acBase.students.length; a++) {
                    if (vm.acBase.students[a].studentId == studentId) {
                        if (vm.acBase.students[a].control.assistance == true) {
                            vm.acBase.students[a].control.assistance = false;

                            // It changed to null the rest of values:
                            vm.acBase.students[a].control.delay = null;
                            vm.acBase.students[a].control.justifiedDelay = null;
                            vm.acBase.students[a].control.uniform = null;

                            console.log(vm.acBase.students[a].control);

                        } else {
                            vm.acBase.students[a].control.assistance = true;
                            vm.acBase.students[a].control.delay = 0;
                            vm.acBase.students[a].control.justifiedDelay = null;
                            vm.acBase.students[a].control.uniform = true;
                        }
                    }
                }

            }

        }
    )