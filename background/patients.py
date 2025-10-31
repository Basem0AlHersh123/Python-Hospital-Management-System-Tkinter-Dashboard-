from background.user import User
from background.file_manager import FileManager
class Patient(User):
    def __init__(self, ID, name, password, role, phone, active=True, birth_day=None, gender=None, medical_history="", status=""):
        super().__init__(ID, name, password, role, name, phone, active)
        self.birth_day = birth_day
        self.gender = gender
        self.medical_history = medical_history
        self.status = status
    def get_appointments(self):
        all_appointments = FileManager.load_data("appointments")
        return [appointment for appointment in all_appointments if appointment.get("patient_id") == self.id]
    @staticmethod
    def add_patient(doctor,patient,patient_id,doctor_id,dt_txt):
            appointments = FileManager.load_data("appointments")
            doctors=FileManager.load_data("doctors")
            new_appointment = {
                "id": max([patient.get("id", 0) for patient in appointments] or [0]) + 1,
                "doctor": doctor,
                "patient": patient,  
                "patient_id": patient_id,
                "doctor_id": doctor_id,
                "date": dt_txt,
                "diagnosis": None,
                "treatment": None,
            }
            appointments.append(new_appointment)
            FileManager.save_data("appointments",appointments)