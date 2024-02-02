from autogen import (
    config_list_from_json,
    UserProxyAgent,
    AssistantAgent,
    GroupChat,
    GroupChatManager
)
from ollama import Subject, Question

class QuestionnaireApp:
    def __init__(self):
        self.subjects = {}
        self.student = UserProxyAgent(
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
        self.concept_assistant = AssistantAgent(
            name="concept_assistant",
            system_message="This Assistance will be to provide assistance for matters in Abstract Algebra that do not touch on group or ring theories",
            llm_config={
                "cache_seed": 55,
                "config_list": config_list,
                "timeout": 300,
                "temperature": 0,
            },
        )
        self.group_assistant = AssistantAgent(
            name="group_assistant",
            system_message="This Assistant will provide assistance with matters regarding Group theory in abstract algebra",
            llm_config={
                "cache_seed": 50,
                "config_list": config_list,
                "timeout": 300,
                "temperature": 0,
            },
        )
        self.ring_assistant = AssistantAgent(
            name="ring_assistant",
            system_message="This assistance will provide assistance with matters regarding ring theory in abstract algebra",
            llm_config={
                "cache_seed": 50,
                "config_list": config_list,
                "timeout": 300,
                "temperature": 0,
            }
        )
        self.group_chat = GroupChat(agents=[self.concept_assistant, self.group_assistant, self.ring_assistant], message=[], student_manager=None)
        self.manager = GroupChatManager(self.group_chat)
    
    def add_subject(self, subject_name):
        if subject_name not in self.subjects:
            self.subjects[subject_name] = Subject(subject_name)
    
    def add_question(self, subject_name, question_text):
        if subject_name in self.subjects:
            self.subjects[subject_name].add_question(question_text)
            self.student.ask_expert(question_text)
    
    def start(self):
        while True:
            print("\nWelcome to the Questionnaire App!")
            print("1. Add Subject")
            print("2. Add Question")
            print("3. Exit")
            choice = input("Enter your choice: ")
            
            if choice == "1":
                subject_name = input("Enter subject name: ")
                self.add_subject(subject_name)
            
            elif choice == "2":
                subject_name = input("Enter subject name: ")
                question_text = input("Enter question text: ")
                self.add_question(subject_name, question_text)
            
            elif choice == "3":
                print("Thank you for using the Questionnaire App!")
                break
            
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = QuestionnaireApp()
    app.start()
