# Task D: Histogram Display

import csv
import tkinter as tk  # Import tkinter module for GUI creation

class HistogramApp:
    def __init__(self, traffic_data, date):
        
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.traffic_data = traffic_data
        self.date = date
        self.root = tk.Tk()
        self.canvas = None  # Will hold the canvas for drawing

    def setup_window(self):
        
        """
        Sets up the Tkinter window and canvas for the histogram.
        """
        self.root.title(f"Histogram")
        self.canvas = tk.Canvas(self.root, width=1200, height=700, bg="white")
        self.canvas.pack()  # Add the canvas to the Tkinter window
        self.draw_histogram()  # Call the method to draw the histogram
        
        pass  # Setup logic for the window and canvas

    def draw_histogram(self):
        
        """
        Draws the histogram with axes, labels, and bars.
        """
        # Process data to calculate hourly traffic for each junction
        hourly_data = {"Elm Avenue/Rabbit Road": [0]*24, "Hanley Highway/Westway": [0]*24}
        for record in self.traffic_data:
            junction = record["JunctionName"]
            hour = int(record["timeOfDay"].split(":")[0]) # Extract the hour from the time string
            hourly_data[junction][hour] += 1   # Increment the vehicle count for the specific hour and junction

        # Add a title to the top
        self.canvas.create_text(400, 20, text=f"Histogram of Vehicle Frequency per Hour ({self.date})", 
                                font=("Arial", 18, "bold"))

        # Scaling
        max_traffic = max(max(hourly_data[junction]) for junction in hourly_data)  # Get the maximum traffic value
        bar_width = 15
        scale_factor = 400 / max_traffic if max_traffic > 0 else 1  # Scale bars to fit within the canvas height

        # Draw Bars
        for hour in range(24):  # Loop over 24 hours
            hour_group_start_x = 50 + hour * 40  # Calculate the starting x-position for the hour group
            for i, (junction, color) in enumerate([("Elm Avenue/Rabbit Road", "light green"), 
                                                  ("Hanley Highway/Westway", "light coral")]):
                bar_height = hourly_data[junction][hour] * scale_factor # Calculate the bar height based on traffic data
                bar_left_x = hour_group_start_x + i * bar_width # Left x-coordinate of the bar
                bar_top_y = 500 - bar_height # Top y-coordinate of the bar
                bar_right_x = hour_group_start_x + (i + 1) * bar_width # Right x-coordinate of the bar
                bar_bottom_y = 500 # Bottom y-coordinate of the bar
                
                # Draw the bar
                self.canvas.create_rectangle(bar_left_x,bar_top_y ,bar_right_x ,bar_bottom_y , fill=color, outline="black",width=1)
                
                # Display the traffic count above the bar
                if junction == 'Elm Avenue/Rabbit Road':
                    text_color = 'green'
                if junction == 'Hanley Highway/Westway':
                    text_color = 'light coral'
                self.canvas.create_text((bar_left_x + bar_right_x) / 2, bar_top_y-10, text=str(hourly_data[junction][hour]), 
                                        font=("Arial", 8), fill=text_color)
                
                
        # X-axis line
        self.canvas.create_line(50, 500, 1000, 500, fill="black", width=2)       

        # X-axis labels (Hours)
        for hour in range(24):
            hour_label_x = 50 + hour * 40 + bar_width / 2
            self.canvas.create_text(hour_label_x, 520, text=f"{hour:02d}", font=("Arial", 10))
            
        # Add a description of the x-axis    
        self.canvas.create_text(550, 550, text=f"Hours 00:00 to 24:00", 
                                font=("Arial", 10))

        # Legend
        self.add_legend()
        
        pass  # Drawing logic goes here

      
    def add_legend(self):
        
        """
        Adds a legend to the histogram to indicate which bar corresponds to which junction.
        """
        self.canvas.create_rectangle(60,70,80,90, fill="light green", outline="black")
        self.canvas.create_text(90,80, text="Elm Avenue/Rabbit Road", font=("Arial",10), anchor="w")

        self.canvas.create_rectangle(60,100,80,120, fill="light coral", outline="black")
        self.canvas.create_text(90,110, text="Hanley Highway/Westway", font=("Arial",10), anchor="w")
        
        pass  # Logic for adding a legend
     
    def run(self):
        
        """
        Runs the Tkinter main loop to display the histogram.
        """
        self.setup_window()
        self.root.mainloop() # Start the Tkinter event loop
        
        pass  # Tkinter main loop logic

# Task E: Code Loops to Handle Multiple CSV Files

from Pythoncode_w2119708_20240582 import (
    validate_date_input,
    validate_continue_input,
    process_csv_data,
    
)
# Class to manage multiple CSV file processing
class MultiCSVProcessor:
    def __init__(self):
        
        """
        Initializes the application for processing multiple CSV files.
        """
        self.current_data = None

    def load_csv_file(self, file_path):
        
        """
        Loads a CSV file and processes its data.
        """
        try:
            with open(file_path, "r") as file:
                reader = csv.DictReader(file)
                self.current_data = [row for row in reader]
            return True
        except FileNotFoundError:
            print("Error: File not found.")
            return False

        pass  # File loading and data extraction logic
    
    def clear_previous_data(self):
        
        """
        Clears data from the previous run to process a new dataset.
        """
        self.current_data = None
    
        pass  # Logic for clearing data
        
    def handle_user_interaction(self):
        
        """
        Handles user input for processing files.
        """
        
        while True:  
                # Reuse Task A's validation for date input
                day, month, year = validate_date_input()
                # Construct the file name and load the CSV file
                selected_date = f"{day:02d}{month:02d}{year}"  # Format the date as DDMMYYYY
                file_name = f"traffic_data{selected_date}.csv"  # Construct the file name

                if not self.load_csv_file(file_name):  # Try to load the specified CSV file
                    print("File not found. Try again.")
                    continue

                # Process data using Task B's function
                process_data = process_csv_data(file_name)
                

                # Create histogram using Task D's HistogramApp
                app = HistogramApp(self.current_data, f"{day:02d}/{month:02d}/{year}")
                app.run()

                # Reuse Task A's validation for continue input
                if validate_continue_input() == "N":
                    break
        
        pass  # Logic for user interaction
    
    def process_files(self):
        
        """
         Main loop for handling multiple CSV files until the user decides to quit.
        """
        self.handle_user_interaction()
        
        pass  # Loop logic for handling multiple files

if __name__ == "__main__":
    processor = MultiCSVProcessor()
    processor.process_files()
    



