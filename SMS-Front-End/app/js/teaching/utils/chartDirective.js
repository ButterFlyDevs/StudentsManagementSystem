var chartDirective = function () {
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
                scope.$watch("config.series", function (newValue, oldValue) {
                    console.log('new data received');
                    console.log('newValue');
                    console.log(newValue);
                    console.log('oldValue');
                    console.log(oldValue);

                    process();
                }, true);
                scope.$watch("config.loading", function (loading) {
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
    };