class DataSeries:
    def __init__(self, name, y, x=None):
        self.name = name
        self.y = y
        self.x = x if x else list(range(len(y)))


class ChartConfig:
    def __init__(self):
        self.chart_type = "line"
        self.title = ""
        self.xlabel = ""
        self.ylabel = ""
        self.legend = True
        self.legend_name = ""
        self.fontsize = 10
        self.line_style = "Сплошная"
        self.line_width = 1.5
        self.marker = "o"
        self.bar_width = 0.8
        self.pie_autopct = True
        self.hist_bins = 10

    @classmethod
    def from_dict(cls, d):
        cfg = cls()
        for k,v in d.items():
            if hasattr(cfg,k):
                setattr(cfg,k,v)
        return cfg
