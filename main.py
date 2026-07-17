import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel,
    QPushButton, QListWidget, QFileDialog,
    QVBoxLayout, QHBoxLayout)


app = QApplication([])
window = QWidget()
window.resize(700, 500)
window.setWindowTitle('Easy Editor by Archi')


folder_button = QPushButton('Folder')
image_list = QListWidget()
image = QLabel('Image')


left = QPushButton('Left')
right = QPushButton('Right')
mirror = QPushButton('Mirror')
sharp = QPushButton('Sharp')
bw = QPushButton('Black & White')


row = QHBoxLayout()


col1 = QVBoxLayout()
col1.addWidget(folder_button)
col1.addWidget(image_list)
col2 = QVBoxLayout()
col2.addWidget(image)
filter_button_row = QHBoxLayout()
filter_button_row.addWidget(left)
filter_button_row.addWidget(right)
filter_button_row.addWidget(mirror)
filter_button_row.addWidget(sharp)
filter_button_row.addWidget(bw)
col2.addLayout(filter_button_row)


row.addLayout(col1)
row.addLayout(col2)
window.setLayout(row)


window.setStyleSheet("background-color: #455c82") #WARNA 1


image_list.setStyleSheet("background-color: #dce1e8") #WARNA 2


folder_button.setStyleSheet("background-color: #c7a006") #WARNA 3
left.setStyleSheet("background-color: #c7a006") #WARNA 3
right.setStyleSheet("background-color: #c7a006") #WARNA 3
mirror.setStyleSheet("background-color: #c7a006") #WARNA 3
sharp.setStyleSheet("background-color: #c7a006") #WARNA 3
bw.setStyleSheet("background-color: #c7a006") #WARNA 3


window.show()


workdir = ''
def filter(files, extensions):
    result = []
    for filename in files:
           for ext in extensions:
               if filename.endswith(ext):
                   result.append(filename)
    return result


def choose_workdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
 
def show_filenames_list():
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.bmp']
    choose_workdir()
    filenames = filter(os.listdir(workdir), extensions)
    image_list.clear()
    for filename in filenames:
        image_list.addItem(filename)


folder_button.clicked.connect(show_filenames_list)


from PIL import Image
from PIL import ImageFilter
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"
  
    def load_image(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)


    def show_image(self, path):
        image.hide()
        pixmapimage = QPixmap(path)
        w, h = image.width(), image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        image.setPixmap(pixmapimage)
        image.show()


    def save_image(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
           os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.save_image()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(image_path)
    
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.save_image()
        image_path = os.path.join(self.dir,self.save_dir,self.filename)
        self.show_image(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.save_image()
        image_path = os.path.join(self.dir,self.save_dir,self.filename)
        self.show_image(image_path)
    
    def do_mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.save_image()
        image_path = os.path.join(self.dir,self.save_dir,self.filename)
        self.show_image(image_path)
    
    def do_sharp(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.save_image()
        image_path = os.path.join(self.dir,self.save_dir,self.filename)
        self.show_image(image_path)


workimage = ImageProcessor()
bw.clicked.connect(workimage.do_bw)
left.clicked.connect(workimage.do_left)
right.clicked.connect(workimage.do_right)
mirror.clicked.connect(workimage.do_mirror)
sharp.clicked.connect(workimage.do_sharp)


def show_choosen_image():
   if image_list.currentRow() >= 0:
       filename = image_list.currentItem().text()
       workimage.load_image(workdir, filename)
       image_path = os.path.join(workimage.dir, workimage.filename)   
       workimage.show_image(image_path)


image_list.currentRowChanged.connect(show_choosen_image)
app.exec_()
