var app = angular.module(
    "managePharmaciesApp",
    [],
    // Change the delimiter symbols to [[ and ]]
    ($interpolateProvider) => {
        $interpolateProvider.startSymbol("[[");
        $interpolateProvider.endSymbol("]]");
    }
);
app.controller("mangePharmaciesCtrl", ($scope, $http) => {
    // Is the pharmacy being edited or viewed?
    $scope.get_template = (pharmacy) => {
        if (pharmacy.id === $scope.selected_pharmacy.id) {
            return "edit";
        } else {
            return "view";
        }
    };

    // check that the pharmacy fields are valid
    var check_pharmacy = (pharmacy) => {
        var err = [];
        if (!pharmacy.name) {
            err.push("Pharmacy must have a name");
        }
        if (!pharmacy.address) {
            err.push("Pharmacy must have an address");
        }
        if (!pharmacy.city) {
            err.push("Pharmacy must have a city");
        }
        if (!pharmacy.state) {
            err.push("Pharmacy must have a state");
        }
        if (!pharmacy.zip) {
            err.push("Pharmacy must have a zip code");
        }

        return err.join(". ");
    };

    // load all pharmacies from the DB
    $scope.load_pharmacies = () => {
        $http.get("/api/pharmacies").then(
            (res) => {
                $scope.pharmacies = res.data;
            },
            (err) => {
                $scope.pharmacies = [];
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

    // pharmacy edit operation is cancelled
    $scope.reset_edit = () => {
        $scope.selected_pharmacy = {};
    };

    // pharmacy has been submitted
    $scope.reset_create = () => {
        $scope.pharmacy = {};
    };

    // reset success and error messages
    $scope.reset_messages = () => {
        $scope.error_message = "";
        $scope.success_message = "";
    };

    // when pharmacy is selected for editing
    $scope.edit_pharmacy = (pharmacy) => {
        $scope.selected_pharmacy = angular.copy(pharmacy);
    };

    // pharmacy has been editing and should not be saved
    $scope.save_pharmacy = () => {
        var err = check_pharmacy($scope.selected_pharmacy);
        if (err) {
            $scope.error_message = err;
            return;
        }

        $http.put("/api/pharmacies", $scope.selected_pharmacy).then(
            (res) => {
                $scope.reset_edit();
                $scope.load_pharmacies();
                $scope.error_message = "";
                $scope.success_message = "Successfully edited pharmacy";
            },
            (err) => {
                $scope.error_message = "" + err.data;
                $scope.success_message = "";
            }
        );
    };

    // pharmacy is being deleted
    $scope.delete_pharmacy = (pharmacy) => {
        if (confirm("Are you sure you want to delete this pharmacy?")) {
            $http.delete("/api/pharmacies/" + pharmacy.id).then(
                (res) => {
                    $scope.load_pharmacies();
                    $scope.error_message = "";
                    $scope.success_message = "Successfully deleted pharmacy";
                },
                (err) => {
                    $scope.error_message = err.data;
                    $scope.success_message = "";
                }
            );
        }
    };

    // a new pharmacy has been submitted for creation
    $scope.add_pharmacy = () => {
        $http.post("/api/pharmacies", $scope.pharmacy).then(
            (res) => {
                $scope.reset_create();
                $scope.load_pharmacies();
                $scope.error_message = "";
                $scope.success_message = "Successfully created pharmacy";
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

    $scope.load_pharmacies();
    $scope.load_states();
});
