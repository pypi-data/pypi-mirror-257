
#==============================================================================#
#== Hammad Saeed ==============================================================#
#==============================================================================#
#== www.hammad.fun ============================================================#
#== hammad@supportvectors.com =================================================#
#==============================================================================#

##== HamPy ==######################################== Hammad's Python Tools ==## 
##== @/hampy ==#################################################################

from .core import MessageStyles, Message
from .core import DynamicInputInteractions, StaticInputInteractions
from .core import Validation
from .core import Frame

from .llms import OpenAIQuery

#==============================================================================#

class HPYError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

#==============================================================================#

class HammadPyTools:
    """
    All Tools are accessible from this class.
    """
    def __init__(self):
        """
        Initializes the HammadPyTools class with required objects.
        """
        self.text = MessageStyles()
        self.ask = StaticInputInteractions()
        self.askbox = DynamicInputInteractions()
    
    def ai(self, key : str): 
        """
        Queries OpenAI Completions.

        Args:
        -   key (str): The API key for OpenAI.
        
        Returns:
        -   OpenAIQuery: An instance of OpenAIQuery.
        """
        self.key = key
        self.ai = OpenAIQuery(key)
        return self.ai
    
    def error(self, message : str):
        """
        Raises an error with a custom message.

        Args:
        -   message (str): The error message.
        
        Returns:
        -   HPYError: An instance of HPYError.
        """
        self.error = HPYError(message)
        return self.error
    
    def frame(self):
        """
        Creates a new pandas DataFrame.

        Returns:
        -   Frame: An instance of Frame.
        """
        self.frame = Frame()
        return self.frame
    
    def say(self, message : str, color : str, bg : str = None, style : str = None):
        """
        Prints a styled message to the terminal.

        Args:
        -   message (str): The message to be printed.
        -   color (str): The color of the text.
        -   bg (str, optional): The background color of the text.
        -   style (str, optional): The style of the text (bold, underline, etc.).
        """
        Message(message, color, bg, style)

    def text(self):
        """
        Returns the MessageStyles object for styled terminal output.

        Returns:
        -   MessageStyles: An instance of MessageStyles.
        """
        return self.text
    
    def ask(self):
        """
        Returns the StaticInputInteractions object for static terminal input.

        Returns:
        -   StaticInputInteractions: An instance of StaticInputInteractions.
        """
        return self.ask
    
    def askbox(self):
        """
        Returns the DynamicInputInteractions object for dynamic terminal input.

        Returns:
        -   DynamicInputInteractions: An instance of DynamicInputInteractions.
        """
        return self.askbox
    
    def validate_type(self, value : str, type : str):
        """
        Validates the type of a value.

        Args:
        -   value (str): The value to be validated.
        -   type (str): The expected type of the value.
        
        Returns:
        -   bool: True if the value matches the expected type, False otherwise.
        """
        self.validator = Validation()
        return self.validator.type(value, type)
    
    def validate_empty(self, value : str):
        """
        Validates that a value is not empty.

        Args:
        -   value (str): The value to be validated.
        
        Returns:
        -   bool: True if the value is not empty, False otherwise.
        """
        self.validator = Validation()
        return self.validator.empty(value)
    
#==============================================================================#

if __name__ == "__main__":
    tools = HammadPyTools()
    input = tools.ask.prompt_input("Test", "This is a test message.")
    tools.say.emphasis(input)
    completion = tools.openai.invoke("Hello!")
    tools.say.blue(completion)


