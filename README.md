# pyfao56-AutoIrrigate-UI
A user interface created to visualize and customize a pyfao56 AutoIrrigate class. 
The purpose of this repository is to aid the decision-making process for designing an AutoIrrigate Class for the pyfao56 Python Package. 

# Key Features:
 
# Required Python packages:
pyfao56
 
 
# Usage Instructions:

Once downloaded, running the streamlit file as a locally hosted web browser requires specific text in the terminal. Additionally, streamlit must be installed to access the app. 

Installation:
If streamlit is not installed, type the following into the terminal

    pip install streamlit

App Launch:
To access the app, type the following into the terminal

    python -m streamlit run "{filepath}"

After the app is running, there are several different capabilities to demonstrate the functionality of the AutoIrrigate tool. There are two distinct tabs in the app, which act to seperate pre-set from customizable parameters. The "Test Case" tab only requires the user to choose a test case predefined in the pyfao56 AutoIrrigate Class using cotton data from a 2018 study. For more customized use, the "Custom Parameters" tab can be selected. 

Custom Parameters:
While this tab, like the "Test Cases" tab is set to reference input files from a 2018 cotton study, the capabilities are much more flexible. Here, the model start and end dates must first be selected using the date selecter tool or by manually inputing the date. These are the dates used to run the model. In some cases, it may be desired for the AutoIrrigate defined irrigation amounts and scheduling to be used for only part of the season. In this case, the user should select the toggle switch labled "Use different date range for AutoIrrigation scheduling." This will allow the user to control the range of dates used for AutoIrrigate to run and manage their ideal output. The model run date select boxes are the only required user input for running the interface. The timeline, shown directly below this function, is a visualization tool for understanding when the AutoIrrigation scheduling will "take over" the model run. The growth stages used here can be altered in the "Timeline Options" collapseable bar. From here, the other inputs are based on user needs, and directly represent variables used in the AutoIrrigate class. 





