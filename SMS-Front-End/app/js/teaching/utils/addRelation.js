/**
 * @ngdoc controller
 * @name myapp.controller:addRelationController
 *
 * @description
 * This is the controller to addRelationTemplate.
 */
angular.module('teachers')
    .controller('addRelationController', function ($scope, $resource, $mdDialog, $stateParams, TeachersService, StudentsService, SubjectsService, ImpartsService, ClassesService, AssociationsService, EnrollmentsService, parentController, itemTypeToAdd, secondaryItem, toastService) {

        var vm = this;


        // References to functions.
        vm.closeDialog = closeDialog;
        vm.saveRelation = saveRelation;
        vm.checkSelectedItem = checkSelectedItem;


        vm.exchangeVar = null;

        vm.subjectSelected = -1;
        vm.classSelected = -1;

        // Errors management.
        vm.errorExists = true; //Becuase normally when the dialog is open the save button is disabled.
        vm.errorMessage = '';

        // Info messages management.
        vm.infoExists = false;
        vm.infoMessage = '';


        vm.itemSelected = -1;

        vm.associationId = -1;

        vm.teacherSelected = -1;


        vm.associationExists = false;
        vm.selectedAssociationId = -1;


        vm.itsAboutTeacher = false;
        vm.impartRelationExists = false;

        vm.itsAboutStudent = false;
        vm.enrollmentRelationExists = false;

        vm.itsAboutSubject = false;

        // When is used from class view.
        vm.itsAboutClass = false;
        vm.subjectRelationExists = false;

        // Specifically vars to control buttons.
        vm.createNewAssociationCheckboxValue = false;
        vm.addButtonEnable = false;

        activate();

        ///////////////////////////////////////////////////////////
        function activate() {
            console.log('Activating addRelation controller.')

            vm.itemTypeToAdd = itemTypeToAdd;

            if (parentController.controllerName == 'teachersProfileController') {
                vm.itsAboutTeacher = true;
                console.log('Its about teacher');
                vm.teacherId = parentController.teacherId;
                vm.teacherTeaching = parentController.teacherTeaching;

                if (vm.itemTypeToAdd == 'subject') {

                    /* When we add a subject to a teacher only can to do this with associating the
                     teacher to an existing association between a subject and a class. And we need check
                     if this exists alreay to show message or to create the new association in the case of it
                     doesn't exists.
                     */

                    vm.subjectsList = SubjectsService.query({}, function () {
                        console.log('List of subjects retrieved.');
                        console.log(vm.subjectsList);
                    }, function () {
                        console.log('Any problem found when was retrieved the subjects list.');
                    });

                    vm.classesList = ClassesService.query({}, function () {
                        console.log('List of clases retrieved.');
                        console.log(vm.classesList);
                    }, function () {
                        console.log('Any problem found when was retrieved the classes list.');
                    });

                    vm.associationsList = AssociationsService.query({}, function () {
                        console.log('List of associations retrieved.');
                        console.log(vm.associationsList);
                    }, function () {
                        console.log('Any problem found when was retrieved the associations list.');
                    })

                } else if (vm.itemTypeToAdd == 'class') {

                    /* When we add a subject to a teacher only can to do this with associating the
                     teacher to an existing association between a subject and a class. And we need check
                     if this exists alreay to show message or to create the new association in the case of it
                     doesn't exists.
                     */

                    vm.classesList = ClassesService.query({}, function () {
                        console.log('List of clases retrieved.');
                        console.log(vm.classesList);
                    }, function () {
                        console.log('Any problem found when was retrieved the classes list.');
                    });

                    // We need check if the association exists previously to add a teacher to impart on it.
                    vm.associationsList = AssociationsService.query({}, function () {
                        console.log('List of associations retrieved.');
                        console.log(vm.associationsList);
                    }, function () {
                        console.log('Any problem found when was retrieved the associations list.');
                    })

                }

            }
            if (parentController.controllerName == 'studentsProfileController') {
                vm.itsAboutStudent = true;
                console.log('Its about student');
                vm.studentId = parentController.studentId;
                vm.studentTeaching = parentController.studentTeaching;

                // From student profile view we want add a new relatión with it and a association relation between
                // a subject and a class.
                if (vm.itemTypeToAdd == 'class-subject') {

                    vm.associationsList = AssociationsService.query({}, function () {
                        console.log('List of associations retrieved.');
                        console.log(vm.associationsList);
                    }, function () {
                        console.log('Any problem found when was retrieved the associations list.');
                    });

                    vm.classesList = ClassesService.query({}, function () {
                        console.log('List of clases retrieved.');
                        console.log(vm.classesList);
                    }, function () {
                        console.log('Any problem found when was retrieved the classes list.');
                    });

                    vm.subjectsList = SubjectsService.query({}, function () {
                        console.log('List of subjects retrieved.');
                        console.log(vm.subjectsList);
                    }, function () {
                        console.log('Any problem found when was retrieved the subjects list.');
                    });

                }
            }
            if (parentController.controllerName == 'subjectsProfileController') {

                vm.itsAboutSubject = true;
                console.log('It\'s about subject')
                vm.subjectId = parentController.subjectId;
                vm.subjectTeaching = parentController.subjectTeaching;


                if (vm.itemTypeToAdd == 'class') {
                    vm.classesList = ClassesService.query({}, function () {
                        console.log('List of clases retrieved.')
                        console.log(vm.classesList)
                    }, function () {
                        console.log('Any problem found when was retrieved the classes list.')
                    })
                }

                // The actions is over the class view, in the process to add a teacher to subject (inside of this class).
                if (vm.itemTypeToAdd == 'teacher') {
                    // We need all teacher
                    vm.teachersList = TeachersService.query({}, function () {
                        console.log('List of teachers retrieved.');
                        console.log(vm.teachersList);
                    }, function () {
                        console.log('Any problem found when was retrieved the teachers list.')
                    });
                }

                if (vm.itemTypeToAdd == 'student') {

                    // We need all subjects of this class, to select in wich the student want to be enrolled.
                    vm.subjectTeaching = parentController.subjectTeaching;


                    // We need all students
                    vm.studentsList = StudentsService.query({}, function () {
                        console.log('List of students retrieved.');
                        console.log(vm.studentsList);
                    }, function () {
                        console.log('Any problem found when was retrieved the students list.')
                    });

                }


            }
            if (parentController.controllerName == 'classesProfileController') {

                vm.itsAboutClass = true;
                console.log('Its about class');
                vm.classId = parentController.classId;
                vm.classTeaching = parentController.classTeaching;


                if (vm.itemTypeToAdd == 'subject') {
                    // We need all subjects
                    vm.subjectsList = SubjectsService.query({}, function () {
                        console.log('List of subjects retrieved.');
                        console.log(vm.subjectsList);
                    }, function () {
                        console.log('Any problem found when was retrieved the subjects list.')
                    });
                }


                // The actions is over the class view, in the process to add a teacher to subject (inside of this class).
                if (vm.itemTypeToAdd == 'teacher') {
                    // We need all teacher
                    vm.teachersList = TeachersService.query({}, function () {
                        console.log('List of teachers retrieved.');
                        console.log(vm.teachersList);
                    }, function () {
                        console.log('Any problem found when was retrieved the teachers list.')
                    });
                }

                if (vm.itemTypeToAdd == 'student') {

                    // We need all subjects of this class, to select in wich the student want to be enrolled.
                    vm.classTeaching = parentController.classTeaching;


                    // We need all students
                    vm.studentsList = StudentsService.query({}, function () {
                        console.log('List of students retrieved.');
                        console.log(vm.studentsList);
                    }, function () {
                        console.log('Any problem found when was retrieved the students list.')
                    });

                }

            }

        }

        // Function to close the dialog
        function closeDialog() {
            $mdDialog.cancel();
        }

        // Function to save relation in the model of parent, in parentController.teacherImparts
        function saveRelation() {

            console.log('saveRelation function called')

            if (vm.itsAboutClass && vm.itemTypeToAdd == 'subject') {
                var newAssociation = new AssociationsService({subjectId: vm.itemSelected, classId: vm.classId});
                newAssociation.$save(
                    function () { // Success
                        toastService.showToast('Asignatura asociada con éxito.')
                        parentController.loadTeaching();  // Reload the teaching data block.
                    },
                    function (error) { // Fail
                        toastService.showToast('Error asociando la asignatura a este grupo.')
                    });
            }
            if (vm.itsAboutClass && vm.itemTypeToAdd == 'teacher') {


                // secondaryItem is the para used to know the subject related in the class view.
                var newImpart = new ImpartsService({teacherId: vm.itemSelected, associationId: secondaryItem});
                newImpart.$save(
                    function () { // Success
                        toastService.showToast('Relación creada con éxito.')
                        parentController.loadTeaching();  // Reload the teaching data block.
                    },
                    function (error) { // Fail
                        toastService.showToast('Error creando la relación.')
                    });
            }
            if (vm.itsAboutClass && vm.itemTypeToAdd == 'student') {


                console.log('saving');
                console.log(vm.associationSelected);

                console.log(vm.studentSelected);
                /*
                 Si la associaiton seleccionada es 0 hay que matricular al estudiante en todas las
                 asignaturas.constructor.

                 Hay que montar un deferred.
                 */

                //Si la associacion es una en concreto pues se matricula a esa en concreto.
                if (vm.associationSelected != 0) {

                    EnrollmentsService.save({associationId: vm.associationSelected, studentId: vm.studentSelected},
                        function () { // Success
                            toastService.showToast('Relación creada con éxito.')
                            parentController.loadStudents(parentController.associationIdSelected);  // Reload the teaching data block.
                        },
                        function (error) { // Fail
                            toastService.showToast('Error creando la relación.')
                        });

                } else {
                    // We want enrollment a student in all subjects that are associated with this class:
                    console.log('Multiple enrollment.');
                    var classTeaching = parentController.classTeaching;
                    var associationsList = []
                    for (var i = 0; i < classTeaching.length; i++)
                        associationsList.push(classTeaching[i].subject.associationId);

                    console.log(associationsList)
                    console.log(vm.studentSelected)
                    EnrollmentsService.multiple_save({associationsIds: associationsList, studentId: vm.studentSelected},
                        function () { // Success
                            toastService.showToast('Matriculación múltiple creada con éxito.')
                            parentController.loadStudents(parentController.associationIdSelected);  // Reload the teaching data block.
                        },
                        function (error) { // Fail
                            toastService.showToast('Error creando la matriculación múltiple.')
                        });

                }


                /*
                 // secondaryItem is the para used to know the subject related in the class view.
                 var newImpart = new ImpartsService({teacherId: vm.itemSelected, associationId: secondaryItem});
                 newImpart.$save(
                 function () { // Success
                 toastService.showToast('Relación creada con éxito.')
                 parentController.loadTeaching();  // Reload the teaching data block.
                 },
                 function (error) { // Fail
                 toastService.showToast('Error creando la relación.')
                 });
                 */
            }

            if (vm.itsAboutSubject && vm.itemTypeToAdd == 'class') {
                var newAssociation = new AssociationsService({classId: vm.itemSelected, subjectId: vm.subjectId});
                newAssociation.$save(
                    function () { // Success
                        toastService.showToast('Grupo asociado con éxito.')
                        parentController.loadTeaching();  // Reload the teaching data block.
                    },
                    function (error) { // Fail
                        toastService.showToast('Error asociando el grupo a esta asignatura.')
                    });
            }
            if (vm.itsAboutSubject && vm.itemTypeToAdd == 'teacher') {

                // secondaryItem is the para used to know the subject related in the class view.
                var newImpart = new ImpartsService({teacherId: vm.itemSelected, associationId: secondaryItem});
                newImpart.$save(
                    function () { // Success
                        toastService.showToast('Relación creada con éxito.')
                        parentController.loadTeaching();  // Reload the teaching data block.
                    },
                    function (error) { // Fail
                        toastService.showToast('Error creando la relación.')
                    });
            }
            if (vm.itsAboutSubject && vm.itemTypeToAdd == 'student') {


                console.log('saving');
                console.log(vm.associationSelected);

                console.log(vm.studentSelected);
                /*
                 Si la associaiton seleccionada es 0 hay que matricular al estudiante en todas las
                 asignaturas.constructor.

                 Hay que montar un deferred.
                 */

                //Si la associacion es una en concreto pues se matricula a esa en concreto.
                if (vm.associationSelected && vm.studentSelected) {

                    EnrollmentsService.save({associationId: vm.associationSelected, studentId: vm.studentSelected},
                        function () { // Success
                            toastService.showToast('Relación creada con éxito.');
                            parentController.loadStudents(parentController.associationIdSelected);  // Reload the teaching data block.
                        },
                        function (error) { // Fail
                            toastService.showToast('Error creando la relación.')
                        });

                }

            }

            if (vm.itsAboutTeacher && vm.itemTypeToAdd == 'subject') {
                // When we do that one teacher impart to an association between a class and subject.

                if (vm.associationExists) {
                    var newImpart = new ImpartsService({
                        teacherId: vm.teacherId,
                        associationId: vm.selectedAssociationId
                    });
                    newImpart.$save(
                        function () { // Success
                            toastService.showToast('Relación creada con éxito.')
                            parentController.loadTeaching();  // Reload the teaching data block.
                        },
                        function (error) { // Fail
                            toastService.showToast('Error creando la relación.')
                        });


                } else {

                    // First: create the association.
                    var newAssociation = new AssociationsService({
                        subjectId: vm.subjectSelected,
                        classId: vm.classSelected
                    });
                    newAssociation.$save(
                        function () { // Success
                            toastService.showToast('Asignatura asociada con éxito.');

                            // Second: Create the relation between the teacher and this.
                            var newImpart = new ImpartsService({
                                teacherId: vm.teacherId,
                                associationId: newAssociation.associationId
                            });
                            newImpart.$save(
                                function () { // Success
                                    toastService.showToast('Relación creada con éxito.')
                                    parentController.loadTeaching();  // Reload the teaching data block.
                                },
                                function (error) { // Fail
                                    toastService.showToast('Error creando la relación.')
                                });


                        },
                        function (error) { // Fail
                            toastService.showToast('Error asociando la asignatura a este grupo.')
                        });

                }

            }
            if (vm.itsAboutTeacher && vm.itemTypeToAdd == 'class') {
                // When we want to add another class in subject which this teacher impart his subject.
                // Maybe the relation betweeen the subject selected and the new class selecte doesn't exists.

                var associationExists = false;
                var associationId = null;

                for (var a = 0; a < vm.associationsList.length; a++)
                    if (vm.associationsList[a].classId == vm.exchangeVar.classId && vm.associationsList[a].subjectId == vm.exchangeVar.subjectId) {
                        associationExists = true;
                        associationId = vm.associationsList[a].associationId;
                    }


                // If exists we only need associate the teacher with it.
                if (associationExists) {
                    var newImpart = new ImpartsService({
                        teacherId: vm.teacherId,
                        associationId: associationId
                    });
                    newImpart.$save(
                        function () { // Success
                            toastService.showToast('Relación creada con éxito.')
                            parentController.loadTeaching();  // Reload the teaching data block.
                        },
                        function (error) { // Fail
                            toastService.showToast('Error creando la relación.')
                        });

                    // If not exists we need to do two steps.
                } else {

                    // First: create the association between the class selected in the dialog and the subject selected in the teacher view.
                    var newAssociation = new AssociationsService({
                        // Using the values in the exchange variable, from checkSelectedItem
                        subjectId: vm.exchangeVar.subjectId,
                        classId: vm.exchangeVar.classId
                    });
                    newAssociation.$save(
                        function () { // Success

                            // Second: Create the relation between the teacher and this.
                            var newImpart = new ImpartsService({
                                teacherId: vm.teacherId,
                                associationId: newAssociation.associationId
                            });
                            newImpart.$save(
                                function () { // Success
                                    toastService.showToast('Relación entre asignatura, grupo y profesor.creada con éxito.')
                                    parentController.loadTeaching();  // Reload the teaching data block.
                                },
                                function (error) { // Fail
                                    toastService.showToast('Error creando la relación multiple..')
                                });


                        },
                        function (error) { // Fail
                            toastService.showToast('Error asociando la asignatura a este grupo.')
                        });
                }

            }

            if (vm.itsAboutStudent && vm.itemTypeToAdd == 'class-subject') {
                // When we do that one teacher impart to an association between a class and subject.

                if (vm.associationExists) {
                    var newEnrollment = new EnrollmentsService({
                        studentId: vm.studentId,
                        associationId: vm.selectedAssociationId
                    });
                    newEnrollment.$save(
                        function () { // Success
                            toastService.showToast('Relación creada con éxito.')
                            parentController.loadTeaching();  // Reload the teaching data block.
                        },
                        function (error) { // Fail
                            toastService.showToast('Error creando la relación.')
                        });


                } else {

                    // First: create the association.
                    var newAssociation = new AssociationsService({
                        subjectId: vm.subjectSelected,
                        classId: vm.classSelected
                    });
                    newAssociation.$save(
                        function () { // Success
                            toastService.showToast('Asignatura asociada con éxito.');

                            var newEnrollment = new EnrollmentsService({
                                studentId: vm.studentId,
                                associationId: newAssociation.associationId
                            });
                            newEnrollment.$save(
                                function () { // Success
                                    toastService.showToast('Relación creada con éxito.')
                                    parentController.loadTeaching();  // Reload the teaching data block.
                                },
                                function (error) { // Fail
                                    toastService.showToast('Error creando la relación.')
                                });


                        },
                        function (error) { // Fail
                            toastService.showToast('Error asociando la asignatura a este grupo.')
                        });

                }

            }

            $mdDialog.cancel();

        }

        function checkSelectedItem(firstItemSelected, secondItemSelected) {

            function checkInside() {
                var error = false;
                for (var i = 0; i < vm.specificStudentList.length; i++) {
                    if (vm.specificStudentList[i].studentId == secondItemSelected) { //secondItemSelected is the studentId of the student.
                        vm.errorExists = true;
                        error = true;
                        if (firstItemSelected == 0) {
                            vm.errorMessage = "El estudiante ya se encuentra matriculado en alguna asignatura de esta clase."
                        } else {
                            vm.errorMessage = "El estudiante ya se encuentra matriculado en esta asignatura."
                        }
                    }
                }
                if (firstItemSelected == 0 && !error) {
                    vm.infoExists = true;
                    vm.infoMessage = 'Ojo, se matriculará a todas las asignaturas de la clase.'
                }
            }

            vm.errorExists = false;
            vm.infoExists = false;
            vm.itemSelected = firstItemSelected;

            if (vm.itsAboutSubject && vm.itemTypeToAdd == 'class') {
                // firstItemSelected is classSelected that is classId
                console.log(firstItemSelected)
                if (firstItemSelected)
                // We check if the classId already exists in the subjectTeaching datablock.
                    for (var i = 0; i < vm.subjectTeaching.length; i++)
                        if (vm.subjectTeaching[i].class.classId == firstItemSelected) {
                            console.log('YEAH')
                            vm.errorExists = true;
                            vm.errorMessage = "El grupo ya está asociado a esta asignatura.";
                        }
            }
            if (vm.itsAboutSubject && vm.itemTypeToAdd == 'teacher') {


                console.log(firstItemSelected)
                console.log(secondaryItem)

                if (firstItemSelected != -1 && secondaryItem !== 'undefined') {

                    /* In this case firstItemSelected is the teacherId. Secondary item is the associationId form
                     classesProfile when the user open the dialog and click in add new teacher, so, the id of
                     association between class and subject is passed to addRelation like secondaryItem. */

                    // Check if the teacher impart the subject in this group already.
                    for (var i = 0; i < vm.subjectTeaching.length; i++)
                        if (vm.subjectTeaching[i].class.associationId == secondaryItem)
                            if (vm.subjectTeaching[i].teachers)
                                for (var j = 0; j < vm.subjectTeaching[i].teachers.length; j++)
                                    if (vm.subjectTeaching[i].teachers[j].teacherId == firstItemSelected) {
                                        vm.errorExists = true;
                                        vm.errorMessage = "El profesor ya imparte la asignatura a este grupo."
                                    }
                } else
                // A teacher must be select. In this case isn't necessary show any message.
                    vm.errorExists = true;
            }
            if (vm.itsAboutSubject && vm.itemTypeToAdd == 'student') {

                console.log('checkSelectedItem')
                console.log(firstItemSelected)
                console.log(secondItemSelected)

                /*In this case firstItemSelected must be a associationId (class related with subject)
                 and secondItemSelected must be a studentId. */

                if (firstItemSelected && secondItemSelected) {
                    console.log('maybe')

                    vm.specificStudentList = AssociationsService.getStudents({id: firstItemSelected},
                        function () {
                            console.log('specificStudentList from specific class in subject profile view');
                            console.log(vm.specificStudentList);
                            //checkInside();
                            if (vm.specificStudentList.length != 0) {
                                for (var i = 0; i < vm.specificStudentList.length; i++)
                                    if (vm.specificStudentList[i].studentId == secondItemSelected) {
                                        vm.errorExists = true;
                                        vm.errorMessage = "El estudiante ya se encuentra matriculado en esta asignatura en este grupo."
                                    }
                            }

                        },
                        function (error) {
                            console.log('Get specificStudentList students process fail.');
                            console.log(error);
                            toastService.showToast('Error obteniendo los alumnos inscritos a este grupo.');
                        }
                    );


                } else
                // The error: both fields have to be selected. But we don't show any erro message.
                    vm.errorExists = true;
            }

            if (vm.itsAboutClass && vm.itemTypeToAdd == 'subject') {

                //In this case firstItemSelected is a subjectId of a subject.

                if (firstItemSelected != -1)
                // We check if this subject already exists in the block.
                    for (var i = 0; i < vm.classTeaching.length; i++)
                        //console.log(vm.classTeaching[i].subject.subjectId)
                        if (vm.classTeaching[i].subject.subjectId == firstItemSelected) {
                            vm.errorExists = true;
                            vm.errorMessage = "La asignatura ya está asociada a este grupo."
                        }
            }
            if (vm.itsAboutClass && vm.itemTypeToAdd == 'teacher') {

                if (firstItemSelected != -1 && secondaryItem !== 'undefined') {

                    /* In this case firstItemSelected is the teacherId. Secondary item is the associationId form
                     classesProfile when the user open the dialog and click in add new teacher, so, the id of
                     association between class and subject is passed to addRelation like secondaryItem. */

                    // Check if the teacher impart the subject in this group already.
                    for (var i = 0; i < vm.classTeaching.length; i++)
                        if (vm.classTeaching[i].subject.associationId == secondaryItem)
                            if (vm.classTeaching[i].teachers)
                                for (var j = 0; j < vm.classTeaching[i].teachers.length; j++)
                                    if (vm.classTeaching[i].teachers[j].teacherId == firstItemSelected) {
                                        vm.errorExists = true;
                                        vm.errorMessage = "El profesor ya imparte la asignatura a este grupo."
                                    }
                } else
                // A teacher must be select. In this case isn't necessary show any message.
                    vm.errorExists = true;
            }
            if (vm.itsAboutClass && vm.itemTypeToAdd == 'student') {

                console.log('checkSelectedItem')
                console.log(firstItemSelected)
                console.log(secondItemSelected)

                //In this case firstItemSelected must be a associationId (subject related with class)
                // and secondItemSelected must be a studentId.

                if (firstItemSelected && secondItemSelected) {
                    console.log('maybe')


                    if (firstItemSelected == 0) {
                        /*We need all students of this class, because if student select already exists in the list, this action must be invalid
                         and specific info message must be showed.*/
                        vm.specificStudentList = ClassesService.getStudents({id: parentController.classId},
                            function () {
                                console.log('specificStudentList form all class');
                                console.log(vm.specificStudentList);
                                checkInside();
                            },
                            function (error) {
                                console.log('Get class students process fail.');
                                console.log(error);
                                toastService.showToast('Error obteniendo los alumnos inscritos a este grupo.');
                            }
                        );
                    } else {
                        vm.specificStudentList = AssociationsService.getStudents({id: firstItemSelected},
                            function () {
                                console.log('specificStudentList from specific subject in class');
                                console.log(vm.specificStudentList);
                                checkInside();
                            },
                            function (error) {
                                console.log('Get SUBJECT- class students process fail.');
                                console.log(error);
                                toastService.showToast('Error obteniendo los alumnos inscritos a este grupo.');
                            }
                        );
                    }

                } else
                // The error: both fields have to be selected. But we don't show any erro message.
                    vm.errorExists = true;
            }

            if (vm.itsAboutTeacher && vm.itemTypeToAdd == 'subject') {

                if (firstItemSelected && secondItemSelected != -1) {

                    console.log(vm.teacherTeaching)
                    console.log(firstItemSelected)
                    console.log(secondItemSelected)
                    /* In this case firstItemSelected is the subjectSelect (subjectId).
                     For other hand SecondaryItem is classSelected (classId)*/

                    // We check first if the pair subjectId - classId exists already in the teacherTeaching  data block.
                    for (var i = 0; i < vm.teacherTeaching.length; i++)
                        if (vm.teacherTeaching[i].subject.subjectId == firstItemSelected)
                            if (vm.teacherTeaching[i].classes)
                                for (var j = 0; j < vm.teacherTeaching[i].classes.length; j++)
                                    if (vm.teacherTeaching[i].classes[j].classId == secondItemSelected) {
                                        vm.errorExists = true;
                                        vm.errorMessage = "El profesor ya imparte la asignatura a este grupo."
                                    }


                    // After we check if this relation exists or must be created in this instant.
                    vm.associationExists = false;
                    console.log(vm.associationsList)
                    for (var i = 0; i < vm.associationsList.length; i++)
                        if (vm.associationsList[i].subjectId == firstItemSelected && vm.associationsList[i].classId == secondItemSelected) {
                            vm.associationExists = true;
                            vm.selectedAssociationId = vm.associationsList[i].associationId;
                        }

                    if (!vm.associationExists) {
                        vm.infoExists = true;
                        vm.infoMessage = 'La relacion entre la clase y la asignatura seleccionada no existe aun. Si acepta la creara al mismo tiempo.';
                    }


                } else
                // A subject and a class must be select. In this case isn't necessary show any message.
                    vm.errorExists = true;
            }
            if (vm.itsAboutTeacher && vm.itemTypeToAdd == 'class') {


                console.log(firstItemSelected);
                console.log(secondaryItem);

                if (firstItemSelected != -1 && secondaryItem !== 'undefined') {

                    var classId = firstItemSelected;
                    var teachingItem = secondaryItem;

                    // To use when we execute saveRelation function.
                    vm.exchangeVar = {classId: classId, subjectId: teachingItem.subject.subjectId}

                    for (var i = 0; i < teachingItem.classes.length; i++)
                        if (classId == teachingItem.classes[i].classId) {
                            vm.errorExists = true;
                            vm.errorMessage = "El profesor ya imparte la asignatura a este grupo."
                        }

                }
            }

            if (vm.itsAboutStudent && vm.itemTypeToAdd == 'class-subject') {

                if (firstItemSelected && secondItemSelected != -1) {

                    console.log(vm.teacherTeaching)
                    console.log(firstItemSelected)
                    console.log(secondItemSelected)

                    /* In this case firstItemSelected is the subjectSelect (subjectId).
                     For other hand secondItemSelected is classSelected (classId)*/

                    // We check first if the pair subjectId - classId exists already in the teacherTeaching  data block.
                    for (var i = 0; i < vm.studentTeaching.length; i++)
                        if (vm.studentTeaching[i].class.classId == secondItemSelected)
                            if (vm.studentTeaching[i].subjects)
                                for (var j = 0; j < vm.studentTeaching[i].subjects.length; j++)
                                    if (vm.studentTeaching[i].subjects[j].subjectId == firstItemSelected) {
                                        vm.errorExists = true;
                                        vm.errorMessage = "El alumno ya esta matriculado en esta asignatura en este grupo.";
                                    }


                    // After we check if this relation exists or must be created in this instant.
                    vm.associationExists = false;
                    console.log(vm.associationsList);
                    for (var i = 0; i < vm.associationsList.length; i++)
                        if (vm.associationsList[i].subjectId == firstItemSelected && vm.associationsList[i].classId == secondItemSelected) {
                            vm.associationExists = true;
                            vm.selectedAssociationId = vm.associationsList[i].associationId;
                        }

                    if (!vm.associationExists) {
                        vm.infoExists = true;
                        vm.infoMessage = 'La relación entre la clase y la asignatura seleccionada no existe aun. ' +
                            'Si acepta la creara al mismo tiempo que matricula al alumno.';
                    }


                } else
                // A subject and a class must be select. In this case isn't necessary show any message.
                    vm.errorExists = true;
            }

        }

    });