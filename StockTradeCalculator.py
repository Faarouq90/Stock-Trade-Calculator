import sys
import csv
from datetime import datetime
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QLabel, QComboBox, QCalendarWidget, QDialog, QApplication, QGridLayout, QSpinBox
from datetime import datetime


class StockTradeProfitCalculator(QDialog):
    '''
    Provides the following functionality:

    - Allows the selection of the stock to be purchased
    - Allows the selection of the quantity to be purchased
    - Allows the selection of the purchase date
    - Displays the purchase total
    - Allows the selection of the sell date
    - Displays the sell total
    - Displays the profit total
    '''

    def __init__(self):
        '''
        This method requires substantial updates.
        Each of the widgets should be suitably initialized and laid out.
        '''
        super().__init__()

        # setting up dictionary of Stocks
        self.data = self.make_data()

        # Check if 'Amazon' exists, if not, handle it gracefully
        if 'Amazon' in self.data:
            self.sellCalendarDefaultDate = sorted(self.data['Amazon'].keys())[-1]
        else:
            print("Amazon not found in the dataset. Available stocks:", self.data.keys())
            self.sellCalendarDefaultDate = QDate.currentDate()  # Default to the current date

        # Set the window title
        self.setWindowTitle("Stock Trade Profit Calculator")

        #Qlabel for stock selection
        self.stockLabel = QLabel("Select Stock:")
        self.stockComboBox = QComboBox()
        self.stockComboBox.addItems(self.data.keys())  # Populate with stock names

        # Create QSpinBox for stock quantity
        self.quantityLabel = QLabel("Quantity:")
        self.quantitySpinBox = QSpinBox()
        self.quantitySpinBox.setMinimum(1)  # Set minimum to 1

        # Create QCalendarWidget for purchase date
        self.purchaseDateCalendar = QCalendarWidget()
        self.purchaseDateCalendar.setSelectedDate(QDate.currentDate().addDays(-14))  # Default to 2 weeks ago

        # Create QCalendarWidget for sell date
        self.sellDateCalendar = QCalendarWidget()
        self.sellDateCalendar.setSelectedDate(QDate.currentDate())  # Default to today

        # Create labels for totals
        self.purchaseTotalLabel = QLabel("Purchase Total: $0.00")
        self.sellTotalLabel = QLabel("Sell Total: $0.00")
        self.profitTotalLabel = QLabel("Profit/Loss: $0.00")

        # Layout initialization
        layout = QGridLayout()
        layout.addWidget(self.stockLabel, 0, 0)
        layout.addWidget(self.stockComboBox, 0, 1)
        layout.addWidget(self.quantityLabel, 1, 0)
        layout.addWidget(self.quantitySpinBox, 1, 1)
        layout.addWidget(QLabel("Purchase Date:"), 2, 0)
        layout.addWidget(self.purchaseDateCalendar, 2, 1)
        layout.addWidget(QLabel("Sell Date:"), 3, 0)
        layout.addWidget(self.sellDateCalendar, 3, 1)
        layout.addWidget(self.purchaseTotalLabel, 4, 0, 1, 2)
        layout.addWidget(self.sellTotalLabel, 5, 0, 1, 2)
        layout.addWidget(self.profitTotalLabel, 6, 0, 1, 2)

        # Set the layout
        self.setLayout(layout)

        # Connect signals to slots
        self.stockComboBox.currentIndexChanged.connect(self.updateUi)
        self.quantitySpinBox.valueChanged.connect(self.updateUi)
        self.purchaseDateCalendar.selectionChanged.connect(self.updateUi)
        self.sellDateCalendar.selectionChanged.connect(self.updateUi)

        # Initial UI update
        self.updateUi()


    def updateUi(self):
        '''
        This requires substantial development.
        Updates the UI when control values are changed; should also be called when the app initializes.
        '''
        try:
            # Get selected stock, quantity, and dates from controls
            selected_stock = self.stockComboBox.currentText()
            quantity = self.quantitySpinBox.value()
            purchase_date = self.purchaseDateCalendar.selectedDate().toPyDate()
            sell_date = self.sellDateCalendar.selectedDate().toPyDate()

            # Convert selected dates to tuple format
            purchase_date_tuple = (purchase_date.year, purchase_date.month, purchase_date.day)
            sell_date_tuple = (sell_date.year, sell_date.month, sell_date.day)

            # Retrieve prices from data dictionary
            purchase_price = self.data[selected_stock].get(purchase_date_tuple, 0.0)
            sell_price = self.data[selected_stock].get(sell_date_tuple, 0.0)

            # Calculate totals and profit/loss
            purchase_total = purchase_price * quantity
            sell_total = sell_price * quantity
            profit_loss = sell_total - purchase_total

            # Update labels with calculated totals
            self.purchaseTotalLabel.setText(f"Purchase Total: ${purchase_total:.2f}")
            self.sellTotalLabel.setText(f"Sell Total: ${sell_total:.2f}")
            self.profitTotalLabel.setText(f"Profit/Loss: ${profit_loss:.2f}")

        except Exception as e:
            print(f"Error in updateUi: {e}")

    def make_data(self):
        '''
        This code reads the stock market CSV file and generates a dictionary structure.
        :return: a dictionary of dictionaries
        '''
        data = {}
        try:
            with open('Transformed_Stock_Market_Dataset.csv', mode='r') as file:
                reader = csv.DictReader(file)
                stock_names = reader.fieldnames[1:]  # All columns except 'Date' are stock names

                for row in reader:
                    date_string = row['Date']
                    date_tuple = self.string_date_into_tuple(date_string)

                    for stock in stock_names:
                        price = row[stock].replace(',', '')
                        try:
                            price = float(price)
                        except ValueError:
                            price = 0.0

                        if stock not in data:
                            data[stock] = {}

                        data[stock][date_tuple] = price

            print("Data loaded successfully.")
            print(f"Stocks available: {stock_names}")  # Debugging: Print all available stock names

        except Exception as e:
            print(f"Error reading data: {e}")
        return data

    def string_date_into_tuple(self, date_string):
        '''
        Converts a date in string format (e.g., "2024-02-02") into a tuple (year, month, day).
        :return: tuple representing the date
        '''
        try:
            if '-' in date_string:
                date_obj = datetime.strptime(date_string, "%d-%m-%Y")
            else:
                date_obj = datetime.strptime(date_string, "%m/%d/%Y")
            return date_obj.year, date_obj.month, date_obj.day
        except ValueError:
            print(f"Error parsing date: {date_string}")
            return None


# This is complete
if __name__ == '__main__':
    app = QApplication(sys.argv)
    stock_calculator = StockTradeProfitCalculator()
    stock_calculator.show()
    sys.exit(app.exec())
