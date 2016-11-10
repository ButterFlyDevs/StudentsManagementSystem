angular.module('teachers')
    .controller('teachersProfileController', function ($scope, moment, $resource, $state, $stateParams, $mdDialog, TeachersService, AssociationsService, ImpartsService, toastService, globalService) {

        var vm = this;

        vm.teacherId = $stateParams.teacherId
        vm.updateButtonEnable = false;
        vm.associationsList = null;

        vm.formUpdated = formUpdated




        // References to functions.
        vm.addRelation = addRelation;
        vm.updateTeacher = updateTeacher;
        vm.showDeleteTeacherConfirm = showDeleteTeacherConfirm

        vm.defaultAvatar = globalService.defaultAvatar;





        activate();

        ///////////////////////////////////////////////////////////////////
        function activate() {
            console.log('Activating teachersProfileController controller.')
            vm.addButtonEnable = false;
            loadData();
        }

        function loadData(){
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

            $scope.$watch('vm.teacher', function(newValue, oldValue) {
                if(newValue != oldValue) {
                    $scope.teacherModelHasChanged = !angular.equals(vm.teacher, vm.teacherOriginalCopy);
                }
                compare()
            }, true);


        }, function (error) {
            console.log('Get teacher process fail.')
            console.log(error)
            // Here we don't use toastService because in the view will appear a message.
            vm.teacher = null;
        })


            vm.teacherImparts = TeachersService.getImparts({id: vm.teacherId},
                function () {
                    console.log('Teachers imparts')
                    console.log(vm.teacherImparts)

                    // ### Do a copy to save process. ###
                    vm.teacherImpartsOriginalCopy = angular.copy(vm.teacherImparts);

                    $scope.teacherImpartsModelHasChanged = false;

                    $scope.$watch('vm.teacherImparts', function(newValue, oldValue) {
                    if(newValue != oldValue) {
                        $scope.teacherImpartsModelHasChanged = !angular.equals(vm.teacherImparts, vm.teacherImpartsOriginalCopy);
                    }
                    compare()
                }, true);

                }, function(error){
                      console.log('Get teacher imparts process fail.')
                            console.log(error)
                            toastService.showToast('Error obteniendo la docencia del profesor.')
                }
            )
        }

        function formUpdated(){
            console.log('formUpdated')
        }

        function compare(){
            console.log('comparing changes ');

            if ($scope.teacherModelHasChanged){
                console.log("teacher Model has changed.")
            }else{
               console.log("teacher Model is equal.")
            }
            if ($scope.teacherImpartsModelHasChanged){
                console.log("teacher Imparts Model has changed.")
            }else{
               console.log("teacher Imparts Model is equal.")
            }

            if ($scope.teacherModelHasChanged || $scope.teacherImpartsModelHasChanged){
                vm.updateButtonEnable = true;
            }else{
                vm.updateButtonEnable = false;
            }
        }

        /**
         * Open the dialog to add a relation to this teacher.
         * The add action is done in addUserToProjectController
         */
        function addRelation() {

            $mdDialog.show({
                locals: {parentScope: $scope, parentController: vm},
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
        function deleteUser() {

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
                    deleteUser();
                },
                function () {
                    console.log('Del teacher operation canceled.')
                }
            );
        };


        /** Update teacher data in server.
         * Call to server with PUT method ($update = PUT) using vm.teacher that is
         * a instance of TeachersService.*/
        function updateTeacher() {
            console.log('Calling updateTeacher() function.')


            if ($scope.teacherModelHasChanged) { // We update teacher data.
                // A dirty solution to problem that does that the date is saved with a day minus.
                vm.teacher.birthdate.setDate(vm.teacher.birthdate.getDate() + 1);
                vm.teacher.$update(
                    function () { // Success
                        console.log('Success saving the teacher.')
                        toastService.showToast('Profesor actualizado con éxito.')
                    },
                    function (error) { // Fail
                        console.log('Error saving the teacher.')
                        console.log(error)
                        toastService.showToast('Error actualizando al profesor.')
                    });
            }

            if ($scope.teacherImpartsModelHasChanged) { // We update the teacher imparts info.

                console.log('teacherImpartsOriginalCopy')
                console.log(vm.teacherImpartsOriginalCopy)
                console.log('teacherImparts')
                console.log(vm.teacherImparts)
                // Algorithm that compare both data blocks and save or delete accordingly.
                processDiferences(vm.teacherImpartsOriginalCopy, vm.teacherImparts)


            }

            // It reloaded all data to avoid problems.
            // How wait to exit from teacher.$update
            loadData();


        }


        function delImpart(id){
          console.log('Deleting impart relation '+ id )
        }

        function newImpart(classId, subjectId){

          // This function will decide if it need create a new A
          // relation before to create new I relation with the teacher related.

          console.log('Creating new impart relation:')
          console.log('classId: ' + classId)
          console.log('subjectId: ' + subjectId)

            var exists = false;
            var index = -1;
            for (var i=0; i<vm.associationsList.length; i++)
                if (vm.associationsList[i].classId == classId &&
                    vm.associationsList[i].subjectId == subjectId) {
                    exists = true;
                    index = i;
                }

            if(exists){ //We need create only a new Imparts relation.

                console.log('Creating a new Imparts relation');
                var newImpart = new ImpartsService({data: {associationId: vm.associationsList[index].associationId,
                                                           teacherId: vm.teacherId}});
                newImpart.$save(
                    function(){ // Success
                        console.log('Success saving the impart.');
                        console.log(newImpart)
                        toastService.showToast('Relación imparte guardada con éxito.')
                    },
                    function(error){ // Fail
                        console.log('Error saving the impart relation.');
                        console.log(newImpart)
                        console.log(error);
                        toastService.showToast('Error al guardar relación imparte.')
                    });

            }else{ // We need create a new Association relation and before a new Imparts relation.
                console.log('Creating a new Association relation and Imparts relation.');

                var newAssociation = new AssociationsService({data: {classId: classId, subjectId: subjectId}});
                newAssociation.$save(
                    function () { // Success
                        console.log('Success saving the association.');
                        console.log(newAssociation);

                        // Now we save the impart with this associationId

                        var newImpart = new ImpartsService({data: {associationId: newAssociation.associationId,
                                                                   teacherId: vm.teacherId}})
                        newImpart.$save(
                            function(){ // Success
                                console.log('Success saving the impart.')
                                console.log(newImpart)
                                toastService.showToast('Relación imparte guardada con éxito.')
                            },
                            function(error){ // Fail
                                console.log('Error saving the impart relation.');
                                console.log(error);
                                toastService.showToast('Error al guardar relación imparte.')
                            })
                    },
                    function (error) { // Fail
                        console.log('Error saving the association.')
                        console.log(error)
                    });



            }

        }

        function processDiferences(original, modified){
          // console.log(original)
          // console.log(modified)

          // Deleted review

          if(original.length !== 0)
            for (var i=0; i<original.length ; i++){
              var index = -1;
              for (var j=0; j<modified.length; j++)
                if(modified[j].subject.subjectId == original[i].subject.subjectId)
                  index = j;
              if(index == -1)
                for(var c=0; c<original[i].classes.length; c++)
                  delImpart(original[i].classes[c].impartId)
              else
                for(var c2=0; c2<original[i].classes.length; c2++){
                  indexC = -1;
                  for(var d=0; d<modified[index].classes.length; d++)
                    if(original[i].classes[c2].classId == modified[index].classes[d].classId)
                      indexC = d;
                  if (indexC == -1)
                    delImpart(original[i].classes[c2].impartId)
                }

            }

            // Created item review

           if(modified.lenght !== 0)
             for (var a=0; a<modified.length; a++){
               var index3 = -1;
               for (var b=0; b<original.length; b++)
                 if (original[b].subject.subjectId == modified[a].subject.subjectId)
                   index3=b;
               if(index3==-1)
                 for(var h=0; h<modified[a].classes.length; h++)
                   newImpart(modified[a].classes[h].classId, modified[a].subject.subjectId);
               else
                 for(var m=0; m<modified[a].classes.length; m++){
                   var index4 = -1;
                   for (var n=0; n<original[index3].classes.length; n++)
                     if(original[index3].classes[n].classId == modified[a].classes[m].classId)
                       index4 = n;
                   if(index4 == -1)
                     newImpart(modified[a].classes[m].classId, modified[a].subject.subjectId);
                 }
             }

        }



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