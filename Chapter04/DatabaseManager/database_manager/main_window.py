"""Database Manager GUI - Main Window

Building Custom UIs with PyQt with Packt Publishing
Chapter 4 - Handling Data with PyQt
Created by: Joshua Willman
"""

# TODO: Filters 
# TODO Find optimization techniques or concepts

# Import necessary modules
import sys
from PyQt6.QtWidgets import (QApplication, QComboBox, QMainWindow, QLabel, QVBoxLayout,  
    QWidget, QPushButton, QLineEdit, QTabWidget, QGroupBox,
    QTableView, QStyledItemDelegate,
    QHeaderView, QHBoxLayout, QDateEdit) 
from PyQt6.QtCore import Qt, QSortFilterProxyModel
from PyQt6.QtSql import (QSqlQuery, QSqlRelation, 
    QSqlRelationalTableModel, QSqlRelationalDelegate, QSqlTableModel)

class DateDelegate(QStyledItemDelegate):

    def createEditor(self, parent, option, index):
        # make sure to explicitly set the parent
        # otherwise it pops up in a top-level window! [EDIT]
        editor = QDateEdit(parent, calendarPopup=True)
        editor.setDisplayFormat("yyyy-MM-dd")
        editor.setAutoFillBackground(True)
        return editor

class MainWindow(QMainWindow):

    def __init__(self, admin_or_not=None):
        """ MainWindow Constructor """
        super().__init__()
        self.admin_or_not = admin_or_not # Use to grant the user Admin privileges
        self.current_proxy_model = None
        self.initializeUI()
        
    def initializeUI(self):
        """Set up the GUI's main window."""
        self.setWindowTitle("Database Manager") 
        self.setMinimumSize(800, 400)
        self.setUpMainWindow()

    def setUpMainWindow(self):
        """Create and arrange widgets in the main window.""" 
        self.customer_tab = QWidget()
        self.orders_tab = QWidget()
        self.details_tab = QWidget()
        self.category_tab = QWidget()
        self.products_tab = QWidget()

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.addTab(self.customer_tab, "Customers")
        self.tabs.addTab(self.orders_tab, "Orders")
        self.tabs.addTab(self.category_tab, "Categories")
        self.tabs.addTab(self.products_tab, "Products")
        if self.admin_or_not == 1:  
            self.staff_tab = QWidget()
            self.tabs.insertTab(0, self.staff_tab, "Staff")
            self.viewStaffTab()
            self.tabs.setCurrentIndex(1) # Set tab to Customers tab
        self.tabs.currentChanged.connect(self.updateWidgetsAndStates)

        self.createCustomersTab()
        self.createOrdersTab()
        self.createCategoriesTab()
        self.createProductsTab()  

        # Create the widgets for the side panel for filtering table results
        self.table_name_label = QLabel("<b>Customers</b>")
        self.table_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create the widgets in the sidebar for filtering table content
        filter_pattern_line = QLineEdit()
        filter_pattern_line.setClearButtonEnabled(True)
        filter_pattern_line.textChanged.connect(self.filterTextChanged)
        filter_syntax_combo = QComboBox()
        #filter_syntax_combo
        self.filter_column_combo = QComboBox()
        self.filter_column_combo.currentIndexChanged.connect(self.selectTableColumn)

        filter_v_box = QVBoxLayout()
        filter_v_box.addWidget(self.table_name_label)
        filter_v_box.addWidget(QLabel("Filter Pattern"))
        filter_v_box.addWidget(filter_pattern_line)
        filter_v_box.addWidget(QLabel("Filter Syntax"))
        filter_v_box.addWidget(filter_syntax_combo)
        filter_v_box.addWidget(QLabel("Select Table Column"))
        filter_v_box.addWidget(self.filter_column_combo)
        filter_v_box.addStretch(2)

        self.filter_group = QGroupBox("Filters/Sorting")
        self.filter_group.setMaximumWidth(260)
        self.filter_group.setLayout(filter_v_box)

        main_h_box = QHBoxLayout()
        main_h_box.addWidget(self.tabs)
        main_h_box.addWidget(self.filter_group)

        main_container = QWidget()
        main_container.setLayout(main_h_box)
        self.setCentralWidget(main_container)

    def viewStaffTab(self):
        """ """
        staff_sql_model = QSqlRelationalTableModel()
        staff_sql_model.setTable("Staff")  
        staff_sql_model.select() # Populate the model with data

        proxy_model = QSortFilterProxyModel()
        proxy_model.setSourceModel(staff_sql_model)

        staff_table = QTableView()
        staff_table.setModel(proxy_model)
        staff_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        staff_table.doubleClicked.connect(self.editTableValues)

        staff_h_box = QHBoxLayout()
        staff_h_box.addWidget(staff_table)
        self.staff_tab.setLayout(staff_h_box) 

    def editTableValues(self): # TODO: EDIT name
        """ """
        current_table = self.tabs.currentWidget().findChild(QTableView)
        print(current_table.model().columnCount())

    def createCustomersTab(self):
        """ """ 
        sql_model = QSqlRelationalTableModel()
        sql_model.setTable("Customers")  
        sql_model.setRelation(sql_model.fieldIndex("staff_id"), QSqlRelation("Staff", "staff_id", "username"))
        sql_model.setHeaderData(sql_model.fieldIndex("staff_id"), Qt.Orientation.Horizontal, "staff_username")
        sql_model.select() # Populate the model with data

        proxy_model = QSortFilterProxyModel()
        proxy_model.setSourceModel(sql_model)

        cust_table = QTableView()
        cust_table.setSortingEnabled(True) # Must be called before disabling sorting by default
        cust_table.setModel( proxy_model)
        cust_table.setItemDelegate(QSqlRelationalDelegate(cust_table))
        cust_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)

        cust_h_box = QHBoxLayout()
        cust_h_box.addWidget(cust_table)
        self.customer_tab.setLayout(cust_h_box)

    def createOrdersTab(self):
        """ """
        sql_model = QSqlRelationalTableModel()
        sql_model.setTable("Orders") 
        sql_model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        sql_model.setRelation(sql_model.fieldIndex("product_id"), QSqlRelation("Products", "product_id", "product_name"))
        sql_model.setRelation(sql_model.fieldIndex("customer_id"), QSqlRelation("Customers", "customer_id", "customer_id"))
        sql_model.select() # Populate the model with data

        sql_model.dataChanged.connect(self.test)

        proxy_model = QSortFilterProxyModel()
        proxy_model.setSourceModel(sql_model)

        ord_table = QTableView()
        ord_table.setSortingEnabled(True)
        ord_table.setModel(proxy_model)
        ord_table.setItemDelegate(QSqlRelationalDelegate(ord_table))

        date_delegate = DateDelegate()
        ord_table.setItemDelegateForColumn(sql_model.fieldIndex("date_of_order"), date_delegate)

        ord_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)

        ord_h_box = QHBoxLayout()
        ord_h_box.addWidget(ord_table)
        self.orders_tab.setLayout(ord_h_box)

    def test(self, topLeft, bottomRight, roles):
        print(topLeft, bottomRight, roles)

    def createCategoriesTab(self):
        sql_model = QSqlRelationalTableModel()
        sql_model.setTable("Categories")  
        sql_model.select() # Populate the model with data

        proxy_model = QSortFilterProxyModel()
        proxy_model.setSourceModel(sql_model)

        cat_table = QTableView()
        cat_table.setSortingEnabled(True)
        cat_table.setModel(proxy_model)
        cat_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)

        cat_h_box = QHBoxLayout()
        cat_h_box.addWidget(cat_table)
        self.category_tab.setLayout(cat_h_box)

    def createProductsTab(self):
        """ """
        sql_model = QSqlRelationalTableModel()
        sql_model.setTable("Products")  
        sql_model.setRelation(sql_model.fieldIndex("category_id"), QSqlRelation("Categories", "category_id", "category_name"))
        sql_model.select() # Populate the model with data

        proxy_model = QSortFilterProxyModel()
        proxy_model.setSourceModel(sql_model)

        prod_table = QTableView()
        prod_table.setSortingEnabled(True)
        prod_table.setModel(proxy_model)
        prod_table.setItemDelegate(QSqlRelationalDelegate(prod_table))
        prod_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)

        prod_h_box = QHBoxLayout()
        prod_h_box.addWidget(prod_table)
        self.products_tab.setLayout(prod_h_box) 

    def filterTextChanged(self, text):
        """ """
        self.current_proxy_model.setFilterRegularExpression(text)
    
    def selectTableColumn(self, index):
        """ """
        self.current_proxy_model.setFilterKeyColumn(self.filter_column_combo.currentIndex())

    def updateWidgetsAndStates(self, index):
        """ """            
        field_names = []   
        self.filter_column_combo.clear()

        current_table = self.tabs.currentWidget().findChild(QTableView)
        if isinstance(current_table.model(), QSqlRelationalTableModel):
            self.table_name_label.setText(f"<b>{current_table.model().tableName()}</b>")

            # Update ... QComboBox columns
            #current_table.model().record().fieldName()
            for col in range(0, current_table.model().columnCount()):
                field_names.append(current_table.model().record().fieldName(col))
            self.filter_column_combo.addItems(field_names)

        elif isinstance(current_table.model(), QSortFilterProxyModel):
            self.table_name_label.setText(f"<b>{current_table.model().sourceModel().tableName()}</b>")
            self.current_proxy_model = current_table.model()

            for col in range(0, current_table.model().sourceModel().columnCount()):
                field_names.append(current_table.model().sourceModel().record().fieldName(col))
            self.filter_column_combo.addItems(field_names)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())