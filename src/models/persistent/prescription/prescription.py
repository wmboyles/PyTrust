"""
This file contains class information on prescriptions, including the fields and
methods a prescription has in the Prescription class, as well as how the
prescrition is serialized as JSON in PrescriptionSchema.

:author William Boyles:
"""

from marshmallow.decorators import post_load
from sqlalchemy.orm import validates

from ..persistent import db, ma
from ...persistent.user.patient.patient import Patient
from ...persistent.institution.pharmacy.pharmacy import Pharmacy
from ...persistent.user.personnel.personnel import Personnel
from ...persistent.drug.drug import Drug
from ....models.enums.user_role.user_role import UserRole


class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    patient_id = db.Column(db.Integer, db.ForeignKey("patient.user_id"), nullable=False)
    # if patient is deleted, delete prescription
    patient = db.relationship(
        Patient, backref=db.backref("prescriptions", cascade="all, delete-orphan")
    )

    prescriber_id = db.Column(
        db.Integer, db.ForeignKey("personnel.user_id"), nullable=False
    )
    # if prescriber is deleted, delete prescription
    prescriber = db.relationship(
        Personnel, backref=db.backref("prescriptions", cascade="all, delete-orphan")
    )

    drug_code = db.Column(db.String(127), db.ForeignKey("drug.code"), nullable=False)
    dosage = db.Column(db.Integer, nullable=False)

    pharmacy_id = db.Column(db.Integer, db.ForeignKey("pharmacy.id"), nullable=True)
    pharmacy = db.relationship(Pharmacy, backref="prescriptions")

    @validates("prescriber")
    def validate_prescriber(self, key, prescriber: Personnel) -> Personnel:
        """
        Validates that the prescribing personnel is an HCP

        :param prescriber: Personnel prescriber to validate
        :return: validated prescriber
        :raises AssertionError: if prescriber is not an HCP
        """

        if not prescriber.user.role == UserRole.HCP:
            raise AssertionError("Prescriber must be an HCP")

        return prescriber

    @validates("dosage")
    def validate_dosage(self, key, dosage: int) -> int:
        """
        Validates that dosage is positive

        :param dosage: dosage to validate
        :return: validated dosage
        :raises AssertionError: if dosage is 0 or negative
        """

        if dosage <= 0:
            raise AssertionError("Dosage must be positive")

        return dosage

    @validates("drug_code")
    def validate_code(self, key, code: str) -> str:
        """
        Validates that code field matches the required pattern.

        :param code: string NDC code to validate
        :return: validated NDC code
        :raises AssertionError: if code does not match pattern
        """

        return Drug.validate_code(None, None, code=code)


class PrescriptionSchema(ma.SQLAlchemyAutoSchema):
    """
    The prescription schema helps with the serialization and deserialization of
    prescriptions.
    """

    class Meta:
        model = Prescription

    patient = ma.Nested("PatientSchema")
    prescriber = ma.Nested("PersonnelSchema")
    pharmacy = ma.Nested("PharmacySchema", allow_none=True)

    @post_load
    def make_prescription(self, data: dict, **kwargs) -> Prescription:
        """
        This method is called when callign a load. It transforms a dictionary
        representing the object into the object itself.

        :param data: dict data representing the prescription object
        """

        return Prescription(**data)
