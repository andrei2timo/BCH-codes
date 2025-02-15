import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
from arithmetic import BCHGenerator, bch_syndrome_generator, signedMod, modular_inverse, arithmetic_sqr_root

# Global variable to hold the processed data after import
json_processed_data = []

# Function to handle the generator button click
def generate_check_digits():
    input_data = input_entry.get()
    
    # Split input data by commas and strip any extra whitespace
    segments = [segment.strip() for segment in input_data.split(',')]
    
    # Ensure we have exactly 12 segments and all are valid integers
    if len(segments) == 12 and all(segment.isdigit() for segment in segments):
        # Convert the segments into a list of integers
        input_array = [int(segment) for segment in segments]
        
        # Call the BCHGenerator function to calculate d13, d14, d15, d16
        generated_digits = BCHGenerator(input_array)
      
        # Check if the generated_digits length is exactly 16
        if len(generated_digits) == 16:
            # Validate all generated digits are within the valid range
            if all(0 <= digit < 17 for digit in generated_digits):
                # Convert the generated digits list to a string
                generated_digits_str = ', '.join(map(str, generated_digits))
                
                # Update the result generator field with the generated digits string
                result_generator_var.set(generated_digits_str)
                
                # Update the specific text boxes for d13, d14, d15, and d16
                d12_entry.config(state='normal')
                d12_entry.delete(0, 'end')
                d12_entry.insert(0, str(generated_digits[12]))
                d12_entry.config(state='readonly')

                d13_entry.config(state='normal')
                d13_entry.delete(0, 'end')
                d13_entry.insert(0, str(generated_digits[13]))
                d13_entry.config(state='readonly')

                d14_entry.config(state='normal')
                d14_entry.delete(0, 'end')
                d14_entry.insert(0, str(generated_digits[14]))
                d14_entry.config(state='readonly')

                d15_entry.config(state='normal')
                d15_entry.delete(0, 'end')
                d15_entry.insert(0, str(generated_digits[15]))
                d15_entry.config(state='readonly')

                # Display the generated last digits (d13 to d16)
                last_digits = f"{generated_digits[12]}, {generated_digits[13]}, {generated_digits[14]}, {generated_digits[15]}"
                last_digits_var.set(last_digits)
            else:
                result_generator_var.set("Error: Generated digits out of range.")
                last_digits_var.set("")
        else:
            result_generator_var.set("Error: Generated digits must be 16 digits long.")
            last_digits_var.set("")  # Clear the last digits field if there's an input error
    else:
        result_generator_var.set("Error: Input must be exactly 12 decimal digits separated by commas.")
        last_digits_var.set("")  # Clear the last digits field if there's an input error

# Function to handle the decode button click
def decode_input():
    # Retrieve the string from the result generator entry
    decoder_str = result_generator_entry.get().strip()
    
    # Convert the string to a list of integers
    try:
        decoder_str = decoder_str.replace(',', ' ')
        decoder_list = list(map(int, decoder_str.split()))
        
        if len(decoder_list) != 16:
            raise ValueError("Input must contain exactly 16 digits.")
        
        # Generate the BCH syndrome
        syndrome = bch_syndrome_generator(decoder_list)
        p = signedMod((syndrome[1] * syndrome[1]) - (syndrome[0] * syndrome[2]), 17)
        q = signedMod((syndrome[0] * syndrome[3]) - (syndrome[1] * syndrome[2]), 17)
        r = signedMod((syndrome[2] * syndrome[2]) - (syndrome[1] * syndrome[3]), 17)
        
        # Error correction logic
        if syndrome[0] == 0 and syndrome[1] == 0 and syndrome[2] == 0 and syndrome[3] == 0:
            after_correction_var.set("No error detected")
        elif p == 0 and q == 0 and r == 0:
            # One error detected
            error_magnitude = syndrome[0]
            error_position = modular_inverse(syndrome[1], syndrome[0], 17) - 1
            
            if error_position != -1:
                decoder_list[error_position] = signedMod(decoder_list[error_position] - error_magnitude, 17)
                digit_number_string = ''.join(map(str, decoder_list))
                after_correction_var.set(f"One error present. Corrected code: {digit_number_string}")
            else:
                after_correction_var.set("More than two errors have occurred for this test. ??")
        else:
            # Two errors detected
            quad = int(arithmetic_sqr_root(signedMod((q * q) - (4 * p * r), 17)))
            ii = modular_inverse(-q + quad, 2 * p, 17)
            j = modular_inverse(-q - quad, 2 * p, 17)
            
            b = modular_inverse(ii * syndrome[0] - syndrome[1], ii - j, 17)
            a = syndrome[0] - b
            
            if ii == 0 or j == 0 or quad == 0:
                after_correction_var.set("More than two errors have occurred. NO square root")
            else:
                decoder_list[ii - 1] = signedMod(decoder_list[ii - 1] - a, 17)
                decoder_list[j - 1] = signedMod(decoder_list[j - 1] - b, 17)

                digit_number_string = ''.join(map(str, decoder_list))
                after_correction_var.set(f"Two errors present. Corrected Code: {digit_number_string[:-1]}")
    
    except ValueError as e:
        result_generator_var.set(f"Error: {str(e)}")

# Function to import a JSON file with multiple 12-digit inputs
def import_json():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not file_path:
            return
        
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        if not isinstance(data, list):
            raise ValueError("JSON format is invalid. Expected a list of 12-digit inputs.")
        
        processed_data = []
        for input_data in data:
            if len(input_data) == 12 and all(isinstance(x, int) for x in input_data):
                generated_digits = BCHGenerator(input_data)
                if len(generated_digits) == 16:
                    processed_data.append(generated_digits)
                else:
                    processed_data.append(input_data + ["Error: Could not generate 4 digits"])
            else:
                processed_data.append(input_data + ["Error: Invalid 12-digit input"])
        
        global json_processed_data
        json_processed_data = processed_data
        messagebox.showinfo("Import Successful", "12-digit inputs successfully imported and processed.")
    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to import or process JSON: {str(e)}")

# Function to export the processed data to a JSON file
def export_json():
    try:
        if not json_processed_data:
            messagebox.showwarning("No Data", "No data available for export. Please import and process JSON first.")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not file_path:
            return
        
        with open(file_path, 'w') as file:
            json.dump(json_processed_data, file, indent=4)
        
        messagebox.showinfo("Export Successful", "Processed data successfully exported to JSON file.")
    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export JSON: {str(e)}")


# Initialize main application window
root = tk.Tk()
root.title("Error Checking Code Generator")
root.geometry("600x400")

# Input label and text box
tk.Label(root, text="Input (12 digits separated by commas):").grid(row=0, column=0, padx=10, pady=5)
input_entry = tk.Entry(root, width=50)
input_entry.grid(row=0, column=1, padx=10, pady=5)

# Labels and text boxes for displaying results
tk.Label(root, text="d13=").grid(row=1, column=0, padx=10, pady=5)
d12_entry = tk.Entry(root, state='readonly')
d12_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="d14=").grid(row=2, column=0, padx=10, pady=5)
d13_entry = tk.Entry(root, state='readonly')
d13_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="d15=").grid(row=3, column=0, padx=10, pady=5)
d14_entry = tk.Entry(root, state='readonly')
d14_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="d16=").grid(row=4, column=0, padx=10, pady=5)
d15_entry = tk.Entry(root, state='readonly')
d15_entry.grid(row=4, column=1, padx=10, pady=5)

# Generator and Decode buttons
generate_button = ttk.Button(root, text="Generate", command=generate_check_digits)
generate_button.grid(row=5, column=0, padx=10, pady=10)

decode_button = ttk.Button(root, text="Decode", command=decode_input)
decode_button.grid(row=5, column=1, padx=10, pady=10)

# Result after generating and decoding
tk.Label(root, text="Result Generator:").grid(row=6, column=0, padx=10, pady=5)
result_generator_var = tk.StringVar()
result_generator_entry = tk.Entry(root, textvariable=result_generator_var, width=50)
result_generator_entry.grid(row=6, column=1, padx=10, pady=5)

tk.Label(root, text="Full 16-Digit Code:").grid(row=7, column=0, padx=10, pady=5)
after_correction_var = tk.StringVar()
after_correction_entry = tk.Entry(root, textvariable=after_correction_var, width=50)
after_correction_entry.grid(row=7, column=1, padx=10, pady=5)

# New text field for displaying generated last digits (d13 to d16)
tk.Label(root, text="Check Digits:").grid(row=8, column=0, padx=10, pady=5)
last_digits_var = tk.StringVar()
last_digits_entry = tk.Entry(root, textvariable=last_digits_var, width=50)
last_digits_entry.grid(row=8, column=1, padx=10, pady=5)

# Import and Export buttons
import_button = ttk.Button(root, text="Import JSON", command=import_json)
import_button.grid(row=9, column=0, padx=10, pady=10)

export_button = ttk.Button(root, text="Export JSON", command=export_json)
export_button.grid(row=9, column=1, padx=10, pady=10)

# Run the main loop
root.mainloop()
