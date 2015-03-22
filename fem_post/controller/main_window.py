__author__ = 'Michael Redmond'

import os
from PyQt4 import QtGui, QtCore

from .vtk_widget2 import VTKWidget
from fem_reader.nastran.bdf.reader import BDFReader

from dock_control import Dock_Picking
from dock_control import Dock_View
from dock_control import Dock_Message

class MainWindow(QtGui.QMainWindow):
 
    def __init__(self, app, ui):
        QtGui.QMainWindow.__init__(self)

        self.app = app
        """:type : QApplication"""
        self.ui = ui
        self.ui.setupUi(self)
        self.ui.menubar.setNativeMenuBar(False)


        self.picking = Dock_Picking()
        self.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.picking)
        self.view = Dock_View()
        self.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.view)
        self.message = Dock_Message()
        self.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.message)

        self.tabifyDockWidget(self.picking, self.view)
        self.view.raise_()


        # Initialize style if available
        self.usrstylefile = r'stylesheet.dat'
        self.usrstyle()

        # Setup Connections
        self.ui.action_Open.triggered.connect(self.on_open)

        self.view.ui.btn_bgcolor1.clicked.connect(self.on_color1)
        self.view.ui.btn_bgcolor2.clicked.connect(self.on_color2)
        self.view.ui.btn_perspectivetoggle.clicked.connect(self.on_toggle_perspective)

        self.picking.ui.btn_toggle_view.clicked.connect(self.toggle_visible)
        self.picking.ui.btn_toggle_hidden.clicked.connect(self.toggle_selected)

        self.picking.ui.btn_single_pick.clicked.connect(self.single_pick_button)
        self.picking.ui.btn_box_pick.clicked.connect(self.box_pick_button)
        self.picking.ui.btn_poly_pick.clicked.connect(self.poly_pick_button)

        self.picking.ui.btn_any.clicked.connect(self.any_button)
        self.picking.ui.btn_nodes.clicked.connect(self.nodes_button)
        self.picking.ui.btn_elements.clicked.connect(self.elements_button)
        self.picking.ui.btn_points.clicked.connect(self.points_button)
        self.picking.ui.btn_bars.clicked.connect(self.bars_button)
        self.picking.ui.btn_tris.clicked.connect(self.tris_button)
        self.picking.ui.btn_quads.clicked.connect(self.quads_button)

        self.picking.ui.btn_replace_selection.clicked.connect(self.replace_selection_button)
        self.picking.ui.btn_append_selection.clicked.connect(self.append_selection_button)
        self.picking.ui.btn_remove_selection.clicked.connect(self.remove_selection_button)

        self.picking.ui.cbx_left_click.setCurrentIndex(0)
        self.picking.ui.cbx_middle_click.setCurrentIndex(1)
        self.picking.ui.cbx_right_click.setCurrentIndex(2)
        self.picking.ui.cbx_ctrl_left_click.setCurrentIndex(3)

        self.bdf = None

        # http://www.paraview.org/Wiki/VTK/Examples/Python/Widgets/EmbedPyQt
        # http://www.vtk.org/pipermail/vtk-developers/2013-July/014005.html
        # see above why self.show() is not implemented here
        # it is implemented inside VTKWidget.view
        #self.show()

        self.vtk_widget = VTKWidget(self)

    def usrstyle(self):

        print(self.usrstylefile)
        if os.path.isfile(self.usrstylefile):
            print "usrstyle file found, reading"
            with open(self.usrstylefile, 'r') as fsty:
                style = fsty.read()
            fsty.close()

            self.setStyleSheet(style)


    def on_color1(self):
        color = self.vtk_widget.bg_color_1
        initial_color = QtGui.QColor(255*color[0], 255*color[1], 255*color[2])
        color = QtGui.QColorDialog().getColor(initial_color, self)

        if not color.isValid():
            return

        red = color.red() / 255.
        blue = color.blue() / 255.
        green = color.green() / 255.
        color1 = (red, green, blue)
        self.vtk_widget.set_background_color(color1=color1)

    def on_color2(self):
        color = self.vtk_widget.bg_color_2
        initial_color = QtGui.QColor(255*color[0], 255*color[1], 255*color[2])
        color = QtGui.QColorDialog().getColor(initial_color, self)

        if not color.isValid():
            return

        red = color.red() / 255.
        blue = color.blue() / 255.
        green = color.green() / 255.
        color2 = (red, green, blue)
        self.vtk_widget.set_background_color(color2=color2)

    def on_open(self):
        # noinspection PyCallByClass

        # For PySide, dir as None ok... For PyQt, dir must be QString()
        #filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', None, "BDF Files (*.bdf);;DAT Files (*.dat)")
        filename = QtGui.QFileDialog.getOpenFileName(self,'Open File','',"BDF Files (*.bdf);;DAT Files (*.dat)")

        if filename[0] == '':
            return

        self.bdf = BDFReader()

        # noinspection PyUnresolvedReferences
        self.app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

        # For PyQt - send reader "filename" .. for PySide - send reader "filename[0]"
        #self.bdf.read_bdf(filename[0])
        self.bdf.read_bdf(filename)

        self.vtk_widget.set_bdf_data(self.bdf)
        # noinspection PyUnresolvedReferences
        self.app.restoreOverrideCursor()

        self.bdf = None

    def on_toggle_perspective(self):
        self.vtk_widget.toggle_perspective()

    def toggle_selected(self):
        self.vtk_widget.toggle_selected()

    def toggle_visible(self):
        self.vtk_widget.toggle_visible()

    def single_pick_button(self):
        self.vtk_widget.single_pick_button()

    def box_pick_button(self):
        self.vtk_widget.box_pick_button()

    def poly_pick_button(self):
        self.vtk_widget.poly_pick_button()

    def any_button(self):
        self.vtk_widget.toggle_picking(0)

    def nodes_button(self):
        self.vtk_widget.toggle_picking(1)

    def elements_button(self):
        self.vtk_widget.toggle_picking(2)

    def points_button(self):
        self.vtk_widget.toggle_picking(2, 1)

    def bars_button(self):
        self.vtk_widget.toggle_picking(2, 2)

    def tris_button(self):
        self.vtk_widget.toggle_picking(2, 3)

    def quads_button(self):
        self.vtk_widget.toggle_picking(2, 4)

    def replace_selection_button(self):
        self.vtk_widget.replace_selection_button()

    def append_selection_button(self):
        self.vtk_widget.append_selection_button()

    def remove_selection_button(self):
        self.vtk_widget.remove_selection_button()

