
import pandas as pd
import plotly.express as px

THEME = "plotly_white"

BACKGROUND = "#F5F7FB"
CARD = "#FFFFFF"
TEXT = "#172033"
BLUE = "#2563EB"

CHART_COLORS = [
    "#2563EB",
    "#16A34A",
    "#F59E0B",
    "#8B5CF6"
]


def style_chart(fig):
    fig.update_layout(
        template=THEME,
        paper_bgcolor=BACKGROUND,
        plot_bgcolor=CARD,
        font=dict(
            family="Arial",
            color=TEXT,
            size=12
        ),
        title_font=dict(
            size=18,
            color=TEXT
        ),
        colorway=CHART_COLORS,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor="#E2E8F0",
        tickfont=dict(color=TEXT)
    )

    fig.update_yaxes(
        gridcolor="#E2E8F0",
        zerolinecolor="#CBD5E1",
        tickfont=dict(color=TEXT)
    )

    return fig


def churn_donut(df):
    if (
        "churn_flag" not in df.columns
        or df["churn_flag"].dropna().empty
    ):
        fig = px.bar(title="Churn Data Unavailable")

    else:
        labels = df["churn_flag"].map({
            0: "Retained",
            1: "Churned"
        }).dropna()

        counts = (
            labels.value_counts()
            .rename_axis("Status")
            .reset_index(name="Customers")
        )

        fig = px.pie(
            counts,
            names="Status",
            values="Customers",
            hole=0.58,
            title="Customer Churn Distribution",
            color="Status",
            color_discrete_map={
                "Retained": "#16A34A",
                "Churned": "#EF4444"
            }
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            marker=dict(
                line=dict(color=CARD, width=3)
            )
        )

    return style_chart(fig)


def risk_bar(df):
    if "churn_score" not in df.columns:
        fig = px.bar(
            title="Churn Score Column Unavailable"
        )
        return style_chart(fig)

    risk = pd.cut(
        df["churn_score"],
        [-1, 39, 69, 100],
        labels=["Low", "Medium", "High"]
    )

    counts = (
        risk.value_counts()
        .reindex(["Low", "Medium", "High"], fill_value=0)
        .rename_axis("Risk")
        .reset_index(name="Customers")
    )

    fig = px.bar(
        counts,
        x="Risk",
        y="Customers",
        color="Risk",
        text="Customers",
        title="Churn Risk Distribution",
        color_discrete_map={
            "Low": "#16A34A",
            "Medium": "#F59E0B",
            "High": "#EF4444"
        },
        category_orders={
            "Risk": ["Low", "Medium", "High"]
        }
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False
    )

    fig.update_layout(
        showlegend=False
    )

    return style_chart(fig)


def churn_by_group(df, group_col):
    data = (
        df.dropna(subset=[group_col, "churn_flag"])
        .groupby(group_col, observed=True)["churn_flag"]
        .mean()
        .mul(100)
        .reset_index(name="Churn Rate (%)")
    )

    fig = px.bar(
        data,
        x=group_col,
        y="Churn Rate (%)",
        color="Churn Rate (%)",
        text_auto=".1f",
        title=(
            f"Churn Rate by "
            f"{group_col.replace('_', ' ').title()}"
        ),
        color_continuous_scale=[
            "#BFDBFE",
            "#2563EB",
            "#1E3A8A"
        ]
    )

    fig.update_traces(
        texttemplate="%{text}%",
        textposition="outside",
        cliponaxis=False
    )

    fig.update_layout(
        coloraxis_showscale=False,
        yaxis_title="Churn Rate (%)",
        xaxis_title=group_col.replace("_", " ").title()
    )

    return style_chart(fig)
