import os
import cmd
import textwrap
from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory

# If you have an accessible langsmith endpoint you can use it.
load_dotenv(find_dotenv(".env_langsmith"))


# This script relies on .env style files.
# Each file should define the following environment variables:
#
# OPENAI.API_TYPE
# OPENAI.API_VERSION
# OPENAI_API_BASE
# OPENAI_API_KEY
# OPENAI_API_DEPLOYMENT_NAME


class MyCmd(cmd.Cmd):
    """
    This is a command-line interface for interacting with a chatbot powered by OpenAI's models.
    You can use commands to select a model and interact with the chatbot.
    """

    intro = """Welcome to Epiq's Private ChatGPT Clone. 
The default model is chatgpt-3.5-turbo.
You can change the model with the 'model' special command.
Type 'help' to list special commands.
Enter your prompt at the command line.  
 """

    prompt = "Human: "

    llm = None
    conversation = None

    def do_quit(self, arg):
        """Exit the program."""
        return True

    def do_clear(self, arg):
        """Start a new chat."""
        print("Start a new chat.\n")

    def do_model(self, arg, verbose=True):
        """
        Select a model (gpt-3.5-turbo or gpt-4) and begin a new chat.
        Usage: model <model_name>
        """
        arg = arg.lower()
        if arg not in ["gpt-3.5-turbo", "gpt-4"]:
            print(
                "Invalid model selection. Use 'model gpt-3.5-turbo' or 'model gpt-4'.\n"
            )
        else:
            if arg == "gpt-3.5-turbo":
                load_dotenv(find_dotenv(".env_azure_openai_gpt35t"))
            else:
                load_dotenv(find_dotenv(".env_azure_openai_gpt4"))

            if verbose:
                print(f"Starting a new chat with {arg}.\n")
            self.llm = AzureChatOpenAI(
                deployment_name=os.environ.get("OPENAI_API_DEPLOYMENT_NAME"),
                temperature=0,
            )

            self.conversation = ConversationChain(
                llm=self.llm,
                memory=ConversationSummaryBufferMemory(llm=self.llm),
                verbose=False,
            )

    def default(self, line):
        """
        Send a user prompt to the chatbot and display the response.
        """

        if self.llm:
            result = self.conversation(line)["response"]
            print(f"\nEpiqGPT: {textwrap.fill(result, subsequent_indent=' ' * 9)}\n")
        else:
            print("Please select a model using 'model gpt-3.5-turbo' or 'model GPT-4'.")


if __name__ == "__main__":
    my_cmd = MyCmd()
    my_cmd.do_model("gpt-3.5-turbo", verbose=False)
    my_cmd.cmdloop()
