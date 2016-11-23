/**
 * @ngdoc controller
 * @name myapp.controller:addRelationController
 *
 * @description
 * This is the controller to addRelationTemplate.
 */
angular.module('teachers')
    .controller('addRelationController',function($scope, $resource, $mdDialog, $stateParams, TeachersService, SubjectsService, ClassesService, AssociationsService, parentController){

            var vm = this;



            // References to functions.
            vm.closeDialog = closeDialog;
            vm.saveRelation = saveRelation;
            vm.checkRelationSelected = checkRelationSelected;

            vm.subjectSelected = -1;
            vm.classSelected = -1;
            vm.associationId = -1;

            vm.associationRelationExists = true;

            var itsAboutTeacher = false;
            vm.impartRelationExists = false;

            var itsAboutStudent = false;
            vm.enrollmentRelationExists = false;

            // Specifically vars to control buttons.
            vm.createNewAssociationCheckboxValue = false;
            vm.addButtonEnable = false;

            activate();

            ///////////////////////////////////////////////////////////
            function activate() {
                console.log('Activating addRelation controller.')

                console.log(parentController.controllerName);

                if(parentController.controllerName == 'teachersProfileController') {
                    itsAboutTeacher = true;
                    console.log('Its about teacher')
                }
                if(parentController.controllerName == 'studentsProfileController') {
                    itsAboutStudent = true;
                    console.log('Its about student')
                }



                // We need all subjects
                vm.subjectsList = SubjectsService.query({}, function(){
                    console.log('List of subjects retrieved.')
                    console.log(vm.subjectsList)
                }, function(){
                    console.log('Any problem found when was retrieved the subjects list.')
                })

                // We need all classes
                vm.classesList = ClassesService.query({}, function(){
                    console.log('List of classes retrieved.')
                    console.log(vm.classesList)
                },function(){
                    console.log('Any problem found when was retrieved the classes list.')
                })

                // We need all associations
                parentController.associationsList = AssociationsService.query({}, function(){
                    console.log('List of associations retrieved.')
                    // This way we have the same info in both controllers.
                    vm.associationsList = parentController.associationsList;
                    console.log(vm.associationsList)
                },function(){
                    console.log('Any problem found when was retrieved the associations list.')
                })

            }

            // Function to close the dialog
            function closeDialog() {
                $mdDialog.cancel();
            }

            // Function to save relation in the model of parent, in parentController.teacherImparts
            function saveRelation(){

                console.log('saveRelation function called')

                var list = null;
                if (itsAboutTeacher)
                    list = parentController.teacherImparts;
                if (itsAboutStudent)
                    list = parentController.studentEnrollments;



                console.log(list)
                console.log(list.length)

                var exists = false;

                if (itsAboutTeacher)
                    // We add the new relation in the parentController array teacherImparts, obviously with the same format.
                    // It searched if the subject exists in the list.
                    for (var i=0; i<list.length; i++){

                        // If the subject already exists in the list
                        if (list[i].subject.subjectId == vm.subjectSelected){
                            exists = true;
                            // We add the class inside a class list inside of item:

                            var index=-1;
                            for(var j=0; j<vm.classesList.length; j++)
                              if(vm.classesList[j].classId == vm.classSelected){index=j;break;}



                            var new_class = {classId: vm.classSelected,
                                         course: vm.classesList[index].course,
                                         level: vm.classesList[index].level,
                                         word: vm.classesList[index].word}

                            console.log(new_class)

                            list[i].classes.push(new_class)

                        }
                    }
                if (itsAboutStudent)
                    // We add the new relation in the parentController array studentEnrollments, obviously with the same format.
                    // It searched if the class exists in the list.
                    for (var i=0; i<list.length; i++){

                        // If the class already exists in the list
                        if (list[i].class.classId == vm.classSelected){
                            exists = true;
                            // We add the subject inside a subjects list inside of item:
                            var index=-1;
                            for(var j=0; j<vm.subjectsList.length; j++)
                              if(vm.subjectsList[j].subjectId == vm.subjectSelected){index=j;break;}

                            var new_subject = {subjectId: vm.subjectSelected, name: vm.subjectsList[index].name}
                            console.log(new_class)
                            list[i].subjects.push(new_subject)
                        }
                    }



                if (!exists){

                    if(itsAboutTeacher) {
                        console.log('REACCHHHERR')
                        // We need create the subject in list and insert the class inside.
                        var indexClass = -1;
                        for (var j = 0; j < vm.classesList.length; j++)
                            if (vm.classesList[j].classId == vm.classSelected) {
                                indexClass = j;
                                break;
                            }
                        var indexSubject = -1;
                        for (var k = 0; k < vm.subjectsList.length; k++)
                            if (vm.subjectsList[k].subjectId == vm.subjectSelected) {
                                indexSubject = k;
                                break;
                            }
                        var new_subject = {
                            subjectId: vm.subjectSelected,
                            name: vm.subjectsList[indexSubject].name
                        }
                        var new_class = {
                            classId: vm.classSelected,
                            course: vm.classesList[indexClass].course,
                            level: vm.classesList[indexClass].level,
                            word: vm.classesList[indexClass].word
                        }
                        var classes_list = []
                        classes_list.push(new_class)
                        list.push({subject: new_subject, classes: classes_list})
                    }

                    if(itsAboutStudent) {
                        console.log('STUDEEEENT')
                        // We need create the class in list and insert the subject inside.
                        var indexSubject = -1;
                        for (var j = 0; j < vm.subjectsList.length; j++)
                            if (vm.subjectsList[j].subjectId == vm.subjectSelected) {
                                indexSubject = j;
                                break;
                            }


                        var indexClass = -1;
                        for (var k = 0; k < vm.classesList.length; k++)
                            if (vm.classesList[k].classId == vm.classSelected) {
                                indexClass = k;
                                break;
                            }

                        var new_class = {
                            classId: vm.classSelected,
                            course: vm.classesList[indexClass].course,
                            level: vm.classesList[indexClass].level,
                            word: vm.classesList[indexClass].word
                        }

                        var new_subject = {
                            subjectId: vm.subjectSelected,
                            name: vm.subjectsList[indexSubject].name
                        }

                        var subjects_list = []
                        subjects_list.push(new_subject)
                        list.push({class: new_class, subjects: subjects_list})
                    }

                }

                console.log(list)

                $mdDialog.cancel();

            }

            function checkRelationSelected(subjectSelected, classSelected) {

                console.log('Executing checkRelationSelected')





                // We first check if the relation between the class and the subject (association) already exists.
                if (subjectSelected != -1 && classSelected != -1 ) {

                    vm.associationRelationExists = false;
                    vm.impartRelationExists = false;
                    vm.enrollmentRelationExists = false;


                    /* Primero comprobamos si la relación "association" existe ya en el servidor con la lista de asociaciones que le pedimos.
                    independientemente de si estamos tratando con una profesor o un estudiante.
                     */
                    for (var i = 0; i < vm.associationsList.length; i++) {
                        if (vm.associationsList[i].subjectId == subjectSelected && vm.associationsList[i].classId == classSelected) {
                            vm.associationRelationExists = true;
                            console.log('detectada en el servidor')
                        }
                    }

                    if(itsAboutTeacher)
                        /* Después comprobamos si la relación existe porque se haya creado en una iteración previa en teacherImparts
                         que aún no se ha subido al servidor. */
                        for (var i=0; i < parentController.teacherImparts.length; i++)
                            if (parentController.teacherImparts[i].subject.subjectId == subjectSelected)
                                for (var j = 0; j < parentController.teacherImparts[i].classes.length; j++)
                                    if (parentController.teacherImparts[i].classes[j].classId == classSelected) {
                                        vm.associationRelationExists = true;
                                        vm.impartRelationExists = true; // Tb vemos que la relacion imparte con este profe existe.
                                    }

                    if(itsAboutStudent)
                        /* Después comprobamos si la relación existe porque se haya creado en una iteración previa en studentEnrollments
                         que aún no se ha subido al servidor. */
                        for (var i=0; i < parentController.studentEnrollments.length; i++)
                            if (parentController.studentEnrollments[i].class.classId == classSelected)
                                for (var j = 0; j < parentController.studentEnrollments[i].subjects.length; j++)
                                    if (parentController.studentEnrollments[i].subjects[j].subjectId == subjectSelected) {
                                        vm.associationRelationExists = true;
                                        vm.enrollmentRelationExists = true; // Tb vemos que la relacion imparte con este profe existe.
                                    }





                    //Si la associacion ya existe se puede asociar este profesor a ella:
                    if(vm.associationRelationExists && (!vm.impartRelationExists && !vm.enrollmentRelationExists) )
                        vm.addButtonEnable = true;
                    else
                        vm.addButtonEnable = false;
                }



            }

});