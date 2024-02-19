from ..code_utils import LabelDict

colors = [
    "#0066cc",
    "#ffcc00",
    "#ff7400",
    "#962fbf",
    "#8b5a2b",
    "#d62976",
    "#b8a7ea",
    "#ed5555",
    "#1da2d8",
]
DATA = LabelDict(
    {
        "markerfacecolor": "none",
        "markeredgecolor": colors[0],
        "marker": "h",
        "linestyle": "none",
    }
)
FIT = LabelDict({"color": colors[1], "linewidth": 2, "label": "fit"})
GUESS = LabelDict({"color": colors[2], "linewidth": 2, "label": "guess", "alpha": 0.6})


VOLT_TIME = LabelDict(
    {
        "xlabel": "Voltage, V",
        "ylabel": "Time, $\mu$s",
    }
)
IQquadrature = LabelDict(
    {
        "xlabel": "I quadrature",
        "ylabel": "Q quadrature",
        "aspect": "equal",
    }
)


DRIVE_FREQ = "Drive frequency (Hz)"
DRIVE_FREQ_GHz = "Drive frequency (GHz)"
READOUT_FREQ = "Readout IF frequency (Hz)"
READOUT_PHASE = "Readout phase (rad)"
LEFT = "Left"
BIAS_VOLTAGE = "Bias voltage (V)"

TWO_TONE = LabelDict({"xlabel": BIAS_VOLTAGE, "ylabel": DRIVE_FREQ}, GHz={"ylabel": DRIVE_FREQ_GHz})
CHEVRON = LabelDict({"xlabel": "Pulse duration (ns)", "ylabel": "Frequency (MHz)"})
AMPLITUDE_TIME = LabelDict({"xlabel": "Pulse duration (ns)", "ylabel": "Frequency (MHz)"})
RAMSEY = LabelDict(
    {
        "label": "ramsey",
        "xlabel": "Pulse duration (ns)",
        "ylabel": "Readout quadrature",
    }
)
REIM = LabelDict(
    {
        "xlabel": "Re(z)",
        "ylabel": "Im(z)",
    }
)

aspect_equal = LabelDict({"aspect": "equal"})
