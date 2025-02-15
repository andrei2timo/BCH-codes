# BCH (16,12) Error Correction Code

## Overview

This project implements BCH (16,12) error correction encoding and decoding using Python and Tkinter. The BCH(16,12) code is designed to detect and correct errors in 16-digit encoded sequences, which are derived from 12-digit input data.

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
