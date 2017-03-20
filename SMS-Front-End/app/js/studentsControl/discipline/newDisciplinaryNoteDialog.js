angular.module('discipline')
    .controller('newDisciplinaryNoteDialogController', function ($scope, $state, $mdDialog, $mdpDatePicker, toastService, StudentsService, DisciplineService, globalService) {

        var vm = this;

        activate();

        // References to functions.
        vm.closeDialog = closeDialog;
        vm.itemQuerySearch = itemQuerySearch;
        vm.saveDisciplinaryNote = saveDisciplinaryNote;

        vm.disciplinaryNote = new DisciplineService();
        vm.defaultAvatar = globalService.defaultAvatar;
        vm.disciplinaryNote.dateTime = new Date();
        vm.thereAreStudents = false;

        ///////////////////////////////////////////////////////////
        function activate() {
            console.log('Activating newDisciplinaryNoteDialogController controller.')

            // List of student formated to be used in md-autocomplete.
            vm.studentsList = StudentsService.query({}, function () {
                console.log('StudentsList received');
                console.log(vm.studentsList);
                if (vm.studentsList.length >0){
                    vm.thereAreStudents = true;

                // Transform the list (adding a field called 'value' to be used in the search process).
                vm.studentsList = vm.studentsList.map(function (student) {
                        student.value = student.name.toLowerCase();
                        if (student.surname)
                            student.value += ' ' + student.surname.toLowerCase();
                        return student;

                    }
                );
                }

                console.log(vm.studentsList);


            }, function (error) {
                console.log('Any problem found when was retrieved the students list.');
                console.log(error);
            })


        }

        // Function to close the dialog
        function closeDialog() {
            $mdDialog.cancel();
        }


        /** Save Disciplinary Note data in server.
         * Call to server with POST method ($save = POST) using vm.disciplinaryNote that is
         * a instance of TeachersService.*/
        function saveDisciplinaryNote() {
            console.log('Calling saveDisciplinaryNote() function.')


    
            // Formating date:
            dt = vm.disciplinaryNote.dateTime;
            new_format = dt.getFullYear()+'-'+dt.getMonth()+'-'+dt.getDate()+' '+dt.getHours()+':'+dt.getMinutes();

            vm.disciplinaryNote.dateTime = new_format;

            console.log(vm.disciplinaryNote.dateTime);

            vm.disciplinaryNote.$save(
                function () { // Success
                    console.log('Disciplinary Note saved successfully');
                    $mdDialog.cancel();
                    $state.reload();
                    toastService.showToast('Parte disciplinario guardado con éxito.')
                },
                function (error) { // Fail
                    toastService.showToast('Error al guardar el parte disciplinario.');
                    console.log('Error while disciplinary note is saved.')
                    console.log(error)
                });

        }


        // Functions related with md-autocomplete for student.

        /**
         * Create filter function for a query string
         */
        function createFilterFor(query) {
            var lowercaseQuery = angular.lowercase(query);
            return function filterFn(state) {
                return (state.value.indexOf(lowercaseQuery) != -1);
            };
        }

        function itemQuerySearch(query, type) {

            var selectedArray = vm.studentsList;

            // If there are query return the list filtered with the query.
            // Filter create a new array with all elements that pass the test
            var results = query ? selectedArray.filter(createFilterFor(query)) : selectedArray;

            return results;
        }

        vm.itemToString = function itemToString(item) {
            nameSurname = item.name;
            if (item.surname)
                nameSurname += ' ' + item.surname;

            return nameSurname;

        }


        vm.items = ['Urgente al Tutor de los implicados.',
                    'Urgente a Jefatura de Estudios.',
                    'A los padres de los implicados.']

        vm.selected = [1];
        vm.toggle = function (item, list) {
            var idx = list.indexOf(item);
            if (idx > -1) {
                list.splice(idx, 1);
            }
            else {
                list.push(item);
            }
        };

        vm.exists = function (item, list) {
            return list.indexOf(item) > -1;
        };

        vm.isIndeterminate = function () {
            return (vm.selected.length !== 0 &&
            vm.selected.length !== vm.items.length);
        };

        vm.isChecked = function () {
            return vm.selected.length === vm.items.length;
        };

        vm.toggleAll = function () {
            if (vm.selected.length === vm.items.length) {
                vm.selected = [];
            } else if (vm.selected.length === 0 || vm.selected.length > 0) {
                vm.selected = vm.items.slice(0);
            }
        };


    });