import os
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtGui, QtWidgets

from Orange.widgets import widget


class FileSelectorApp(widget.OWWidget):

    # Chemin du répertoire du script
    dossier_du_script = os.path.dirname(os.path.abspath(__file__))
    name = "Load Workflow"
    description = "Select a workflow from a list of example, and duplicate it locally"    
    icon = "icons/duplicate.png"


    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Charger l'interface utilisateur à partir du fichier .ui créé avec Qt Designer
        loadUi(os.path.join(self.dossier_du_script, 'widget_designer/load_workflow.ui'), self)
        # Récupérer la ComboBox
        self.comboBox = self.findChild(QtWidgets.QComboBox, 'comboBox')
        # Connecter le signal currentIndexChanged de la ComboBox au slot handleComboBoxChange
        self.comboBox.currentIndexChanged.connect(self.handleComboBoxChange)
        # Récupérer le bouton "Save As"
        self.saveButton = self.findChild(QtWidgets.QPushButton, 'save')
        # Connecter le signal clicked du bouton au slot saveFile
        self.saveButton.clicked.connect(self.saveFile)
        # Remplir la ComboBox avec les noms de fichiers du dossier
        self.populate_combo_box()

    def populate_combo_box(self):
        # Récupérer le chemin du dossier contenant les fichiers
        directory_path = os.path.join(self.dossier_du_script, 'ows_example')
        # Obtenir la liste des fichiers dans le dossier
        file_names = [file for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]
        # Ajouter les noms des fichiers à la QComboBox
        self.comboBox.addItems(file_names)

    def handleComboBoxChange(self, index):
        # Gérer le changement de sélection dans la ComboBox
        selected_file = self.comboBox.itemText(index)
        print("Selected file:", selected_file)

    def saveFile(self):
        # Méthode pour sauvegarder le fichier sélectionné dans un nouvel emplacement
        selected_file = self.comboBox.currentText()
        if selected_file:
            # Chemin du fichier source
            file_path = os.path.join(self.dossier_du_script, 'ows_example', selected_file)
            # Obtenir le chemin de destination à l'aide d'une boîte de dialogue
            destination_path, _ = QFileDialog.getSaveFileName(self, "Save file as", selected_file)
            if destination_path:
                try:
                    # Copier le fichier source vers le chemin de destination
                    shutil.copyfile(file_path, destination_path)
                    print("File successfully copied to:", destination_path)
                except Exception as e:
                    print("Error copying file:", str(e))


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = FileSelectorApp()
    window.show()
    sys.exit(app.exec_())
