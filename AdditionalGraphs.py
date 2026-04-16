"""
########################################################################
The AdditionalGraphs.py module contains the AdditionalGraphs class, 
which provides tools for visualizing pyfao56 Model output.

The AdditionalGraphs.py module contains the following:
    AdditionalGraphs - A child class to add more graphs to pyFAO-56

########################################################################
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pyfao56.tools import  Visualization
class AdditionalGraphs (Visualization):
    """
    A class for visualizing pyfao56 Model output with measurements.
    
    Attributes
    ----------
    mdl : pyfao56 Model class
        Provides the simulated data

    """
    def __init__(self, mdl):
        super().__init__(mdl)
        self.mdl = mdl

        # Remove duplicate columns in mdl.odata
        self.vdata = mdl.odata.T.drop_duplicates().T
        
        #Set zero rain and irrigation to NaN
        NaN = float('NaN')
        self.vdata['Rain'].replace(0.0,NaN,inplace=True)
        self.vdata['Irrig'].replace(0.0,NaN,inplace=True)
     
    def plotly_Dr(self, title='',filepath=None):
        """Plot soil water depletion (Dr) and related water data.

        Parameters
        ----------
        title : str
            Specify the title as the provided string
            (default = '')
        
        """
        print("Generating Dr plot...")
        print()

        subrow1 = 1
        subrow2 = 3
        subrow3 = 11
        subrowend=subrow3
        specs=[
            [{"rowspan":2}],
            [None],
            [{"rowspan":8}],
            [None],
            [None],
            [None],
            [None],
            [None],
            [None],
            [None],
            [{"rowspan":2}],
            [None]
        ]
        fig= make_subplots(rows=12,
                cols=1,
                shared_xaxes=True,
                specs=specs,
                vertical_spacing=0.02)
        
        #Prepare the data for plotting
        d = self.vdata
        d=d.rename_axis('Year-DOY').reset_index()
        d['DOY'] = d['Year-DOY'].str.split('-').str[1].astype(int)
        x = d['DOY']
        y = d['Ks']

        #Create the Ks plot
        trace = go.Scatter(x=x,
                        y=y,
                        line_color='lightsalmon',
                        name='Simlulated Ks',
                        hovertemplate = 
                                    'DOY: %{x}<br>' +
                                    'Ks: %{y}<extra></extra>')
        fig.append_trace(trace, row=subrow1, col=1)
            
        #Create the DP plot
        trace = go.Scatter(mode='markers',
                                    x=x,
                                    y=d['DP'],
                                    marker_color='crimson',
                                    marker_symbol='triangle-up',
                                    marker_size=10, 
                                    name='Deep Percolation (DP)',
                                    hovertemplate = 
                                    'DOY: %{x}<br>' +
                                    'Depth(mm): %{y}<extra></extra>')
        fig.append_trace(trace, row=subrow3, col=1)
          
        #Create the main plot
        trace = go.Scatter(x=x,
                            y=d['Dr'],
                            line_color='darkblue',
                            name='Simulated Root Zone Depletion',
                            hovertemplate = 
                                     'DOY: %{x}<br>' +
                                     'Depth(mm): %{y}<extra></extra>')
        fig.append_trace(trace, row=subrow2, col=1)
        
        #Add the Drmax trace
        trace = go.Scatter(x=x,
                            y=d['Drmax'],
                            line_color='deepskyblue',
                            name='Simulated Max Root Zone Depletion',
                            hovertemplate = 
                                    'DOY: %{x}<br>' +
                                    'Depth(mm): %{y}<extra></extra>')
        fig.append_trace(trace, row=subrow2, col=1)
        
        #Add the RAW trace
        trace = go.Scatter(x=x,
                                    y=d['RAW'], 
                                    line_color='mediumorchid',
                                    name='Readily Available Water (RAW)',
                                    hovertemplate = 
                                    'DOY: %{x}<br>' +
                                    'Depth(mm): %{y}<extra></extra>')
        fig.append_trace(trace, row=subrow2, col=1)
        
            
        #Add scatter traces for rain and irrigation events
        trace= go.Scatter(
            x=x,
            y=d['Rain'],
            mode="markers",
            name="Rain",
            marker_symbol="cross-thin",
            marker_size=10,
            marker_line_color="navy",
            marker_line_width=1,
            hovertemplate = 
                'DOY: %{x}<br>' +
                'Amount(mm): %{y}<extra></extra>'
        )
        fig.append_trace(trace, row=subrow2, col=1)
        trace=go.Scatter(
            x=x,
            y=d['Irrig'],
            mode="markers",
            name="Irrigation",
            marker_symbol="x-thin",
            marker_size=10,
            marker_line_color="navy",
            marker_line_width=1,
            hovertemplate = 
                'DOY: %{x}<br>' +
                'Amount(mm): %{y}<extra></extra>'
        )
        fig.append_trace(trace, row=subrow2, col=1)
        
        # Set plot layout
        fig.update_yaxes(title="Ks", row=subrow1, col=1)
        fig.update_yaxes(title="DP(mm)", range=[20,1],  row=subrow3, col=1)
        
        fig.update_yaxes(title="Depth(mm)", row=subrow2, col=1)
        fig.update_xaxes(title='Day of Year(DOY)', row=subrowend, col=1)
        fig.update_layout(title={
                          'text':title,
                          'x':0.5,
                          'xanchor': 'center'},
                          title_font=dict(size=30))
        if filepath:
            fig.write_html(filepath)

        return fig   
