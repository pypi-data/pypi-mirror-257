class Colors:
    GREY = "#424C5C"
    RED = "#FF718B"


def create_bar_plot(ax, xdata, ydata, title="", xlabel="", ylabel="", label="", width="", xticks=[], xticklabels=[], color=Colors.GREY):
    """
    Helper function to create bar plot elements of plots.
    """

    ax.bar(xdata, ydata, label=label, width=width, color=color)

    ax.set_title(title, fontsize=15)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels, fontsize=12, rotation=45)
    ax.tick_params(axis='y', labelsize=12)
    ax.set_ylabel(ylabel, fontsize=15)
    ax.legend(fontsize=12, loc="upper right") 

    return ax
  
def create_line_plot(ax, ydata, title="", label="", xlabel="", ylabel="", xticks=[], xticklabels=[], color=Colors.GREY, alpha=1.0):
    """
    Helper function to create line plot elements of plots.
    """
    
    ax.plot(ydata, marker='o', alpha=alpha, label=label, color=color)

    ax.set_title(title, fontsize=15)
    ax.set_xlabel(xlabel, fontsize=15)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels, fontsize=12, rotation=45)
    ax.set_ylabel(ylabel, fontsize=15)
    ax.tick_params(axis='y', labelsize=12)

    return ax