angular.module('attendanceControls')
    .controller('newAttendanceControlDialogController', function ($scope, $state, $mdDialog, TeachersService, ClassesService, toastService, globalService) {

            var vm = this;

            activate();

            // References to functions.
            vm.closeDialog = closeDialog;
            vm.itemQuerySearch = itemQuerySearch;
            vm.defaultAvatar = globalService.defaultAvatar;

            vm.okToRealize = false;

            vm.goToDoAC = goToDoAC;


            ///////////////////////////////////////////////////////////
            function activate() {

                console.log('Activating newAttendanceControlDialog controller.')

                vm.teachersList = TeachersService.query({}, function () {
                    console.log('TeacherList received');
                    console.log(vm.teachersList);

                    vm.teachersList = vm.teachersList.map(function (teacher) {
                            teacher.value = teacher.name.toLowerCase() + ' ' +
                                            teacher.surname.toLowerCase();
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
                return function filterFn(state) { return (state.value.indexOf(lowercaseQuery) != -1); };
            }

            function itemQuerySearch(query, type) {

                var selectedArray = null;

                if (type == 'teacher')
                    selectedArray = vm.teachersList;
                if (type == 'subject')
                    selectedArray = vm.subjectsList;
                if (type == 'class')
                    selectedArray = vm.classesList;

                // If there are query return the list filtered with the query.
                // Filter create a new array with all elements that pass the test
                var results = query ? selectedArray.filter(createFilterFor(query)) : selectedArray;

                return results;

            }

            vm.itemToString = function itemToString(item, type) {
                if (type == 'teacher') {
                    return item.name + ' ' + item.surname
                }
                if (type == 'class') {
                    return item.course + ' ' + item.word + ' ' + item.level
                }

            }

            function goToDoAC() {
                console.log('YEAH');
                // TODO: add associationId in teachingData block.
                console.log(vm.classSelected)
                $state.go('newAttendanceControl', {'associationId': vm.classSelected.associationId});
                $mdDialog.cancel();
            }

            function loadTeaching() {
                // Using the perfect teacher teaching data block.
                vm.teacherTeaching = TeachersService.getTeaching({id: vm.teacherSelected.teacherId},
                    function () {

                        /*We create a new array adding a new item named value with the name of the
                        subject in lowercase.
                        */
                        vm.subjectsList = vm.teacherTeaching.map(function (item) {
                                item.subject.value = item.subject.name.toLowerCase();
                                return item.subject;
                            }
                        );

                    }, function (error) {
                        console.log('Any problem found when was retrieved the teacher teaching data block.');
                        console.log(error);
                    })
            }

            function loadClasses(item) {

                //Now we load the classes from the teaching data block to the selected subject.
                vm.classesList = []

                for (var a = 0; a < vm.teacherTeaching.length; a++) {
                    if (vm.teacherTeaching[a].subject.subjectId == item.subjectId)
                        if (vm.teacherTeaching[a].classes)
                            for (var b = 0; b < vm.teacherTeaching[a].classes.length; b++)
                                vm.classesList.push(vm.teacherTeaching[a].classes[b])
                }

                vm.classesList = vm.classesList.map(function (item) {
                        item.value = item.course.toString().toLowerCase() + ' ' +
                            item.word.toLowerCase() + ' ' +
                            item.level.toLowerCase() + ' '
                        return item;
                    }
                );
            }

            vm.selectedItemChange = function selectedItemChange(item, type) {
                // when a teacher is selected the list of classes must be loaded
                // and show the selector.

                if (item && type == 'teacher')
                    loadTeaching();
                if (item && type == 'subject')
                    loadClasses(item);
                if (item && type == 'class' && vm.teacherSelected && vm.subjectSelected)
                    vm.okToRealize = true;
                else
                    vm.okToRealize = false;
            }

        }
    );