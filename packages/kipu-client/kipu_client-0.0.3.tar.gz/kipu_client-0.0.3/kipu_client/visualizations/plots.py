
import numpy as np
import matplotlib.pyplot as plt

def comparison_plot(results:dict, num_qubits : int):
    """
    Plot to compare solutions from different algorithm output

    Args:
        results (dict): Dictionary structure holding the measurement probability
            for a set of states under a particular circuit execution.

            Example:
                {"DCQO : 
                    { "00" : 0.25,
                      "01" : 0.25,
                      "10" : 0.25,
                      "11" : 0.25
                    }
                }
        num_qubits (int): Number of qubits
    """

    label_list = list(results.keys())
    num_plots = len(label_list)

    # set up figure environment
    fig, axs = plt.subplots(num_plots, sharex=True, figsize=(8,5))
    fig.suptitle("Comparison plot", y=.95, fontname='Helvetica')

    # plot given results
    for indx, label in enumerate(label_list):

        counts = results[label]

        axs[indx].bar(
            x=np.arange(len(list(counts.keys()))),
            height=list(counts.values()),
            width=.5,
        )
        axs[indx].text(
            x = 0,
            y = 0,
            s = label,
            fontname='Helvetica'
        )

    plt.subplots_adjust(wspace=0, hspace=0.0)
    fig.supxlabel(
        "Selected bitstrings of length "+ str(num_qubits) + " (as integers)", fontname='Helvetica'
    )
    fig.supylabel("Probability", fontname='Helvetica', x=0.05)

    plt.show()
