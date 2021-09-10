"""Database Manager GUI - Main Window

Building Custom UIs with PyQt with Packt Publishing
Chapter 4 - Handling Data with PyQt
Created by: Joshua Willman
"""

# Import necessary modules
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, 
    QWidget, QLabel, QCheckBox, QComboBox, QLineEdit, 
    QTabWidget, QGroupBox, QTableView, QHeaderView, 
    QHBoxLayout, QVBoxLayout) 
from PyQt6.QtCore import (Qt, 
    QSortFilterProxyModel, QRegularExpression)
from PyQt6.QtSql import (QSqlRelation, QSqlRelationalTableModel)
# Import relative modules
from .model_view.delegates import (PhoneDelegate, 
    DateDelegate, SqlProxyDelegate, ReadOnlyDelegate)

class MainWindow(QMainWindow):

    def __init__(self, admin_or_not=None):
        """ MainWindow Constructor """
        super().__init__()
        self.admin_or_not = admin_or_not # Used to grant the user admin privileges
        self.curr_proxy_model = None # Variable that refers to the current page's proxy mmodel
        self.initializeUI()
        
    def initializeUI(self):
        """Set up the GUI's main window."""
        self.setWindowTitle("Database Manager") 
        self.setMinimumSize(800, 400)
        self.setUpMainWindow()

    def setUpMainWindow(self):
        """Create and arrange widgets in the main window.""" 
        # Create the container widget for each of the pages 
        # in the tab widget
        self.customer_tab = QWidget()
        self.orders_tab = QWidget()
        self.category_tab = QWidget()
        self.products_tab = QWidget()

        # Add or insert the tabs into the tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.addTab(self.customer_tab, "Customers")
        self.tabs.addTab(self.orders_tab, "Orders")
        self.tabs.addTab(self.category_tab, "Categories")
        self.tabs.addTab(self.products_tab, "Products")
        if self.admin_or_not == 1:  
            self.staff_tab = QWidget()
            self.tabs.insertTab(0, self.staff_tab, "Staff")
            self.createStaffTab()
            self.tabs.setCurrentIndex(1) # Set tab to Customers tab
        self.tabs.currentChanged.connect(
            self.updateWidgetsAndStates)

        # Call the methods to construct each page
        self.createCustomersTab()
        self.createOrdersTab()
        self.createCategoriesTab()
        self.createProductsTab()  

        # Create the widgets in the sidebar for filtering table content
        self.table_name_label = QLabel("<b>Customers</b>")
        self.table_name_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter)

        self.filter_pattern_line = QLineEdit()
        self.filter_pattern_line.setClearButtonEnabled(True)
        self.filter_pattern_line.textChanged.connect(self.filterRegExpChanged)

        self.filter_regex_combo = QComboBox()
        filter_options = ["Default", "Wildcard", 
                          "Fixed String"]
        self.filter_regex_combo.addItems(filter_options)
        self.filter_regex_combo.currentIndexChanged.connect(
            self.filterRegExpChanged)

        self.filter_field_combo = QComboBox()
        self.updateWidgetsAndStates(1) # Initialize the values in filter_field_combo
        self.filter_field_combo.currentIndexChanged.connect(
            self.selectTableColumn)

        filter_case_sensitivity_cb = QCheckBox(
            "Filter with Case Sensitivity")
        filter_case_sensitivity_cb.toggled.connect(
            self.toggleCaseSensitivity)
        filter_case_sensitivity_cb.toggle()

        # Layout for the sidebar 
        filter_v_box = QVBoxLayout()
        filter_v_box.addWidget(self.table_name_label)
        filter_v_box.addWidget(QLabel("Filter Pattern"))
        filter_v_box.addWidget(self.filter_pattern_line)
        filter_v_box.addWidget(QLabel("Filter Syntax"))
        filter_v_box.addWidget(self.filter_regex_combo)
        filter_v_box.addWidget(QLabel("Select Table Column"))
        filter_v_box.addWidget(self.filter_field_combo)
        filter_v_box.addWidget(filter_case_sensitivity_cb)
        filter_v_box.addStretch(2)

        self.filter_group = QGroupBox("Filtering")
        self.filter_group.setMaximumWidth(260)
        self.filter_group.setLayout(filter_v_box)

        # Arrange the containers in the main window
        main_h_box = QHBoxLayout()
        main_h_box.addWidget(self.tabs)
        main_h_box.addWidget(self.filter_group)

        main_container = QWidget()
        main_container.setLayout(main_h_box)
        self.setCentralWidget(main_container)

    def createStaffTab(self):
        """Create the page to view the Staff table from the database."""
        staff_sql_model = QSqlRelationalTableModel()
        staff_sql_model.setTable("Staff")  
        staff_sql_model.select() # Populate the model with data

        staff_proxy_model = QSortFilterProxyModel()
        staff_proxy_model.setSourceModel(staff_sql_model)

        staff_table = QTableView()
        staff_table.setSortingEnabled(True)
        staff_table.setModel(staff_proxy_model)
        staff_table.setItemDelegateForColumn(staff_sql_model.fieldIndex("staff_id"), ReadOnlyDelegate())
        staff_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)

        staff_h_box = QHBoxLayout()
        staff_h_box.addWidget(staff_table)
        self.staff_tab.setLayout(staff_h_box) 

    def createCustomersTab(self):
        """Create the page to view the Customers table from the database."""
        cust_sql_model = QSqlRelationalTableModel()
        cust_sql_model.setTable("Customers")  
        cust_sql_model.setRelation(
            cust_sql_model.fieldIndex("staff_id"), 
            QSqlRelation("Staff", "staff_id", "username"))
        cust_sql_model.setHeaderData(
            cust_sql_model.fieldIndex("staff_id"), 
            Qt.Orientation.Horizontal, "staff_username")
        cust_sql_model.select() # Populate the model with data

        cust_proxy_model = QSortFilterProxyModel()
        cust_proxy_model.setSourceModel(cust_sql_model)

        cust_table = QTableView()
        cust_table.setSortingEnabled(True)
        cust_table.setModel(cust_proxy_model)
        cust_table.setItemDelegate(SqlProxyDelegate(
            cust_table))
        cust_table.setItemDelegateForColumn(
            cust_sql_model.fieldIndex("phone"), PhoneDelegate())
        cust_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)

        cust_h_box = QHBoxLayout()
        cust_h_box.addWidget(cust_table)
        self.customer_tab.setLayout(cust_h_box)

    def createOrdersTab(self):
        """Create the page to view the Orders table from the database."""
        ord_sql_model = QSqlRelationalTableModel()
        ord_sql_model.setTable("Orders") 
        ord_sql_model.setRelation(ord_sql_model.fieldIndex("product_id"), QSqlRelation("Products", "product_id", "product_name"))
        ord_sql_model.setRelation(ord_sql_model.fieldIndex("customer_id"), QSqlRelation("Customers", "customer_id", "first_name"))
        ord_sql_model.setHeaderData(ord_sql_model.fieldIndex("customer_id"), Qt.Orientation.Horizontal, "customer_name")
        ord_sql_model.select() # Populate the model with data

        ord_proxy_model = QSortFilterProxyModel()
        ord_proxy_model.setSourceModel(ord_sql_model)

        ord_table = QTableView()
        ord_table.setSortingEnabled(True)
        ord_table.setModel(ord_proxy_model)
        ord_table.setItemDelegate(SqlProxyDelegate(
            ord_table))
        ord_table.setItemDelegateForColumn(
            ord_sql_model.fieldIndex("date_of_order"), 
            DateDelegate())
        ord_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)

        ord_h_box = QHBoxLayout()
        ord_h_box.addWidget(ord_table)
        self.orders_tab.setLayout(ord_h_box)

    def createCategoriesTab(self):
        """Create the page to view the Categories table from the database."""
        cat_sql_model = QSqlRelationalTableModel()
        cat_sql_model.setTable("Categories")  
        cat_sql_model.select() # Populate the model with data

        cat_proxy_model = QSortFilterProxyModel()
        cat_proxy_model.setSourceModel(cat_sql_model)

        cat_table = QTableView()
        cat_table.setSortingEnabled(True)
        cat_table.setModel(cat_proxy_model)
        cat_table.setItemDelegateForColumn(
            cat_sql_model.fieldIndex("category_id"), 
            ReadOnlyDelegate())
        cat_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)

        cat_h_box = QHBoxLayout()
        cat_h_box.addWidget(cat_table)
        self.category_tab.setLayout(cat_h_box)

    def createProductsTab(self):
        """Create the page to view the Products table from the database."""
        prod_sql_model = QSqlRelationalTableModel()
        prod_sql_model.setTable("Products")  
        prod_sql_model.setRelation(
            prod_sql_model.fieldIndex("category_id"), 
            QSqlRelation("Categories", "category_id", 
            "category_name"))
        prod_sql_model.select() # Populate the model with data

        prod_proxy_model = QSortFilterProxyModel()
        prod_proxy_model.setSourceModel(prod_sql_model)

        prod_table = QTableView()
        prod_table.setSortingEnabled(True)
        prod_table.setModel(prod_proxy_model)
        prod_table.setItemDelegate(SqlProxyDelegate(
            prod_table))
        prod_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)

        prod_h_box = QHBoxLayout()
        prod_h_box.addWidget(prod_table)
        self.products_tab.setLayout(prod_h_box) 

    def filterRegExpChanged(self, value):
        """Slot for collecting the expression (exp) for filtering
        items in the tables. Expressions are then passed to various
        QSortFilterProxyModel methods depending upon the value in 
        filter_regex_combo."""
        exp = self.filter_pattern_line.text()
        syntax = self.filter_regex_combo.currentText()
        model = self.curr_proxy_model # NOTE: Used to shorten the length of the text for the book

        if syntax == "Default":
            model.setFilterRegularExpression(exp)
        if syntax == "Wildcard":
            regex = QRegularExpression()
            wildcard = regex.wildcardToRegularExpression(
                exp, 
                QRegularExpression.WildcardConversionOption.UnanchoredWildcardConversion)            
            model.setFilterRegularExpression(wildcard)
        if syntax == "Fixed String":
            model.setFilterFixedString(exp)
    
    def selectTableColumn(self, index):
        """Select the field (column) in the SQL table to be filtered."""
        self.curr_proxy_model.setFilterKeyColumn(index)

    def toggleCaseSensitivity(self, toggled):
        """Toggle whether items are filtered with or without case sensitivity."""
        if toggled:
            self.curr_proxy_model.setFilterCaseSensitivity(
                Qt.CaseSensitivity.CaseSensitive)
        else:
            self.curr_proxy_model.setFilterCaseSensitivity(
                Qt.CaseSensitivity.CaseInsensitive)

    def updateWidgetsAndStates(self, index):
        """Whenever the user switches a tab, update information regarding
        the tab selected, the current table's QSortFilterProxyModel, and information
        displayed in the sidebar for filtering."""            
        field_names = []   
        self.filter_field_combo.clear()
        curr_table = self.tabs.currentWidget().findChild(
            QTableView)
        curr_model = curr_table.model().sourceModel()

        # Set text to display current table's name in the sidebar
        self.table_name_label.setText(
            f"<b>{curr_model.tableName()}</b>")
        self.curr_proxy_model = curr_table.model()

        # Update QComboBox values based on currently selected tab
        for col in range(0, curr_model.columnCount()):
            field_names.append(
                curr_model.record().fieldName(col))
            if curr_model.tableName() == "Orders" and \
                "first_name" in field_names:
                field_names = ["customer_name" 
                               if n=="first_name" else n 
                               for n in field_names]
        self.filter_field_combo.addItems(field_names)

        # NOTE: To the reader, the following code differs slightly from the book. 
        # This portion is left here as reference should you need to use both 
        # QSqlTableModel and QSqlRelationalTableModel classes. Simply replace the code 
        # above with the code below.
        """
        if isinstance(curr_table.model(), QSqlRelationalTableModel):
            self.table_name_label.setText(f"<b>{curr_table.model().tableName()}</b>")

            # Update QComboBox values based on currently selected tab
            for col in range(0, curr_table.model().columnCount()):
                field_names.append(curr_table.model().record().fieldName(col))
            self.filter_field_combo.addItems(field_names)

        elif isinstance(curr_table.model(), QSortFilterProxyModel):
            self.table_name_label.setText(f"<b>{curr_model.tableName()}</b>")
            self.curr_proxy_model = curr_table.model()

            # Update QComboBox values based on currently selected tab
            for col in range(0, curr_model.columnCount()):
                field_names.append(curr_model.record().fieldName(col))
                if "first_name" in field_names:
                    field_names = ["customer_name" if i=="first_name" else i for i in field_names]
            self.filter_field_combo.addItems(field_names)
        """

    def closeEvent(self, event):
        """Close database connection when window is closed."""
        model = self.curr_proxy_model.sourceModel()
        model.database().close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())