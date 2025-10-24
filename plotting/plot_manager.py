import matplotlib.pyplot as plt
import matplotlib.cm as cm
from itertools import cycle

class PlotManager:
    def render(self, ax, series_list, config):
        chart_type = config.chart_type

        linestyle_map = {
            "Сплошная": "-",
            "Пунктирная": "--",
            "Точечная": ":"
        }

        color_cycle = cycle(cm.tab10.colors)
        colors = [next(color_cycle) for _ in series_list]

        for idx, s in enumerate(series_list):
            y = s.y
            x = s.x if hasattr(s, "x") else list(range(len(y)))

            marker = config.marker
            if marker == "нет":
                marker = None

            label = s.name if config.legend else None

            if chart_type == "line":
                ax.plot(
                    x, y,
                    linestyle=linestyle_map.get(config.line_style, "-"),
                    linewidth=config.line_width,
                    marker=marker,
                    label=label,
                    color=colors[idx]
                )

            elif chart_type == "bar":
                n = len(series_list)
                width = config.bar_width
                x_positions = [i + idx * width / n for i in range(len(y))]
                ax.bar(
                    x_positions, y,
                    width=width / n,
                    label=label,
                    color=colors[idx],
                    edgecolor='black',
                    alpha=0.7
                )
                if idx == 0:
                    ax.set_xticks([i + width / 2 for i in range(len(y))])
                    if hasattr(s, "x_labels") and s.x_labels:
                        ax.set_xticklabels(s.x_labels)
                    else:
                        ax.set_xticklabels([str(i+1) for i in range(len(y))])

            elif chart_type == "scatter":
                ax.scatter(
                    x, y,
                    s=config.line_width*20,
                    marker=marker,
                    label=label,
                    color=colors[idx],
                    edgecolor='black'
                )

            elif chart_type == "pie":
                pie_colors = [next(color_cycle) for _ in y]
                labels = getattr(s, "x_labels", [f"{i+1}" for i in range(len(y))])
                ax.pie(
                    y,
                    labels=labels,
                    autopct="%1.1f%%" if config.pie_autopct else None,
                    startangle=90,
                    colors=pie_colors
                )

            else:
                raise ValueError(f"Неизвестный тип графика: {chart_type}")

        if config.legend and chart_type not in ["pie"]:
            ax.legend()

        ax.set_title(config.title, fontsize=config.fontsize)
        ax.set_xlabel(config.xlabel, fontsize=config.fontsize)
        ax.set_ylabel(config.ylabel, fontsize=config.fontsize)
        ax.grid(True)
