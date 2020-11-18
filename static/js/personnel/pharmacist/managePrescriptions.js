var app = angular.module(
    "managePrescriptionsApp",
    [],
    // Change the delimiter symbols to [[ and ]]
    ($interpolateProvider) => {
        $interpolateProvider.startSymbol("[[");
        $interpolateProvider.endSymbol("]]");
    }
);
app.controller("managePrescriptionsCtrl", ($scope, $http) => {
    // always in view mode
    $scope.get_template = (prescription) => {
        return "view";
    };

    // get list of all prescriptions sent to pharmacist's pharmacy
    $scope.load_prescriptions = () => {
        $http.get("/api/prescriptions").then(
            (res) => {
                $scope.prescriptions = res.data;
                if ($scope.prescriptions.length === 0) {
                    $scope.success_message = "No prescriptions";
                }
            },
            (err) => {
                $scope.prescriptions = [];
            }
        );
    };

    // fill a prescription
    $scope.fill_prescription = (prescription) => {
        $http.put("/api/prescriptions/fill/" + prescription.id).then(
            (res) => {
                $scope.error_message = "";
                $scope.success_message = res.data;
                $scope.load_prescriptions();
            },
            (err) => {
                $scope.error_message = err.data;
                $scope.success_message = "";
            }
        );
    };

    // runs on page load
    $scope.load_prescriptions();
});
