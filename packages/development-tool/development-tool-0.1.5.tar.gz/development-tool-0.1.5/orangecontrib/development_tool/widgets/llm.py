import os
import sys

import Orange.data
from Orange.widgets import widget

from orangecontrib.development_tool.widgets import MetManagement, shared_variables, shared_functions
from Orange.widgets.utils.signals import Input, Output
from PyQt5 import QtCore, QtWidgets

from PyQt5 import uic
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon


from orangecontrib.development_tool.widgets.Gpt4AllManagement import call_completion_api

class LLM(widget.OWWidget):
    name = "LLM"
    description = "Large language model"
    icon = "icons/chat-bot.png"
    priority = 10

    dossier_du_script = os.path.dirname(os.path.abspath(__file__))
    input_data = None
    model_name = "orca-mini-3b-gguf2-q4_0.gguf" #example; a remplacer
    output_data = None
    input_data = None

    localhost = ""
    message_content = ""

    class Inputs:
        input_data = Input("Data", Orange.data.Table)


    class Outputs:
        data_out = Output("Data", Orange.data.Table)

    @Inputs.input_data
    def set_data(self, dataset):
        self.input_data = dataset





    def __init__(self):
        super().__init__()


        self.setFixedWidth(1200)
        self.setFixedHeight(200)
        self.setAutoFillBackground(True)

        # QT Management
        uic.loadUi(self.dossier_du_script + '/widget_designer/llm.ui', self)
        self.setAutoFillBackground(True)

        self.label = self.findChild(QtWidgets.QLabel, 'label')
        self.checkBox_add_a_condition = self.findChild(QtWidgets.QCheckBox, 'checkBox_add_a_condition')

        self.localhost = self.findChild(QtWidgets.QLineEdit, 'localhost')
        self.localhost.setText("localhost:4891")
        self.message_content = self.findChild(QtWidgets.QLineEdit, 'message')


        self.applyButton = self.findChild(QtWidgets.QPushButton, 'applyButton')
        self.applyButton.clicked.connect(self.use_llm)
        self.operator = self.findChild(QtWidgets.QComboBox, 'operator_2')

        self.push_button = self.findChild(QtWidgets.QPushButton, 'pushButton_show_hkh_website')
        self.push_button.setIcon(QIcon(self.dossier_du_script+'/icons/Logo_HKH.svg'))
        self.push_button.setIconSize(QSize(65, 65))
        self.push_button.clicked.connect(shared_functions.openlink)
        self.refresh_all()


        MetManagement.force_save(self)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.WindowActivate:
            self.refresh_all()
        # return super.eventFilter(obj,event) # True on filtre l element
        return super().eventFilter(source, event)


        # True ou False -> False on ne filtre pas

    def refresh_all(self):
        return



    def Enable_conditions(self, booleen):
        # Method to enable or disable conditions based on the boolean parameter.

        # Parameters:
        # - booleen (bool): True to enable conditions, False to disable conditions.

        # Actions:
        # - If 'booleen' is True:
        #   - Sets 'AddAcondition' to 1.
        #   - Attempts to read a dictionary of variables. If an error occurs, prints a message.
        # - If 'booleen' is False:
        #   - Sets 'AddAcondition' to 0.
        # - Calls 'UpdateMetFile' to update metadata file parameters.
        # - Enables or disables various UI components based on 'booleen'.


        # Calls methods to populate combo boxes with relevant data.
        return



    def maj_formula(self):
        if self.checkBox_add_a_condition.isChecked() == False:
            self.label_formula.setText("Formula :")
            self.UpdateMetFile()
            return
        if self.partie_1 == "" or self.partie_2 == "":
            self.label_formula.setText("Formula :")
        else:
            texte_a_afficher = "If "
            texte_a_afficher += self.partie_1 + self.operateur + self.partie_2
            texte_a_afficher += ' goto label Else "standard output"'
            self.label_formula.setText(texte_a_afficher)
        self.UpdateMetFile()

    def use_llm(self):

        localhost = self.localhost.text()
        message_content = self.message_content.text()
        res = call_completion_api(localhost, message_content)

        print("res", res)
        self.Outputs.data_out.send("oui")

if __name__ == "__main__":
    # sys.exit(main())
    from Orange.data.io import CSVReader

    shared_variables.current_doc = os.path.dirname(__file__) + "/dataset_devellopper/fakeows.ows"

    file = os.path.dirname(__file__) + "/dataset_devellopper/fake_input.csv"  #
    objet_csv_reader = CSVReader(file)
    objet_csv_reader.DELIMITERS = ';'
    data = objet_csv_reader.read()


    from AnyQt.QtWidgets import QApplication

    app = QApplication(sys.argv)
    mon_objet = LLM()
    mon_objet.show()


    mon_objet.handleNewSignals()
    app.exec_()
