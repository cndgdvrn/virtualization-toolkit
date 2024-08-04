import vtk

def read_stl(filename):
    reader = vtk.vtkSTLReader()
    reader.SetFileName(filename)
    reader.Update()
    return reader.GetOutput()

def write_stl(polydata, filename):
    writer = vtk.vtkSTLWriter()
    writer.SetFileName(filename)
    writer.SetInputData(polydata)
    writer.Write()

def clean_mesh(polydata):
    cleaner = vtk.vtkCleanPolyData()
    cleaner.SetInputData(polydata)
    cleaner.Update()
    return cleaner.GetOutput()

def fill_holes(polydata):
    hole_filler = vtk.vtkFillHolesFilter()
    hole_filler.SetInputData(polydata)
    hole_filler.SetHoleSize(1000.0)
    hole_filler.Update()
    return hole_filler.GetOutput()

def repair_mesh(polydata):
    clean_polydata = clean_mesh(polydata)
    
    filled_polydata = fill_holes(clean_polydata)
    
    return filled_polydata

def main():
    input_filename = './stls/torus_1.stl'
    output_filename = './stls/torus_1_repaired.stl'
    
    polydata = read_stl(input_filename)
    
    repaired_polydata = repair_mesh(polydata)
    
    write_stl(repaired_polydata, output_filename)

if __name__ == "__main__":
    main()
