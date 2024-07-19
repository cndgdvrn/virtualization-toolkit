import vtk
import numpy as np

# Örnek bir dalga yüzeyi (sine wave) oluşturan fonksiyon
def create_wave_mesh():
    points = vtk.vtkPoints()
    polys = vtk.vtkCellArray()

    wave_size = 40  # Mesh çözünürlüğünü artırdık
    for i in range(wave_size):
        for j in range(wave_size):
            x = i
            y = j
            z = 2 * np.sin(i * 0.4) * np.cos(j * 0.4)  # Frekansı ve genliği artırdık
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

# Komşuları bulan fonksiyon
def find_neighbors(mesh, point_id):
    neighbors = set()
    cell_ids = vtk.vtkIdList()
    mesh.GetPointCells(point_id, cell_ids)
    
    for i in range(cell_ids.GetNumberOfIds()):
        cell_id = cell_ids.GetId(i)
        cell = mesh.GetCell(cell_id)
        
        for j in range(cell.GetNumberOfPoints()):
            neighbor_id = cell.GetPointId(j)
            if neighbor_id != point_id:
                neighbors.add(neighbor_id)
    
    return list(neighbors)

# Aşağı yöne bakan ekstremum noktalarını bulan fonksiyon
def find_downward_extrema_points(mesh):
    points = mesh.GetPoints()
    num_points = points.GetNumberOfPoints()
    
    downward_extrema_points = vtk.vtkPoints()
    
    for i in range(num_points):
        point_z = points.GetPoint(i)[2]
        neighbors = find_neighbors(mesh, i)
        
        is_min = True
        
        for neighbor in neighbors:
            neighbor_z = points.GetPoint(neighbor)[2]
            if point_z >= neighbor_z:
                is_min = False
        
        if is_min:
            downward_extrema_points.InsertNextPoint(points.GetPoint(i))
    
    # Aşağı yöne bakan ekstremum noktalarını yazdır
    print(f"Bulunan aşağı yöne bakan ekstremum noktaları sayısı: {downward_extrema_points.GetNumberOfPoints()}")
    for i in range(downward_extrema_points.GetNumberOfPoints()):
        print(downward_extrema_points.GetPoint(i))
    
    return downward_extrema_points

# Görselleştirme fonksiyonu
def visualize(mesh, extrema_points):
    extrema_polydata = vtk.vtkPolyData()
    extrema_polydata.SetPoints(extrema_points)
    
    sphere = vtk.vtkSphereSource()
    sphere.SetRadius(0.3)  # Küre boyutunu artırdım
    
    glyph3D = vtk.vtkGlyph3D()
    glyph3D.SetSourceConnection(sphere.GetOutputPort())
    glyph3D.SetInputData(extrema_polydata)
    glyph3D.Update()
    
    extrema_mapper = vtk.vtkPolyDataMapper()
    extrema_mapper.SetInputConnection(glyph3D.GetOutputPort())
    
    extrema_actor = vtk.vtkActor()
    extrema_actor.SetMapper(extrema_mapper)
    extrema_actor.GetProperty().SetColor(1, 0, 0)
    
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(mesh)
    
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)
    
    renderer.AddActor(actor)
    renderer.AddActor(extrema_actor)
    renderer.SetBackground(0.1, 0.2, 0.4)
    
    render_window.Render()
    render_window_interactor.Start()

if __name__ == "__main__":
    # Örnek dalga yüzeyi oluştur
    mesh = create_wave_mesh()
    # Aşağı yöne bakan ekstremum noktalarını bul
    downward_extrema_points = find_downward_extrema_points(mesh)
    # Görselleştir
    visualize(mesh, downward_extrema_points)
