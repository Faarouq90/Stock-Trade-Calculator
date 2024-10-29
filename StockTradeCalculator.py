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



    def updateUi(self):
        '''
        This requires substantial development.
        Updates the UI when control values are changed; should also be called when the app initializes.
        '''
        try:
            # TODO: get selected dates from calendars

            # TODO: perform necessary calculations to calculate totals

            # TODO: update the label displaying totals
            pass  # placeholder for future code
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
