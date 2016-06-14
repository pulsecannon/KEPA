/**
 * @fileoverview The main kepa angular application.
 */

var app = angular.module('kepa', ['nvd3']);

app.controller('KepaDashCtrl', function($scope, $http) {
  $scope.options = {
      chart: {
        type: 'pieChart',
        height: 500,
        x: function(d){return d.key;},
        y: function(d){return d.y;},
        showLabels: true,
        duration: 500,
        labelThreshold: 0.01,
        labelSunbeamLayout: true,
        legend: {
          margin: {
            top: 5,
            right: 35,
            bottom: 5,
            left: 0
          }
        }
      }
    };

  $http.get('/agg-reports/').success(function(data) {
    $scope.data = data;
  });

});
