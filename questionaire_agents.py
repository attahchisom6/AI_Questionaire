#!/usr/bin/env python3

from autogen import (
    config_list_from_json,
    UserProxyAgent,
    AssistantAgent,
    GroupChat,
    GroupChatManager
)

# Load autogen configuration
config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")

llm_config={
    "cache_seed": 55,
    "config_list": config_list,
    "timeout": 300,
    "temperature": 0,
  }

# Define UserProxyAgent for student
student = UserProxyAgent(
    name="student",
    system_message="This will execute and fetch a reasonably answer from the expert to the student",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    code_execution_config={
        "work_dir": "student_manager",
        "use_docker": False,
    },
    map_function={"ask_expert": ["concept_assistant", "group_assistant", "ring_assistant"]}
)

# Define AssistantAgents for concept, group, and ring assistance
concept_assistant = AssistantAgent(
    name="concept_assistant",
    system_message="This Assistance will be to provide assistance for matters in Abstract Algebra that do not touch on group or ring theories",
    llm_config=llm_config,
)

group_assistant = AssistantAgent(
    name="group_assistant",
    system_message="This Assistant will provide assistance with matters regarding Group theory in abstract algebra",
    llm_config=llm_config,
)

ring_assistant = AssistantAgent(
    name="ring_assistant",
    system_message="This assistance will provide assistance with matters regarding ring theory in abstract algebra",
    llm_config=llm_config,
)

# Define a GroupChat with the agents
group_chat = GroupChat(agents=[concept_assistant, group_assistant, ring_assistant], message=[], student_manager=None)

# Create a GroupChatManager and pass the group chat to it
manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)
