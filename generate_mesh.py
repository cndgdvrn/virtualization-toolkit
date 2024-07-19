import vtk

def create_sample_mesh():
    # Create points
    points = vtk.vtkPoints()
    points.InsertNextPoint(0.0, 0.0, 0.0)
    points.InsertNextPoint(1.0, 0.0, 0.0)
    points.InsertNextPoint(1.0, 1.0, 0.0)
    points.InsertNextPoint(0.0, 1.0, 0.0)
    points.InsertNextPoint(0.0, 0.0, 1.0)
    points.InsertNextPoint(1.0, 0.0, 1.0)
    points.InsertNextPoint(1.0, 1.0, 1.0)
    points.InsertNextPoint(0.0, 1.0, 1.0)

    # Create a hexahedron from the points
    hexahedron = vtk.vtkHexahedron()
    for i in range(8):
        hexahedron.GetPointIds().SetId(i, i)

    # Create a cell array to store the hexahedron in
    cells = vtk.vtkCellArray()
    cells.InsertNextCell(hexahedron)

    # Create an unstructured grid to store everything in
    ugrid = vtk.vtkUnstructuredGrid()
    ugrid.SetPoints(points)
    ugrid.InsertNextCell(hexahedron.GetCellType(), hexahedron.GetPointIds())

    # Write the unstructured grid to a .vtk file
    writer = vtk.vtkUnstructuredGridWriter()
    writer.SetFileName("sample_mesh.vtk")
    writer.SetInputData(ugrid)
    writer.Write()
    print("Mesh created successfully")

if __name__ == "__main__":
    create_sample_mesh()
