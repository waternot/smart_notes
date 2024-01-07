from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog
from ui import Ui_MainWindow
import json

class Widget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
       
        self.ui.button_note_create.clicked.connect(self.add_note)
        self.ui.button_note_save.clicked.connect(self.save_note)
        self.ui.button_note_del.clicked.connect(self.del_note)
        self.ui.button_tag_add.clicked.connect(self.add_tag)
        self.ui.button_tag_del.clicked.connect(self.del_tag)
        self.ui.button_tag_search.clicked.connect(self.search_tag)

        self.ui.list_notes.itemClicked.connect(self.show_note)



        with open("notes_data.json","r") as file:
            self.notes = json.load(file)
            self.ui.list_notes.addItems(self.notes)

    def show_note(self):
        key = self.ui.list_notes.selectedItems()[0].text()
        self.ui.field_text.setText(self.notes[key]["текст"])
        self.ui.list_tags.clear()
        self.ui.list_tags.addItems(self.notes[key]["теги"])
        print(self.notes)

    def add_note(self):
        note_name, ok = QInputDialog.getText(ex, "додати замітку","назва замітки:")
        if ok and note_name !="":
            self.notes[note_name] = {"текст":"","теги":[]}
            self.ui.list_notes.addItem(note_name)
            self.ui.list_tags.addItems(self.notes[note_name]["теги"])
            print(self.notes)


    def save_note(self):
        if self.ui.list_notes.selectedItems():
            key = self.ui.list_notes.selectedItems()[0].text()
            self.notes[key]["текст"] = self.ui.field_text.toPlainText()
            with open("notes_data.json","w") as file:
                json.dump(self.notes,file, sort_keys=True,ensure_ascii=False)
            print(self.notes)
        else:
            print("Замітка для збереження не вибрана")

    def del_note(self):
        if self.ui.list_notes.selectedItems():
            key = self.ui.list_notes.selectedItems()[0].text()
            del self.notes[key]
            self.ui.list_notes.clear()
            self.ui.list_tags.clear()
            self.ui.field_text.clear()
            self.ui.list_notes.addItems(self.notes)
            with open("notes_data.json","w") as file:
                json.dump(self.notes,file,sort_keys=True,ensure_ascii=False)
            print(self.notes)
        else:
            print("Замітка для вилучення не вибрана")
 

    def add_tag(self):
        if self.ui.list_notes.selectedItems():
            key = self.ui.list_notes.selectedItems()[0].text()
            tag = self.ui.field_tag.text()
            if not tag in self.notes[key]["теги"]:
                self.notes[key]["теги"].append(tag)
                self.ui.list_tags.addItem(tag)
                self.ui.field_tag.clear()
            with open("notes_data.json","w") as file:
                json.dump(self.notes,file,sort_keys=True,ensure_ascii=False)
            print(self.notes)
        else:
            print("Замітка для додавання тега не обрана!")

    def del_tag(self):
        if self.ui.list_tags.selectedItems():
            key = self.ui.list_notes.selectedItems()[0].text()
            tag = self.ui.list_tags.selectedItems()[0].text()
            self.notes[key]["теги"].remove(tag)
            self.ui.list_tags.clear()
            self.ui.list_tags.addItems(self.notes[key]["теги"])
            with open("notes_data.json","w") as file:
                json.dump(self.notes,file,sort_keys=True,ensure_ascii=False)
        else:
            print("Тег для вилучення не обраний")

    def search_tag(self):
        print(self.ui.button_tag_search.text())
        tag = self.ui.field_tag.text()
        if self.ui.button_tag_search.text() == "Шукати замітки по тегу" and tag:
            print(tag)
            notes_filtered = {}
            for note in self.notes:
                if tag in self.notes[note]["теги"]:
                    notes_filtered[note] = self.notes[note]
            self.ui.button_tag_search.setText("Скинути пошук")
            self.ui.list_notes.clear()
            self.ui.list_tags.clear()
            self.ui.list_notes.addItems(notes_filtered)
            print(self.ui.button_tag_search.text())
        elif self.ui.button_tag_search.text() == "Скинути пошук":
            self.ui.field_tag.clear()
            self.ui.list_notes.clear()
            self.ui.list_tags.clear()
            self.ui.list_notes.addItems(self.notes)
            self.ui.button_tag_search.setText("Шукати замітки по тегу")
            print(self.ui.button_tag_search.text())
        else:
            pass


app = QApplication([])
ex = Widget()
ex.show()
app.exec_()