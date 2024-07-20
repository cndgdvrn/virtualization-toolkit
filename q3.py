import vtk
import numpy as np

def create_wave_mesh():
    points = vtk.vtkPoints()  
    polys = vtk.vtkCellArray()  

    wave_size = 40  

    for i in range(wave_size):
        for j in range(wave_size):
            x = i
            y = j
            z = 2 * np.sin(i * 0.4) * np.cos(j * 0.4)  
            points.InsertNextPoint(x, y, z)  

    for i in range(wave_size - 1):
        for j in range(wave_size - 1):
            quad = vtk.vtkQuad()
            quad.GetPointIds().SetId(0, i * wave_size + j)
            quad.GetPointIds().SetId(1, (i + 1) * wave_size + j)
            quad.GetPointIds().SetId(2, (i + 1) * wave_size + (j + 1))
            quad.GetPointIds().SetId(3, i * wave_size + (j + 1))
            polys.InsertNextCell(quad)

    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetPolys(polys)

    return polydata

def visualize(mesh):
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(mesh)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(0.1, 0.2, 0.4)

    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)

    render_window.Render()
    render_window_interactor.Start()

if __name__ == "__main__":
    mesh = create_wave_mesh()
    visualize(mesh)
