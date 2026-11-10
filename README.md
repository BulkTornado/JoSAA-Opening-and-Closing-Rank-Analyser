# JoSAA-Opening-and-Closing-Rank-Analyser

This repository contains the JoSAA Opening and Closing Rank data from the year 2025(rounds 1 to 6) and 2026(rounds 1 to 5) in csv files.

A python script(located in the `src` directory) parses through all of the csv files, collects all of the data from them, and compiles and saves it into a sqlite database.

The `main.py` currently contains boilerplate code to query the database for the total number of rows, i.e. data, and displays it in a tabular format.

This project stands incomplete except for the result parsing script.
