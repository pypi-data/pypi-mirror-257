# https://orange3.readthedocs.io/projects/orange-development/en/latest/tutorial-settings.html
import os
import sys
import ntpath

from Orange.widgets import widget
from Orange.widgets.utils.signals import Input, Output

from Orange.data import Domain, Table, StringVariable, ContinuousVariable, DiscreteVariable

from LTTL.Segmentation import Segmentation

from PyQt5 import uic
from PyQt5 import QtWidgets
from AnyQt.QtWidgets import QApplication

from gpt4all import GPT4All

class OWChatbot(widget.OWWidget):
    name = "Chatbot"
    description = """Select a local language model (.gguf file) to process a text request ! 
    The Table "Parameters" contains the following columns :
    Max length | Temperature | Top K | Top P | Repeat penalty | Repeat last n | Batch size"""
    icon = "icons/chatbot.svg"
    priority = 10
    want_control_area = False

    class Inputs:
        preprompt = Input("Pre-prompt", Segmentation)
        request = Input("Request", Segmentation)
        postprompt = Input("Post-prompt", Segmentation)
        parameters = Input("Parameters", Table)

    class Outputs:
        data = Output("Data", Table)

    class Error(widget.OWWidget.Error):
        pass

    @Inputs.preprompt
    def set_preprompt(self, in_segmentation):
        self.preprompt = in_segmentation.to_string().split('content:\t"')[-1].split('"\n\tstr_index')[0]
        print("pre", self.preprompt)

    @Inputs.request
    def set_request(self, in_segmentation):
        self.request = in_segmentation.to_string().split('content:\t"')[-1].split('"\n\tstr_index')[0]
        print("req", self.request)

    @Inputs.postprompt
    def set_postprompt(self, in_segmentation):
        self.postprompt = in_segmentation.to_string().split('content:\t"')[-1].split('"\n\tstr_index')[0]
        print("post", self.postprompt)

    @Inputs.parameters
    def set_parameters(self, in_table):
        try:
            max_tokens = int(in_table[0][in_table.domain.index("Max length")])
        except ValueError:
            max_tokens = 200
        try:
            temp = in_table[0][in_table.domain.index("Temperature")].value
        except ValueError:
            temp = 0.7
        try:
            top_k = int(in_table[0][in_table.domain.index("Top K")])
        except ValueError:
            top_k = 40
        try:
            top_p = in_table[0][in_table.domain.index("Top P")].value
        except ValueError:
            top_p = 0.4
        try:
            repeat_penalty = in_table[0][in_table.domain.index("Repeat penalty")].value
        except ValueError:
            repeat_penalty = 1.18
        try:
            repeat_last_n = int(in_table[0][in_table.domain.index("Repeat last n")])
        except ValueError:
            repeat_last_n = 64
        try:
            n_batch = int(in_table[0][in_table.domain.index("Batch size")])
        except ValueError:
            n_batch = 8
        self.parameters["max_tokens"] = max_tokens
        self.parameters["temperature"] = temp
        self.parameters["top_k"] = top_k
        self.parameters["top_p"] = top_p
        self.parameters["repeat_penalty"] = repeat_penalty
        self.parameters["repeat_last_n"] = repeat_last_n
        self.parameters["n_batch"] = n_batch


    def __init__(self):
        super().__init__()
        self.preprompt = "USER:"
        self.request = None
        self.postprompt = "ASSISTANT:"
        self.parameters = {"max_tokens": 200, "temperature": 0.7, "top_k": 40, "top_p": 0.4,
                           "repeat_penalty": 1.18, "repeat_last_n":64, "n_batch":8}
        self.llm = None

        # QT Management
        uic.loadUi(os.path.dirname(os.path.abspath(__file__)) + '/widget_designer/owchatbot.ui', self)
        self.setFixedWidth(571)
        self.setFixedHeight(245)
        self.setAutoFillBackground(True)

        self.pushbtn_selectModel = self.findChild(QtWidgets.QPushButton, "selectModel")
        self.label_selectedModel = self.findChild(QtWidgets.QLabel, "selectedModel")
        self.pushbtn_runLLM = self.findChild(QtWidgets.QPushButton, "runLLM")

        self.pushbtn_selectModel.clicked.connect(self.load_model)
        self.pushbtn_runLLM.clicked.connect(self.query)


    def load_model(self):
        """Loads the selected model"""
        path = QtWidgets.QFileDialog.getOpenFileName()[0]
        try:
            self.llm = GPT4All(model_path=path,
                               model_name=path,
                               allow_download=False)
            model_name = ntpath.basename(path)
            self.label_selectedModel.setText(f"Model {model_name} successfully loaded !")
            self.Error.clear()
        except ValueError:
            self.label_selectedModel.setText(f"No model loaded")
            self.Error.add_message("data", "Could not load the model, was it a correct .gguf file ?")
            getattr(self.Error, "data")()


    def query(self):
        """Completes the input query"""
        print("1", self.request)
        print("2", self.preprompt)
        print("3", self.postprompt)
        prompt = self.preprompt  + self.request + self.postprompt
        answer = self.llm.generate(prompt=prompt,
                                   max_tokens=self.parameters["max_tokens"],
                                   temp=self.parameters["temperature"],
                                   top_k=self.parameters["top_k"],
                                   top_p=self.parameters["top_p"],
                                   repeat_penalty=self.parameters["repeat_penalty"],
                                   repeat_last_n=self.parameters["repeat_last_n"],
                                   n_batch=self.parameters["n_batch"])
        self.create_output(answer)
        # self.Error.add_message("data", "WTF IS WRONG ?")
        # getattr(self.Error, "data")()
        # out_var = None
        # getattr(self.Outputs, "data").send(out_var)


    def create_output(self, answer):
        request_domain = StringVariable(name="Request")
        answer_domain = StringVariable(name="Answer")
        domain = Domain([], metas=[request_domain, answer_domain])
        out_data = Table.from_list(domain=domain, rows=[[self.request, answer]])
        self.Outputs.data.send(out_data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mon_objet = OWChatbot()
    mon_objet.show()

    mon_objet.handleNewSignals()
    app.exec_()
