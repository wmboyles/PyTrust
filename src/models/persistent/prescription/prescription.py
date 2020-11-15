"""
This file contains class information on prescriptions, including the fields and
methods a prescription has in the Prescription class, as well as how the
prescrition is serialized as JSON in PrescriptionSchema.

:author William Boyles:
"""

from datetime import datetime
from marshmallow import fields
from marshmallow.decorators import post_load
from sqlalchemy.orm import validates

from ..persistent import db, ma
from ...persistent.user.patient.patient import Patient
from ...persistent.institution.pharmacy.pharmacy import Pharmacy
from ...persistent.user.personnel.personnel import Personnel
from ...persistent.drug.drug import Drug
from ....models.enums.user_role.user_role import UserRole


class Prescription(db.Model):
    """
    A prescription is an assignment of a certain dosage of a drug by an hcp to
    a patient. Prescriptions are sent to a pharmacy, where a pharmacist will
    fill the prescription. Prescriptions have start and end dates that
    determine when the patient is eligible to have their prescription filled or
    renewed.

    :param id: unique id in the db of the prescription
    :param patient_id: user id of patient to whom the prescription is assigned
    :param patient: patient object. This field is generally how the patient
        will be set, and the id will be updated automatically.
    :param prescriber_id: user id of hcp who assigned the prescription
    :param prescriber: prescriber personnel object. This field is generally how
        the prescriber will be set, and the id will be updated automatically.
    :param drug_code: NDC code of prescribed drug. We don't store the actual
        drug object so that the pharmacist can take into account patient drug
        type preferences.
    :param dosage: amount of drug that patient should take
    :param renewals: number of times that prescription can be re-filled between
        the start and end dates. The inital filling of the prescription does
        not count here, so a prescription that should only be filled and never
        renewed should have a renewals of 0.
    :param pharmacy_id: id of pharmacy where this prescription will be sent.
    :param pharmacy: pharmacy object. This field is generally how the pharmacy
        will be set, and the id will be updated automatically.
    :param start_date: Earliest date that a prescription can be filled.
    :param end_date: Latest date that a prescription can be filled.
    """

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
    renewals = db.Column(db.Integer, nullable=False)

    pharmacy_id = db.Column(db.Integer, db.ForeignKey("pharmacy.id"), nullable=True)
    pharmacy = db.relationship(Pharmacy, backref="prescriptions")

    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

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

    @validates("renewals")
    def validate_renwals(self, key, renewals: int) -> int:
        """
        Validates that renewals is non-negative

        :param rewewals: number of renewals of prescription
        :returns: validated renewals
        :raises AssertionError: if renewals is negative
        """

        if renewals < 0:
            raise AssertionError("Renewals cannot be negative")

        return renewals

    @validates("drug_code")
    def validate_code(self, key, code: str) -> str:
        """
        Validates that code field matches the required pattern.

        :param code: string NDC code to validate
        :return: validated NDC code
        :raises AssertionError: if code does not match pattern
        """

        return Drug.validate_code(None, None, code=code)

    @validates("start_date", "end_date")
    def validate_end_date(self, key, date: datetime) -> datetime:
        """
        Validates that the start/end date is after the start date and after today.

        :param date: end date to validate
        :return: validated end date
        :raises AssertionError: if end date is before the start date
        :raises AssertionError: if end date is before the current date
        """

        if key == "start_date":
            return date
        else:
            if date < self.start_date:
                raise AssertionError("End date must be after start date")
            if date < datetime.today():
                raise AssertionError("End date must be on or after the current date.")

            return date


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

    start_date = fields.Date(format="%m/%d/%Y")
    end_date = fields.Date(format="%m/%d/%Y")

    @post_load
    def make_prescription(self, data: dict, **kwargs) -> Prescription:
        """
        This method is called when callign a load. It transforms a dictionary
        representing the object into the object itself.

        :param data: dict data representing the prescription object
        """

        return Prescription(**data)
