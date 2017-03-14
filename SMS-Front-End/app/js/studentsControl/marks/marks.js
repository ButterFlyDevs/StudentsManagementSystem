angular.module('marks')
    .controller('marksController', function ($scope, moment, $q, $resource, $state, $stateParams, $mdDialog, MarksService, SubjectsService, AssociationsService, toastService, globalService) {

        var vm = this;

        console.log(vm.action);

        vm.defaultAvatar = globalService.defaultAvatar;


        activate();

        vm.subjectIsReady = false;
        vm.classesIsReady = false;
        vm.studentIsReady = false;
        vm.selectorsAreReady = false;
        vm.marksAreReady = false;
        vm.isANewMark = false;

        ///////////////////////////////////////////////////////////////////
        function activate() {
            console.log('Activating marks controller.');

            // First we request a complete list of subjects.
            vm.subjectsList = SubjectsService.query({}, function () {
                console.log('subjectList received');
                console.log(vm.subjectsList);

                vm.subjectsList = vm.subjectsList.map(function (subject) {
                        subject.value = subject.name.toLowerCase()
                        return subject;
                    }
                );
                vm.dataIsReady = true;
                console.log(vm.teachersList)

            }, function (error) {
                console.log('Any problem found when was retrieved the teachers list.');
                console.log(error);
            })


        }

        function createFilterFor(query) {
            var lowercaseQuery = angular.lowercase(query);
            return function filterFn(state) {
                return (state.value.indexOf(lowercaseQuery) != -1);
            };
        }

        /**
         * To put item selected in md-autocomplete (once selected) with the our own format.
         * @param item The item to format.
         * @param type The kind of object.
         * @returns {string}
         */
        vm.itemToString = function itemToString(item, type) {


            if (type == 'student') {
                return item.name + ' ' + item.surname
            }
            if (type == 'class') {
                return item.course + ' ' + item.word + ' ' + item.level
            }

        }
        vm.itemQuerySearch = function itemQuerySearch(query, type) {

            console.log('BASTAR')
            console.log('QUERY')
            console.log(query)

            var selectedArray = null;

            if (type == 'student')
                selectedArray = vm.studentsList;
            if (type == 'subject')
                selectedArray = vm.subjectsList;
            if (type == 'class')
                selectedArray = vm.classesList;

            // If there are query return the list filtered with the query.
            // Filter create a new array with all elements that pass the test
            var results = query ? selectedArray.filter(createFilterFor(query)) : selectedArray;
            console.log('RESULTADOS');
            console.log(results);
            return results;

        }
        vm.selectedItemChange = function selectedItemChange(item, type) {
            // when a teacher is selected the list of classes must be loaded
            // and show the selector.

            console.log('CAMBIO')

            if (item && type == 'class')
                loadStudents(item);

            if (item && type == 'student')
                loadMark(item);

            // If is loaded the subject
            if (item && type == 'subject')
            // When subject has been selected we charge the classes related.
                loadClasses(item);

            if (item && type == 'class' && vm.teacherSelected && vm.subjectSelected)
                vm.okToRealize = true;
            else
                vm.okToRealize = false;
        }



        /**
         * with item, that is a class item with associationId inside we are going to search all student enrollment in this
         association between a class and a subject.
         * @param item
         */
        function loadStudents(item) {
            console.log('loadStudents')
            console.log(item);

            vm.studentsList = AssociationsService.get({id: item.associationId}, function () {

                console.log(vm.studentsList);
                vm.studentsList = vm.studentsList.students;

                vm.studentsList = vm.studentsList.map(function (item) {
                        item.value = item.name.toString().toLowerCase() + ' ' + item.surname.toLowerCase()
                        return item;
                    }
                );

                console.log(vm.studentsList);
                vm.studentsIsReady = true;

            }, function (error) {
                console.log('Any problem found when was retrieved the teachers list.');
                console.log(error);
            })

        }

        function loadMark(item){
            console.log('LOADING MARK');
            console.log(item);
            console.log(vm.studentSelected);

            // Request to get the marks of this student, using his enrollmentId.
            vm.mark = MarksService.get({enrollmentId: item.enrollmentId}, function(){
                console.log('HOOO');
                console.log(vm.mark);
                vm.marksAreReady=true;
            }, function(error){
                console.log('Any problem found when was retrieved the marks of student.');
                console.log(error);
                console.log(error.status);

                if (error.status == 404){
                    // Means that user haven't any mark yet.
                    console.log('ok');
                    vm.mark = new MarksService();
                    vm.marksAreReady=true;
                    vm.isANewMark =true;
                    console.log(vm.mark);
                }
            });

        }

        /**
         *
         * @param marks
         * @returns {*}
         */
        function parseMarks(marks){

            marks.preFirstEv = parseFloat(marks.preFirstEv);
            marks.firstEv    = parseFloat(marks.firstEv );
            marks.preSecondEv    = parseFloat(marks.preSecondEv );
            marks.thirdEv    = parseFloat(marks.firstEv );
            marks.final    = parseFloat(marks.final );

            return marks
        }

          /** Update subject data in server.
         * Call to server with PUT method ($update = PUT) using vm.subject that is
         * a instance of SubjectsService.*/
        vm.updateMark = function updateMark() {
            console.log('Calling updateSubject() function.');

            if (vm.isANewMark){

                // We need complete a bit of data before.

                console.log('DATA FILL');
                console.log(vm.studentSelected);
                console.log(vm.classSelected);
                console.log(vm.subjectSelected);

                vm.mark.studentId = vm.studentSelected.studentId;
                vm.mark.enrollment = {};
                vm.mark.enrollment.enrollmentId = vm.studentSelected.enrollmentId;
                vm.mark.enrollment.classId = vm.classSelected.classId;
                vm.mark.enrollment.subjectId = vm.subjectSelected.subjectId;
                vm.mark.enrollment.teacherId = 1; // It will be te active user or the teacher that impart the subject.

                vm.mark.marks = parseMarks(vm.mark.marks);

                vm.mark.$save(
                    function () {
                        console.log('COOL');
                        vm.isANewMark = false;
                    },function(){
                        console.log('FAIL');
                        vm.isANewMark = false;
                    })

                }

            else{

                vm.mark.marks = parseMarks(vm.mark.marks);

            vm.mark.$update(
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
        }

        /**
         * Enable all fields to can change attributes of item.
         */
        vm.modValues = function modValues() {
            vm.editValuesEnabled = true;
        }

        /**
         * Set all values to null to reset the "Mark Searcher"
         */
        vm.clean = function clean(){
            vm.mark = null;
            vm.studentsIsReady = null;
            vm.studentsList = null;
            vm.classesIsReady = null;
            vm.classesList = null;

            vm.subjectSearchText = null;

            vm.classSearchText = null;
            vm.classSelected = null;

            vm.studentSearchText = null;
            vm.studentSelected = null;


            vm.marksAreReady = null;
            vm.mark = null;

        }

        /**
         * Cancel all mods over the subject attributes.
         */
        vm.cancelModValues = function cancelModValues() {
            // Do all fields not editables.
            vm.editValuesEnabled = false;
            // Back to previous state without new request:
            //vm.subject = angular.copy(vm.subjectOriginalCopy);
        };

        function loadClasses(item) {

            //Now we load the classes from the teaching data block to the selected subject.
            vm.classesList = [];
            console.log('loadClasses')
            console.log(vm.subjectSelected);

            vm.classesList = SubjectsService.getTeaching({id: vm.subjectSelected.subjectId}, function () {

                // Once received must be deleted the 'teachers' section of any object in the list and replace the
                // entry name class.class
                for (var a = 0; a < vm.classesList.length; a++) {

                    delete(vm.classesList[a].teachers);
                    vm.classesList[a] = vm.classesList[a].class;
                }


                vm.classesList = vm.classesList.map(function (item) {
                        item.value = item.course.toString().toLowerCase() + ' ' +
                            item.word.toLowerCase() + ' ' +
                            item.level.toLowerCase() + ' '
                        return item;
                    }
                );

                console.log(vm.classesList);
                vm.classesIsReady = true;

            }, function (error) {
                console.log('Any problem found when was retrieved the teachers list.');
                console.log(error);
            })

        }


    });