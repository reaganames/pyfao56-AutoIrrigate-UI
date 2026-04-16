import streamlit as st
import pandas as pd
import pyfao56 as fao
import datetime as dt
import os
from AdditionalGraphs import AdditionalGraphs
import plotly.io as pio
from streamlit_timeline import st_timeline



#The goal of this gui is to create a streamlit app that allows users to input all information needed
#for the AutoIrrigate file to run on the pyfao56 model. This will ultimately provide the output
#file of the model, primarily with a focus on irrigation amounts. 

pio.templates.default = "plotly_white"

# make the container wide
st.set_page_config(layout="wide")
#Creating title on streamlit app
st.title("AutoIrrigate GUI")

tab1, tab2 = st.tabs(['Test Cases', 'Custom Parameters'])

#Seperating and setting up the tabs 
with tab1:
    irrpath = "inputs/cotton2018_full.irr"
    halfirrpath = "inputs/cotton2018_half.irr"
    parpath = "inputs/cotton2018.par"
    wthpath = "inputs/cotton2018.wth"
    solpath = "inputs/cotton2018.sol"
    sol = fao.SoilProfile()
    sol.loadfile(solpath)
    irrfull = fao.Irrigation()
    irrfull.loadfile(irrpath)
    irrhalf = fao.Irrigation()
    irrhalf.loadfile(halfirrpath)
    par = fao.Parameters()
    par.loadfile(parpath)
    wth = fao.Weather()
    wth.loadfile(wthpath)
    airr = fao.AutoIrrigate()
    #Defining test cases based on AutoIrrigate class test cases defined in pyfao56 
    testoptions = {0:"Case 0: Actual irrigation record, No autoirrigation",
                   1:"Case 1: Minimal Autoirrigation Input Case",
                   2: "Case 2: Mixing half-season record and autoirrigation",
                   3: "Case 3: Full season autoirrigate with mad = 0.4",
                   4: "Case 4: Autoirrigate with mad = 0.4 only on Tuesday and Friday",
                   5: "Case 5: Autoirrigate with mad = 0.4, but cancel autoirrigation if 25 mm rain coming in the next three days",
                   6: "Case 6: Autoirrigate with mad = 0.4, but if 25 mm rain coming in the next three days, reduce irrigation by rain amount.",
                   7: "Case 7: Autoirrigate based on Dr, not fractional Dr.",
                   8: "Case 8: Fix problem with early season irrigation in Case 7.",
                   9: "Case 9: Autoirrigate when Ksend > 0.6.",
                   10: "Case 10: Autoirrigate every 6 days",
                   11: "Case 11: Autoirrigate every 4 days or sooner with mad=0.3",
                   12: "Case 12: Autoirrigate every 5 days after watering event > 14 mm",
                   13: "Case 13: Autoirrigate 20 mm fixed rate every 4 days",
                   14: "Case 14: Autoirrigate with mad=0.4 targeting 15 mm Dr deficit",
                   15: "Case 15: Autoirrigate with mad=0.4 targeting 0.1 fDr deficit",
                   16: "Case 16: Autoirrigate every 5 days with 5-day ET replacement less precipitation. Default ET is ETa.",
                   17: "Case 17: Autoirrigate with mad=0.4 and replace ET less precipitation since last irrigation event. Default ET is ETa.",
                   18: "Case 18: Autoirrigate with mad=0.4 and replace ET less precipitation since last watering event > 14 mm. Default ET is ETa.",
                   19: "Case 19: Autoirrigate every 5 days with 5-day ET replacement less precipitation. Use ETc instead of ETa.",
                   20: "Case 20: Autoirrigate with mad=0.45 and apply 90% of default rate",
                   21: "Case 21: Autoirrigate with mad=0.45 considering an application efficiency of 80%.",
                   22: "Case 22: Autoirrigate with mad=0.4 considering a minimum application rate of 12 mm.",
                   23: "Case 23: Autoirrigate with mad=0.4 considering a minimum application rate of 12 mm and maximum rate of 24 mm.",
                   24: "Case 24: Autoirrigate with mad=0.4 and specify fw for the irrigation method at 0.5",
                   25: "Case 25: Full season autoirrigate with mad = 0.3",
                   26: "Case 26: Full season autoirrigate with mad = 0.5",
                   27: "Case 27: Full season autoirrigate with mad = 0.6",
                   28: "Case 28: Full season autoirrigate with mad = 0.7",
                   29: "Case 29: Autoirrigate when Ksend > 0.5.",
                   30: "Case 30: Autoirrigate when Ksend > 0.7.",
                   31: "Case 31: Autoirrigate when Ksend > 0.8.",
                   32: "Case 32: Autoirrigate when Ksend > 0.9.",
                   33: "Case 33: Autoirrigate every 5 days with 5-day ETcm replacement less precipitation.",
                   34: "Case 34: Autoirrigate 10 mm fixed rate with mad=0.4",
                   35: "Case 35: Autoirrigate 20 mm fixed rate with mad=0.4",
                   36: "Case 36: Autoirrigate 30 mm fixed rate with mad=0.4",
                   37: "Case 37: Mixing half-season record and autoirrigation with mad=0.4",
                   38: "Case 38: Replicate actual 2018 irrigation management",
                   39: "Case 39: Practical example for Arizona cotton furrow irrigation",
                   40: "Case 40: Practical example for Arizona cotton sprinkler irrigation",
                   41: "Case 41: Practical example for Arizona cotton microirrigation"}
    #Adding a drop down menu to select test cases to run
    testcase = st.selectbox("Select a Test Case to Run", options=testoptions,format_func=lambda x: testoptions[x], key="testcase")
    
    #Storing the selected test case
    case = st.session_state.testcase
    
    #Case 0: Actual irrigation record, No autoirrigation
    if case==0:
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        irr=irrfull, K_adj=True)
    #Case 1: Minimal autoirrigation input case
    #        Autoirrigate targeting Dr=0 every day from start to end
    elif case==1:
        airr.addset('2018-108','2018-250')
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 2: Mixing half-season record and autoirrigation
    #        alre is 'True' by default
    #        Actual irrigation record for first half season
    #        Then autoirrigate targeting daily Dr=0 in last half season
    elif case==2:
        airr.addset('2018-108','2018-250')
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        irr=irrhalf, autoirr=airr, K_adj=True)
    #Case 3: Full season autoirrigate with mad = 0.4
    elif case==3:
        airr.addset('2018-108','2018-250',mad=0.4)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 4: Autoirrigate with mad = 0.4 only on Tuesday and Friday
    elif case==4:
        airr.addset('2018-108','2018-250',mad=0.4,idow='25')
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 5: Autoirrigate with mad = 0.4, but cancel autoirrigation
    #        if 25 mm rain coming in the next three days
    elif case==5:
        airr.addset('2018-108','2018-250',mad=0.4,fpdep=25.,fpday=3,
                    fpact='cancel')
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 6: Autoirrigate with mad = 0.4, but if 25 mm rain coming in
    #        the next three days, reduce irrigation by rain amount.
    elif case==6:
        airr.addset('2018-108','2018-250',mad=0.4,fpdep=25.,fpday=3,
                    fpact='reduce')
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 7: Autoirrigate based on Dr, not fractional Dr.
    #        Notice lack of irrigation until June when root zone
    #        increases enough to have 40 mm of storage.
    elif case==7:
        airr.addset('2018-108','2018-250',madDr=40.)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 8: Fix problem with early season irrigation in Case 7.
    elif case==8:
        airr.addset('2018-108','2018-120',madDr=10.)
        airr.addset('2018-121','2018-150',madDr=20.)
        airr.addset('2018-151','2018-250',madDr=40.)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 9: Autoirrigate when Ksend > 0.6.
    elif case==9:
        airr.addset('2018-108','2018-250',ksc=0.6)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 10: Autoirrigate every 6 days
    elif case==10:
        airr.addset('2018-108','2018-250',dsli=6)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 11: Autoirrigate every 4 days or sooner with mad=0.3
    #         Early season mad driven, Late season dsli driven
    elif case==11:
        airr.addset('2018-108','2018-250',dsli=4)
        airr.addset('2018-108','2018-250',mad=0.3)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 12: Autoirrigate every 5 days after watering event > 14 mm
    elif case==12:
        airr.addset('2018-108','2018-250',dsle=5,evnt=14.)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 13: Autoirrigate 20 mm fixed rate every 4 days
    elif case==13:
        airr.addset('2018-108','2018-250',dsli=4,icon=20.)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 14: Autoirrigate with mad=0.4 targeting 15 mm Dr deficit
    #         #Mostly nonsensible scheduling in the early season
    elif case==14:
        airr.addset('2018-108','2018-250',mad=0.4,itdr=15.)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 15: Autoirrigate with mad=0.4 targeting 0.1 fDr deficit
    #         Somewhat more sensible than Case 14.
    elif case==15:
        airr.addset('2018-108','2018-250',mad=0.4,itfdr=0.1)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 16: Autoirrigate every 5 days with 5-day ET replacement
    #         less precipitation. Default ET is ETa.
    elif case==16:
        airr.addset('2018-108','2018-250',dsli=5,ietrd=5,ettyp='ETa')
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 17: Autoirrigate with mad=0.4 and replace ET less
    #         precipitation since last irrigation event. Default ET is
    #         ETa.
    elif case==17:
        airr.addset('2018-108','2018-250',mad=0.4,ietri=True)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 18: Autoirrigate with mad=0.4 and replace ET less
    #         precipitation since last watering event > 14 mm.
    #         Default ET is ETa.
    elif case==18:
        airr.addset('2018-108','2018-250',mad=0.4,evnt=14.,ietre=True)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 19: Autoirrigate every 5 days with 5-day ET replacement
    #         less precipitation. Use ETc instead of ETa.
    elif case==19:
        airr.addset('2018-108','2018-250',dsli=5,ietrd=5,ettyp='ETc')
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 20: Autoirrigate with mad=0.45 and apply 90% of default rate
    elif case==20:
        airr.addset('2018-108','2018-250',mad=0.45,iper=90.)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 21: Autoirrigate with mad=0.45 considering an application
    #         efficiency of 80%.
    elif case==21:
        airr.addset('2018-108','2018-250',mad=0.45,ieff=80.)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 22: Autoirrigate with mad=0.4 considering a minimum
    #         application rate of 12 mm.
    elif case==22:
        airr.addset('2018-108','2018-250',mad=0.4,imin=12.)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 23: Autoirrigate with mad=0.4 considering a minimum
    #         application rate of 12 mm and maximum rate of 24 mm.
    elif case==23:
        airr.addset('2018-108','2018-250',mad=0.4,imin=12.,imax=24.)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 24: Autoirrigate with mad=0.4 and specify fw for the
    #         irrigation method at 0.5
    elif case==24:
        airr.addset('2018-108','2018-250',mad=0.4,fw=0.5)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)

    #Additional cases for the autoirrigation paper
    #Case 25: Full season autoirrigate with mad = 0.3
    elif case==25:
        airr.addset('2018-108','2018-250',mad=0.3)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 26: Full season autoirrigate with mad = 0.5
    elif case==26:
        airr.addset('2018-108','2018-250',mad=0.5)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 27: Full season autoirrigate with mad = 0.6
    elif case==27:
        airr.addset('2018-108','2018-250',mad=0.6)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 28: Full season autoirrigate with mad = 0.7
    elif case==28:
        airr.addset('2018-108','2018-250',mad=0.7)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 29: Autoirrigate when Ksend > 0.5.
    elif case==29:
        airr.addset('2018-108','2018-250',ksc=0.5)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 30: Autoirrigate when Ksend > 0.7.
    elif case==30:
        airr.addset('2018-108','2018-250',ksc=0.7)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 31: Autoirrigate when Ksend > 0.8.
    elif case==31:
        airr.addset('2018-108','2018-250',ksc=0.8)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 32: Autoirrigate when Ksend > 0.9.
    elif case==32:
        airr.addset('2018-108','2018-250',ksc=0.9)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 33: Autoirrigate every 5 days with 5-day ETcm replacement
    #         less precipitation.
    elif case==33:
        airr.addset('2018-108','2018-250',dsli=5,ietrd=5,ettyp='ETcm')
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 34: Autoirrigate 10 mm fixed rate with mad=0.4
    elif case==34:
        airr.addset('2018-108','2018-250',mad=0.4,icon=10.)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 35: Autoirrigate 20 mm fixed rate with mad=0.4
    elif case==35:
        airr.addset('2018-108','2018-250',mad=0.4,icon=20.)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 36: Autoirrigate 30 mm fixed rate with mad=0.4
    elif case==36:
        airr.addset('2018-108','2018-250',mad=0.4,icon=30.)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 37: Mixing half-season record and autoirrigation with mad=0.4
    #        alre is 'True' by default
    #        Actual irrigation record for first half season
    #        Then autoirrigate targeting daily Dr=0 in last half season
    elif case==37:
        airr.addset('2018-108','2018-250',mad=0.4)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        irr=irrhalf, autoirr=airr, K_adj=True)
    #Case 38: Replicate actual 2018 irrigation management
    elif case==38:
        airr.addset('2018-108','2018-118',idow='25' ,icon=20.4) #Emergence irrigation
        airr.addset('2018-127','2018-150',idow='3'  ,icon=20.4) #Establishment irrigation
        airr.addset('2018-155','2018-250',idow='34',mad=0.45,ietrd=4,imax=42)
        airr.addset('2018-155','2018-250',idow='45',mad=0.20,ietrd=3,imax=42)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 39: Practical example for Arizona cotton furrow irrigation
    elif case==39:
        airr.addset('2018-109','2018-109',icon=50.,fw=0.6)
        airr.addset('2018-119','2018-150',dsli=20,icon=50.,fw=0.6)
        airr.addset('2018-151','2018-250',mad=0.50,fpdep=25.,fpday=3,
                    fpact='cancel',imin=50.,fw=0.6)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 40: Practical example for Arizona cotton sprinkler irrigation
    elif case==40:
        airr.addset('2018-108','2018-129',dsli=4,icon=20.)
        airr.addset('2018-130','2018-250',mad=0.40,dsli=3,fpdep=25.,fpday=3,
                    fpact='reduce',imin=5.,imax=30.)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Case 41: Practical example for Arizona cotton microirrigation
    elif case==41:
        airr.addset('2018-108','2018-129',dsli=4,icon=15.,fw=0.3)
        airr.addset('2018-130','2018-150',idow='25',fpdep=25.,fpday=3,
                    fpact='reduce',icon=10.,fw=0.3)
        airr.addset('2018-151','2018-171',idow='25',fpdep=25.,fpday=3,
                    fpact='reduce',icon=20.,fw=0.3)
        airr.addset('2018-172','2018-192',idow='135',fpdep=25.,fpday=3,
                    fpact='reduce',icon=25.,fw=0.3)
        airr.addset('2018-193','2018-228',idow='135',fpdep=25.,fpday=3,
                    fpact='reduce',icon=20.,fw=0.3)
        airr.addset('2018-229','2018-250',idow='25',fpdep=25.,fpday=3,
                    fpact='reduce',icon=20.,fw=0.3)
        mdl = fao.Model('2018-108','2018-303', par, wth, sol=sol,
                        autoirr=airr, K_adj=True)
    #Adding a button to run the selected test case and display results
    st.button("Run Test Case", key="run_test_case")
    if st.session_state.run_test_case:
        #Writting the autoirrigate file based on selected test case
        st.write(airr)
        #Running the model by referencing the autoirrigate file
        mdl.run()
        mdl.savefile(os.path.join('outputs', f'cotton2018_{case}.out'))
        #Referencing the AdditionalGraphs class to create a Dr plot for the selected test case and save it as an html file in the outputs folder
        viz = AdditionalGraphs(mdl)
        htmlpath = os.path.join('outputs', f'cotton2018_{case}_Dr.html')
        fig = viz.plotly_Dr(title=f'Dr for Cotton 2018 Case {case}',filepath=htmlpath)
        fig.update_layout(template='plotly_white',height=600) 
        st.plotly_chart(fig, theme=None, use_container_width=True)
        print("Model run complete. Output file and Dr plot saved.")
        st.balloons()


# Tab 2: Custom Parameters
with tab2:
    
    #Date Select
    st.date_input("Select Model Start Date", key="start",value=pd.to_datetime("2018-108", format="%Y-%j"))
    st.date_input("Select Model End Date", key="end", value=pd.to_datetime("2018-302", format="%Y-%j"))
    #Adding toggle for date selection (if user wants to specify a custom date range for autoirrigation scheduling)
    different_dates = st.toggle ("Use a different date range for AutoIrrigation scheduling (rather than model range)", key="different_dates")
    if different_dates:
        st.date_input("Select AutoIrrigation Start Date", key="airr_start",value=pd.to_datetime("2018-108", format="%Y-%j"))
        st.date_input("Select AutoIrrigation End Date", key="airr_end", value=pd.to_datetime("2018-302", format="%Y-%j"))
        airr_start = st.session_state.airr_start.strftime('%Y-%j')
        airr_end = st.session_state.airr_end.strftime('%Y-%j')
        airr_start_date = st.session_state.airr_start.strftime('%Y-%m-%d')
        airr_end_date = st.session_state.airr_end.strftime('%Y-%m-%d')
    #Storing date inputs
    mdl_start_date = st.session_state.start.strftime('%Y-%m-%d')
    mdl_end_date = st.session_state.end.strftime('%Y-%m-%d')
    mdl_start = st.session_state.start.strftime('%Y-%j')
    mdl_end = st.session_state.end.strftime('%Y-%j')
    

    #Creating a dropdown for timeline parameters/options
    with st.expander("Timeline Options"):
        Lini = st.number_input("Length of Lini Stage (days)", min_value=0, value=35, key="Lini")
        Ldev = st.number_input("Length of Ldev Stage (days)", min_value=0, value=50, key="Ldev")
        Lmid = st.number_input("Length of Lmid Stage (days)", min_value=0, value=46, key="Lmid")
        Lend = st.number_input("Length of Lend Stage (days)", min_value=0, value=39, key="Lend")
    #Creating a default timeline with the growing season stages to visualize autoirrigation scheduling
    Lini_start = mdl_start_date
    Lini_Ldev = pd.to_datetime(mdl_start_date) + (pd.Timedelta(days=Lini))
    Ldev_Lmid = pd.to_datetime(mdl_start_date) + (pd.Timedelta(days=(Lini+Ldev)))
    Lmid_Lend = pd.to_datetime(mdl_start_date) + (pd.Timedelta(days=(Lini+Ldev+Lmid)))
    Lend_end = pd.to_datetime(mdl_start_date) + (pd.Timedelta(days=(Lini+Ldev+Lmid+Lend)))
    print(Lini_start, Lini_Ldev, Ldev_Lmid, Lmid_Lend, Lend_end)

    #Adding background colors for each growth stage defined above
    items = [{"id":1, "content":"Lini", "start": Lini_start, "end": dt.datetime.strftime(Lini_Ldev, '%Y-%m-%d'), "type": "background", "style": "background-color:#C7EDC7"},
            {"id":2, "content":"Ldev", "start": dt.datetime.strftime(Lini_Ldev, '%Y-%m-%d'), "end": dt.datetime.strftime(Ldev_Lmid, '%Y-%m-%d'), "type": "background"},
            {"id":3, "content":"Lmid", "start": dt.datetime.strftime(Ldev_Lmid, '%Y-%m-%d'), "end": dt.datetime.strftime(Lmid_Lend, '%Y-%m-%d'), "type": "background", "style": "background-color:#C7EDC7"},
            {"id":4, "content":"Lend", "start": dt.datetime.strftime(Lmid_Lend, '%Y-%m-%d'), "end": dt.datetime.strftime(Lend_end, '%Y-%m-%d'), "type": "background"},
            ]
    options = {"editable": True, "selectable": True, "stack": False}

    #Adding a button to update the timeline based on changes in date inputs or timeline options
    st.button("Update Timeline", key="update_timeline")
    if st.session_state.update_timeline:
        id = len(items) + 1
        if different_dates:
            items.append({"id":id, "content":"AutoIrr", "start":airr_start_date, "end":airr_end_date,"selectable":True, "type": "range", "style": "color:blue"})
        else:
            items.append({"id":id, "content":"AutoIrr", "start": mdl_start_date, "end": mdl_end_date,"selectable":True, "type": "range", "style": "color:blue"})
        
    timeline = st_timeline(items, groups = [], options=options, height="150px")
    

    #Irrigation Parameters Bin
    idow_options = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    dow = st.multiselect("Select Irrigation Days of the Week", options=idow_options, default=['Tuesday','Friday'], key="dow")
    idow = []
    for day in dow:
        if day == 'Sunday':
            idow.append(0)
        elif day == 'Monday':
            idow.append(1)
        elif day == 'Tuesday':
            idow.append(2)
        elif day == 'Wednesday':
            idow.append(3)
        elif day == 'Thursday':
            idow.append(4)
        elif day == 'Friday':
            idow.append(5)
        elif day == 'Saturday':
            idow.append(6)
    idow.sort()
    idow = ''.join(map(str, idow))

    with st.expander("Irrigation Parameters"):
        imin = st.number_input("Minimum Irrigation Amount (mm)", min_value=0.0, value=0.00, key="imin")
        imax = st.number_input("Maximum Irrigation Amount (mm)", min_value=0.0, value=None, key="imax")
        if imax == None:
            imax = 'NaN'
        icon = st.number_input("Apply Fixed Irrigation Amount (mm)",value=None, key="icon")
        if icon == None:
            icon = 'NaN'
        iper = st.number_input("Adjust Irrigation by a Percentage (%)",value=100.0, key="iper")
        ieff = st.number_input("Irrigation Efficiency (%)", min_value=0.0, max_value=100.0, value=100.0, key="ieff")

    #Forecasting Parameters Bin
    with st.expander("Forecasting Parameters"):
        fpday = st.number_input("Number of Days to Consider in Forecast", min_value=1, value=3, key="fpday")
        fpdep = st.number_input("Threshold for Forecast Depth (mm)", min_value=0.0, value=25.0, key="fpdep")
        fpact = st.selectbox("Forecast Action if Threshold Exceeded", options=
                            ['Proceed with Irrigation','Cancel Irrigation','Reduce Irrigation'], index=0, key="fpact")
        if fpact == 'Proceed with Irrigation':
            fpact = 'proceed'
        elif fpact == 'Cancel Irrigation':
            fpact = 'cancel'
        elif fpact == 'Reduce Irrigation':
            fpact = 'reduce'
        st.markdown("The following parameters do not use a forecast, and look at the previous days to trigger irrigation.")
        dsli = st.number_input("Automatically Irrigate if Days Since Last Irrigation Event Exceeded", min_value=0, value = None, key="dsli")
        dsle = st.number_input("Automatically Irrigate if Days Since Last Watering Event Exceeded", min_value=0, value = None, key="dsle")
        if dsli == None:
            dsli = 'NaN'
        if dsle == None:
            dsle = 'NaN'
        evnt = st.number_input("Depth of Precipitation to be Considered a Watering Event (mm)", min_value=0.0, value=10.0, key="evnt")

    #Management Criteria Bin
    with st.expander("Management Criteria"):
        ksc= st.number_input("Critical Value for Water Stress Coefficient (Ks)", min_value=0.0, value = None, max_value=1.0, key="ksc")
        if ksc == None:
            ksc = 'NaN'
        fractional = st.toggle("Use Fractional Management Criteria",  key="fractional")
        if fractional:
            mad = 'NaN'
            itdr = 'NaN'
            madDr = st.number_input("Management Allowed Depletion (%)", min_value=0.0, max_value=100.0, key="madDr")
            itfdr = st.number_input("Target Fractional Depletion After Irrigation (%)", min_value=0.0, max_value=100.0, key="itfdr")
        else:
            madDr = 'NaN'
            itfdr = 'NaN'
            mad = st.number_input("Management Allowed Depletion (mm)", value = None, key="mad")
            itdr = st.number_input("Target Depletion After Irrigation (mm)", value = None, key="itdr")
            
            if mad == None:
                mad = 'NaN'
            else:
                mad = mad/100
            if itdr == None:
                itdr = 'NaN'
            else:
                itdr = itdr/100
            

    #ET Parameters Bin
    with st.expander("Irrigation Based on ET Parameters"):
        ettyp = st.selectbox("Type of ET to Base Irrigation From", options= ['ETa','ETcm','ETc'], key="ettyp"), 
        st.markdown("The following parameters adjust the ET value used to determine irrigation amounts.")
        etadj = st.selectbox("Watering Type to Subtract from ET", 
                            options = ['No Adjustment',
                                        'ietrd: Effective Precipitation in the Past Number of Days',
                                        'ietri: Effective Precipitation Since Last Irrigation Event',
                                        'ietre: Effective Precipitation Since Last Watering Event'], index=0, key="etadj")
        if etadj == 'ietrd: Effective Precipitation in the Past Number of Days':
            ietrd = st.number_input("Number of Days to Consider for Effective Precipitation", min_value=1, key="etadjp")
        else:
            ietrd = 'NaN'
        if etadj == 'ietri:Effective Precipitation Since Last Irrigation Event':
            ietri = True
        else:
            ietri = False
        if etadj == 'ietre: Effective Precipitation Since Last Watering Event':
            ietre = True
        else:
            ietre = False
    st.select_slider("Use an existing Irrigation File?", options=["No", "Yes - Half Season", "Yes- Full Season"], key="use_irr_file")

    #AutoIrrigate Button and File Save
    if 'airr' not in st.session_state:
        st.session_state.airr = fao.AutoIrrigate()
    if st.button("Run AutoIrrigate for Parameters"):      
        if different_dates: 
            st.session_state.airr.addset(start=airr_start,end=airr_end,idow=idow,fpdep=fpdep,fpday=fpday,fpact=fpact,dsli=dsli,dsle=dsle,evnt=evnt,icon=icon,
                    imin=imin,imax=imax,iper=iper,ieff=ieff,ksc=ksc,mad=mad,itdr=itdr,madDr=madDr,itfdr=itfdr,
                    ettyp=ettyp[0],ietrd=ietrd,ietri=ietri,ietre=ietre)
        else:
            st.session_state.airr.addset(start=mdl_start,end=mdl_end,idow=idow,fpdep=fpdep,fpday=fpday,fpact=fpact,dsli=dsli,dsle=dsle,evnt=evnt,icon=icon,
                    imin=imin,imax=imax,iper=iper,ieff=ieff,ksc=ksc,mad=mad,itdr=itdr,madDr=madDr,itfdr=itfdr,
                    ettyp=ettyp[0],ietrd=ietrd,ietri=ietri,ietre=ietre)
        print("AutoIrrigate parameters set.")
        st.write(st.session_state.airr)
    if st.button("Save AutoIrrigate File"):
        st.session_state.airr.savefile(os.path.join('inputs', f'cotton2018.ati'))
        # Clear the session state after saving the file
        st.session_state.airr = fao.AutoIrrigate()
        print("AutoIrrigate file created and saved.")
        st.write("AutoIrrigate file created and saved.")

    if st.button("Run Model"):
        solpath = "inputs/cotton2018.sol"
        irrpath = "inputs/cotton2018_full.irr"
        halfirrpath = "inputs/cotton2018_half.irr"
        parpath = "inputs/cotton2018.par"
        atipath = "inputs/cotton2018.ati"
        wthpath = "inputs/cotton2018.wth"
        irr = fao.Irrigation()
        sol = fao.SoilProfile()
        sol.loadfile(solpath)
        par = fao.Parameters()
        par.loadfile(parpath)
        airr = fao.AutoIrrigate()
        airr.loadfile(atipath)
        wth = fao.Weather()
        wth.loadfile(wthpath)

        if st.session_state.use_irr_file == "Yes - Half Season":
            irr.loadfile(halfirrpath)
            mdl = fao.Model(start=mdl_start,end=mdl_end, par=par, wth=wth, autoirr=airr, irr=irr, sol=sol)
        elif st.session_state.use_irr_file == "Yes- Full Season":
            irr.loadfile(irrpath)
            mdl = fao.Model(start=mdl_start,end=mdl_end, par=par, wth=wth, autoirr=airr, irr=irr, sol=sol)
        else:
            mdl = fao.Model(start=mdl_start,end=mdl_end, par=par, wth=wth, autoirr=airr, sol=sol)

        mdl.run()
        mdl.savefile(os.path.join('outputs', 'cotton2018.out'))
        viz = AdditionalGraphs(mdl)
        htmlpath = os.path.join('outputs', f'cotton2018_Dr.html')
        fig = viz.plotly_Dr(title=f'Dr for Cotton 2018',filepath=htmlpath)
        fig.update_layout(template='plotly_white',height=600) 
        st.plotly_chart(fig, theme=None, use_container_width=True)
        print("Model run complete. Output file and Dr plot saved.")
        st.balloons()

