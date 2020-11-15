var app = angular.module(
    "manageDrugsApp",
    [],
    // Change the delimiter symbols to [[ and ]]
    ($interpolateProvider) => {
        $interpolateProvider.startSymbol("[[");
        $interpolateProvider.endSymbol("]]");
    }
);
app.controller("manageDrugsCtrl", ($scope, $http) => {
    // Is drug being edited or viewed?
    $scope.get_template = (drug) => {
        if (drug.id === $scope.selectedDrug.id) {
            return "edit";
        } else {
            return "view";
        }
    };

    // check that drug fields are valid
    var check_drug = (drug) => {
        var err = [];
        if (!drug.name) {
            err.push("Must have a name");
        }
        if (!drug.description) {
            err.push("Must have a description");
        }
        if (!drug.code || !/^\d{4}-\d{4}-\d{2}$/.test(drug.code)) {
            err.push("Code must be in the format ####-####-##");
        }

        return err.join(". ");
    };

    // load all the drugs from the DB
    $scope.load_drugs = () => {
        $http.get("/api/drugs").then(
            (res) => {
                $scope.drugs = res.data;
            },
            (err) => {
                $scope.drugs = [];
            }
        );
    };

    // load all the drug types from the db
    $scope.load_drug_types = () => {
        $http.get("/api/drug_types").then(
            (res) => {
                $scope.drug_types = res.data.filter(
                    (type) => type !== "Not Specified"
                );
            },
            (err) => {
                $scope.drug_types = [];
            }
        );
    };

    // drug edit operation is cancelled
    $scope.reset_edit = () => {
        $scope.selectedDrug = {};
    };

    // drug has been submitted
    $scope.reset_create = () => {
        $scope.drug = {};
    };

    // reset success and error messages
    $scope.reset_messages = () => {
        $scope.error_message = "";
        $scope.success_message = "";
    };

    // when drug is selected for editing
    $scope.edit_drug = (drug) => {
        $scope.selectedDrug = angular.copy(drug);
    };

    // drug has been edited and now should be saved
    $scope.save_drug = () => {
        var err = check_drug($scope.selectedDrug);
        if (err) {
            $scope.error_message = err;
            return;
        }

        $http.put("/api/drugs", $scope.selectedDrug).then(
            (res) => {
                $scope.reset_edit();
                $scope.load_drugs();
                $scope.error_message = "";
                $scope.success_message = "Successfully edited drug";
            },
            (err) => {
                $scope.error_message = "" + err.data;
                $scope.success_message = "";
            }
        );
    };

    // drug is being deleted
    $scope.delete_drug = (drug) => {
        if (confirm("Are you sure you want to delete this drug?")) {
            $http.delete("/api/drugs/" + drug.id).then(
                (res) => {
                    $scope.load_drugs();
                    $scope.error_message = "";
                    $scope.success_message = "Successfully deleted drug";
                },
                (err) => {
                    $scope.error_message = err.data;
                    $scope.success_message = "";
                }
            );
        }
    };

    // a new drug has been submitted for creation
    $scope.add_drug = () => {
        $http.post("/api/drugs", $scope.drug).then(
            (res) => {
                $scope.reset_create();
                $scope.load_drugs();
                $scope.error_message = "";
                $scope.success_message = "Successfully created drug";
            },
            (err) => {
                $scope.error_message = "" + err.data;
                $scope.success_message = "";
            }
        );
    };

    // Runs on page load
    $scope.reset_edit();
    $scope.reset_create();
    $scope.reset_messages();

    $scope.load_drugs();
    $scope.load_drug_types();
});
