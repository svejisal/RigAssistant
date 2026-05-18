try:
    from PySide6 import QtWidgets, QtCore, QtGui
    from PySide6.QtWidgets import QMainWindow, QWidget, QApplication, QDialog, QGridLayout, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QTabWidget, QLabel, QLineEdit, QGroupBox, QDoubleSpinBox, QSpinBox, QColorDialog, QButtonGroup, QRadioButton, QSlider, QTextEdit, QDialogButtonBox, QCheckBox, QComboBox
    from PySide6.QtGui import QColor, QPixmap, QFont, QDrag
    from PySide6.QtCore import Qt, QByteArray, QMimeData, QTimer
    from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
    import base64
    import os
    import pickle
    from shiboken6 import wrapInstance
    import maya.OpenMayaUI as omui
    import maya.cmds as cmds
    import maya.mel as mel
except ImportError:
    from PySide2 import QtWidgets, QtCore, QtGui
    from PySide2.QtWidgets import QMainWindow, QWidget, QApplication, QDialog, QGridLayout, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QTabWidget, QLabel, QLineEdit, QGroupBox, QDoubleSpinBox, QSpinBox, QColorDialog, QButtonGroup, QRadioButton, QSlider, QTextEdit, QDialogButtonBox, QCheckBox, QComboBox
    from PySide2.QtGui import QColor, QPixmap, QFont, QDrag
    from PySide2.QtCore import Qt, QByteArray, QMimeData, QTimer
    from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
    import base64
    import os
    import pickle
    from shiboken2 import wrapInstance
    import maya.OpenMayaUI as omui
    import maya.cmds as cmds
    import maya.mel as mel

def get_maya_window():
    get_window = omui.MQtUtil.mainWindow()
    return wrapInstance(int(get_window), QMainWindow)

class DraggableButton(QtWidgets.QPushButton):
    def __init__(self, text, parent=None):
        super(DraggableButton, self).__init__(text, parent)
        self.setAcceptDrops(True)
        self.code = ""  # Initialize the code attribute
        self.drag_start_position = None  # Store the position where the drag starts
        self.drag_timer = QTimer(self)  # Timer for drag delay
        self.drag_timer.timeout.connect(self.start_drag)  # Connect timer to drag start
        self.is_dragging = False  # Track whether a drag operation is in progress

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
            self.drag_timer.start(150)
        super().mousePressEvent(event)  # Simplified super() syntax

    def mouseReleaseEvent(self, event):
        self.drag_timer.stop()
        if not self.is_dragging:
            super().mouseReleaseEvent(event)  # Simplified super() syntax
        else:
            self.setDown(False)
            self.is_dragging = False
            
    def mouseMoveEvent(self, event):
        # Stop the timer if the mouse moves outside the button before the drag starts
        if self.drag_start_position is not None:
            if (event.pos() - self.drag_start_position).manhattanLength() > 10:  # Small movement threshold
                self.drag_timer.stop()
        super(DraggableButton, self).mouseMoveEvent(event)  # Call parent class's mouseMoveEvent

    def start_drag(self):
        # Stop the timer
        self.drag_timer.stop()
        # Set the dragging flag
        self.is_dragging = True
        # Start the drag operation
        drag = QDrag(self)
        mime = QMimeData()
        mime.setText(self.text())
        mime.setData('application/x-button-code', self.code.encode())
        drag.setMimeData(mime)
        # Execute the drag operation
        drag.exec_(Qt.MoveAction)
        # Reset the button's state after the drag operation
        self.setDown(False)
        self.is_dragging = False  # Reset the dragging flag

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        source_button = event.source()
        target_button = self
        
        # Get the layout and indexes
        layout = self.parent().layout()
        source_index = layout.indexOf(source_button)
        target_index = layout.indexOf(target_button)
        
        if source_index != -1 and target_index != -1:
            # Remove and reinsert widgets to reorder them
            layout.removeWidget(source_button)
            layout.removeWidget(target_button)
            
            # Swap positions
            if source_index > target_index:
                layout.insertWidget(target_index, source_button)
                layout.insertWidget(source_index, target_button)
            else:
                layout.insertWidget(source_index, target_button)
                layout.insertWidget(target_index, source_button)

class EDG707_002(MayaQWidgetDockableMixin, QMainWindow):
    def __init__(self):
        super(EDG707_002, self).__init__(get_maya_window())
        
        self.setAcceptDrops(True)

        self.dist_spinBox_UI = CreatePoleV()
        
        #Setup the UI
        self.adjustSize()
        self.setWindowTitle("Rig Assistant")
        self.setWindowFlag(Qt.WindowType.Tool)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame_layout = QVBoxLayout(frame)
        main_layout.addWidget(frame)
        
        logo_paste = QLabel()
        logo_paste.setPixmap(self.logo_import())
        logo_paste.setAlignment(Qt.AlignmentFlag.AlignCenter)
        frame_layout.addWidget(logo_paste)

        #Tab Setup
        tab_widget = QTabWidget()
        frame_layout.addWidget(tab_widget)

        #Tab 1
        tab_1 = QWidget()
        tab1_layout = QVBoxLayout(tab_1)
        #EMOJIS
        emoji_leg = base64.b64decode("8J+mvw==").decode("utf-8")  # ??
        emoji_bone = base64.b64decode("8J+mtA==").decode("utf-8")  # ??
        emoji_ribbon = base64.b64decode("8J+Ol++4jw==").decode("utf-8")  # ???
        emoji_globe_wireframe = base64.b64decode("8J+MkA==").decode("utf-8") # ??
        emoji_controller = base64.b64decode("8J+Org==").decode("utf-8") # ??
        emoji_folder_closed = base64.b64decode("8J+TgQ==").decode("utf-8") # ??
        emoji_color_palette = base64.b64decode("8J+OqA==").decode("utf-8") # ??
        
        #AUTORIG
        AutoRig_GRP = QGroupBox("AUTORIG")
        AutoRig_GRP.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        AutoRig_GRP_layout = QVBoxLayout(AutoRig_GRP)
        AutoRig_btn = QPushButton("AUTORIG MANIPULATOR")
        AutoRig_GRP_layout.addWidget(AutoRig_btn)
        AutoRig_btn.clicked.connect(self.AutoRig_call)
        tab1_layout.addWidget(AutoRig_GRP)
        
        #
        jnt_manip_grp = QGroupBox("Joint's Manipulators")
        jnt_manip_grp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        jnt_manip_grp_layout = QGridLayout(jnt_manip_grp)
        
        ikCreate_button = QPushButton(f"Create IK {emoji_leg}")
        poleV_button = QPushButton(f"Create Pole Vector {emoji_bone}")
        ribbon_tool = QPushButton(f"Create Ribbon {emoji_ribbon}")
        axis_vis = QPushButton(f"Local Axis Visibility {emoji_globe_wireframe}")
        axis_vis.mouseDoubleClickEvent = self.on_axis_vis_double_click

        jnt_manip_grp_layout.addWidget(ikCreate_button, 0, 0)
        jnt_manip_grp_layout.addWidget(poleV_button, 0, 1)
        jnt_manip_grp_layout.addWidget(ribbon_tool, 1, 0)
        jnt_manip_grp_layout.addWidget(axis_vis, 1, 1)
        
        #
        ctrl_grp = QGroupBox("Controls Editor")
        ctrl_grp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ctrl_grp_layout = QGridLayout(ctrl_grp)
        
        controller_button = QPushButton(f"Create Controller {emoji_controller}")
        grouping_button = QPushButton(f"Create Groups {emoji_folder_closed}")

        ctrl_grp_layout.addWidget(controller_button, 0, 0)
        ctrl_grp_layout.addWidget(grouping_button, 0, 1)
        
        #
        color_grp = QGroupBox("Color Override")
        color_grp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        color_grp_layout = QVBoxLayout(color_grp)
        
        override_color = QPushButton(f"Change Controller/Joints Color {emoji_color_palette}")
        color_grp_layout.addWidget(override_color)
        
        #
        tab1_layout.addWidget(jnt_manip_grp)
        tab1_layout.addWidget(ctrl_grp)
        tab1_layout.addWidget(color_grp)
        

        #Tab 2
        tab_2 = QWidget()
        tab_2_layout = QVBoxLayout(tab_2)

        sel_grp = QGroupBox("Selection Tools")
        sel_grp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sel_grp_layout = QVBoxLayout(sel_grp)

        tab_2_layout.addWidget(sel_grp)

        sel_grp.setMaximumSize(400, 120)

        #
        sel_name_btn = QPushButton("Select by Name")
        ren_all_btn = QPushButton("Rename Selected")
        ren_manip_btn = QPushButton("Rename Manip")
        
        #Tab 3
        tab_3 = QWidget()
        tab_3_layout = QVBoxLayout(tab_3)
        
        add_button = QPushButton("Add New Button")
        add_button.clicked.connect(self.open_codeEditor)
        tab_3_layout.addWidget(add_button)
        
        ##Scroll Area for Dynamic Buttons
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_content = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_area.setWidgetResizable(True)
        tab_3_layout.addWidget(self.scroll_area)
        
        bottom_layout = QHBoxLayout()
        tab_3_layout.addLayout(bottom_layout)
        
        # Add the Save and Load buttons after the box
        save_button = QtWidgets.QPushButton("Save Preset")
        save_button.clicked.connect(self.save_preset)
        bottom_layout.addWidget(save_button)
        
        load_button = QtWidgets.QPushButton("Load Preset")
        load_button.clicked.connect(self.load_preset)
        bottom_layout.addWidget(load_button)
        
        #Tab 4
        tab_4 = QWidget()
        tab_4_layout = QVBoxLayout(tab_4)
        
        about_grp = QGroupBox("About")
        about_grp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        about_grp_layout = QVBoxLayout(about_grp)
        
        tab_4_layout.addWidget(about_grp)
        
        tab_4.setMaximumSize(400, 200)
        
        info1_label = QLabel("Created by <b>Edvard</b><br>Email: edvard9909@gmail.com<br>LinkTree: https://linktr.ee/edgul<br><br>Special thanks to <b>RETSYN</b> and <b>MUNORR</b>!")
        info1_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        about_grp_layout.addWidget(info1_label)

        #Tab1 Click
        sel_grp_layout.addWidget(sel_name_btn)
        sel_grp_layout.addWidget(ren_all_btn)
        sel_grp_layout.addWidget(ren_manip_btn)
        
        ikCreate_button.clicked.connect(self.create_IK)
        poleV_button.clicked.connect(self.create_PoleVector_Dialog)
        ribbon_tool.clicked.connect(self.show_ribbon_tool)
        axis_vis.clicked.connect(self.toggle_Axis_Display_Joints)

        controller_button.clicked.connect(self.create_Controller)
        grouping_button.clicked.connect(self.create_Group)

        override_color.clicked.connect(self.controller_color)

        #Tab2 Click
        sel_name_btn.clicked.connect(self.sel_Tool)
        ren_all_btn.clicked.connect(self.renameAll_Tool)
        ren_manip_btn.clicked.connect(self.show_Rename_Manip)

        tab_widget.addTab(tab_1, "AutoRig")
        tab_widget.addTab(tab_2, "Outliner")
        tab_widget.addTab(tab_3, "Custom")
        tab_widget.addTab(tab_4, "Info")
        
    def create_PoleVector_Dialog(self):
    # Show the pole vector creation dialog
        self.dist_spinBox_UI.show()
    
    def open_codeEditor(self, button=None):
        # If editing, pass the button's current name and code
        if button:
            dialog = CodeEditor_Dialog(self, button.text(), button.code)
        else:
            dialog = CodeEditor_Dialog(self)
        
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            button_name = dialog.get_button_name()
            code = dialog.get_code()
            
            if button:
                # Update the existing button
                button.setText(button_name)
                button.code = code
            else:
                # Create a new button
                self.create_new_button(button_name, code)
        
    def create_new_button(self, button_name, code):
        if not button_name:
            button_name = "Custom Button"
            
        # Create draggable button
        new_button = DraggableButton(button_name)
        new_button.code = code
        
        def execute_code():
            try:
                exec(new_button.code, globals())
            except Exception as e:
                cmds.warning(f"Error executing code: {str(e)}")
            finally:
                self.bring_to_front()

        new_button.clicked.connect(execute_code)
        new_button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        new_button.customContextMenuRequested.connect(lambda pos: self.show_context_menu(new_button, pos))
    
        self.scroll_layout.addWidget(new_button)
        
    def show_context_menu(self, button, pos):
        # Create a context menu
        context_menu = QtWidgets.QMenu(self)
        
        # Add an "Edit" action to the menu
        edit_action = context_menu.addAction("Edit")
        edit_action.triggered.connect(lambda: self.open_codeEditor(button))
        
        # Add a "Delete" action to the menu
        delete_action = context_menu.addAction("Delete")
        delete_action.triggered.connect(lambda: self.delete_button(button))
        
        # Show the context menu at the cursor's position
        context_menu.exec_(button.mapToGlobal(pos))
    
    def delete_button(self, button):
        # Remove the button from the layout and delete it
        self.scroll_layout.removeWidget(button)
        button.deleteLater()
    
    def bring_to_front(self):
        # Bring the window to the front
        self.raise_()
        self.activateWindow()
    
    # Drag and drop functionality
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.endswith((".txt", ".py")):
                self.process_file(file_path)
    
    def process_file(self, file_path):
        # Extract the file name without extension
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        
        # Read the file content with proper encoding and preserve newlines and spaces
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                file_content = file.read()
                print("File content read successfully:")  # Debugging
                print(file_content)  # Debugging: Print the file content to verify
        except Exception as e:
            cmds.warning(f"Error reading file: {str(e)}")
            return
        
        # Create a new button with the file name and content
        self.create_new_button(file_name, file_content)
    
    def save_preset(self):
        # Collect button data (name and code)
        button_data = []
        for i in range(self.scroll_layout.count()):
            button = self.scroll_layout.itemAt(i).widget()
            if isinstance(button, QtWidgets.QPushButton):
                button_data.append((button.text(), button.code))
        
        # Open a file dialog to save the preset
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save Preset", "", "Preset Files (*.preset)"
        )
        
        if file_path:
            # Save the button data to the file
            with open(file_path, "wb") as file:
                pickle.dump(button_data, file)
            cmds.warning(f"Preset saved to: {file_path}")
    
    def load_preset(self):
        # Open a file dialog to load the preset
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Load Preset", "", "Preset Files (*.preset)"
        )
        
        if file_path:
            # Load the button data from the file
            with open(file_path, "rb") as file:
                button_data = pickle.load(file)
            
            # Clear existing buttons
            for i in reversed(range(self.scroll_layout.count())):
                widget = self.scroll_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()
            
            # Create new buttons from the loaded data
            for name, code in button_data:
                self.create_new_button(name, code)
            cmds.warning(f"Preset loaded from: {file_path}")

    def logo_import(self):
        image_data = b"iVBORw0KGgoAAAANSUhEUgAAADUAAAAjCAYAAAA0aUL2AAAACXBIWXMAAAsSAAALEgHS3X78AAACw0lEQVRYhe2Yv24TQRDGf0FICE2By1DleIL4DXx5AsITkEcIBRVFQoMo/QaENzBPwKahvhRUUFy6SDSOxEh0obi5eG/Zu9uzZQVb/qTTrefGs/PNn72x9+7u7tg2PHpoB9aBHalNwY7UpmArST1+aAdCqOo+MAb27XpujyZAAbwVkV9dNtZOSlVHVE5i95Gtc8ABMxEpTPcE+NRh7tC+c9G1594yL19VDZ0DyOyCyvljW39NMPlCREpVnQPPenQ/iMi7LoVBmVLVGfAyUb0AThJ1M1XNaBJ6T5WVAijpJ3uPoQdFnqh3LSJzFmUHcAu8Ao6Az4F+EbE9FRFndmpCV8D3vs2TMxWJZBec3X1ShYjMzNapJ78WkbmVdCjL7fMbFuX+rW/zIeWXR2SXwLmtSxEp6wd2QBx6us5bjyPyRgCMUKwfp32ODiE1jsimIuIi8ph+fcKNgANfHpMRD2Jd1p1YlZTr0M9bdGPyNl2As8T97jGE1CQiO/XqPqOK9pFl758esXUjOCJSqOpxIHMAqlrSJFWkOJpEKmhiH2cRWWn3Ro9469xbX0ZkqOoFzfdeDdfiRwOpmWojFeLWXqJhj4xU9dzs+Bl3LXZeR2RX9eTRh1RSeYLOLYvxJdSfEC9fZ/ei5Xltd0bCqVdjlUwd1Q5FTqS+zF4B53XviMipqk6pglGaztybCTOqqWOckq2k2U9VQ6VrEck69KdATXTOoqcaAfAOmbahd0LVdw5wHa+PBnoz5W3so9W49dMscDC3q476QeSrUJVawUASIVLKL1ZKmdf4flS/UNV+ymQOFQnHgkTSQdCHZUm1NX7bJFBjLSRCpJDKB9hzQGNYZfHzYW0kQnQeFKr6BPiTaOtSRHKbwOdUJMrVXRyOPlJPgY/28Qfw266fJrsRkZu1ergElvo5/79jK/8i25HaFOxIbQq2ktRfaLEGxyXdCS4AAAAASUVORK5CYII="
        pixmap = QPixmap()
        pixmap.loadFromData(base64.b64decode(image_data))
        return pixmap
        
    def show_ribbon_tool(self):
        
        self.rib_wid = Ribbon_Tool(self)
        self.rib_wid.setWindowFlags(Qt.WindowType.Window)
        self.rib_wid.show()

    def AutoRig_call(self):
        self.rig_widg = AutoRig(self)
        self.rig_widg.setWindowFlags(Qt.WindowType.Window)
        self.rig_widg.show()

    def show_Rename_Manip(self):

        self.ren_wid = Rename_Manip(self)
        self.ren_wid.setWindowFlags(Qt.WindowType.Window)
        self.ren_wid.show()

    def controller_color(self):
        # Open color dialog and get the selected color
        palette = QColorDialog.getColor()
        
        # Check if a valid color was selected
        if not palette.isValid():
            cmds.warning("No color selected.")
            return
        
        cmds.undoInfo(openChunk=True)
        # Normalize the color values to the range [0, 1]
        color = [palette.red() / 255, palette.green() / 255, palette.blue() / 255]
        
        # Get the selected objects
        sel = cmds.ls(selection=True)
        
        if len(sel)==0:
            cmds.warning("No objects selected.")
            return
        
        # Iterate over the selected objects
        for i in sel:
            # Check if the object is a joint
            if cmds.objectType(i, isType="joint"):
                print(f"Processing joint: {i}")
                
                # Enable override and set RGB color for the joint
                cmds.setAttr(f"{i}.overrideEnabled", 1)
                cmds.setAttr(f"{i}.overrideRGBColors", 1)
                cmds.setAttr(f"{i}.overrideColorRGB", color[0], color[1], color[2])
                    
            else:
                print(f"Processing joint: {i}")
            
                cmds.setAttr(f"{i}.overrideEnabled", 1)
                cmds.setAttr(f"{i}.overrideRGBColors", 1)
                cmds.setAttr(f"{i}.overrideColorRGB", color[0], color[1], color[2])
                
            # Process shapes of the object (for shape objects)
            shapes = cmds.listRelatives(i, shapes=True, fullPath=True) or []
            for shape in shapes:
                print(f"Processing shape: {shape}")
                cmds.setAttr(f"{shape}.overrideEnabled", 1)
                cmds.setAttr(f"{shape}.overrideRGBColors", 1)
                cmds.setAttr(f"{shape}.overrideColorRGB", color[0], color[1], color[2])
        
        cmds.undoInfo(closeChunk=True)
        
    def toggle_Axis_Display_Joints(self):
        cmds.undoInfo(openChunk=True)
        jointList = cmds.ls(sl=1, type="joint")
		
        if len(jointList) == 0:
            jointList = cmds.ls(type="joint")
        for jnt in jointList:
            currentStateJnts = cmds.getAttr(jnt + ".displayLocalAxis")
            cmds.setAttr(jnt + ".displayLocalAxis", not currentStateJnts)
            
        cmds.undoInfo(closeChunk=True)
        
    def on_axis_vis_double_click(self, event):
        cmds.undoInfo(openChunk=True)
        
        jointList = cmds.ls(type="joint")
        if jointList:
            currentStateJnts = cmds.getAttr(jointList[0] + ".displayLocalAxis")
            
            for jnt in jointList:
                cmds.setAttr(jnt + ".displayLocalAxis", not currentStateJnts)
            event.accept()
            
        cmds.undoInfo(closeChunk=True)
        
    def create_IK(self):
        fSel = cmds.ls(sl=1, type="joint")
        
        cmds.select(hi=1)

        sel = cmds.ls(sl=1, type="joint")

        cmds.joint(e=1, zso=1)

        IK = cmds.ikHandle (n="IKHandle_001", sj=sel[0], ee=sel[-1], sol="ikRPsolver", srp=1)
        
        cmds.select(fSel)
        
    def create_Controller(self):
        
        cmds.undoInfo(openChunk=True)
        
        fSel = cmds.ls(sl=1, type="joint")


        sel = cmds.ls(sl=1)
        selMult = cmds.ls(sl=1)
        ikSel = cmds.ls(sl=1, type="ikHandle")

        if len(ikSel) > 0:
            for i in sel:
                crcl = cmds.circle(n=i+"_CTRL", nr=(0,1,0), c=(0,0,0))
                grp1 = cmds.group(crcl, n=i+"_xform")
                grp2 = cmds.group(grp1, n=i+"_adj")
                grp3 = cmds.group(grp2, n=i+"_topGr")
                cnstrGr = cmds.parentConstraint(i, grp3, mo=0)
                cmds.delete(cnstrGr)
            
                #cnstrCtrl = cmds.parentConstraint(crcl, i, mo=0)

                if not sel:
                    cmds.circle(n="Circle_001", nr=(0,1,0), c=(0,0,0))
                    return
                return    

        for i in selMult:
            crcl = cmds.circle(n=i+"_CTRL", nr=(0,1,0), c=(0,0,0))
            grp1 = cmds.group(crcl, n=i+"_xform")
            grp2 = cmds.group(grp1, n=i+"_adj")
            grp3 = cmds.group(grp2, n=i+"_topGr")
            cnstrGr = cmds.parentConstraint(i, grp3, mo=0)
            cmds.delete(cnstrGr)
            
            #cnstrCtrl = cmds.parentConstraint(crcl, i, mo=0)
            
        if not selMult:
            cmds.circle(n="Circle_001", nr=(0,1,0), c=(0,0,0))

        cmds.undoInfo(closeChunk=True)
        
    def create_Group(self):
        
        cmds.undoInfo(openChunk=True)
        
        sel = cmds.ls(sl=1)

        for i in sel:
            grp1 = cmds.group(em=1, n=i+"_xform")
            grp2 = cmds.group(grp1, n=i+"_adj")
            grp3 = cmds.group(grp2, n=i+"_topGr")
            cnstr = cmds.parentConstraint(i, grp3, mo=0)
            cmds.delete(cnstr)
            cmds.parent(i, grp1)

        if not sel:
            grp1 = cmds.group(em=1, n="null_xform")
            grp2 = cmds.group(grp1, n="null_adj")
            grp3 = cmds.group(grp2, n="null_topGr")

        cmds.undoInfo(closeChunk=True)
        
    def sel_Tool(self):
        cmds.select(d=1)
        
        selected = cmds.ls(sl=1)
        
        get_word = cmds.promptDialog(
            title = "Selection Tool",
            message = "Select:",
            button = ["OK","Cancel"],
            defaultButton = "OK",
            cancelButton = "Cancel",
            dismissString = "Cancel",
        )

        if get_word == "OK":
            what_word = cmds.promptDialog(q=1, text=1)
        
        selectWord = cmds.ls(f"*{what_word}*")

        if selected == 0:
            cmds.select(selectWord)
        
        else:
            result = selectWord + selected
            cmds.select(result)

    def renameAll_Tool(self):
        
        cmds.undoInfo(openChunk=True)
        
        selected = cmds.ls(orderedSelection=True)
        
        if not selected:
            cmds.warning("No objects selected!")
            return
        
        get_word = cmds.promptDialog(
            title="Rename Tool",
            message="Rename to:",
            button=["OK", "Cancel"],
            defaultButton="OK",
            cancelButton="Cancel",
            dismissString="Cancel",
        )

        if get_word != "OK":
            return
        
        what_word = cmds.promptDialog(q=1, text=1)
        
        if not what_word:
            cmds.warning("No name entered!")
            return
        
        index = 1
        order_sel = []
        if len(selected) == 1:
            # Rename the single selected object
            new_obj = cmds.rename(selected[0], what_word)
            cmds.select(new_obj)
            
        else:
            # Rename multiple objects with 3-digit numbering
            for obj in selected:
                new_name = f"{what_word}_{index:03d}"  # Use :03d for 3-digit numbering
                rename = cmds.rename(obj, new_name)
                index += 1
                order_sel.append(rename)
                
            cmds.select(order_sel)
#class Create_Controller(QWidget):
 #   def __init__(self, parent=None):
  #      super(Create_Controller, self).__init__(parent)
   #     self.setWindow

        cmds.undoInfo(closeChunk=True)
        
class  CodeEditor_Dialog(QDialog):
    def __init__(self, parent=None, button_name="", code=""):
        super(CodeEditor_Dialog, self).__init__(parent)
        self.setWindowTitle("Code Editor")
        self.setMinimumSize(400, 300)
        
        #Layout
        self.layout = QVBoxLayout(self)
        
        #Button Naming
        self.name_label = QLabel("Button Name:")
        self.layout.addWidget(self.name_label)
        
        self.name_input = QLineEdit(button_name)
        self.layout.addWidget(self.name_input)
        
        #Text Editor
        self.text_edit = CustomTextEdit()
        self.text_edit.setAcceptRichText(True)
        self.text_edit.setPlainText(code)
        self.layout.addWidget(self.text_edit)
        
        #OK and Cancel Buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)
        
    def get_code(self):
        return self.text_edit.toPlainText()
    
    def get_button_name(self):
        return self.name_input.text()

class CustomTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super(CustomTextEdit, self).__init__(parent)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab:
            
            cursor = self.textCursor()
            cursor.insertText("    ")
            
        else:
            super(CustomTextEdit, self).keyPressEvent(event)

class CreatePoleV(QDialog):
    def __init__(self, parent=None):
        super(CreatePoleV, self).__init__(parent)
        self.poleV_layout = QVBoxLayout(self)
        
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        
        self.dist_text = QLabel("Distance:")
        self.poleV_layout.addWidget(self.dist_text)
        
        self.dist_spinBox = QDoubleSpinBox()
        self.dist_spinBox.setMinimum(0)
        self.dist_spinBox.setMaximum(1000)
        self.dist_spinBox.setValue(4)
        self.poleV_layout.addWidget(self.dist_spinBox)
        
        self.dialog_btn_box_poleV = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.dialog_btn_box_poleV.accepted.connect(self.create_PoleVector)
        self.dialog_btn_box_poleV.rejected.connect(self.reject)
        self.poleV_layout.addWidget(self.dialog_btn_box_poleV)
        
    def find_perf_vect(self):
        sel = cmds.ls(sl=1, type="joint")

        #Joints' vector
        f_Vec = cmds.xform(sel[0], q=1, ws=1,t=1)
        s_Vec = cmds.xform(sel[1], q=1, ws=1, t=1)
        t_Vec = cmds.xform(sel[2], q=1, ws=1,t=1)

        #Vector between two joints
        f_s_Vec = [s_Vec[i] - f_Vec[i] for i in range(3)]
        f_t_Vec = [t_Vec[i] - f_Vec[i] for i in range(3)]

        #The calculation of projection of vector a on vector b
        dot_Product = sum(f_s_Vec[i] * f_t_Vec[i] for i in range(3))
        magnitude = sum(f_t_Vec[i] **2 for i in range(3))
        projection = [dot_Product / magnitude * f_t_Vec[i] for i in range(3)]

        perpendicular = [f_s_Vec[i] - projection[i] for i in range(3)]
        
        length = sum(perpendicular[i] **2 for i in range(3)) ** 0.5
        normalized_perpendicular = [perpendicular[i] / length for i in range(3)]
        
        dist_multiplier = self.dist_spinBox.value() #You can change this value, if you think that distance from pole vector and leg doesn't fit you
        
        pole_Vec_Pos = [s_Vec[i] + normalized_perpendicular[i] * dist_multiplier for i in range(3)]
        return pole_Vec_Pos

    def create_PoleVector(self):
        cmds.undoInfo(openChunk=True)
        
        selList = cmds.ls(sl=1)
        ikSel = cmds.ls(sl=1, type="ikHandle")

        if len(selList) < 3  or len(ikSel) != 1:
            cmds.warning("Please select 3 joints and 1 ikHandle!")
            return

        pole_Vec_Pos = self.find_perf_vect()

        crcl = cmds.circle(n=f"PoleV_CTRL", nr=(0,1,0), c=(0,0,0))
        grp1 = cmds.group(crcl, n="PoleV_xform")
        grp2 = cmds.group(grp1, n=f"PoleV_adj")
        grp3 = cmds.group(grp2, n=f"PoleV_topGr")

        cmds.xform(grp3, t=pole_Vec_Pos, ws=1)

        cmds.poleVectorConstraint(crcl[0], ikSel[0], n="poleV_constraint", w=1)
        cmds.select(crcl)

        cmds.undoInfo(closeChunk=True)

class Ribbon_Tool(QWidget):
    def __init__(self, parent=None):
        super(Ribbon_Tool, self).__init__(parent)
        self.setWindowTitle("Ribbon Tools")
        self.setGeometry(400, 100, 276, 100)

        self.setWindowFlag(Qt.Tool)

        pop_widget_layout = QVBoxLayout()

        radio_grp = QButtonGroup()

        numbers_layout = QHBoxLayout()
        number_labels = []

        for i in range(1, 11):
            label = QLabel(str(i))
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            numbers_layout.addWidget(label)
            number_labels.append(label)

        pop_frame = QFrame()
        pop_frame.setFrameShape(QFrame.Shape.StyledPanel)
        pop_frame_layout = QVBoxLayout(pop_frame)
        pop_widget_layout.addWidget(pop_frame)

        pop_inner_group = QGroupBox()
        pop_inner_group_layout = QGridLayout(pop_inner_group)
        pop_frame_layout.addWidget(pop_inner_group)

        axis_label = QLabel("Nurbs Along:")

        self.axis_x = QRadioButton("X Axis")
        self.axis_y = QRadioButton("Y Axis")
        self.axis_z = QRadioButton("Z Axis")

        self.axis_x.setChecked(True)

        number_spans_label = QLabel("Number of Spans:")
        self.s_slider = QSlider(Qt.Orientation.Horizontal)
        self.s_slider.setMinimum(1)
        self.s_slider.setMaximum(10)
        self.s_slider.setValue(4)
        
        dist_label = QLabel("Ribbon Width:")
        self.dist_box = QDoubleSpinBox()
        self.dist_box.setMinimum(0)
        self.dist_box.setMaximum(1000)
        self.dist_box.setValue(1)

        btn1 = QPushButton("Create Ribbon")
        #btn2 = QPushButton("Make nHair")

        pop_inner_group_layout.addWidget(axis_label, 0, 0)
        radio_grp.addButton(self.axis_x)
        radio_grp.addButton(self.axis_y)
        radio_grp.addButton(self.axis_z)

        pop_inner_group_layout.addWidget(self.axis_x, 1, 0)
        pop_inner_group_layout.addWidget(self.axis_y, 1, 1)
        pop_inner_group_layout.addWidget(self.axis_z, 1, 2)

        pop_inner_group_layout.addWidget(number_spans_label, 2, 0, 1, 3)
        pop_inner_group_layout.addLayout(numbers_layout, 3, 0, 1, 3)
        pop_inner_group_layout.addWidget(self.s_slider, 4, 0, 1, 3)
        
        pop_inner_group_layout.addWidget(dist_label, 5, 0, 1, 3)
        pop_inner_group_layout.addWidget(self.dist_box, 5, 1)

        pop_inner_group_layout.addWidget(btn1, 6, 0, 1, 3)
        #pop_inner_group_layout.addWidget(btn2, 6, 0, 1, 3)

        self.setLayout(pop_widget_layout)

        btn1.clicked.connect(self.create_ribbon)

    def create_ribbon(self):
        #Store a story
        cmds.undoInfo(openChunk = True)
        
        sel = cmds.ls(sl=1, type="joint")
        
        #Check if selected 2 joints
        if len(sel) >= 2:
            # Store existing follicles and curves before creation
            existing_follicles = set(cmds.ls(type="follicle", long=True))
            existing_joints = set(cmds.ls(type="joint", long=True))
            existing_curves = set(cmds.ls(type="nurbsCurve", long=True))
            
            curves_array = []
            dist = self.dist_box.value()
            for i in sel:
                pos = cmds.xform(i, q=1, t=1, ws=1)
                mat = cmds.xform(i, q=1, m=1, ws=1)
                x_axis = [mat[0], mat[1], mat[2]]
                y_axis = [mat[4], mat[5], mat[6]]
                z_axis = [mat[8], mat[9], mat[10]]
                if self.axis_x.isChecked():
                    chosen_axis = x_axis
                elif self.axis_y.isChecked():
                    chosen_axis = y_axis
                else:
                    chosen_axis = z_axis
                fst_pnt = [pos[0] + chosen_axis[0]*dist, pos[1] + chosen_axis[1]*dist, pos[2] + chosen_axis[2]*dist]
                snd_pnt = [pos[0] - chosen_axis[0]*dist, pos[1] - chosen_axis[1]*dist, pos[2] - chosen_axis[2]*dist]
                cur = cmds.curve(n=f"curve_{i}", p=[fst_pnt, snd_pnt], d=1)
                curves_array.append(cur)
            
            spans = self.s_slider.value()
            jnts_cnt_nHair = len(sel)-1
            edges = spans * jnts_cnt_nHair + 1
            
            # Create lofted surface
            loft = cmds.loft(curves_array, u=1, ar=1, d=3, ss=spans, rn=1, po=0)
            
            # Create hair system
            nHair = mel.eval(f"createHair {edges} 1 3 1 0 1 1 1 0 1 1 1")
            
            # Get newly created follicles
            new_follicles = set(cmds.ls(type="follicle", long=True)) - existing_follicles
            
            # Clean up ALL curves - both our temporary ones and any created by the hair system
            all_new_curves = set(cmds.ls(type="nurbsCurve", long=True)) - existing_curves
            for curve in all_new_curves:
                curve_parent = cmds.listRelatives(curve, parent=True, fullPath=True)
                if curve_parent:
                    cmds.delete(curve_parent)
            
            # Clean up hair system and nucleus
            hair = cmds.listRelatives(["*hairSystemShape*", "*pfxHairShape*"], parent=1)
            nucl = cmds.ls(type="nucleus")
            if hair:
                cmds.delete(hair, nucl)
                
            # Clean up any existing joints under follicles
            for follicle in new_follicles:
                follicle_parent = cmds.listRelatives(follicle, parent=True, fullPath=True)[0]
                existing_children = cmds.listRelatives(follicle_parent, children=True, type="joint", fullPath=True)
                if existing_children:
                    cmds.delete(existing_children)
            
            # Create new joints
            for i, follicle in enumerate(new_follicles, 1):
                follicle_parent = cmds.listRelatives(follicle, parent=True, fullPath=True)[0]
                cmds.select(clear=True)
                jnt = cmds.joint(n=f"{follicle_parent}_{i:03d}", p=[0,0,0])
                constraint = cmds.parentConstraint(follicle_parent, jnt)
                cmds.delete(constraint)
                cmds.parent(jnt, follicle_parent)
            
            cmds.select(clear=True)
        
        else:
            cmds.warning("You need to select at least 2 joints!")
        
        cmds.undoInfo(closeChunk = True)
        

class Rename_Manip(QWidget):
    def __init__(self, parent=None):
        super(Rename_Manip, self).__init__(parent)

        self.setWindowTitle("Renaming Control")
        self.setGeometry(500, 200, 276, 100)

        self.setWindowFlag(Qt.WindowType.Tool)

        self.sel_widget_layout = QVBoxLayout()

        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_layout = QVBoxLayout(self.frame)

        self.txt_bef = QLabel("Search for:")
        self.txt_1 = QLineEdit()
        self.txt_aft = QLabel("Replace with:")
        self.txt_2 = QLineEdit()
        self.ok_btn = QPushButton("Ok")

        self.frame_layout.addWidget(self.txt_bef)
        self.frame_layout.addWidget(self.txt_1)
        self.frame_layout.addWidget(self.txt_aft)
        self.frame_layout.addWidget(self.txt_2)
        self.frame_layout.addWidget(self.ok_btn)
        self.sel_widget_layout.addWidget(self.frame)                

        self.setLayout(self.sel_widget_layout)
        
        self.txt_1.returnPressed.connect(self.ok_btn.click)
        self.txt_2.returnPressed.connect(self.ok_btn.click)

        self.ok_btn.clicked.connect(self.rename_selected)

    def rename_selected(self):
        cmds.undoInfo(openChunk=True)
        
        search_text = self.txt_1.text()
        replace_text = self.txt_2.text()
        
        sel = cmds.ls(sl=True, l=True)
        
        #Sort by hirarchy, more | the object has, the deeper selection is
        reverse_sel = sorted(sel, key = lambda x: x.count("|"), reverse=True)
        
        #For counting the number of objects
        renamed_obj = []
        
        for i in reverse_sel:
            #Get last name of the short name
            short_name = i.split("|")[-1]
            
            if search_text in short_name:
                #Create new name
                new_name = short_name.replace(search_text, replace_text)
                
                if cmds.objExists(i):
                    #Paste the naming onto object
                    new_name_paste = cmds.rename(i, new_name)
                    renamed_obj.append(new_name_paste)
                    print(f"SUCCESS: Renamed {short_name} ? {new_name}")
        
        cmds.select(renamed_obj)
        
        cmds.warning(f"SUMMARY: Renamed {len(renamed_obj)} of {len(sel)} objects!")
        self.close()
        cmds.undoInfo(closeChunk=True)
    
class AutoRig(MayaQWidgetDockableMixin, QWidget):
    def __init__(self, parent=None):
        super(AutoRig, self).__init__(parent)
        ###SETUP###
        self.setWindowTitle("AutoRig")
        self.adjustSize()
        #self.setFixedSize(self.sizeHint())
        
        self.setWindowFlag(Qt.Tool)
        self.IK_tool_layout = QVBoxLayout()
        
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame_layout = QVBoxLayout(frame)
        self.IK_tool_layout.addWidget(frame)
        
        group_001 = QGroupBox("AUTORIG")
        group_001.setStyleSheet("QGroupBox {font-weight: bold;}")
        
        frame_layout.addWidget(group_001)
        group_001_layout = QVBoxLayout(group_001)
        group_001_layout.setSpacing(10)
        
        text_000 = QLabel("<i>PLEASE RENAME CONTROLLERS AND <br>ITS GROUPS BEFORE APPLYING AGIAN</i>")
        text_000.setAlignment(Qt.AlignCenter)
        group_001_layout.addWidget(text_000)
        
        #FK CHECK
        FK_btn = QCheckBox("FK Create")
        FK_btn.setChecked(True)
        
        group_001_layout.addWidget(FK_btn)
        
        #IK CHECK
        RadioButton_layout = QHBoxLayout()
        group_001_layout.addLayout(RadioButton_layout)
        self.IK_spline_rad = QRadioButton("IK Spline")
        self.IK_reg_rad = QRadioButton("IK Regular")
        self.IK_spline_rad.setChecked(True)
        
        RadioButton_layout.addWidget(self.IK_spline_rad)
        RadioButton_layout.addWidget(self.IK_reg_rad)
        
        #DISTANCE OF CONTROLLER
        text_001 = QLabel("Set <b>MAIN CONTROLLER</b> distance:")
        group_001_layout.addWidget(text_001)
        
        #combo
        distContr_layout = QHBoxLayout()
        group_001_layout.addLayout(distContr_layout)
        
        xyz_combo = QComboBox()
        xyz_combo.addItem("X")
        xyz_combo.addItem("Y")
        xyz_combo.addItem("Z")
        xyz_combo.setCurrentIndex(0)
        
        #distance
        dist = QDoubleSpinBox()
        dist.setValue(5)
        
        distContr_layout.addWidget(xyz_combo)
        distContr_layout.addWidget(dist)
        
        #stretch
        text_002 = QLabel("<b>STRETCH</b> joints along:")
        group_001_layout.addWidget(text_002)
        
        stretch_combo = QComboBox()
        stretch_combo.addItem("X")
        stretch_combo.addItem("Y")
        stretch_combo.addItem("Z")
        stretch_combo.setCurrentIndex(0)
        
        group_001_layout.addWidget(stretch_combo)
        
        #SPANS
        self.text_003 = QLabel("Number of <b>SPANS</b>:")
        group_001_layout.addWidget(self.text_003)
        
        self.spans = QSpinBox()
        self.spans.setValue(1)
        group_001_layout.addWidget(self.spans)
        
        self.setLayout(self.IK_tool_layout)

        # Connect signals to slot
        self.IK_spline_rad.toggled.connect(self.update_visibility)
        self.IK_reg_rad.toggled.connect(self.update_visibility)
        
        create_btn = QPushButton("CREATE RIG")
        create_btn.setStyleSheet("QPushButton {font-weight: bold;}")
        group_001_layout.addWidget(create_btn)

        # Initial state
        self.update_visibility()

    def update_visibility(self):
        if self.IK_spline_rad.isChecked():
            self.text_003.show()
            self.spans.show()
        else:
            self.text_003.hide()
            self.spans.hide()

def show_ui():

    shayMakeWindow = EDG707_002()
    shayMakeWindow.show(dockable=True, dockArea=Qt.LeftDockWidgetArea)

show_ui()