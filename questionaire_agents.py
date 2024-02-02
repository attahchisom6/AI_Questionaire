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
user_proxy = UserProxyAgent(
    name="student",
    system_message="This will execute and fetch a reasonably answer from the expert to the student",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=8,
    code_execution_config=False,
)

# we define an expert to execcute code based on what it recieves from rhe other assistants and pass back result to the user
exper = AssistantAgent(
    name="expert",
    system_message="you recieves messages from other assistants, evaluates, execute and pass an understandable message to the student, if the student is not send back the student response to ths appropraite agent for a better answer",
    code_execution={"last_n_message": 3, "work_dir": "student_feedback"}
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

# Define a GroupChat with the agents and a manager to manage the them, then initiate a chat with the manager

group_chat = GroupChat(agents=[concept_assistant, group_assistant, ring_assistant], message=[], max_round=50)

manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)

user_proxy.initiate_chat(manager, message="i would love you to answer questions regarding only matters in abstract algebra, example list 5 most popular group, rings orvtgeories in abstract algebra")
