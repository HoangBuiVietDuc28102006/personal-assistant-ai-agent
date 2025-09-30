from agent.agent import Agent

class CLI:
    def __init__(self):
        self.agent = Agent()

    def run(self):
        print("Type 'q' to quit!")
        print("Personal Assistant Chat:")
        while True:
            user_input = input("You: ")
            if user_input.lower() == "q":
                print("Quitting...")
                break
            
            reply = self.agent.chat(user_input)
            print(f"Assistant: {reply}")