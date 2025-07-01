from preswald import text, connect, table, text_input, slider, plotly
import pandas as pd
import plotly.express as px

# 1. HEADER #
text("# NETFLIX EXPLORER")
text("Plan your next Netflix marathon with precision.")

# 2. FILTERS #
text("### Filters")

# Release Year slider
year = slider("Release Year", min_val=2000, max_val=2023, default=2021)

# Type input
content_type = text_input("Type (Movie / TV Show):", placeholder="e.g., Movie")

# Title search
title_search = text_input("Search Title", placeholder="Enter part of a title...")

# 3. LOAD DATA #
connect()
df = pd.read_csv("data/netflix_titles.csv", 
                 usecols=["type", "title", "release_year", "country", "rating"])

# Clean data
df['type'] = df['type'].str.strip().str.title()
df = df.dropna(subset=["release_year"])

# 4. FILTER DATA #
results = df[df["release_year"] == year]

if content_type.strip().title() in ["Movie", "Tv Show"]:
    results = results[results["type"] == content_type.strip().title()]

if title_search.strip():
    results = results[results["title"].str.contains(title_search.strip(), case=False)]

# 5. RESULTS TABLE #
text(f"Total Titles Found: **{len(results)}**", style={"font-size": "1.2em"})
table(results.sort_values("release_year", ascending=False).head(20))

# 6. SHOW BAR CHART (by Rating) #
if not results.empty:
    chart_data = results["rating"].value_counts().reset_index()
    chart_data.columns = ["Rating", "Count"]
    fig = px.bar(chart_data, x="Rating", y="Count", title="Distribution by Rating")
    plotly(fig)
else:
    text("No data to show chart.")

def export_to_html(filename="netflix_explorer_export.html"):
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Netflix Explorer Export</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }}
            h1 {{
                color: #E50914;
                border-bottom: 2px solid #E50914;
                padding-bottom: 10px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th {{
                background-color: #E50914;
                color: white;
                padding: 10px;
                text-align: left;
            }}
            td {{
                padding: 8px;
                border-bottom: 1px solid #ddd;
            }}
            .filters {{
                background: #f5f5f5;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        <h1>Netflix Explorer</h1>
        <div class="filters">
            <h3>Active Filters:</h3>
            <p><strong>Release Year:</strong> {year}</p>
            <p><strong>Content Type:</strong> {content_type if content_type else "All"}</p>
        </div>
        <h2>Results ({len(results)} Titles)</h2>
        {results.to_html(index=False)}
    </body>
    </html>
    """
    
    with open(filename, "w") as f:
        f.write(html_content)
    print(f"Successfully exported to {filename}")
export_to_html()