from background.user import User
from background.file_manager import FileManager
class Doctor(User):
    def __init__(self, ID, name, password, role, full_name, phone, license_number, specialty, active=True):
        super().__init__(ID, name, password, role, full_name, phone, active)
        self.license_number = license_number
        self.specialty = specialty
    def get_appointments(self):
        appointments = FileManager.load_data("appointments")
        return [appointment for appointment in appointments if appointment.get("doctor_id") == self.id]
    @staticmethod
    def add_diagnosis(appointment_id, diagnosis, treatment):
        appointments = FileManager.load_data("appointments")
        updated = False
        for appointment in appointments:
            if appointment.get("id") == appointment_id:
                appointment["diagnosis"] = diagnosis
                appointment["treatment"] = treatment
                updated = True
                break
        if updated:
            FileManager.save_data("appointments", appointments)
        return updated