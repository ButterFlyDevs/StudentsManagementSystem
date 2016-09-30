var CalculatorService = angular.module('CalculatorService', [])
    .config(function(){
        console.log('Activating CalculatorService.');

      })
    .service('Calculator', function () {
        this.square = function (a) { return a*a};
    });