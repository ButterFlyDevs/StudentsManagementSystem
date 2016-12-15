angular.module('classes')
// Directive for generic chart, pass in chart options
    .directive('hcChart', function () {
        return {
            restrict: 'E',
            template: '<div></div>',
            scope: {
                options: '='
            },
            link: function (scope, element) {
                Highcharts.chart(element[0], scope.options);
            }
        };
    })
    .directive('chart', function () {
        return {
            restrict: 'E',
            replace: true,
            template: '<div></div>',
            scope: {
                config: '='
            },
            link: function (scope, element, attrs) {
                var chart;
                var process = function () {
                    var defaultOptions = {
                        chart: {renderTo: element[0]},
                    };
                    var config = angular.extend(defaultOptions, scope.config);
                    chart = new Highcharts.Chart(config);
                };
                process();
                $scope.$watch("config.series", function (newValue, oldValue) {
                    console.log('new data received');
                    console.log('newValue');
                    console.log(newValue);
                    console.log('oldValue');
                    console.log(oldValue);

                    process();
                });
                $scope.$watch("config.loading", function (loading) {
                    if (!chart) {
                        return;
                    }
                    if (loading) {
                        chart.showLoading();
                    } else {
                        chart.hideLoading();
                    }
                });
            }
        };
    })
    .directive('hcPieChart', function () {
        return {
            restrict: 'E',
            template: '<div></div>',
            scope: {
                title: '@',
                data: '='
            },
            link: function (scope, element) {
                Highcharts.chart(element[0], {
                    chart: {
                        type: 'pie'
                    },
                    title: {
                        text: scope.title
                    },
                    plotOptions: {
                        pie: {
                            allowPointSelect: true,
                            cursor: 'pointer',
                            dataLabels: {
                                enabled: true,
                                format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                            }
                        }
                    },
                    series: [{
                        data: scope.data
                    }]
                });
            }
        };
    })
    .controller('classesProfileController', function ($scope, $resource, $state, $stateParams, $mdDialog, ClassesService, toastService) {

        var vm = this;

        // Vars:
        vm.controllerName = 'classesProfileController';
        vm.classId = $stateParams.classId;
        vm.updateButtonEnable = false; // To control when the update button could be enabled.
        vm.defaultAvatar = 'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcThQiJ2fHMyU37Z0NCgLVwgv46BHfuTApr973sY7mao_C8Hx_CDPrq02g'

        // References to functions.
        vm.updateClass = updateClass;
        vm.showDeleteClassConfirm = showDeleteClassConfirm;
        vm.addRelation = addRelation;


        vm.classReport = null;
        activate();


        ///////////////////////////////////////////////////////////
        function activate() {
            console.log('Activating classesProfileController controller.')
            loadData();

        }


        function loadData() {

            // Retrieve all data from this class
            vm.class = ClassesService.get({id: vm.classId}, function () {
                console.log(vm.class);

                // ### Do a copy to save process. ###
                vm.classOriginalCopy = angular.copy(vm.class);

                $scope.classModelHasChanged = false;
                $scope.$watch('vm.class', function (newValue, oldValue) {
                    if (newValue != oldValue) {
                        $scope.classModelHasChanged = !angular.equals(vm.class, vm.classOriginalCopy);
                    }
                    compare();
                }, true);


            }, function (error) {
                console.log('Get class process fail.');
                console.log(error);
                vm.class = null;
            });


            vm.classStudents = ClassesService.getStudents({id: vm.classId},
                function () {
                    console.log('Class Students');
                    console.log(vm.classStudents);
                },
                function (error) {
                    console.log('Get class students process fail.');
                    console.log(error);
                    toastService.showToast('Error obteniendo los alumnos inscritos a este grupo.');
                }
            );


            vm.classTeaching = ClassesService.getTeaching({id: vm.classId},
                function () {
                    console.log('Class Teaching Data Block');
                    console.log(vm.classTeaching);

                    // ### Do a copy to save process. ###
                    vm.classTeachingOriginalCopy = angular.copy(vm.classTeaching);

                    $scope.classTeachingModelHasChanged = false;

                    $scope.$watch('vm.classTeaching', function (newValue, oldValue) {
                        if (newValue != oldValue) {
                            $scope.classTeachingModelHasChanged = !angular.equals(vm.classTeaching, vm.classTeachingOriginalCopy);
                        }
                        compare()
                    }, true);

                }, function (error) {
                    console.log('Get class subjects process fail.');
                    console.log(error);
                    toastService.showToast('Error obteniendo las asignaturas que se imparten en la clase.')
                }
            );

            vm.classReport = ClassesService.getReport({id: vm.classId},
                function () {
                    console.log('Class Report Data Block');
                    console.log(vm.classReport);

                    vm.chartConfig['series'][0]['data'] = [vm.classReport['students']['gender_percentage']['M'],
                                                           vm.classReport['students']['gender_percentage']['F']];
                    console.log(vm.chartConfig);

                    $scope.pieData = [{
                        name: "Chicos",
                        y: vm.classReport['students']['gender_percentage']['M']
                    },
                        {
                            name: "Chicas",
                            y: vm.classReport['students']['gender_percentage']['M']
                        }]
                }, function (error) {
                    console.log('Get class report process fail.');
                    console.og(error);
                    toastService.showToast('Error obteniendo las asignaturas que se imparten en la clase.')
                })

        }

        function compare() {
            if ($scope.classModelHasChanged || $scope.classTeachingModelHasChanged) {
                vm.updateButtonEnable = true;
            } else {
                vm.updateButtonEnable = false;
            }
        }

        /** Delete class in server.
         * Call to server with DELETE method ($delete= DELETE) using vm.class that is
         * a instance of ClassesService.*/
        function deleteClass() {

            vm.class.$delete(
                function () { // Success
                    console.log('Class deleted successfully.')
                    $state.go('classes')
                    toastService.showToast('Clase eliminada con éxito.')
                },
                function (error) { // Fail
                    console.log('Class deleted process fail.')
                    console.log(error)
                    toastService.showToast('Error eliminando la clase.')
                });

        }

        /** Show the previous step to delete item, a confirm message */
        function showDeleteClassConfirm() {

            var confirm = $mdDialog.confirm()
                .title('¿Está seguro de que quiere eliminar este grupo?')
                //.textContent('Si lo hace todos los alumnos quedarán ')
                //.ariaLabel('Lucky day')
                .ok('Estoy seguro')
                .cancel('Cancelar');

            $mdDialog.show(confirm).then(function () {
                deleteClass();
            }, function () {
                console.log('Operacion cancelada.')
            });

        };


        /** Update class data in server.
         * Call to server with PUT method ($update = PUT) using vm.class that is
         * a instance of ClassesService.*/
        function updateClass() {
            console.log('Calling updateClass() function.')
            vm.class.$update(
                function () { // Success
                    console.log('Class updated successfully.')
                    toastService.showToast('Clase actualizada con éxito.')
                },
                function (error) { // Fail
                    console.log('Error updating class.')
                    console.log(error)
                    toastService.showToast('Error actualizando la clase.')
                });
        }


        /*
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

        // Sample options for first chart
        vm.chartOptions = {
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: 0,
                plotShadow: false
            },
            title: {
                text: 'Browser<br>shares<br>2015',
                align: 'center',
                verticalAlign: 'middle',
                y: 40
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            plotOptions: {
                pie: {
                    dataLabels: {
                        enabled: true,
                        distance: -50,
                        style: {
                            fontWeight: 'bold',
                            color: 'white'
                        }
                    },
                    startAngle: -90,
                    endAngle: 90,
                    center: ['50%', '75%']
                }
            },
            series: [{
                type: 'pie',
                name: 'Browser share',
                innerSize: '50%',
                data: [
                    // ['Chicas', vm.classReport['students']['gender_percentage']['F']],
                    // ['Chicos', vm.classReport['students']['gender_percentage']['M']],
                    ['Chicas', 40],
                    ['Chicos', 60],
                    {
                        name: 'Proprietary or Undetectable',
                        y: 0.2,
                        dataLabels: {
                            enabled: false
                        }
                    }
                ]
            }]
        };

        // Sample data for pie chart
        $scope.pieData = [{
            name: "Microsoft Internet Explorer",
            y: 56.33
        }, {
            name: "Chrome",
            y: 24.03,
            sliced: true,
            selected: true
        }, {
            name: "Firefox",
            y: 10.38
        }, {
            name: "Safari",
            y: 4.77
        }, {
            name: "Opera",
            y: 0.91
        }, {
            name: "Proprietary or Undetectable",
            y: 0.2
        }]


        vm.chartConfig = {
            xAxis: {
                categories: ['Jan', 'Feb']
            },
            title: {
                text: 'USD to EUR exchange rate from 2006 through 2008'
            }, subtitle: {
                text: document.ontouchstart === undefined ?
                    'Click and drag in the plot area to zoom in' :
                    'Pinch the chart to zoom in'
            },
            yAxis: {title: {text: 'Temperature (Celsius)'}},
            tooltip: {valueSuffix: ' celsius'},
            legend: {align: 'center', verticalAlign: 'bottom', borderWidth: 0},
            plotOptions: {
                area: {
                    fillColor: {
                        linearGradient: {x1: 0, y1: 0, x2: 0, y2: 1},
                        stops: [
                            [0, Highcharts.getOptions().colors[0]],
                            [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                        ]
                    },
                    marker: {
                        radius: 2
                    },
                    lineWidth: 1,
                    states: {
                        hover: {
                            lineWidth: 1
                        }
                    },
                    threshold: null
                }
            },
            series: [{
                type: 'area',
                data: [0, 1]
            }]
        };
        console.log('ACCESS')
        console.log(vm.chartConfig['series'])
        vm.chartConfig['series'][0]['data'] = [1,1];
        console.log(vm.chartConfig['series'])


    });


