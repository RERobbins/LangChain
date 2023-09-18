import cmd
import textwrap
from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory

load_dotenv(find_dotenv(".langsmith_env"))
load_dotenv(find_dotenv())


class MyCmd(cmd.Cmd):
    intro = "Welcome to Felica, a Private ChatGPT Clone. Type 'help' to list special commands."
    prompt = "Human> "

    llm = None
    conversation = None

    def do_quit(self, arg):
        """Exit the program."""
        return True

    def do_clear(self, arg):
        """Start a new chat."""
        print("Start a new chat.")

    def do_model(self, arg):
        """Select a model (gpt-3.5-turbo or gpt-4)."""
        arg = arg.lower()
        if arg not in ["gpt-3.5-turbo", "gpt-4"]:
            print(
                "Invalid model selection. Use 'model gpt-3.5-turbo' or 'model gpt-4'."
            )
        else:
            print(f"Current model is {arg}")
            self.llm = ChatOpenAI(model_name=arg, temperature=0)
            self.conversation = ConversationChain(
                llm=self.llm,
                memory=ConversationSummaryBufferMemory(llm=self.llm,
                                                       max_token_limit=100),
                verbose=True,
            )

    def default(self, line):
        """Send a user prompt to the chatbot."""
        if self.llm:
            result = self.conversation(line)['response']
            print(textwrap.fill(result))
        else:
            print("Please select a model using 'model gpt-3.5-turbo' or 'model GPT-4'.")


if __name__ == "__main__":
    my_cmd = MyCmd()
    my_cmd.do_model("gpt-3.5-turbo")  # Force a model command call
    my_cmd.cmdloop()
