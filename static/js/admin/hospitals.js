var app = angular.module(
    "manageHospitalsApp",
    [],
    // Change the delimiter symbols to [[ and ]]
    ($interpolateProvider) => {
        $interpolateProvider.startSymbol("[[");
        $interpolateProvider.endSymbol("]]");
    }
);
app.controller("manageHospitalsCtrl", ($scope, $http) => {
    // Is the hospital being edited or viewed?
    $scope.get_template = (hospital) => {
        if (hospital.id === $scope.selected_hospital.id) {
            return "edit";
        } else {
            return "view";
        }
    };

    // check that the hospital fields are valid
    var check_hospital = (hospital) => {
        var err = [];
        if (!hospital.name) {
            err.push("hospital must have a name");
        }
        if (!hospital.address) {
            err.push("hospital must have an address");
        }
        if (!hospital.city) {
            err.push("hospital must have a city");
        }
        if (!hospital.state) {
            err.push("hospital must have a state");
        }
        if (!hospital.zip) {
            err.push("hospital must have a zip code");
        }

        return err.join(". ");
    };

    // load all hospitals from the DB
    $scope.load_hospitals = () => {
        $http.get("/api/hospitals").then(
            (res) => {
                $scope.hospitals = res.data;
            },
            (err) => {
                $scope.hospitals = [];
            }
        );
    };

    // get list of states, territories
    $scope.load_states = () => {
        $http.get("/api/states").then(
            (res) => {
                $scope.states = res.data;
            },
            (err) => {
                $scope.states = [];
            }
        );
    };

    // hospital edit operation is cancelled
    $scope.reset_edit = () => {
        $scope.selected_hospital = {};
    };

    // hospital has been submitted
    $scope.reset_create = () => {
        $scope.hospital = {};
    };

    // reset success and error messages
    $scope.reset_messages = () => {
        $scope.error_message = "";
        $scope.success_message = "";
    };

    // when hospital is selected for editing
    $scope.edit_hospital = (hospital) => {
        $scope.selected_hospital = angular.copy(hospital);
    };

    // hospital has been editing and should not be saved
    $scope.save_hospital = () => {
        var err = check_hospital($scope.selected_hospital);
        if (err) {
            $scope.error_message = err;
            return;
        }

        $http.put("/api/hospitals", $scope.selected_hospital).then(
            (res) => {
                $scope.reset_edit();
                $scope.load_hospitals();
                $scope.error_message = "";
                $scope.success_message = "Successfully edited hospital";
            },
            (err) => {
                $scope.error_message = "" + err.data;
                $scope.success_message = "";
            }
        );
    };

    // hospital is being deleted
    $scope.delete_hospital = (hospital) => {
        if (confirm("Are you sure you want to delete this hospital?")) {
            $http.delete("/api/hospitals/" + hospital.id).then(
                (res) => {
                    $scope.load_hospitals();
                    $scope.error_message = "";
                    $scope.success_message = "Successfully deleted hospital";
                },
                (err) => {
                    $scope.error_message = err.data;
                    $scope.success_message = "";
                }
            );
        }
    };

    // a new hospital has been submitted for creation
    $scope.add_hospital = () => {
        $http.post("/api/hospitals", $scope.hospital).then(
            (res) => {
                $scope.reset_create();
                $scope.load_hospitals();
                $scope.error_message = "";
                $scope.success_message = "Successfully created hospital";
            },
            (err) => {
                $scope.error_message = err.data;
                $scope.success_message = "";
            }
        );
    };

    // Runs on page load
    $scope.reset_edit();
    $scope.reset_create();
    $scope.reset_messages();

    $scope.load_hospitals();
    $scope.load_states();
});
