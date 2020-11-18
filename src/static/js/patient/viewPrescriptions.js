var app = angular.module(
    "viewPrescriptionsApp",
    [],
    // Change the delimiter symbols to [[ and ]]
    ($interpolateProvider) => {
        $interpolateProvider.startSymbol("[[");
        $interpolateProvider.endSymbol("]]");
    }
);
app.controller("viewPrescriptionsCtrl", ($scope, $http) => {
    // show only the view template
    $scope.get_template = (prescription) => {
        return "view";
    };

    // get all prescriptions for this user
    $scope.load_prescriptions = () => {
        $http.get("/api/prescriptions").then(
            (res) => {
                $scope.prescriptions = res.data;
            },
            (err) => {
                $scope.prescriptions = [];
            }
        );
    };

    // runs on pabe load
    $scope.load_prescriptions();
});
