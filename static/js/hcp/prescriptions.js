var app = angular.module(
    "managePrescriptionsApp",
    [],
    // Change the delimiter symbols to [[ and ]]
    ($interpolateProvider) => {
        $interpolateProvider.startSymbol("[[");
        $interpolateProvider.endSymbol("]]");
    }
);
app.factory("waitForLoadSelf", ($http) => {
    var load_self = () => {
        return $http.get("/api/personnel/self").then((res) => {
            return res.data;
        });
    };

    return { load_self, load_self };
});
app.controller("managePrescriptionsCtrl", ($scope, $http, waitForLoadSelf) => {
    // Is drug being edited or viewed?
    $scope.get_template = (prescription) => {
        if (prescription.id == $scope.selectedPrescription.id) {
            return "edit";
        } else {
            return "view";
        }
    };

    $scope.load_prescriptions = () => {
        $http.get("/api/prescriptions").then(
            (res) => {
                var prescriptions = res.data;
                for (var i in prescriptions) {
                    prescriptions[i].start_date = new Date(
                        prescriptions[i].start_date
                    );
                    prescriptions[i].end_date = new Date(
                        prescriptions[i].end_date
                    );
                }
                $scope.prescriptions = prescriptions;
            },
            (err) => {
                $scope.prescriptions = [];
            }
        );
    };

    $scope.load_patients = () => {
        $http.get("/api/patients").then(
            (res) => {
                $scope.patients = res.data;
            },
            (err) => {
                $scope.patients = [];
            }
        );
    };

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

    $scope.reset_edit = () => {
        $scope.selectedPrescription = {};
        $scope.selectedPrescription.prescriber = $scope.self;
    };

    $scope.reset_create = () => {
        $scope.prescription = {};
        $scope.prescription.prescriber = $scope.self;
    };

    // reset success and error messages
    $scope.reset_messages = () => {
        $scope.error_message = "";
        $scope.success_message = "";
    };

    $scope.edit_prescription = (prescription) => {
        $scope.selectedPrescription = angular.copy(prescription);
    };

    $scope.save_prescription = () => {
        // TODO check for error

        $scope.selectedPrescription.start_date = Intl.DateTimeFormat(
            "en-US"
        ).format($scope.selectedPrescription.start_date);
        $scope.selectedPrescription.end_date = Intl.DateTimeFormat(
            "en-US"
        ).format($scope.selectedPrescription.end_date);

        $http.put("/api/prescriptions", $scope.selectedPrescription).then(
            (res) => {
                $scope.reset_edit();
                $scope.load_prescriptions();
                $scope.error_message = "";
                $scope.success_message = "Successfully edited prescription";
            },
            (err) => {
                $scope.error_message = err.data;
                $scope.success_message = "";
            }
        );
    };

    $scope.delete_prescription = (prescription) => {
        if (confirm("Are you sure you want to delete this prescription?")) {
            $http.delete("/api/prescriptions/" + prescription.id).then(
                (res) => {
                    $scope.load_prescriptions();
                    $scope.error_message = "";
                    $scope.success_message = res.data;
                },
                (err) => {
                    $scope.error_message = err.data;
                    $scope.success_message = "";
                }
            );
        }
    };

    $scope.add_prescription = () => {
        // TODO check for error

        $scope.prescription.start_date = Intl.DateTimeFormat("en-US").format(
            $scope.prescription.start_date
        );
        $scope.prescription.end_date = Intl.DateTimeFormat("en-US").format(
            $scope.prescription.end_date
        );

        $http.post("/api/prescriptions", $scope.prescription).then(
            (res) => {
                $scope.load_prescriptions();
                $scope.reset_create();
                $scope.error_message = "";
                $scope.success_message = "Successfully created prescription";
            },
            (err) => {
                $scope.error_message = err.data;
                $scope.success_message = "";
            }
        );
    };

    // runs on page load

    var load_self_promise = waitForLoadSelf.load_self();
    load_self_promise.then((res) => {
        $scope.self = res;
        $scope.reset_edit();

        $scope.load_patients();
        $scope.reset_messages();

        $scope.load_drugs();

        $scope.load_pharmacies();
        $scope.load_prescriptions();
        $scope.reset_create();
    });
});
