angular.module('attendanceControls')
    .controller('newAttendanceControlDialogController', function ($scope, $state, $mdDialog, TeachersService, toastService, globalService) {

            var vm = this;

            activate();

            // References to functions.
            vm.closeDialog = closeDialog;
            vm.querySearch = querySearch;

            vm.defaultAvatar = globalService.defaultAvatar;


            ///////////////////////////////////////////////////////////
            function activate() {

                console.log('Activating newAttendanceControlDialog controller.')

                vm.teachersList = TeachersService.query({}, function () {
                    console.log('TeacherList received');
                    console.log(vm.teachersList);

                    vm.teachersList = vm.teachersList.map(function (teacher) {
                            teacher.value = teacher.name.toLowerCase();
                            return teacher;
                        }
                    );
                    console.log(vm.teachersList)

                }, function (error) {
                    console.log('Any problem found when was retrieved the teachers list.');
                    console.log(error);
                })
            }

            // Function to close the dialog
            function closeDialog() {
                $mdDialog.cancel();
            }

            /**
             * Create filter function for a query string
             */
            function createFilterFor(query) {
                var lowercaseQuery = angular.lowercase(query);

                return function filterFn(state) {
                    return (state.value.indexOf(lowercaseQuery) === 0);
                };
            }

            function querySearch(query) {
                var results = query ? vm.teachersList.filter(createFilterFor(query)) : vm.teachersList;
                return results;

            }


        }
    );