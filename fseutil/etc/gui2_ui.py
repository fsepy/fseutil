MAIN_WINDOW = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>486</width>
    <height>554</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QGroupBox" name="groupBox">
    <property name="geometry">
     <rect>
      <x>30</x>
      <y>30</y>
      <width>421</width>
      <height>431</height>
     </rect>
    </property>
    <property name="title">
     <string>GroupBox</string>
    </property>
    <widget class="QTableView" name="tableView">
     <property name="geometry">
      <rect>
       <x>20</x>
       <y>30</y>
       <width>151</width>
       <height>101</height>
      </rect>
     </property>
    </widget>
    <widget class="QLineEdit" name="lineEdit">
     <property name="geometry">
      <rect>
       <x>20</x>
       <y>139</y>
       <width>151</width>
       <height>21</height>
      </rect>
     </property>
    </widget>
    <widget class="QSpinBox" name="spinBox">
     <property name="geometry">
      <rect>
       <x>20</x>
       <y>170</y>
       <width>151</width>
       <height>22</height>
      </rect>
     </property>
    </widget>
    <widget class="QDoubleSpinBox" name="doubleSpinBox">
     <property name="geometry">
      <rect>
       <x>20</x>
       <y>200</y>
       <width>151</width>
       <height>22</height>
      </rect>
     </property>
    </widget>
    <widget class="QCheckBox" name="checkBox">
     <property name="geometry">
      <rect>
       <x>200</x>
       <y>60</y>
       <width>70</width>
       <height>17</height>
      </rect>
     </property>
     <property name="text">
      <string>CheckBox</string>
     </property>
    </widget>
    <widget class="QRadioButton" name="radioButton">
     <property name="geometry">
      <rect>
       <x>200</x>
       <y>90</y>
       <width>82</width>
       <height>17</height>
      </rect>
     </property>
     <property name="text">
      <string>RadioButton</string>
     </property>
    </widget>
    <widget class="QToolButton" name="toolButton">
     <property name="geometry">
      <rect>
       <x>200</x>
       <y>30</y>
       <width>25</width>
       <height>19</height>
      </rect>
     </property>
     <property name="text">
      <string>...</string>
     </property>
    </widget>
    <widget class="QCommandLinkButton" name="commandLinkButton">
     <property name="geometry">
      <rect>
       <x>200</x>
       <y>120</y>
       <width>172</width>
       <height>41</height>
      </rect>
     </property>
     <property name="text">
      <string>CommandLinkButton</string>
     </property>
    </widget>
    <widget class="QDialogButtonBox" name="buttonBox">
     <property name="geometry">
      <rect>
       <x>200</x>
       <y>180</y>
       <width>156</width>
       <height>23</height>
      </rect>
     </property>
     <property name="standardButtons">
      <set>QDialogButtonBox::Cancel|QDialogButtonBox::Ok</set>
     </property>
    </widget>
   </widget>
   <widget class="QPushButton" name="pushButton">
    <property name="geometry">
     <rect>
      <x>370</x>
      <y>470</y>
      <width>81</width>
      <height>23</height>
     </rect>
    </property>
    <property name="text">
     <string>PushButton</string>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>486</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
"""