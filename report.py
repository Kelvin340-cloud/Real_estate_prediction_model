from datetime import datetime
import numpy as np
import pandas as pd
import os
from io import BytesIO, StringIO

import streamlit as st
from supabase import create_client, Client  # type: ignore

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle

# --- Supabase init (validate env) ---
SUPABASE_URL = os.environ.get("supabase_url")
SUPABASE_KEY = os.environ.get("supabase_key")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Supabase credentials not found in environment variables.")

supabase: Client | None = None
try:
    if SUPABASE_URL and SUPABASE_KEY:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)  # type: ignore
except Exception as e:
    st.error(f"Failed initializing Supabase client: {e}")
    supabase = None


# --- PDF Builder (no charts) ---
def build_pdf(df: pd.DataFrame, user_info: dict, logo_path: str = "./img/Logo1.png") -> BytesIO:
    """
    Build a multi-section PDF using reportlab.platypus and return BytesIO buffer.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter,
        rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
    )
    styles = getSampleStyleSheet()
    story = []

    # Cover
    title_style = styles["Title"]
    normal = styles["BodyText"]
    small = ParagraphStyle("small", parent=styles["Normal"], fontSize=9)

    # Logo (optional)
    try:
        if os.path.exists(logo_path):
            story.append(RLImage(logo_path, width=150, height=75))
    except Exception:
        pass

    story.append(Spacer(1, 12))
    story.append(Paragraph("PREDICTION REPORT", title_style))
    story.append(Spacer(1, 6))
    story.append(
        Paragraph(
            f"Generated for <b>{user_info.get('name','N/A')}</b> ({user_info.get('email','N/A')}) "
            f"on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.",
            normal,
        )
    )
    story.append(Spacer(1, 12))
    story.append(
        Paragraph(
            "This report provides an overview of predicted housing prices from your recent queries. "
            "It includes summary statistics and a preview of the predictions.",
            normal,
        )
    )
    story.append(Spacer(1, 18))

    # Summary Stats
    story.append(Paragraph("Summary Statistics", styles["Heading2"]))
    stats_data = []
    def fmt(x): return f"{x:,.0f}" if pd.notna(x) else "N/A"
    avg_price = df["predicted_price"].mean() if not df["predicted_price"].empty else np.nan
    min_price = df["predicted_price"].min() if not df["predicted_price"].empty else np.nan
    max_price = df["predicted_price"].max() if not df["predicted_price"].empty else np.nan
    std_price = df["predicted_price"].std() if not df["predicted_price"].empty else np.nan

    stats_data.append(["Average Predicted Price:", fmt(avg_price)])
    stats_data.append(["Minimum Predicted Price:", fmt(min_price)])
    stats_data.append(["Maximum Predicted Price:", fmt(max_price)])
    stats_data.append(["Std Dev of Predicted Price:", fmt(std_price)])

    t = Table(stats_data, colWidths=[250, 200])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("LINEBELOW", (0, 0), (-1, -1), 0.25, colors.grey),
            ]
        )
    )
    story.append(t)
    story.append(Spacer(1, 12))

    # Preview Table (first 10 rows with predicted price range)
    story.append(Paragraph("Predictions Preview (first 10 rows)", styles["Heading2"]))
    preview = df.head(10).copy()
    if not preview.empty:
        preview["predicted_price_range"] = preview["predicted_price"].apply(
            lambda x: f"{max(x-50000,0):,.0f} - {x+50000:,.0f}" if pd.notna(x) else "N/A"
        )

    cols_to_show = ["sub_county", "neighborhood", "sq_mtrs", "bedrooms", "bathrooms", "predicted_price", "predicted_price_range"]
    cols = [c for c in cols_to_show if c in preview.columns]

    if preview.empty:
        story.append(Paragraph("No data to display.", normal))
    else:
        table_data = [cols]
        for _, row in preview[cols].iterrows():
            line = []
            for c in cols:
                val = row[c]
                if pd.isna(val):
                    line.append("")
                elif c in ["predicted_price"]:
                    line.append(f"{val:,.0f}")
                else:
                    line.append(str(val))
            table_data.append(line)

        tbl = Table(table_data, repeatRows=1, colWidths=[80] * len(cols))
        tbl.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f2f2f2")),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                ]
            )
        )
        story.append(tbl)

    story.append(Spacer(1, 18))

    # Disclaimer & Footer
    story.append(Paragraph("Notes", styles["Heading2"]))
    story.append(
        Paragraph(
            "These predictions are generated by a statistical model and should be used for informational purposes only. "
            "They are estimates and may not reflect actual market prices. Use additional sources when making financial decisions.",
            normal,
        )
    )
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"© {datetime.now().year} Kelvin Njuguna | All rights reserved.", small))

    # Build document
    doc.build(story)
    buffer.seek(0)
    return buffer


# --- Main display_report function (no charts) ---
def display_report():
    if "user" not in st.session_state:
        st.warning("You need to log in to access the report.")
        return

    if supabase is None:
        st.error("Supabase client not initialized. Check environment variables.")
        return

    user = st.session_state["user"]
    user_email = getattr(user, "email", "N/A")
    user_name = "N/A"
    if getattr(user, "user_metadata", None):
        if isinstance(user.user_metadata, dict):
            user_name = user.user_metadata.get("full_name", user.user_metadata.get("name", "N/A"))
        else:
            user_name = str(user.user_metadata)
    user_uid = getattr(user, "uid", "N/A")

    st.title("Prediction Report")
    st.write(f"Logged in as: **{user_name}** ({user_email})")

    # Fetch predictions
    try:
        res = supabase.table("prediction").select("*").eq("user_id", user_uid).execute()
    except Exception as e:
        st.error(f"Error fetching data from Supabase: {e}")
        return

    if not res.data:
        st.warning("No prediction data found for the logged-in user.")
        return

    try:
        df = pd.DataFrame(res.data)
    except Exception as e:
        st.error(f"Failed to convert prediction data to DataFrame: {e}")
        return

    if "predicted_price" not in df.columns:
        st.error("Prediction data does not contain 'predicted_price' column.")
        return

    # cast numeric
    df["predicted_price"] = pd.to_numeric(df["predicted_price"], errors="coerce")

    # Filters
    st.sidebar.header("Filters")
    if "neighborhood" in df.columns:
        neighborhoods = sorted(df["neighborhood"].dropna().unique().tolist())
        chosen_nbh = st.sidebar.multiselect("Neighborhood", options=neighborhoods, default=neighborhoods[:5])
        if chosen_nbh:
            df = df[df["neighborhood"].isin(chosen_nbh)]

    # Summary metrics
    st.subheader("Summary Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Average Predicted", f"{df['predicted_price'].mean():,.0f}")
    col2.metric("Min Predicted", f"{df['predicted_price'].min():,.0f}")
    col3.metric("Max Predicted", f"{df['predicted_price'].max():,.0f}")

    # Table preview (with range)
    st.subheader("Predictions Preview")
    if not df.empty:
        df_preview = df.head(50).copy()
        df_preview["predicted_price_range"] = df_preview["predicted_price"].apply(
            lambda x: f"{max(x-50000,0):,.0f} - {x+50000:,.0f}" if pd.notna(x) else "N/A"
        )
        st.dataframe(df_preview)
    else:
        st.write("No data to display.")

    # Download CSV
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_bytes = csv_buffer.getvalue().encode("utf-8")
    st.download_button("Download Predictions CSV", data=csv_bytes, file_name="predictions.csv", mime="text/csv")

    # PDF Report
    with st.spinner("Generating PDF..."):
        pdf_buffer = build_pdf(df, {"name": user_name, "email": user_email})

    st.download_button("Download PDF Report", data=pdf_buffer, file_name="prediction_report.pdf", mime="application/pdf")

    st.success("Report ready!")
