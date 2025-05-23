import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

BLINKIT_YELLOW = "#FFE600"
BLINKIT_GREEN = "#1BAF5D"
DARK_BG = "#23272F"
CARD_BG = "#2C313A"
LIGHT_TEXT = "#F8F8F2"

st.set_page_config(page_title="Blinkit Grocery Analytics Dashboard", layout="wide", initial_sidebar_state="expanded")

st.markdown(f"""
    <style>
    .stApp {{ background-color: {DARK_BG} !important; color: {LIGHT_TEXT} !important; }}
    .main .block-container {{ background-color: {DARK_BG} !important; color: {LIGHT_TEXT} !important; }}
    .header-container {{ background-color: {CARD_BG} !important; color: {LIGHT_TEXT} !important; border-radius: 10px; margin-bottom: 0.3rem; margin-top: 0.2rem; box-shadow: 0 0 4px rgba(0,0,0,0.15); padding: 12px 18px 10px 18px; display: flex; align-items: center; justify-content: space-between; }}
    .metric-card {{ background: none !important; color: {LIGHT_TEXT} !important; border: none; border-radius: 0; margin: 0; box-shadow: none; padding: 0; min-height: 50px; display: flex; flex-direction: column; justify-content: center; align-items: flex-start; }}
    .metric-icon {{ font-size: 28px; font-weight: bold; display: inline-block; margin-bottom: -8px; margin-right: 8px; vertical-align: middle; }}
    .metric-icon-yellow {{ color: {BLINKIT_YELLOW}; }}
    .metric-icon-green {{ color: {BLINKIT_GREEN}; }}
    .metric-label {{ color: {LIGHT_TEXT}; font-size: 16px; font-weight: bold; letter-spacing: 0.5px; margin-bottom: 0.2rem; margin-top: 0.1rem; }}
    .metric-value {{ color: {LIGHT_TEXT}; font-size: 20px; font-weight: bold; margin-bottom: 0.1rem; }}
    .sidebar-content, .chart-container, .table-container {{ background-color: {CARD_BG} !important; color: {LIGHT_TEXT} !important; border-radius: 8px; box-shadow: 0 0 4px rgba(0,0,0,0.12); margin-bottom: 0.5rem; padding: 12px 12px 10px 12px; }}
    [data-testid="stSidebar"] {{ background-color: {DARK_BG} !important; color: {LIGHT_TEXT} !important; padding-top: 0.5rem !important; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 8px; }}
    .stTabs [data-baseweb="tab"] {{ height: 32px; background-color: {DARK_BG}; color: {LIGHT_TEXT} !important; border-radius: 4px 4px 0px 0px; padding: 4px 16px; font-size: 14px; }}
    .stTabs [aria-selected="true"] {{ background-color: #393E46; color: {BLINKIT_YELLOW} !important; }}
    .filter-header, .category {{ color: {BLINKIT_YELLOW} !important; font-weight: bold; font-size:14px; }}
    </style>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class="header-container">
        <div style="display:flex;align-items:center;">
            <span style="color:{BLINKIT_GREEN};font-weight:bold;font-size:32px;">blink</span>
            <span style="color:{BLINKIT_YELLOW};font-weight:bold;font-size:32px;">it</span>
            <span style="color:{LIGHT_TEXT};font-size:24px;font-weight:500;margin-left:8px;">
                Grocery Analytics Dashboard
            </span>
        </div>
        <div style="color:#CCCCCC;font-size:14px;">India's Last Minute App</div>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
st.sidebar.markdown('<p class="filter-header">UPLOAD DATA</p>', unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel", type=['csv', 'xlsx', 'xls'])
st.sidebar.markdown('</div>', unsafe_allow_html=True)

@st.cache_data
def load_data(file):
    if file is not None:
        try:
            if file.name.endswith('.csv'):
                return pd.read_csv(file)
            elif file.name.endswith(('.xlsx', '.xls')):
                return pd.read_excel(file)
        except Exception as e:
            st.error(f"Error loading file: {e}")
    return None

def create_sample_data():
    np.random.seed(42)
    outlet_types = ['Supermarket Type1', 'Supermarket Type2', 'Supermarket Type3', 'Grocery Store']
    outlet_sizes = ['Small', 'Medium', 'High']
    outlet_locations = ['Tier 1', 'Tier 2', 'Tier 3']
    item_types = ['Fruits and Vegetables', 'Snack Foods', 'Household', 'Frozen Foods', 
                 'Dairy', 'Canned', 'Baking Goods', 'Health and Hygiene', 'Meat',
                 'Soft Drinks', 'Breads', 'Hard Drinks', 'Others', 'Starchy Foods', 'Breakfast', 'Seafood']
    fat_contents = ['Low Fat', 'Regular']
    n_items = 1200
    outlet_ids = [f'OUT{i:03d}' for i in range(1, 15)]
    establishment_years = np.random.choice(range(2010, 2023), len(outlet_ids))
    outlet_data = pd.DataFrame({
        'Outlet ID': outlet_ids,
        'Outlet Establishment Year': establishment_years,
        'Outlet Size': np.random.choice(outlet_sizes, len(outlet_ids)),
        'Outlet Location Type': np.random.choice(outlet_locations, len(outlet_ids)),
        'Outlet Type': np.random.choice(outlet_types, len(outlet_ids))
    })
    item_ids = [f'ITM{i:04d}' for i in range(1, n_items+1)]
    data = []
    for item_id in item_ids:
        outlet = outlet_data.sample(1).iloc[0]
        item_type = np.random.choice(item_types)
        fat_content = np.random.choice(fat_contents)
        base_sales = 100 + np.random.gamma(2, 50)
        sales_multiplier = 1.5 if 'Supermarket' in outlet['Outlet Type'] else 1.0
        item_multiplier = 1.8 if item_type in ['Fruits and Vegetables', 'Snack Foods'] else 1.5 if item_type in ['Household', 'Dairy'] else 1.0
        sales = base_sales * sales_multiplier * item_multiplier
        visibility = np.random.uniform(0.01, 0.2)
        rating = np.random.uniform(3.0, 5.0)
        data.append({
            'Item Identifier': item_id,
            'Item Weight': np.random.uniform(5, 20),
            'Item Fat Content': fat_content,
            'Item Visibility': visibility,
            'Item Type': item_type,
            'Sales': sales,
            'Rating': rating,
            'Outlet Identifier': outlet['Outlet ID'],
            'Outlet Establishment Year': outlet['Outlet Establishment Year'],
            'Outlet Size': outlet['Outlet Size'],
            'Outlet Location Type': outlet['Outlet Location Type'],
            'Outlet Type': outlet['Outlet Type']
        })
    return pd.DataFrame(data)

if uploaded_file:
    df = load_data(uploaded_file)
    if df is None:
        st.error("Failed to load the file. Using sample data.")
        df = create_sample_data()
else:
    df = create_sample_data()
    st.sidebar.info("Currently using sample data. Upload your CSV file to use your own data.")

with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown('<p class="filter-header">FILTERS</p>', unsafe_allow_html=True)
    location_filter = st.selectbox("Outlet Location Type", ["All"] + sorted(df["Outlet Location Type"].unique()), 0)
    size_filter = st.selectbox("Outlet Size", ["All"] + sorted(df["Outlet Size"].unique()), 0)
    item_filter = st.selectbox("Item Type", ["All"] + sorted(df["Item Type"].unique()), 0)
    outlet_type_filter = st.selectbox("Outlet Type", ["All"] + sorted(df["Outlet Type"].unique()), 0)
    fat_content_filter = st.selectbox("Item Fat Content", ["All"] + sorted(df["Item Fat Content"].unique()), 0)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown('<p class="filter-header">YEAR RANGE</p>', unsafe_allow_html=True)
    min_year = int(df["Outlet Establishment Year"].min())
    max_year = int(df["Outlet Establishment Year"].max())
    year_range = st.slider("Establishment Year", min_year, max_year, (min_year, max_year))
    st.markdown('</div>', unsafe_allow_html=True)

filtered_df = df.copy()
if location_filter != "All":
    filtered_df = filtered_df[filtered_df["Outlet Location Type"] == location_filter]
if size_filter != "All":
    filtered_df = filtered_df[filtered_df["Outlet Size"] == size_filter]
if item_filter != "All":
    filtered_df = filtered_df[filtered_df["Item Type"] == item_filter]
if outlet_type_filter != "All":
    filtered_df = filtered_df[filtered_df["Outlet Type"] == outlet_type_filter]
if fat_content_filter != "All":
    filtered_df = filtered_df[filtered_df["Item Fat Content"] == fat_content_filter]
filtered_df = filtered_df[(filtered_df["Outlet Establishment Year"] >= year_range[0]) & 
                          (filtered_df["Outlet Establishment Year"] <= year_range[1])]

col1, col2, col3, col4 = st.columns([1,1,1,1], gap="small")
with col1:
    st.markdown(f'''
        <div class="metric-card">
            <span class="metric-icon metric-icon-yellow">&#9689;</span>
            <span class="metric-label">TOTAL SALES</span>
            <span class="metric-value">${filtered_df['Sales'].sum()/1_000_000:.2f}M</span>
        </div>
    ''', unsafe_allow_html=True)
with col2:
    st.markdown(f'''
        <div class="metric-card">
            <span class="metric-icon metric-icon-yellow">&#9689;</span>
            <span class="metric-label">AVG SALES</span>
            <span class="metric-value">${filtered_df['Sales'].mean():.0f}</span>
        </div>
    ''', unsafe_allow_html=True)
with col3:
    st.markdown(f'''
        <div class="metric-card">
            <span class="metric-icon metric-icon-yellow">&#9689;</span>
            <span class="metric-label">NO OF ITEMS</span>
            <span class="metric-value">{len(filtered_df)}</span>
        </div>
    ''', unsafe_allow_html=True)
with col4:
    st.markdown(f'''
        <div class="metric-card">
            <span class="metric-icon metric-icon-green">&#9689;</span>
            <span class="metric-label">AVG RATING</span>
            <span class="metric-value">{filtered_df['Rating'].mean():.1f}</span>
        </div>
    ''', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["Total Sales", "Outlet Analysis", "Item Analysis", "Ratings"])

with tab1:
    row1 = st.columns(3)
    sales_by_year = filtered_df.groupby('Outlet Establishment Year').agg({'Sales':'sum','Item Identifier':'count'}).reset_index()
    fig_combo = go.Figure()
    fig_combo.add_trace(go.Bar(x=sales_by_year['Outlet Establishment Year'], y=sales_by_year['Sales'],
                               name='Sales', marker_color=BLINKIT_GREEN, yaxis='y1'))
    fig_combo.add_trace(go.Scatter(x=sales_by_year['Outlet Establishment Year'], y=sales_by_year['Item Identifier'],
                                   name='Item Count', marker_color=BLINKIT_YELLOW, yaxis='y2', mode='lines+markers'))
    fig_combo.update_layout(
        yaxis=dict(title='Sales', showgrid=False),
        yaxis2=dict(title='Items', overlaying='y', side='right', showgrid=False),
        plot_bgcolor=CARD_BG, paper_bgcolor=CARD_BG, font_color=LIGHT_TEXT, margin=dict(l=10, r=10, t=10, b=10), height=260, showlegend=False
    )
    row1[0].plotly_chart(fig_combo, use_container_width=True)

    fat_content_sales = filtered_df.groupby('Item Fat Content')['Sales'].sum().reset_index()
    fig_pie = px.pie(fat_content_sales, names='Item Fat Content', values='Sales',
                     color_discrete_sequence=[BLINKIT_YELLOW, BLINKIT_GREEN], hole=0.6)
    fig_pie.update_traces(textinfo='percent+label')
    fig_pie.update_layout(plot_bgcolor=CARD_BG, paper_bgcolor=CARD_BG, font_color=LIGHT_TEXT, margin=dict(l=10, r=10, t=10, b=10), height=260, showlegend=False)
    row1[1].plotly_chart(fig_pie, use_container_width=True)

    # No yellow item bar chart here! (Only in Item Analysis)
    item_type_sales = filtered_df.groupby('Item Type')['Sales'].sum().sort_values(ascending=False).head(7).reset_index()
    fig_item_type = px.bar(item_type_sales, x='Item Type', y='Sales', color='Sales', color_continuous_scale='YlGn')
    fig_item_type.update_layout(plot_bgcolor=CARD_BG, paper_bgcolor=CARD_BG, font_color=LIGHT_TEXT, margin=dict(l=10, r=10, t=10, b=40), height=260, showlegend=False)
    row1[2].plotly_chart(fig_item_type, use_container_width=True)

    row2 = st.columns(2)
    heatmap_data = filtered_df.groupby(['Item Type','Outlet Size'])['Sales'].sum().reset_index()
    heatmap_pivot = heatmap_data.pivot(index='Item Type', columns='Outlet Size', values='Sales').fillna(0)
    fig_heatmap = px.imshow(heatmap_pivot, color_continuous_scale='YlGnBu', aspect='auto')
    fig_heatmap.update_layout(plot_bgcolor=CARD_BG, paper_bgcolor=CARD_BG, font_color=LIGHT_TEXT, margin=dict(l=10, r=10, t=10, b=10), height=220, coloraxis_showscale=False)
    row2[0].plotly_chart(fig_heatmap, use_container_width=True)
    fig_hist = px.histogram(filtered_df, x="Sales", nbins=30, color_discrete_sequence=[BLINKIT_GREEN])
    fig_hist.update_layout(plot_bgcolor=CARD_BG, paper_bgcolor=CARD_BG, font_color=LIGHT_TEXT, margin=dict(l=10, r=10, t=10, b=10), height=220, showlegend=False)
    row2[1].plotly_chart(fig_hist, use_container_width=True)

with tab2:
    row1 = st.columns(2)
    outlet_size_sales = filtered_df.groupby('Outlet Size')['Sales'].sum().reset_index()
    fig_size = px.pie(outlet_size_sales, names='Outlet Size', values='Sales',
                      color_discrete_sequence=[BLINKIT_GREEN, BLINKIT_YELLOW, "#FFA500"], hole=0.5)
    fig_size.update_traces(textinfo='percent+label')
    fig_size.update_layout(plot_bgcolor=CARD_BG, paper_bgcolor=CARD_BG, font_color=LIGHT_TEXT, margin=dict(l=10, r=10, t=10, b=10), height=260, showlegend=True)
    row1[0].plotly_chart(fig_size, use_container_width=True)

    location_sales = filtered_df.groupby('Outlet Location Type')['Sales'].sum().reset_index()
    fig_location = px.bar(location_sales, x='Outlet Location Type', y='Sales', color='Sales', color_continuous_scale='YlGn')
    fig_location.update_layout(plot_bgcolor=CARD_BG, paper_bgcolor=CARD_BG, font_color=LIGHT_TEXT, margin=dict(l=10, r=10, t=10, b=10), height=260, showlegend=False)
    row1[1].plotly_chart(fig_location, use_container_width=True)

    # Power BI-style colored OUTLET TYPE table
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    st.markdown("#### OUTLET TYPE")
    outlet_type_data = filtered_df.groupby('Outlet Type').agg({
        'Sales': ['sum', 'mean'],
        'Item Identifier': 'count',
        'Rating': 'mean',
        'Item Visibility': 'mean'
    }).reset_index()
    outlet_type_data.columns = ['Outlet Type', 'Total Sales', 'Avg Sales', 'No of Items', 'Avg Rating', 'Item Visibility']
    outlet_type_data['Total Sales'] = outlet_type_data['Total Sales'].apply(lambda x: f"${x/1000:.2f}K")
    outlet_type_data['Avg Sales'] = outlet_type_data['Avg Sales'].apply(lambda x: f"${x:.0f}")
    outlet_type_data['Avg Rating'] = outlet_type_data['Avg Rating'].apply(lambda x: f"{x:.1f}")
    outlet_type_data['Item Visibility'] = outlet_type_data['Item Visibility'].apply(lambda x: f"{x:.2f}")
    def color_cell(val, col):
        if col == 'Total Sales':
            return "background-color:#FFE600;font-weight:bold;color:#111111;text-align:center;"
        elif col == 'No of Items':
            return "background-color:#1BAF5D;font-weight:bold;color:#fff;text-align:center;"
        elif col == 'Avg Sales':
            return "background-color:#F87171;font-weight:bold;color:#fff;text-align:center;"
        elif col == 'Avg Rating':
            return "background-color:#60A5FA;font-weight:bold;color:#fff;text-align:center;"
        elif col == 'Item Visibility':
            return "background-color:#FACC15;font-weight:bold;color:#111111;text-align:center;"
        else:
            return "text-align:left;"
    table_html = """
    <table style="width:100%;border-collapse:separate;border-spacing:0 8px;">
        <tr>
            <th style="text-align:left;padding:6px 12px;">Outlet Type</th>
            <th style="text-align:center;padding:6px 12px;">Total Sales</th>
            <th style="text-align:center;padding:6px 12px;">No of Items</th>
            <th style="text-align:center;padding:6px 12px;">Avg Sales</th>
            <th style="text-align:center;padding:6px 12px;">Avg Rating</th>
            <th style="text-align:center;padding:6px 12px;">Item Visibility</th>
        </tr>
    """
    for _, row in outlet_type_data.iterrows():
        table_html += "<tr>"
        table_html += f'<td style="background:#fff;border-radius:8px 0 0 8px;padding:6px 12px;color:#222;font-weight:500;">{row["Outlet Type"]}</td>'
        table_html += f'<td style="{color_cell(row["Total Sales"], "Total Sales")}border-radius:0;">{row["Total Sales"]}</td>'
        table_html += f'<td style="{color_cell(row["No of Items"], "No of Items")}border-radius:0;">{row["No of Items"]}</td>'
        table_html += f'<td style="{color_cell(row["Avg Sales"], "Avg Sales")}border-radius:0;">{row["Avg Sales"]}</td>'
        table_html += f'<td style="{color_cell(row["Avg Rating"], "Avg Rating")}border-radius:0;">{row["Avg Rating"]}</td>'
        table_html += f'<td style="{color_cell(row["Item Visibility"], "Item Visibility")}border-radius:0 8px 8px 0;">{row["Item Visibility"]}</td>'
        table_html += "</tr>"
    table_html += "</table>"
    st.markdown(table_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    item_type_sales = filtered_df.groupby('Item Type')['Sales'].sum().sort_values(ascending=False).reset_index()
    fig_item_type = px.bar(
        item_type_sales,
        y="Item Type",
        x="Sales",
        orientation="h",
        color_discrete_sequence=["#FFE600"]
    )
    fig_item_type.update_traces(
        marker_line_color='#B8A200',
        marker_line_width=2,
        text=item_type_sales['Sales'].apply(lambda x: f"${x/1_000:.2f}K"),
        textposition='outside',
        insidetextanchor='start'
    )
    fig_item_type.update_layout(
        plot_bgcolor="#23272F",
        paper_bgcolor="#23272F",
        font_color="#F8F8F2",
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=True,
            title=None,
            tickfont=dict(color="#F8F8F2", size=16, family="sans-serif")
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=True,
            title=None,
            tickfont=dict(color="#F8F8F2", size=14, family="sans-serif")
        ),
        margin=dict(l=0, r=0, t=10, b=10),
        showlegend=False
    )
    st.plotly_chart(fig_item_type, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    row = st.columns(2)
    fig_rating = px.histogram(filtered_df, x="Rating", nbins=20, color_discrete_sequence=[BLINKIT_GREEN])
    fig_rating.update_layout(plot_bgcolor=CARD_BG, paper_bgcolor=CARD_BG, font_color=LIGHT_TEXT)
    row[0].plotly_chart(fig_rating, use_container_width=True)
    avg_rating_item = filtered_df.groupby('Item Type')['Rating'].mean().reset_index().sort_values('Rating', ascending=False)
    fig_avg_rating = px.bar(avg_rating_item, x='Item Type', y='Rating', color='Rating', color_continuous_scale='YlGnBu')
    fig_avg_rating.update_layout(plot_bgcolor=CARD_BG, paper_bgcolor=CARD_BG, font_color=LIGHT_TEXT)
    row[1].plotly_chart(fig_avg_rating, use_container_width=True)

