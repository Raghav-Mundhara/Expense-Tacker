import tkinter as tk
from tkinter import messagebox
import sqlite3
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class PieChartWindow:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
        self.cursor = None

        self.root = tk.Tk()
        self.root.title("Pie Chart from SQLite Database")
        self.root.geometry("500x500")
        # self.root.configure(bg="#1b1b1b")
        self.create_widgets()

        self.root.mainloop()
        
    def create_widgets(self):
    # create a frame to hold the pie chart and the button
        chart_frame = tk.Frame(self.root,)
        chart_frame.grid(row=0, column=0, sticky="nsew")

        # connect to the database
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error connecting to database: {e}")

        # fetch data from the database
        try:
            self.cursor.execute("SELECT Expense, SUM(Amount) as Total_Expenditure FROM ExpenseTracker GROUP BY Expense")
            data = self.cursor.fetchall()
            print(data)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching data from database: {e}")
            return

        # prepare data for the pie chart
        labels = [row[0] for row in data]
        sizes = [row[1] for row in data]
        # create a figure and a pie chart
        fig = Figure(figsize=(5, 5))
        ax = fig.add_subplot(111)
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")

        # create a canvas to display the pie chart
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.get_tk_widget().grid(row=0, column=0, rowspan=2, sticky="nsew")

        # create a button to go back
        back_button = tk.Button(chart_frame, text="Back", command=self.root.destroy,bg='#1b1b1b',fg='white',font=('Arial', 10, 'bold'))
        back_button.grid(row=1, column=0, sticky="s")

    def __del__(self):
        # close the database connection when the window is closed
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    db_file = "Expense Tracker.db"
    app = PieChartWindow(db_file)
