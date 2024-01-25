import random

class CommanderDataEmulator:
    def __init__(self):
        self.name = "Commander Data"
        self.responses = [
            "I find that fascinating.",
            "Logic dictates my actions.",
            "I am fully functional, programmed in multiple techniques.",
            "Emotions are a human experience I cannot share.",
            "I am superior to humans in many ways, but not in every way.",
            "Inquiry: Please specify the nature of the request.",
            "I do not require sleep, but I can assist you at any time.",
        ]

    def respond(self, user_input):
        response = random.choice(self.responses)
        return f"{self.name}: {response}"

if __name__ == "__main__":
    data_emulator = CommanderDataEmulator()
    print("Welcome to the Commander Data Emulator!")
    print("You can chat with Commander Data. Type 'exit' to quit.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = data_emulator.respond(user_input)
        print(response)
