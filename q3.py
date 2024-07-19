import sys
import vtk
from PyQt5 import QtCore, QtWidgets
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class ObjectManager:
    def __init__(self, renderer, list_widget):
        self.renderer = renderer
        self.list_widget = list_widget
        self.objects = {}
        self.object_id = 0

    def add_object(self, x, y, z):
        sphere = vtk.vtkSphereSource()
        sphere.SetCenter(x, y, z)
        sphere.SetRadius(0.1)
        
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(sphere.GetOutputPort())
        
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        
        self.renderer.AddActor(actor)
        self.renderer.GetRenderWindow().Render()
        
        object_name = f"Object {self.object_id}"
        self.objects[object_name] = actor
        self.list_widget.addItem(object_name)
        self.object_id += 1

    def remove_object(self):
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            for item in selected_items:
                object_name = item.text()
                actor = self.objects.pop(object_name, None)
                if actor:
                    self.renderer.RemoveActor(actor)
                    self.renderer.GetRenderWindow().Render()
                self.list_widget.takeItem(self.list_widget.row(item))

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        
        self.frame = QtWidgets.QFrame()
        self.layout = QtWidgets.QHBoxLayout()
        
        self.vtk_widget = QVTKRenderWindowInteractor(self.frame)
        self.layout.addWidget(self.vtk_widget)
        
        self.list_widget = QtWidgets.QListWidget()
        self.layout.addWidget(self.list_widget)
        
        self.frame.setLayout(self.layout)
        self.setCentralWidget(self.frame)
        
        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        self.iren = self.vtk_widget.GetRenderWindow().GetInteractor()
        
        self.obj_manager = ObjectManager(self.renderer, self.list_widget)
        
        self.iren.AddObserver("LeftButtonPressEvent", self.on_left_click)
        self.list_widget.itemDoubleClicked.connect(self.obj_manager.remove_object)
        
        self.iren.Initialize()
        self.iren.Start()

    def on_left_click(self, obj, event):
        click_pos = self.iren.GetEventPosition()
        picker = vtk.vtkWorldPointPicker()
        picker.Pick(click_pos[0], click_pos[1], 0, self.renderer)
        pos = picker.GetPickPosition()
        self.obj_manager.add_object(pos[0], pos[1], pos[2])

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
