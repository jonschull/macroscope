import plotly.graph_objs as go
from plotly.offline import plot
import re

def makeFig(data, layout, filename='Scatt2.html'):
    # Build layout
    
    # Build Figure
    fig = go.Figure(
        data=data,
        layout=layout)

    # Get HTML representation of plotly.js and this figure
    plot_div = plot(fig, output_type='div', include_plotlyjs=True)

    # Get id of html div element that looks like
    # <div id="301d22ab-bfba-4621-8f5d-dc4fd855bb33" ... >
    res = re.search('<div id="([^"]*)"', plot_div)
    div_id = res.groups()[0]

    # Build JavaScript callback for handling clicks
    # and opening the URL in the trace's customdata          #_blank (below) should make it open in the same window. but not so.
    js_callback = """
    <script>
    var plot_element = document.getElementById("{div_id}");
    plot_element.on('plotly_click', function(data){{
        console.log(data);
        var point = data.points[0];
        if (point) {{
            console.log(point.customdata);
            window.open(point.customdata,'_blank');
        }}
    }})
    </script>
    """.format(div_id=div_id)

    # Build HTML string
    html_str = """
    <html>
    <body>
    {plot_div}
    {js_callback}
    </body>
    </html>
    """.format(plot_div=plot_div, js_callback=js_callback)

    # Write out HTML file
    if filename:
        with open(filename, 'w') as f:
            f.write(html_str)
        print('Exported', filename)

    return fig
    #!open Scatt2.html
    
if __name__=='__main__':

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=[0, 1, 2, 3, 4, 5, 6, 7, 8],
        y=[0, 1, 2, 3, 4, 5, 6, 7, 8],
        name="Name of Trace 1"       # this sets its legend entry
    ))


    fig.add_trace(go.Scatter(
        x=[0, 1, 2, 3, 4, 5, 6, 7, 8],
        y=[1, 0, 3, 2, 5, 4, 7, 6, 8],
        name="Name of Trace 2"
    ))

    fig.update_layout(
        title="Plot Title",
        xaxis_title="x Axis Title",
        yaxis_title="y Axis Title",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
            )
        )
    
    makeFig(fig,'test.html')
        