import os
import json
import openai  # Import OpenAI library
from autogen import WorkAgentFlow, cache_seed, UserProxyAgent, GroupChat, GroupChatManager
from ollama import Subject, Question, Answer

class QuestionnaireApp:
    def __init__(self, api_key):
        self.subjects = {}
        self.api_key = api_key
        self.load_questions()
        openai.api_key = api_key  # Set the API key for OpenAI
        
    def add_subject(self, subject_name):
        if subject_name not in self.subjects:
            self.subjects[subject_name] = Subject(subject_name)
    
    def add_question(self, subject_name, question_text):
        if subject_name in self.subjects:
            self.subjects[subject_name].add_question(question_text)
            self.generate_answer(subject_name, question_text)  # Generate answer when adding question
    
    def generate_answer(self, subject_name, question_text):
        response = openai.Completion.create(
            engine="text-davinci-003",  # GPT-3.5 engine
            prompt=question_text,
            max_tokens=50
        )
        generated_answer = response.choices[0].text.strip()  # Extract generated answer
        self.subjects[subject_name].set_answer(question_text, generated_answer)  # Store generated answer
    
    def get_answer(self, subject_name, question_text):
        if subject_name in self.subjects:
            return self.subjects[subject_name].get_answer(question_text)
        return "Subject not found."
    
    def load_questions(self):
        # Load questions from file storage (if any)
        pass
    
    def start(self):
        group_chat = GroupChat()
        group_chat_manager = GroupChatManager(group_chat)
        
        while True:
            print("\nWelcome to the Questionnaire App!")
            print("1. Add Subject")
            print("2. Add Question")
            print("3. Get Answer")
            print("4. Exit")
            choice = input("Enter your choice: ")
            
            if choice == "1":
                subject_name = input("Enter subject name: ")
                self.add_subject(subject_name)
            
            elif choice == "2":
                subject_name = input("Enter subject name: ")
                question_text = input("Enter question text: ")
                self.add_question(subject_name, question_text)
            
            elif choice == "3":
                subject_name = input("Enter subject name: ")
                question_text = input("Enter question text: ")
                answer = self.get_answer(subject_name, question_text)
                print("Answer:", answer)
            
            elif choice == "4":
                print("Thank you for using the Questionnaire App!")
                break
            
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    api_key = "YOUR_OPENAI_API_KEY"  # Replace with your OpenAI API key
    app = QuestionnaireApp(api_key)
    app.start()
