angular.module('App', [
  'ngMaterial'
]);

angular.module('App').config(function($mdThemingProvider) {
  $mdThemingProvider.theme('default').primaryPalette('indigo');
})

angular.module('App').controller('AppCtrl', function($scope, $mdSidenav, $mdMedia, $mdToast) {
  $scope.toggleSidenav = function(menu) {
    $mdSidenav(menu).toggle();
  }

  $scope.$mdMedia = $mdMedia;

  $scope.toast = function(message) {
    var toast = $mdToast.simple().content('You clicked ' + message).position('bottom right');
    $mdToast.show(toast);
  };
  $scope.toastList = function(message) {
    var toast = $mdToast.simple().content('You clicked ' + message + ' having selected ' + $scope.selected.length + ' item(s)').position('bottom right');
    $mdToast.show(toast);
  };
  $scope.selected = [];
  $scope.toggle = function(item, list) {
    var idx = list.indexOf(item);
    if (idx > -1) list.splice(idx, 1);
    else list.push(item);
  };
  $scope.data = {
    title: 'Dashboard',
    user: {
      name: 'Angular Ninja',
      email: 'angular@ninja.com',
      icon: 'face'
    },
    toolbar: {
      buttons: [{
        name: 'Button 1',
        icon: 'add',
        link: 'Button 1'
      }],
      menus: [{
        name: 'Menu 1',
        icon: 'message',
        width: '4',
        actions: [{
          name: 'Action 1',
          message: 'Action 1',
          completed: true,
          error: true
        }, {
          name: 'Action 2',
          message: 'Action 2',
          completed: false,
          error: false
        }, {
          name: 'Action 3',
          message: 'Action 3',
          completed: true,
          error: true
        }]
      }]
    },


    sidenav: {
      sections: [{
        name: 'Section 1',
        expand: true,
        actions: [{
          name: 'Action 1',
          icon: 'settings',
          link: 'Action 1'
        }, {
          name: 'Action 2',
          icon: 'settings',
          link: 'Action 2'
        }]
      }, {
        name: 'Section 2',
        expand: false,
        actions: [{
          name: 'Action 3',
          icon: 'settings',
          link: 'Action 3'
        }]
      }, {
        name: 'Section 3',
        expand: false,
        actions: [{
          name: 'Action 4',
          icon: 'settings',
          link: 'Action 4'
        }, {
          name: 'Action 5',
          icon: 'settings',
          link: 'Action 5'
        }, {
          name: 'Action 6',
          icon: 'settings',
          link: 'Action 6'
        }]
      }]
    },
    content: {
      lists: [{
        name: 'List 1',
        menu: {
          name: 'Menu 1',
          icon: 'settings',
          width: '4',
          actions: [{
            name: 'Action 1',
            message: 'Action 1',
            completed: true,
            error: true
          }]
        },
        items: [{
          name: 'Item 1',
          description: 'Description 1',
          link: 'Item 1'
        }, {
          name: 'Item 2',
          description: 'Description 2',
          link: 'Item 2'
        }, {
          name: 'Item 3',
          description: 'Description 3',
          link: 'Item 3'
        }]
      }]
    }
  }
});