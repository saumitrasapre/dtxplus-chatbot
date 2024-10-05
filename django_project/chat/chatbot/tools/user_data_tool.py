from langchain_core.tools import tool
from django.contrib.auth.models import User
from ..common.common import UserInfo
import json


@tool("fetch_user_info_tool")
def fetch_user_info_tool():
    """Gets the first name, last name, age, phone_number, medical condition, medication regimen, last appointment date and time ,next appointment date and time, the doctor's name
    and additional entities (which includes user's preference for appointment time, or any user mention of a medication /diet/allergy) of the currently logged in user. Used as the absolute ground truth for any information regarding the
    user. Any info that contradicts these details is untrue and incorrect.
    This tool should compulsorily be used to obtain user info if any of these details are required. This information should not be asked to the user.
    """

    if UserInfo.user:
        c_usr_id = UserInfo.user.id
        current_user = User.objects.filter(id=c_usr_id).first()
        info = {
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "age": current_user.profile.age, 
            "phone_number": current_user.profile.phone_number,
            "medical_condition": current_user.profile.medical_condition,
            "medication_regimen": current_user.profile.medication_regimen,
            "last_appointment": current_user.profile.last_appointment_datetime,
            "next_appointment": current_user.profile.next_appointment_datetime,
            "doctor_name": current_user.profile.doctors_name,
            "additional_entities": json.dumps(current_user.profile.additional_entities)
        }
        return json.dumps(info, default=str)
    
    else:
        # User is not logged in, send dummy data instead (This should not happen in the normal case)
        info = {
            "first_name": "Jake",
            "last_name": "Doe",
            "age": 25, 
            "phone_number": 1234567890,
            "medical_condition": "",
            "medication_regimen": "",
            "last_appointment": "",
            "next_appointment": "",
            "doctor_name": "",
        }
        
        return json.dumps(info)


def get_user_info_tool():
    return fetch_user_info_tool