import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .chatbot.langchain_cbt import invoke_graph_updates
from .chatbot.common.common import UserInfo, ChatInfo


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        # Set the current user that is logged in
        UserInfo.user = self.scope['user']
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()  # Accept the WebSocket connection

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Logic to process the incoming message and generate a response
        response_messages = self.process_message(message)

        # Send message to room group
        for response_message in response_messages:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': response_message
                }
            )
    
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
    
    # Method to handle notifications
    async def send_notification(self, event):
        notification_message = event['notification_message']
        await self.send(text_data=json.dumps({
            'notification': notification_message
        }))

    def process_message(self, message):
        thread_id = self.scope['session'].get('new_chat_thread_id', '1')
        
        # Set the current chat thread id that the user is interacting with
        ChatInfo.chat_thread_id = thread_id

        print("Chat_id - ",thread_id)
        res = invoke_graph_updates(user_input=message, thread_id=thread_id)
        # Uncomment to debug
        # print(res)
        ans = []
        for ele in res:
            msg = ele["messages"][-1]
            if not hasattr(msg, "tool_call_id"):
                ans.append(msg.content)
        return ans  
