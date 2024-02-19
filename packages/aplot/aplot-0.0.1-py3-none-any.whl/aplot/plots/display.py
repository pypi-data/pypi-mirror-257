import typing as _t

import matplotlib.pyplot as plt


def display_limits(fig: plt.Figure):
    axes: _t.List[plt.Axes] = fig.get_axes()

    import ipywidgets as widgets
    from IPython.display import display

    zoom_text = widgets.Text(
        description="Zoom Size:",
        disabled=True,
        layout=widgets.Layout(width="700px"),
    )

    display(zoom_text)

    def update_zoom_text(ax: plt.Axes):
        x_min, x_max = ax.get_xlim()
        y_min, y_max = ax.get_ylim()

        zoom_text.value = (
            f"X: ({(x_max+x_min)/2:.3f}, {x_max-x_min:.3f}),"
            f"Y: ({(y_max+y_min)/2:.3f}, {y_max-y_min:.3f})"
        )

    # Event handlers for changes in axis limits
    def on_xlims_change(event_ax):
        update_zoom_text(event_ax)

    def on_ylims_change(event_ax):
        update_zoom_text(event_ax)

    # Connect the event handlers
    for ax in axes:
        ax.callbacks.connect("xlim_changed", on_xlims_change)
        ax.callbacks.connect("ylim_changed", on_ylims_change)
