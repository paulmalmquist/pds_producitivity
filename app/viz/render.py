"""Chart rendering using matplotlib or plotly."""
from __future__ import annotations

import base64
from io import BytesIO
from typing import Dict, List

from app.config import get_settings
from app.utils import encode_plot


class ChartRenderer:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.engine = self.settings.chart_engine.lower()

    def render(self, chart_type: str, spec: Dict[str, str], rows: List[Dict[str, object]], title: str) -> str:
        if self.engine == "plotly":
            return self._render_plotly(chart_type, spec, rows, title)
        return self._render_matplotlib(chart_type, spec, rows, title)

    def _render_matplotlib(self, chart_type: str, spec: Dict[str, str], rows: List[Dict[str, object]], title: str) -> str:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(6, 4))
        x_field = spec.get("x")
        y_field = spec.get("y")
        group_field = spec.get("group")
        if chart_type == "line" and x_field and y_field:
            ax.plot([row[x_field] for row in rows], [row[y_field] for row in rows], marker="o")
            ax.set_xlabel(x_field)
            ax.set_ylabel(y_field)
        elif chart_type == "bar" and x_field and y_field:
            labels = [row[x_field] for row in rows]
            values = [row[y_field] for row in rows]
            ax.bar(labels[:25], values[:25])
            if len(labels) > 8:
                ax.tick_params(axis="x", rotation=45)
            ax.set_xlabel(x_field)
            ax.set_ylabel(y_field)
        elif chart_type == "pie" and x_field and y_field:
            labels = [row[x_field] for row in rows][:10]
            values = [row[y_field] for row in rows][:10]
            ax.pie(values, labels=labels, autopct="%1.1f%%")
        elif chart_type == "scatter" and x_field and y_field:
            colors = None
            if group_field:
                groups = list({row[group_field] for row in rows})
                color_map = {group: idx for idx, group in enumerate(groups)}
                colors = [color_map[row[group_field]] for row in rows]
            ax.scatter([row[x_field] for row in rows], [row[y_field] for row in rows], c=colors)
            ax.set_xlabel(x_field)
            ax.set_ylabel(y_field)
        elif chart_type == "kpi" and x_field:
            fig.clf()
            fig, ax = plt.subplots(figsize=(4, 2))
            ax.axis("off")
            value = rows[0].get(x_field, "-")
            ax.text(0.5, 0.6, str(value), fontsize=28, ha="center")
            ax.text(0.5, 0.2, x_field, fontsize=12, ha="center")
        else:
            ax.text(0.5, 0.5, "Chart not available", ha="center")
        note = spec.get("note")
        subtitle = f"\n{note}" if note else ""
        ax.set_title(f"{title}{subtitle}")
        return encode_plot(fig)

    def _render_plotly(self, chart_type: str, spec: Dict[str, str], rows: List[Dict[str, object]], title: str) -> str:
        import plotly.express as px

        if chart_type == "line":
            fig = px.line(rows, x=spec.get("x"), y=spec.get("y"), title=title)
        elif chart_type == "bar":
            fig = px.bar(rows, x=spec.get("x"), y=spec.get("y"), title=title)
        elif chart_type == "pie":
            fig = px.pie(rows, names=spec.get("x"), values=spec.get("y"), title=title)
        elif chart_type == "scatter":
            fig = px.scatter(rows, x=spec.get("x"), y=spec.get("y"), color=spec.get("group"), title=title)
        elif chart_type == "kpi":
            import matplotlib.pyplot as plt

            fig_mat, _ = plt.subplots(figsize=(4, 2))
            return encode_plot(fig_mat)
        else:
            import matplotlib.pyplot as plt

            fig_mat, _ = plt.subplots()
            return encode_plot(fig_mat)
        buffer = BytesIO()
        fig.write_image(buffer, format="png")
        buffer.seek(0)
        return base64.b64encode(buffer.read()).decode("utf-8")


__all__ = ["ChartRenderer"]
