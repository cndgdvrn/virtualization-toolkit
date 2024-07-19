



# import vtk
# import math

# def create_wave_mesh():
#     points = vtk.vtkPoints()
#     polys = vtk.vtkCellArray()
    
#     wave_size = 20
#     for i in range(wave_size):
#         for j in range(wave_size):
#             x = i
#             y = j
#             z = 2 * math.sin(i * 0.2) * math.cos(j * 0.2)
#             points.InsertNextPoint(x, y, z)
    
#     for i in range(wave_size - 1):
#         for j in range(wave_size - 1):
#             quad = vtk.vtkQuad()
#             quad.GetPointIds().SetId(0, i * wave_size + j)
#             quad.GetPointIds().SetId(1, (i + 1) * wave_size + j)
#             quad.GetPointIds().SetId(2, (i + 1) * wave_size + (j + 1))
#             quad.GetPointIds().SetId(3, i * wave_size + (j + 1))
#             polys.InsertNextCell(quad)
    
#     polydata = vtk.vtkPolyData()
#     polydata.SetPoints(points)
#     polydata.SetPolys(polys)
    
#     return polydata

# def project_to_xz_plane(mesh):
#     projected_points = vtk.vtkPoints()
#     for i in range(mesh.GetNumberOfPoints()):
#         x, y, z = mesh.GetPoint(i)
#         projected_points.InsertNextPoint(x, 0, z)
    
#     projected_mesh = vtk.vtkPolyData()
#     projected_mesh.SetPoints(projected_points)
#     projected_mesh.SetPolys(mesh.GetPolys())
#     return projected_mesh

# def visualize(mesh, projected_mesh):
#     original_mapper = vtk.vtkPolyDataMapper()
#     original_mapper.SetInputData(mesh)
    
#     original_actor = vtk.vtkActor()
#     original_actor.SetMapper(original_mapper)
#     original_actor.GetProperty().SetColor(0, 0, 1)  # Mavi renk
#     original_actor.GetProperty().SetOpacity(0.5)    # Orijinal mesh yarı saydam
    
#     projected_mapper = vtk.vtkPolyDataMapper()
#     projected_mapper.SetInputData(projected_mesh)
    
#     projected_actor = vtk.vtkActor()
#     projected_actor.SetMapper(projected_mapper)
#     projected_actor.GetProperty().SetColor(1, 0, 0)  # Kırmızı renk
#     projected_actor.GetProperty().SetOpacity(0.5)    # Projeksiyon yarı saydam
    
#     renderer = vtk.vtkRenderer()
#     renderer.AddActor(original_actor)
#     renderer.AddActor(projected_actor)
#     renderer.SetBackground(1, 1, 1)  # Beyaz arkaplan
    
#     render_window = vtk.vtkRenderWindow()
#     render_window.AddRenderer(renderer)
    
#     render_window_interactor = vtk.vtkRenderWindowInteractor()
#     render_window_interactor.SetRenderWindow(render_window)
    
#     # Kamerayı projeksiyon düzlemine dik konumlandır
#     camera = renderer.GetActiveCamera()
#     camera.SetPosition(10, 30, 30)
#     camera.SetFocalPoint(10, 10, 0)
    
#     render_window.Render()
#     render_window_interactor.Start()

# def main():
#     # Dalga yüzeyi oluştur
#     mesh = create_wave_mesh()
    
#     # Projeksiyon işlemini gerçekleştir
#     projected_mesh = project_to_xz_plane(mesh)
    
#     # Mesh'i ve projeksiyonu görselleştir
#     visualize(mesh, projected_mesh)

# if __name__ == "__main__":
#     main()s


import numpy as np
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# Örnek bir mesh oluştur
# Bu örnekte, bir küre mesh'i kullanacağız
phi, theta = np.mgrid[0.0:2.0 * np.pi:100j, 0.0:np.pi:50j]
x = np.sin(theta) * np.cos(phi)
y = np.sin(theta) * np.sin(phi)
z = np.cos(theta)

# Mesh'in x-z düzlemine izdüşümünü hesapla
# İzdüşüm alırken y bileşenini göz ardı edeceğiz
x_proj = x
z_proj = z

# 3D mesh'i ve izdüşümünü görselleştir
fig = plt.figure(figsize=(12, 6))

# 3D mesh
ax1 = fig.add_subplot(121, projection='3d')
ax1.plot_surface(x, y, z, color='b', alpha=0.6)
ax1.set_title('Original 3D Mesh')
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Z')

# X-Z düzlemine izdüşüm
ax2 = fig.add_subplot(122)
ax2.scatter(x_proj, z_proj, color='r', s=0.1)
ax2.set_title('Projection on X-Z Plane')
ax2.set_xlabel('X')
ax2.set_ylabel('Z')

plt.tight_layout()
plt.show()
