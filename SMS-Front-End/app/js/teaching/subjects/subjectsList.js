angular.module('subjects')
    .controller('subjectsListController', function ($scope, $mdDialog, SubjectsService) {

        var vm = this;

        vm.openNewSubjectDialog = openNewSubjectDialog;

        // To control the loading spinner.
        vm.dataIsReady = false;

        activate();

        ///////////////////////////////////////////////////////////
        function activate() {

            console.log('Activating subjectsListController controller.')

            vm.subjectsList = SubjectsService.query({}, function () {
                vm.dataIsReady = true;
            }, function (error) {
                console.log('Any problem found when was retrieved the subjects list.');
                console.log(error);
            })

        }

        /**
         * Open the floating dialog to create a new subject.
         */
        function openNewSubjectDialog() {
            $mdDialog.show({
                locals: {parentScope: $scope, parentController: vm}, controller: 'newSubjectDialogController',
                controllerAs: 'vm', templateUrl: 'app/views/teaching/subjects/newSubjectDialog.html'
            }).then(function () {}, function () {});
        }


    });
