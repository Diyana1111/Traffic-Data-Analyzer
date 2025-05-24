#Author: K.A.H.D.Diyana Senadi Jayasekara
#Date: 05/12/2024
#Student ID: w2119708 / 20240582

import csv # For reading and processing CSV files

# Task A: Input Validation

def validate_date_input():
    
    """
    Prompts the user for a date in DD MM YYYY format, validates the input for:
    - Correct data type
    - Correct range for day, month, and year
    """

    
# Initialize variables for day,month and year     
    day,month,year = 0,0,0
    

    # Validation day input
    while not(1 <= day <= 31):
        try:
            day_value = input("Please enter the day of the survey in the format dd :")
            if not day_value:
                print("Input cannot be empty. Please enter a day.")
                continue
            day = int(day_value)
            if not(1 <= day <= 31):
                print("Out of range - values must be in the range 1 and 31")
        except ValueError:
            print("Integer required") # Error message for invalid input
            
            
    # Validation month intput
    while not(1 <= month <= 12):
        try:
            month_value = input("Please enter the day of the survey in the format MM :")
            if not month_value:
                print("Input cannot be empty. Please enter a month.")
                continue
            month = int(month_value)    
            if not(1 <= month <= 12):
                 print("Out of range - values must be in the range 1 and 12")
        except ValueError:
            print("Integer required") # Error message for invalid input
            
            
    # Validation year input       
    while not(2000 <= year <= 2024):
        try:
            year_value = input("Please enter the day of the survey in the format YYYY :")
            if not year_value:
                print("Input cannot be empty. Please enter a year.")
                continue
            year = int(year_value)
            if not(2000 <= year <= 2024):
                print("Out of range - values must be in the range 2000 and 2024")
            elif month == 2 and day > 28:   #check if year is leap year or not
                if not ((year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)):
                    print("Invalid date - February has only 28 days in a non-leap year. Please enter a valid year.")
                    year = 0  
                
        except ValueError:
                print("Integer required")# Error message for invalid input
            
            
    return day,month,year  # Return the validated day, month, and year       
           
pass  # Validation logic goes here


def validate_continue_input():
    
    """
    Prompts the user to decide whether to load another dataset:
    - Validates "Y" or "N" input
    """
    
    while True:
        response = input("Load another dataset? (Y/N): ").strip().upper()  # Prompt user and convert input to uppercase
        if response in ['Y', 'N']:  # Validate input
            return response 
        else:
            print("Invalid input. Enter 'Y' or 'N'.") # Error message for invalid input
    
    
    pass  # Validation logic goes here


# Task B: Processed Outcomes
def process_csv_data(file_path):
    
    """
    Processes the CSV data for the selected date and extracts:
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Two-wheeled vehicles, and other requested metrics
    """
    
    # Initialize outcomes dictionary with default value
    outcomes = {"file_name":file_path,
                "total_vehicles":0,
                "total_trucks":0,
                "total_electric_vehicles":0,
                "total_two_wheeled_vehicles":0,
                "busses_north_elm":0,
                "vehicles_with_noturn":0,
                "Total_Bicycles":0,
                "truck_percentage":0,
                "average_bicycles_hours":0,
                "over_speed_vehicles":0,
                "elm_junction_vehicles":0,
                "hanley_junction_vehicles":0,
                "elm_scooters":0,
                "elm_scooter_percentage":0,
                "vehicles_peak_hour_hanley":0,
                "peak_traffic_hour_hanley":0,
                "rain_hours":0,
                }
    try:
        with open(file_path,mode="r") as file:  # Open the CSV file
            reader = csv.DictReader(file) # Read CSV data as a dictionary
            hourly_counts_hanley = {}  # Dictionary to track hourly counts at Hanley Highway
            
            for row in reader:
                outcomes["total_vehicles"] += 1 # Count all vehicles
                
                # Count total trucks 
                if row['VehicleType'] == "Truck":
                    outcomes["total_trucks"] += 1
                    
                # count total electric vehicles    
                if row['elctricHybrid'] == "True":
                    outcomes["total_electric_vehicles"] += 1
                    
                # count two-wheeled vehicles    
                if row['VehicleType'] in ["Bicycle","Motorcycle","Scooter"]:
                    outcomes["total_two_wheeled_vehicles"] += 1
                    
                # Count busses heading north at Elm Avenue  
                if row['VehicleType'] == "Buss" and row['JunctionName'] == "Elm Avenue/Rabbit Road" and row['travel_Direction_out'] == "N":
                    outcomes["busses_north_elm"] += 1
                    
                # Count vehicles not turning at junctions    
                if row['JunctionName'] in ['Elm Avenue/Rabbit Road', 'Hanley Highway/Westway'] and row['travel_Direction_out'] == row['travel_Direction_in']:
                    outcomes["vehicles_with_noturn"] += 1
                    

                # count total bicycles
                if row['VehicleType'] == "Bicycle":
                    outcomes["Total_Bicycles"] += 1

                                        
                # Count over-speeding vehicles   
                if int(row['VehicleSpeed']) > int(row['JunctionSpeedLimit']):
                    outcomes["over_speed_vehicles"] += 1

                    
                    
                # Count vehicles at Elm Avenue and Hanley junctions   
                if row['JunctionName'] == "Elm Avenue/Rabbit Road":
                    outcomes["elm_junction_vehicles"] += 1
                if row['JunctionName'] == "Hanley Highway/Westway":
                    outcomes["hanley_junction_vehicles"] += 1

                    
                    
                # Track hourly vehicle counts for Hanley    
                if row['JunctionName'] == 'Hanley Highway/Westway':
                    hour = row['timeOfDay'].split(':')[0]
                    hourly_counts_hanley[hour] = hourly_counts_hanley.get(hour, 0) + 1

                
                
                # Count scooters at Elm Avenue    
                if row['VehicleType'] == "Scooter" and row['JunctionName'] == "Elm Avenue/Rabbit Road":
                    outcomes["elm_scooters"] += 1
                    

                    
                # Count hours of rain    
                if row["Weather_Conditions"] in ["Heavy Rain","Light Rain"]:
                    outcomes["rain_hours"] += 1

                    
                    
        # calculate truck percentage            
        if outcomes["total_vehicles"] > 0:   # Avoid division by zero
            outcomes["truck_percentage"] = round((outcomes["total_trucks"]/outcomes["total_vehicles"])*100)

            
                                          
        # calculate bicycle average                            
        outcomes["average_bicycles_hours"] = int(outcomes["Total_Bicycles"] / 24)
        
        
        # calculate scooter percentage
        if outcomes["elm_junction_vehicles"] > 0: # Avoid division by zero
            outcomes["elm_scooter_percentage"] = int((outcomes["elm_scooters"] / outcomes["elm_junction_vehicles"]) * 100)
                                                     


        # Determine peak hour at Hanley Highway                                             
        if hourly_counts_hanley:
                peak_hour_count = max(hourly_counts_hanley.values())
                outcomes["vehicles_peak_hour_hanley"] = peak_hour_count
                outcomes["peak_traffic_hour_hanley"] = [
                    f"Between {hour}:00 and {int(hour)+1}:00"
                    for hour, count in hourly_counts_hanley.items() if count == peak_hour_count
                ]
                
        
        return outcomes  # Return the processed outcomes dictionary
    except FileNotFoundError:   # Handle missing file errors
        print(f"File {file_path} not found.")
        return None  # Return None if the file does not exist
        
pass  # Logic for processing data goes here

def display_outcomes(outcomes):
    
    """
    Displays the calculated outcomes in a clear and formatted way.
    """
    print("\n***************************")
    print(f"Data file selected is {outcomes['file_name']}")
    print("***************************")
    print(f"The total number of vehicles recorded for this date is {outcomes['total_vehicles']}")
    print(f"The total number of trucks recorded for this date is {outcomes['total_trucks']}")
    print(f"The total number of electric vehicles for this date is {outcomes['total_electric_vehicles']}")
    print(f"The total number of two-wheeled vehicles for this date is {outcomes['total_two_wheeled_vehicles']}")
    print(f"The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcomes['busses_north_elm']}")
    print(f"The total number of Vehicles through both junctions not turning left or right is {outcomes['vehicles_with_noturn']}")
    print(f"The percentage of total vehicles recorded that are trucks for this date is {outcomes['truck_percentage']}%")
    print(f"The average number of Bikes per hour for this date is {outcomes['average_bicycles_hours']}")
    print(f"The total number of vehicles recorded as over the speed limit for this date is {outcomes['over_speed_vehicles']}")
    print(f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes['elm_junction_vehicles']}")
    print(f"The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes['hanley_junction_vehicles']}")
    print(f"{outcomes['elm_scooter_percentage']}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.")
    print(f"The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes['vehicles_peak_hour_hanley']}")
    print(f"The most vehicles through Hanley Highway/Westway were recorded at {outcomes['peak_traffic_hour_hanley']}")
    print(f"The number of hours of rain for this date is {outcomes['rain_hours']}")
  

    
pass  # Printing outcomes to the console


# Task C: Save Results to Text File
def save_results_to_file(outcomes,file_name="results.txt"):
    
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    """
    
    with open(file_name, mode='a') as file:
        file.write("\n***************************")
        file.write(f"Data file selected is {outcomes['file_name']}")
        file.write("***************************")
        file.write(f"The total number of vehicles recorded for this date is {outcomes['total_vehicles']}\n")
        file.write(f"The total number of trucks recorded for this date is {outcomes['total_trucks']}\n")
        file.write(f"The total number of electric vehicles for this date is {outcomes['total_electric_vehicles']}\n")
        file.write(f"The total number of two-wheeled vehicles for this date is {outcomes['total_two_wheeled_vehicles']}\n")
        file.write(f"The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcomes['busses_north_elm']}\n")
        file.write(f"The total number of Vehicles through both junctions not turning left or right is {outcomes['vehicles_with_noturn']}\n")
        file.write(f"The percentage of total vehicles recorded that are trucks for this date is {outcomes['truck_percentage']}\n")
        file.write(f"The average number of Bikes per hour for this date is {outcomes['average_bicycles_hours']}\n")
        file.write(f"The total number of vehicles recorded as over the speed limit for this date is {outcomes['over_speed_vehicles']}\n")
        file.write(f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes['elm_junction_vehicles']}\n")
        file.write(f"The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes['hanley_junction_vehicles']}\n")
        file.write(f"{outcomes['elm_scooter_percentage']}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.\n")
        file.write(f"The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes['vehicles_peak_hour_hanley']}\n")
        file.write(f"The most vehicles through Hanley Highway/Westway were recorded at {outcomes['peak_traffic_hour_hanley']}\n")
        file.write(f"The number of hours of rain for this date is {outcomes['rain_hours']}\n")
        
    
    
pass  # File writing logic goes here

# if you have been contracted to do this assignment please do not remove this line



# Main Program Loop
def main():
    
    while True:
        day,month,year = validate_date_input() # get and validate date input 
        file_name = f"traffic_data{day:02}{month:02}{year}.csv"  # genarate CSV file name
        
        outcomes = process_csv_data(file_name)
        if outcomes:
            display_outcomes(outcomes)  # Display results to the user
            save_results_to_file(outcomes)  # Save results to a file
            
        if validate_continue_input() == "N":  # Check if the user wants to continue
            break  # Exit loop if the user does not wish to continue
    
    
        
if __name__ == "__main__":
    main()
    
