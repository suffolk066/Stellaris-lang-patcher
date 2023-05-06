import os
import re
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox

default_address = r'C:\Program Files (x86)\Steam\steamapps\workshop\content\281990'


def replace_l_english_to_l_korean(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_contents = file.read()

    new_contents = file_contents.replace('l_english:', 'l_korean:')

    return new_contents


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('gui.ui', parentWidget=None)
        self.ui.toolButton.clicked.connect(self.get_path)
        if not self.ui.textEdit.toPlainText():
            self.ui.textEdit.setText(default_address)
        self.ui.pushButton.clicked.connect(self.start_patch)

    def get_path(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        directory_path = QFileDialog.getExistingDirectory(self, 'Select Directory', default_address, options=options)
        if directory_path:
            print(directory_path)
            self.ui.textEdit.setText(directory_path)

    def start_patch(self):
        find_file_count = 0
        replace_file_count = 0
        find_file_address = []

        for root, dirs, _ in os.walk(self.ui.textEdit.toPlainText()):
            if 'localisation' in dirs:
                loc_path = os.path.join(root, 'localisation')
                english_loc_path = os.path.join(loc_path, 'english') if 'english' in os.listdir(loc_path) else loc_path

                if english_loc_path != loc_path:
                    korean_loc_path = os.path.join(loc_path, 'korean')

                    if not os.path.exists(korean_loc_path):
                        os.makedirs(korean_loc_path)
                else:
                    korean_loc_path = loc_path

                print(f'현재 경로 : {english_loc_path}')

                for loc_file in os.listdir(english_loc_path):
                    if re.search(r'.+english\.yml', loc_file):
                        new_file_name = loc_file.replace('english.yml', 'korean.yml')
                        old_file_path = os.path.join(english_loc_path, loc_file)
                        new_file_path = os.path.join(korean_loc_path, new_file_name)

                        if not os.path.exists(new_file_path):
                            new_contents = replace_l_english_to_l_korean(old_file_path)
                            with open(new_file_path, 'w', encoding='utf-8') as new_file:
                                new_file.write(new_contents)

                            replace_file_count += 1
                            # print(f'korean 파일 생성 완료 : {new_file_path}')
                        else:
                            # print(f'korean 파일 이미 존재함 : {new_file_path}')
                            pass

                        find_file_count += 1
                        find_file_address.append(english_loc_path)
                        # print(f'파일 작성 끝 : {english_loc_path}')

        print(f'찾은 파일 개수 : {find_file_count}')
        print(f'변경한 파일 개수 : {replace_file_count}')
        print(f'파일 주소 : {find_file_address}')
        QMessageBox.information(self, '작업 완료', f'찾은 파일 개수 : {find_file_count}\n변경한 파일 개수 : {replace_file_count}')

    def main(self):
        self.ui.show()


if __name__ == "__main__":
    app = QApplication([])
    widget = MyWidget()
    widget.main()
    app.exec()
