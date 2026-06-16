import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os

# Global variable to hold the dynamic data table in system memory
loaded_dataframe = None

# 1. FILE UPLOAD INGESTION PIPELINE (Pandas Layer)
def upload_csv_file():
    global loaded_dataframe
    
    # Open Windows File Explorer dialog window
    file_path = filedialog.askopenfilename(
        title="Select Wind Tunnel Telemetry File",
        filetypes=[("CSV Files", "*.csv"), ("Text Files", "*.txt")]
    )
    
    if file_path:
        try:
            # Leverage Pandas to read ANY structural CSV data sheet instantly
            loaded_dataframe = pd.read_csv(file_path)
            
            # DATA INTEGRITY CHECK: Ensure required structural metrics exist
            required_columns = ['AoA_deg', 'Cl', 'Cd']
            if not all(col in loaded_dataframe.columns for col in required_columns):
                messagebox.showerror(
                    "Data Format Error", 
                    "Uploaded file must contain exactly these header columns:\n'AoA_deg', 'Cl', and 'Cd'"
                )
                loaded_dataframe = None
                return
            
            # Update visual interface text parameters on success
            file_label.config(text=f"📂 Ingested: {os.path.basename(file_path)}", fg="forestgreen")
            status_display.config(text="✅ Database Ingested. Ready for evaluation.", fg="blue", font=("Arial", 10, "italic"))
            
        except Exception as e:
            messagebox.showerror("Ingestion Failure", f"Failed to parse CSV file: {str(e)}")

# 2. RUN TIME SIMULATION EVALUATOR
def evaluate_performance():
    global loaded_dataframe
    
    # Safety Check: Stop execution if no data sheet is currently loaded
    if loaded_dataframe is None:
        messagebox.showerror("Execution Error", "Please ingest a wind tunnel CSV data sheet first!")
        return
        
    try:
        # Grab the target text parameter typed into the Entry slot
        user_aoa = int(aoa_input.get())
        
        # Fast DataFrame Filtering: Query the table array for a matching AoA row
        matching_row = loaded_dataframe[loaded_dataframe['AoA_deg'] == user_aoa]
        
        # Validation Filter: Check if the user's input angle exists in the uploaded file
        if matching_row.empty:
            messagebox.showerror("Query Error", f"Angle of Attack {user_aoa}° not found in the uploaded matrix!")
            return
            
        # Extract direct scalar floats from the matched Pandas Series element
        cl = float(matching_row['Cl'].values[0])
        cd = float(matching_row['Cd'].values[0])
        
        # Calculate aerodynamic efficiency matrix ratio (Cl/Cd)
        efficiency = round(cl / cd, 1)
        
        # Dynamically map calculated variables back to screen display panels
        cl_display.config(text=f"Lift Coefficient (Cl): {cl}", fg="black")
        cd_display.config(text=f"Drag Coefficient (Cd): {cd}", fg="black")
        ratio_display.config(text=f"Aerodynamic Efficiency (Cl/Cd): {efficiency}", fg="black")
        
        # CLOSED-LOOP FLIGHT BOUNDARY DETECTOR (Stall Condition Filter)
        if user_aoa >= 20:
            status_display.config(text="🚨 CRITICAL FLIGHT STATE: STALL APPARENT", fg="crimson", font=("Arial", 11, "bold"))
        else:
            status_display.config(text="✅ SAFE FLIGHT CONDITIONS: Attached Airflow", fg="forestgreen", font=("Arial", 11, "bold"))
            
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid numeric Angle of Attack value!")

# 3. CONSTRUCTING THE VISUAL INTERFACE CORE FRAMES
root = tk.Tk()
root.title("Flight Performance Evaluation Tool")
root.geometry("460x420")
root.configure(bg="#F4F4F4")

# Main Tool Header Text
header = tk.Label(root, text="Flight Performance Evaluation Tool", font=("Arial", 14, "bold"), bg="#F4F4F4", fg="#002060")
header.pack(pady=15)

# SECTION A: THE FILE BROWSER WIDGET PANEL (Ingestion Box)
file_frame = tk.Frame(root, bg="#EAEAEA", bd=1, relief=tk.SOLID, padx=10, pady=10)
file_frame.pack(pady=15, fill=tk.X, padx=25)

browse_btn = tk.Button(file_frame, text="📁 Browse Data Sheet", command=upload_csv_file, bg="#333333", fg="white", font=("Arial", 9, "bold"))
browse_btn.pack(side=tk.LEFT, padx=5)

file_label = tk.Label(file_frame, text="No CSV file uploaded yet.", font=("Arial", 9, "italic"), bg="#EAEAEA", fg="gray")
file_label.pack(side=tk.LEFT, padx=10)

# SECTION B: INTERACTIVE DATA MATRIX QUERY CONTROLS
input_frame = tk.Frame(root, bg="#F4F4F4")
input_frame.pack(pady=10)

input_label = tk.Label(input_frame, text="Enter Target Angle of Attack (AoA deg):", font=("Arial", 10), bg="#F4F4F4")
input_label.pack(side=tk.LEFT, padx=5)

aoa_input = tk.Entry(input_frame, width=6, font=("Arial", 10), justify="center")
aoa_input.pack(side=tk.LEFT, padx=5)
aoa_input.insert(0, "0")  # Set default display baseline value to 0

run_btn = tk.Button(root, text="Run Performance Evaluation", command=evaluate_performance, bg="#002060", fg="white", font=("Arial", 10, "bold"), padx=15)
run_btn.pack(pady=15)

# SECTION C: FLIGHT PHYSICS OUTPUT DASHBOARD PANELS
cl_display = tk.Label(root, text="Lift Coefficient (Cl): -", font=("Arial", 10), bg="#F4F4F4")
cl_display.pack(pady=3)

cd_display = tk.Label(root, text="Drag Coefficient (Cd): -", font=("Arial", 10), bg="#F4F4F4")
cd_display.pack(pady=3)

ratio_display = tk.Label(root, text="Aerodynamic Efficiency (Cl/Cd): -", font=("Arial", 10), bg="#F4F4F4")
ratio_display.pack(pady=3)

# Boundary Safety Check Status Field
status_display = tk.Label(root, text="Status: Waiting for data ingestion...", font=("Arial", 10, "italic"), bg="#F4F4F4", fg="gray")
status_display.pack(pady=15)

# 4. INITIATE THE CONTINUOUS LOOP WINDOW INTERACTION
root.mainloop()
