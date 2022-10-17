import datetime as dt
import csv


class IndexModel:
    def __init__(self) -> None:
        # read all the data
        with open('data_sources/stock_prices.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)    # remove titles

            self.data = list(csv_reader)     # store data in list
            self.index_output = []
            self.date_index = []
            # loop through data and enumerate all dates into new array
            for i in range(len(self.data)):
                self.date_index.append(self.data[i][0])


    def calc_index_level(self, start_date: dt.date, end_date: dt.date) -> None:


        dt_str = self.data[self.date_index.index(start_date.strftime('%d/%m/%Y'))][0]
        curr_date = start_date
        curr_date_str = curr_date.strftime('%d/%m/%Y')
        end_date_str = end_date.strftime('%d/%m/%Y')
        prev_date = None
        i = self.date_index.index(curr_date_str)

        while curr_date_str != end_date_str:

            # if first day of month or initial loop, rebalance index
            if curr_date == start_date:
                index_info = self.rebalance(self.data[i-1])
                index_stocks = index_info[1]
            elif curr_date.month != prev_date.month:
                index_info = self.rebalance(self.data[i-1])
                index_level = index_info[0]
                index_stocks = index_info[1]

            index_level = 0.5 * float(self.data[i][index_stocks[0]])  0.25 * float(self.data[i][index_stocks[1]]) + 0.25 * float(self.data[i][index_stocks[2]])
            if curr_date == start_date:
                self.index_output.append((self.data[i][0], 100))
            else:
                self.index_output.append((self.data[i][0], round(index_level, 2)))

            # change current date
            i += 1
            prev_date = curr_date
            curr_date_str = self.data[i][0]
            curr_date = dt.datetime.strptime(curr_date_str, '%d/%m/%Y')

    def export_values(self, file_name: str) -> None:
        file = open(file_name, 'w', newline='')
        writer = csv.writer(file)
        writer.writerow(["Date", "Index_Level"])
        writer.writerows(self.index_output)


    def rebalance(self, arr: list) -> tuple:
        # new values weighted/300 (base value)
        stocks = []
        index = []
        daily_data = []
        # Convert values in arr to float
        for i in range(1, len(arr)):
            daily_data.append(float(arr[i]))
        # Sort list and enumerate with original indicies
        sorted_arr = sorted(list(enumerate(daily_data)), key=lambda x:x[1], reverse=True)

        # Find three largest values and get their index to track later
        for i in range(3):
            stocks.append(float(sorted_arr[i][1]))
            index.append(sorted_arr[i][0] + 1)  # Add one since we got rid of date column

        return ((stocks[0] * 0.5 + stocks[1] * 0.25 + stocks[2] * 0.25)/300), tuple(i for i in index)
