import os
import sys
import uuid

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), './../../'))
sys.path.append(parent_dir)

from ingenious.services.chat_services.multi_agent.agent_factory import ToolFunctions
import ingenious.dependencies as deps
import asyncio
from ingenious.models.chat import ChatRequest, ChatResponse
import ingenious.config.config as config



async def process_message(chat_request: ChatRequest) -> ChatResponse:
    user = await deps.get_chat_history_repository().get_user(chat_request.user_name)
    print("user_id:", chat_request.user_id)
    print("user:", user)
    cs = deps.get_chat_service(
        deps.get_chat_history_repository(),
        conversation_flow=chat_request.conversation_flow
    )
    res = await cs.get_chat_response(chat_request)
    return res


# Generate a unique thread ID and create a chat request
new_guid = uuid.uuid4()
chat_request: ChatRequest = ChatRequest(
    thread_id=str(new_guid),
    user_id="elliot",  # Assuming the user_id is "elliot"
    user_prompt="",
    user_name="elliot",
    conversation_flow="knowledge_base_agent"  # Using the classification agent flow
)

#reset memory
_config = config.get_config()
memory_path = _config.chat_history.memory_path
with open(f"{memory_path}/context.md", "w") as memory_file:
    memory_file.write("new conversation, please derive context from question")



# Example 1 search knowledge base under one ambiguous topic with memory
chat_request.user_prompt = f"Tell me about contact number?"
res: ChatResponse = asyncio.run(process_message(chat_request=chat_request))

chat_request.user_prompt = f"for safety?"
res = asyncio.run(process_message(chat_request=chat_request))



# Example 2 search knowledge base under known topic(s)
# chat_request.user_prompt = f"Who is our first aider in health and emergency coordinator in safety?"
# res: ChatResponse = asyncio.run(process_message(chat_request=chat_request))




# Print the final response
print(res)