# BCH (16,12) Error Correction Code

## Overview

This project implements BCH (16,12) error correction encoding and decoding using Python and Tkinter. The BCH(16,12) code is designed to detect and correct errors in 16-digit encoded sequences, which are derived from 12-digit input data.

## Mathematical Background

### Vandermonde Matrix and Operations

The Vandermonde Matrix is essential in constructing the generator matrix for BCH(16,12) codes. Below is an example of the Vandermonde matrix used in this implementation:

![Vandermonde Matrix](images/vandermonde_matrix.png)

The operations performed on this matrix to generate the **Parity Check Matrix** involve several steps of matrix transformations, which are necessary for detecting and correcting errors in the encoded sequences.

#### Operations

1. **Step 1**: Apply the first transformation to the Vandermonde matrix.  
   ![First Operation](images/first_operation.png)

2. **Step 2**: Perform the second transformation to create the Parity Check Matrix.  
   ![Parity Check Matrix](images/parity_check_matrix.png)

The resulting **Parity Check Matrix** is used in the error detection and correction process.

### Syndrome Computation

The syndrome computation helps in determining the presence and location of errors by applying modular arithmetic to the Parity Check Matrix.


## Features

- **BCH Generator**: Computes check digits for a given 12-digit input.
- **Error Detection & Correction**: Uses syndrome calculations to detect and correct up to two errors in the encoded sequence.
- **Hexadecimal Support**: Accepts hexadecimal inputs (e.g., A, B, C for values 10, 11, 12) and outputs check digits in hexadecimal format (e.g., D, E, F).
- **JSON Import/Export**: Supports batch processing by importing and exporting multiple input sequences using JSON format.
- **Graphical User Interface (GUI)**: Built with Tkinter to provide an easy-to-use interface for users.

## Implementation Details

The implementation follows these key mathematical concepts:

- **Vandermonde Matrix**: Used in constructing the generator matrix.
- **Syndrome Computation**: Determines the presence and location of errors.
- **Modular Arithmetic**: Used for performing error correction calculations.

## Example Input & Output

### Encoding Example

**Input**: 1, 2, 3, 4, 5, 6, 7, 8, 9, A, B, C  
**Generated Check Digits**: D, E, F, G

### Decoding Example

**Input**: 1, 2, 3, 4, 5, 6, 7, 8, 9, A, B, C, D, E, F, G  
**Error Correction**: If an error is detected, it will be corrected and displayed.

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/bch-16-12.git
   cd bch-16-12

2. Install dependencies:

   ```bash
   pip install tkinter json

3. Run the application:

   ```bash
   python BCH.py

## Usage

- **Input**: Enter a 12-digit sequence using numbers (0-9) and letters (A-C).
- **Generate**: Click **Generate** to compute the check digits.
- **Decode**: Click **Decode** to validate and correct errors in a 16-digit encoded input.
- **Import JSON**: Use this option to process multiple input sequences from a JSON file.
- **Export JSON**: Save the processed data to a JSON file.

## References

- **Mathematical Background**: Vandermonde Matrices and BCH Code Theory.
- **Implementation Details**: Based on matrix transformations and modular arithmetic.

## License

This project is licensed under the MIT License.
