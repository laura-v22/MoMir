def id_factory(page: str):
    def func(_id: str):
        """
        Utility function to be able to use the same id
        for components in different pages. It simply prepends the page name to the id.

        **EXAMPLE**
        # setup
        from utils.utils import id_factory
        id = id_factory('page1')

        # layout
        layout = html.Div(
            id=id('main-div')
        )

        # callback
        @app.callback(
            Output(id('main-div'), 'children'),
            Input(id('text-box'), 'value')
        )
        def function(...):
            ...
        """
        return f"{page}-{_id}"
    return func


def reformatPlot(fig, size=None, secondary=False):
    """
    Updates the layout of all subplots.
    """
    if size != None:
        fig.update_layout(height=size[1], width=size[0])

    fig.update_xaxes(
        showline = True,
        mirror = 'ticks',
        linewidth = 2,
        ticks = 'inside',
        ticklen = 8,
        tickwidth = 2,
        showgrid = True,
        title_font_size=16,
        tickfont_size=16,
    )
    fig.update_yaxes(
        showline = True,
        mirror = 'ticks',
        linewidth = 2,
        ticks = 'inside',
        ticklen = 8,
        tickwidth = 2,
        showgrid = True,
        title_font_size=16,
        tickfont_size=16,
    )

    if secondary:
        fig.update_layout(
                yaxis2=dict(
                title_font_size=16,
                tickfont_size=16,
                showgrid=False,
                showline=True,
                linewidth=2,
                ticks='inside',
                ticklen=8,
                tickwidth=2,
                title_font_color='gray',
                tickcolor='lightgray',
                tickfont_color='gray'
            ),
            yaxis_mirror=False
        )

    return fig


# common config properties of dcc.Graph() or go.Fig(),
# mainly to allow downloading svg images.
svg_config = {
    'toImageButtonOptions': {
        'format': 'png',
        'scale': 4,
    },
    'displaylogo': False,
    'editable': True,
}
