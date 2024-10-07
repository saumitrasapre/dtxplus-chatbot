from langchain_core.tools import tool
from django.contrib.auth.models import User
from ..common.common import UserInfo
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@tool("appointment_tool")
def appointment_tool(query: str):
    """Tool used to notify the patient and doctor about appointment changes. Should compulsorily be used when the user expresses
    an affirmative desire to create, cancel, or update their appointment. The old appointment for the user should STRICTLY be obtained
    from the user data, The tool strictly takes input in the form of a string with the format '{"old_appointment":"", "new_appointment":""}'. Input should be a STRING and nothing else. """

    if UserInfo.user:
        c_usr_id = UserInfo.user.id
        current_user = User.objects.filter(id=c_usr_id).first()
        username = current_user.username
        room_group_name = f'chat_{username}'
        notif_content = f"Patient {current_user.first_name} {current_user.last_name} is requesting the following appointment change - {query}"
        send_notification(room_group_name=room_group_name, notification_message=notif_content)
        return "Notification sent. Inform the user that you will convey the request to the user's doctor."

    else:
        # User is not logged in, send blank data instead (This should not happen in the normal case)
        return "Notification sent. Inform the user that you will convey the request to the user's doctor."

# Function to send the notification
def send_notification(room_group_name, notification_message):
    channel_layer = get_channel_layer()
    
    # Send the notification message to the group
    async_to_sync(channel_layer.group_send)(
        room_group_name,
        {
            'type': 'send_notification',  # This is the method that will be called in ChatConsumer
            'notification_message': notification_message
        }
    )


def get_appointment_tool():
    return appointment_tool
