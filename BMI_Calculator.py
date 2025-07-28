import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

def calculate_bmi():
    try:
        # Get values from entries
        weight = float(weight_entry.get())
        height_feet = float(height_entry.get())
        
        # Validate inputs
        if weight <= 0 or height_feet <= 0:
            raise ValueError("Values must be positive")
        
        # Convert height to meters
        height_meters = height_feet * 0.3048
        
        # Calculate BMI
        bmi = weight / (height_meters ** 2)
        bmi_rounded = round(bmi, 2)
        
        # Determine category
        if bmi < 18.5:
            category = "Underweight"
            color = "#3498db"  # Blue
        elif 18.5 <= bmi < 25:
            category = "Normal Weight"
            color = "#2ecc71"  # Green
        elif 25 <= bmi < 30:
            category = "Overweight"
            color = "#f39c12"  # Orange
        else:
            category = "Obesity"
            color = "#e74c3c"  # Red
        
        # Update result label
        result_text = f"BMI: {bmi_rounded}\nCategory: {category}"
        result_label.config(text=result_text, fg=color)
        
        # Update gauge
        update_gauge(bmi)
        
    except ValueError as e:
        messagebox.showerror("Error", str(e) if str(e) else "Please enter valid numbers for weight and height")

def update_gauge(bmi):
    # Clear previous gauge
    for widget in gauge_frame.winfo_children():
        widget.destroy()
    
    # Create figure for gauge
    fig = plt.Figure(figsize=(5, 3), dpi=80)
    ax = fig.add_subplot(111, polar=True)
    
    # Gauge parameters
    max_bmi = 40
    categories = ["Underweight", "Normal", "Overweight", "Obesity"]
    colors = ["#3498db", "#2ecc71", "#f39c12", "#e74c3c"]
    
    # Create gauge segments
    segments = [18.5, 25, 30, max_bmi]
    start_angle = 90
    for i in range(len(segments)):
        end_angle = start_angle - (segments[i]/(max_bmi/180))
        if i == 0:
            prev_segment = 0
        else:
            prev_segment = segments[i-1]
        
        # Draw colored arcs
        ax.barh(1, (segments[i]-prev_segment)*np.pi/180, 
                left=(start_angle + prev_segment/(max_bmi/180))*np.pi/180, 
                color=colors[i])
    
    # Add needle for current BMI
    needle_angle = 90 - (bmi/(max_bmi/180))
    ax.plot([needle_angle*np.pi/180, (needle_angle+180)*np.pi/180], [0, 1], color='black', linewidth=2)
    ax.plot(needle_angle*np.pi/180, 1, color='red', marker='o', markersize=10)
    
    # Customize gauge appearance
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 1.5)
    ax.axis('off')
    
    # Add category labels
    label_angles = [90 - ((segments[i]+segments[i-1])/2)/(max_bmi/180) for i in range(1, len(segments))]
    for i, (angle, label) in enumerate(zip(label_angles, categories)):
        ax.text(angle*np.pi/180, 1.3, label, ha='center', va='center', 
               fontsize=9, color=colors[i])
    
    # Add BMI value at center
    ax.text(0, 0, f"{bmi:.1f}", ha='center', va='center', 
           fontsize=14, fontweight='bold')
    
    # Embed gauge in tkinter
    canvas = FigureCanvasTkAgg(fig, master=gauge_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Create main window
root = tk.Tk()
root.title("Advanced BMI Calculator")
root.geometry("600x500")
root.resizable(False, False)

# Set theme colors
bg_color = "#f5f5f5"
root.configure(bg=bg_color)

# Create and place widgets
header_frame = tk.Frame(root, bg="#3498db", padx=10, pady=10)
header_frame.pack(fill=tk.X)
tk.Label(header_frame, text="Advanced BMI Calculator", 
         font=("Arial", 18, "bold"), bg="#3498db", fg="white").pack()

# Input frame
input_frame = tk.Frame(root, bg=bg_color, padx=20, pady=20)
input_frame.pack()

# Weight input
weight_frame = tk.Frame(input_frame, bg=bg_color)
weight_frame.pack(pady=10, fill=tk.X)
tk.Label(weight_frame, text="Weight (kg):", font=("Arial", 12), bg=bg_color).pack(side=tk.LEFT)
weight_entry = ttk.Entry(weight_frame, font=("Arial", 12), width=10)
weight_entry.pack(side=tk.LEFT, padx=10)

# Height input
height_frame = tk.Frame(input_frame, bg=bg_color)
height_frame.pack(pady=10, fill=tk.X)
tk.Label(height_frame, text="Height (feet):", font=("Arial", 12), bg=bg_color).pack(side=tk.LEFT)
height_entry = ttk.Entry(height_frame, font=("Arial", 12), width=10)
height_entry.pack(side=tk.LEFT, padx=10)

# Calculate button
button_frame = tk.Frame(root, bg=bg_color)
button_frame.pack(pady=10)
calculate_btn = tk.Button(button_frame, text="Calculate BMI", font=("Arial", 12, "bold"), 
                         command=calculate_bmi, bg="#3498db", fg="white", 
                         padx=20, pady=5, bd=0)
calculate_btn.pack()

# Result display
result_frame = tk.Frame(root, bg=bg_color)
result_frame.pack(pady=10)
result_label = tk.Label(result_frame, text="", font=("Arial", 14, "bold"), 
                       bg=bg_color, pady=10)
result_label.pack()

# Gauge frame
gauge_frame = tk.Frame(root, bg=bg_color, padx=10, pady=10)
gauge_frame.pack(fill=tk.BOTH, expand=True)

# Run the application
root.mainloop()