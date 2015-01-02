__author__ = 'Michael Redmond'

import vtk
from ..filters import ExtractSelectionFilter


class ModelData(object):
    def __init__(self):
        super(ModelData, self).__init__()

        self.points = vtk.vtkPoints()
        self.nodes = vtk.vtkUnstructuredGrid()
        self.elements = vtk.vtkUnstructuredGrid()
        self.rbes = vtk.vtkUnstructuredGrid()

        self.nodes.SetPoints(self.points)
        self.elements.SetPoints(self.points)
        self.rbes.SetPoints(self.points)

        self.node_global_ids = vtk.vtkIdTypeArray()
        self.element_global_ids = vtk.vtkIdTypeArray()
        self.rbe_global_ids = vtk.vtkIdTypeArray()

        self.nodes.GetCellData().SetGlobalIds(self.node_global_ids)
        self.elements.GetCellData().SetGlobalIds(self.element_global_ids)
        self.rbes.GetCellData().SetGlobalIds(self.rbe_global_ids)

        self.node_visible = vtk.vtkIntArray()
        self.element_visible = vtk.vtkIntArray()
        self.rbe_visible = vtk.vtkIntArray()

        self.node_visible.SetName("visible")
        self.element_visible.SetName("visible")
        self.rbe_visible.SetName("visible")

        self.nodes.GetCellData().AddArray(self.node_visible)
        self.elements.GetCellData().AddArray(self.element_visible)
        self.rbes.GetCellData().AddArray(self.rbe_visible)

        self.node_original_ids = vtk.vtkIntArray()
        self.element_original_ids = vtk.vtkIntArray()
        self.rbe_original_ids = vtk.vtkIntArray()

        self.node_original_ids.SetName("original_ids")
        self.element_original_ids.SetName("original_ids")
        self.rbe_original_ids.SetName("original_ids")

        self.nodes.GetCellData().AddArray(self.node_original_ids)
        self.elements.GetCellData().AddArray(self.element_original_ids)
        self.rbes.GetCellData().AddArray(self.rbe_original_ids)

        selected = vtk.vtkIntArray()
        selected.SetName("visible")
        selected.InsertNextValue(1)
        selected.InsertNextValue(1)

        self.node_filter = ExtractSelectionFilter(selected)
        self.element_filter = ExtractSelectionFilter(selected)
        self.rbe_filter = ExtractSelectionFilter(selected)

        self.node_filter.set_input_data(self.nodes)
        self.element_filter.set_input_data(self.elements)
        self.rbe_filter.set_input_data(self.rbes)

        self.node_filter.Update()
        self.element_filter.Update()
        self.rbe_filter.Update()

    def update(self):

        self.nodes.Modified()
        self.elements.Modified()
        self.rbes.Modified()

        self.node_filter.execute()
        self.element_filter.execute()
        self.rbe_filter.execute()

        # should these be commented or not?
        #self.node_filter.set_input_data(self.nodes)
        #self.element_filter.set_input_data(self.elements)
        #self.rbe_filter.set_input_data(self.rbes)


        # these have been commented for a while
        #self.node_filter.execute()
        #self.element_filter.execute()
        #self.rbe_filter.execute()

    def reset(self):
        self.points.Reset()
        self.elements.Reset()
        self.rbes.Reset()

        self.node_global_ids.Reset()
        self.element_global_ids.Reset()
        self.rbe_global_ids.Reset()

        self.node_original_ids.Reset()
        self.element_original_ids.Reset()
        self.rbe_original_ids.Reset()

        self.node_visible.Reset()
        self.element_visible.Reset()
        self.rbe_visible.Reset()

        self.nodes.GetCellData().SetGlobalIds(self.node_global_ids)
        self.elements.GetCellData().SetGlobalIds(self.element_global_ids)
        self.rbes.GetCellData().SetGlobalIds(self.rbe_global_ids)

        self.nodes.GetCellData().AddArray(self.node_visible)
        self.elements.GetCellData().AddArray(self.element_visible)
        self.rbes.GetCellData().AddArray(self.rbe_visible)

        self.nodes.GetCellData().AddArray(self.node_original_ids)
        self.elements.GetCellData().AddArray(self.element_original_ids)
        self.rbes.GetCellData().AddArray(self.rbe_original_ids)

        self.set_points()

    def set_points(self):
        self.nodes.SetPoints(self.points)
        self.elements.SetPoints(self.points)
        self.rbes.SetPoints(self.points)

    def squeeze(self):
        self.points.Squeeze()
        self.nodes.Squeeze()
        self.elements.Squeeze()
        self.rbes.Squeeze()

        self.node_global_ids.Squeeze()
        self.element_global_ids.Squeeze()
        self.rbe_global_ids.Squeeze()

        self.node_visible.Squeeze()
        self.element_visible.Squeeze()
        self.rbe_visible.Squeeze()

        self.node_original_ids.Squeeze()
        self.element_original_ids.Squeeze()
        self.rbe_original_ids.Squeeze()

    def shown_nodes(self):
        return self.node_filter.selected_data()

    def hidden_nodes(self):
        return self.node_filter.unselected_data()

    def shown_elements(self):
        return self.element_filter.selected_data()

    def hidden_elements(self):
        return self.element_filter.unselected_data()

    def shown_rbes(self):
        return self.rbe_filter.selected_data()

    def hidden_rbes(self):
        return self.rbe_filter.unselected_data()