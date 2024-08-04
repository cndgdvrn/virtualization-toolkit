import sys
import vtk
from PyQt5 import QtCore, QtWidgets
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import random

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        self.frame = QtWidgets.QFrame()
        self.layout = QtWidgets.QVBoxLayout()

        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.layout.addWidget(self.vtkWidget)

        self.frame.setLayout(self.layout)
        self.setCentralWidget(self.frame)
        
        self.renderer = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)
        self.interactor = self.vtkWidget.GetRenderWindow().GetInteractor()

        self.read_and_display_models('/mnt/data/packing.stl')

        self.show()
        self.interactor.Initialize()
        self.interactor.Start()

    def read_and_display_models(self, file_path):
        model = self.read_stl(file_path)
        all_models = []
        for _ in range(random.randint(3, 7)):
            all_models.extend(self.duplicate_models(model, random.randint(3, 7)))
        packed_models = self.pack_models(all_models)
        self.visualize_models(packed_models)

    def read_stl(self, file_path):
        reader = vtk.vtkSTLReader()
        reader.SetFileName(file_path)
        reader.Update()
        return reader.GetOutput()

    def duplicate_models(self, model, num_copies):
        models = []
        for _ in range(num_copies):
            transform = vtk.vtkTransform()
            transform.Translate(random.uniform(0, 100), random.uniform(0, 100), 0)
            transform_filter = vtk.vtkTransformPolyDataFilter()
            transform_filter.SetInputData(model)
            transform_filter.SetTransform(transform)
            transform_filter.Update()
            models.append(transform_filter.GetOutput())
        return models

    def check_intersection(self, model1, model2):
        bounding_box1 = model1.GetBounds()
        bounding_box2 = model2.GetBounds()
        return not (bounding_box1[1] < bounding_box2[0] or bounding_box1[0] > bounding_box2[1] or
                    bounding_box1[3] < bounding_box2[2] or bounding_box1[2] > bounding_box2[3])

    def pack_models(self, models):
        packed_models = []
        for model in models:
            placed = False
            while not placed:
                intersecting = False
                for placed_model in packed_models:
                    if self.check_intersection(model, placed_model):
                        intersecting = True
                        break
                if not intersecting:
                    packed_models.append(model)
                    placed = True
                else:
                    transform = vtk.vtkTransform()
                    transform.Translate(random.uniform(0, 100), random.uniform(0, 100), 0)
                    transform_filter = vtk.vtkTransformPolyDataFilter()
                    transform_filter.SetInputData(model)
                    transform_filter.SetTransform(transform)
                    transform_filter.Update()
                    model = transform_filter.GetOutput()
        return packed_models

    def visualize_models(self, models):
        for model in models:
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputData(model)
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            self.renderer.AddActor(actor)
        self.renderer.SetBackground(0.1, 0.2, 0.4)
        self.vtkWidget.GetRenderWindow().Render()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
