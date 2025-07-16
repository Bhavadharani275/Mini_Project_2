import streamlit as st 
import pandas as pd 
import plotly.express as px 
import plotly.graph_objects as go 
from db_config import load_data

# Load data
df = load_data()
filtered_df = df.copy()

# Header
st.set_page_config(page_title="🐦 Species Analysis Dashboard", layout="wide")
st.sidebar.title("🧭 Dashboard Navigation")

# Define filterable columns (column: label)
filter_columns = {
    "MonthName" : "Month",
    "Common_Name": "Common Name",
    "Sex": "Gender",
    "Location_Type" : "Location",
    "ID_Method" : "Identify Method", 
}

#  Store selected values in a dictionary
filter_values = {}

for col, label in filter_columns.items():
    unique_values = df[col].dropna().unique()
    filter_values[col] = st.sidebar.multiselect(f"Select {label}", sorted(unique_values))

# Filtered Data
for col, selected in filter_values.items():
    if selected:
        filtered_df = filtered_df[filtered_df[col].isin(selected)]

# Empty Data
if filtered_df.empty:
    st.warning("🚫 No data found for the selected combination. Try adjusting your filters.")
    st.stop()

# Summary Section
total_sightings = len(filtered_df)
unique_species = filtered_df["Common_Name"].nunique()
most_common_species = filtered_df["Common_Name"].mode().values[0]
avg_temp = round(filtered_df["Temperature"].mean(), 1)

# Title
st.markdown("<h1 style='text-align:center;'>🦜 Species Observation Analysis Dashboard</h1>",unsafe_allow_html=True)

# Metrics
TotalSightings, UniqueSpecies, commonSpecies, AvgTemp = st.columns(4, border=True, gap="medium")
TotalSightings.metric("Total Sightings", total_sightings)
UniqueSpecies.metric("Unique Species", unique_species)
commonSpecies.markdown(f"""
<div style='font-size:16px;'>Most Seen Species</div>
<div style='font-size:22px; font-family:'Roboto', sans-serif; font-weight:bold;'>{most_common_species}</div>
""", unsafe_allow_html=True)
# col3.metric("Most Seen Species", most_common_species)
AvgTemp.metric("Avg Temp (°C)", avg_temp)

# Sighitings over months
def show_time_series():
    st.subheader("🕒 Sightings Over Months")
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    filtered_df["MonthName"] = pd.Categorical(filtered_df["MonthName"], categories=month_order, ordered=True)
    time_chart = filtered_df.groupby(["Year", "MonthName"]).size().reset_index(name='Sightings')
    fig = px.line(time_chart, x="MonthName", y="Sightings", color="Year", markers=True)
    st.plotly_chart(fig, use_container_width=True)



# Species Frequency
def show_top_species():
    st.subheader("🕊️ Top Observed Species")
    top_species = filtered_df["Common_Name"].value_counts().nlargest(10).reset_index()
    top_species.columns = ["Species", "Count"]
    fig = px.bar(top_species, x="Species", y="Count")
    st.plotly_chart(fig, use_container_width=True)

    # Species Overlap Between Location Types
    st.subheader("🕊️ Species Overlap Between Locations")
    location_species = df.groupby('Location_Type')['Common_Name'].unique()
    # Convert to sets
    loc1_species = set(location_species.iloc[0])
    loc2_species = set(location_species.iloc[1])
    # Counts
    shared = len(loc1_species & loc2_species)
    only_loc1 = len(loc1_species - loc2_species)
    only_loc2 = len(loc2_species - loc1_species)
    # Labels and values
    labels = [f"Shared ({shared})",
        f"Only {location_species.index[0]} ({only_loc1})",
        f"Only {location_species.index[1]} ({only_loc2})"]
    values = [shared, only_loc1, only_loc2]
    colors = ["#9F0C20", "#3210c9", "#26e248"]
    fig = go.Figure(data=[go.Pie(labels=labels,values=values,marker=dict(colors=colors),textinfo='label+percent',
                    hoverinfo='label+percent')])
    fig.update_layout(height=600,width=600,showlegend=True,)
    st.plotly_chart(fig, use_container_width=False)

    #species by Distrubction
    st.subheader("🕊️ species by Disturbance ")
    heatmap_data = (
        filtered_df.groupby(['Disturbance', 'Common_Name']).size().reset_index(name='Sightings')
        .pivot(index="Disturbance", columns="Common_Name", values="Sightings").fillna(0))
    fig_dis = px.imshow(heatmap_data.T, color_continuous_scale="YlGnBu",
                    labels={"x": "Disturbance", "y": "Common Name", "color": "Sightings"},aspect="auto")
    fig_dis.update_layout(width=5000,height=800)
    st.plotly_chart(fig_dis, use_container_width=False)


    # Species by Hours 
    st.subheader("🕊️ Species by Hours")
    bins = range(4, 13)
    labels = [f"{i}:00–{i+1}:00" for i in bins[:-1]]
    filtered_df['Hour_Bin'] = pd.cut(filtered_df['Mid_Hour'], bins = bins, labels = labels , right=False)
    heatmap_data = (
        filtered_df.groupby(["Common_Name", "Hour_Bin"]).size().reset_index(name="Sightings")
        .pivot(index="Common_Name", columns="Hour_Bin", values="Sightings").fillna(0))
    fig = px.imshow(heatmap_data, color_continuous_scale="YlGnBu",
                    labels={"x": "Hours", "y": "Common_Name", "color": "Sightings"},aspect="auto")
    fig_dis.update_layout(width=5000,height=800)
    st.plotly_chart(fig, use_container_width=False)


    # Species by Visit 
    st.subheader("🕊️ Species by Visit")
    heatmap_data = (
        filtered_df.groupby(['Visit', 'Common_Name']).size().reset_index(name='Sightings')
        .pivot(index="Visit", columns="Common_Name", values="Sightings").fillna(0))
    fig_dis = px.imshow(heatmap_data.T, color_continuous_scale="YlGnBu",
                    labels={"x": "Visit", "y": "Common Name", "color": "Sightings"},aspect="auto")
    fig_dis.update_layout(width=5000,height=800)
    st.plotly_chart(fig_dis, use_container_width=False)
    

# Environmental Correlation
def show_temperature_vs_sightings():
    st.subheader("🌡️ Temperature vs Sightings")
    env_chart = filtered_df.groupby("Temperature").size().reset_index(name="Sightings")
    fig = px.scatter(env_chart, x="Temperature", y="Sightings")
    st.plotly_chart(fig, use_container_width=True)

    # Temperature vs. Bird Count per Species
    st.subheader("🌞 Sightings vs. Temperature by Species")
    bar_data = filtered_df.groupby(["Common_Name", "Temperature"]).size().reset_index(name="Sightings")
    fig = px.bar(bar_data, x="Temperature", y="Sightings", color="Common_Name")
    st.plotly_chart(fig, use_container_width=True)



# Observer by Admin unit code
def show_observer_heatmap():
    st.subheader("🕵️📍 Observer by Location")
    heatmap_data = (
        filtered_df.groupby(["Observer", "Admin_Unit_Code"]).size().reset_index(name="Sightings")
        .pivot(index="Observer", columns="Admin_Unit_Code", values="Sightings").fillna(0))
    fig = px.imshow(heatmap_data, color_continuous_scale="YlGnBu",
                    labels={"x": "Admin Unit", "y": "Observer", "color": "Sightings"})
    st.plotly_chart(fig, use_container_width=True)


    #Observer by Distrubction
    st.subheader("🕵️🐤 Observer by species")
    heatmap_data = (
        filtered_df.groupby(['Observer', 'Common_Name']).size().reset_index(name='Sightings')
        .pivot(index="Observer", columns="Common_Name", values="Sightings").fillna(0))
    fig_dis = px.imshow(heatmap_data.T, color_continuous_scale="YlGnBu",
                    labels={"x": "Observer", "y": "Common Name", "color": "Sightings"},
                    aspect="auto")
    fig_dis.update_layout(width=5000,height=800)
    st.plotly_chart(fig_dis, use_container_width=False)


    # Hour and Observer 
    st.subheader("🕵️⏳ Observer by Hours")
    bins = range(4, 13)
    labels = [f"{i}:00–{i+1}:00" for i in bins[:-1]]
    filtered_df['Hour_Bin'] = pd.cut(filtered_df['Mid_Hour'], bins = bins, labels = labels , right=False)
    heatmap_data = (
        filtered_df.groupby(["Observer", "Hour_Bin"]).size().reset_index(name="Sightings")
        .pivot(index="Observer", columns="Hour_Bin", values="Sightings").fillna(0))
    fig = px.imshow(heatmap_data, color_continuous_scale="YlGnBu",
                    labels={"x": "Hours", "y": "Observer", "color": "Sightings"})
    st.plotly_chart(fig, use_container_width=True)



# Environmental Condition Exploration
def show_environmental_conditions():
    st.subheader("☁️ Temperature vs. Humidity (Sky)")
    fig = px.bar(filtered_df, x="Temperature", y="Humidity", color="Sky")
    st.plotly_chart(fig, use_container_width=True)

    # Wind,Temp and humidity
    st.subheader("💨 Temperature vs. Humidity (Wind)")
    fig = px.bar(filtered_df, x="Temperature", y="Humidity", color="Wind")
    st.plotly_chart(fig, use_container_width=True)

    # Environmental Influence on Species Behavior
    st.subheader("⚖️ Aggregate by species and environmental features")
    env_influence = (
        filtered_df.groupby("Common_Name")
        .agg({
            "Plot_Name": lambda x: ", ".join(x.mode().astype(str)) if not x.mode().empty else None,
            "Temperature": "mean",
            "Humidity": "mean",
            "Sky": lambda x: ", ".join(x.mode().astype(str)) if not x.mode().empty else None,
            "Wind": lambda x: ", ".join(x.mode().astype(str)) if not x.mode().empty else None,
        })
        .reset_index())
    st.dataframe(env_influence)



# Identify High-Activity Regions & Seasons
def show_high_activity_regions():
    st.subheader("📅📈 High-Activity Regions by Month")
    region_activity = filtered_df.groupby(["Plot_Name", "MonthName"]).size().reset_index(name="Sightings")
    fig = px.bar(region_activity, x="Plot_Name", y="Sightings", color="MonthName")
    st.plotly_chart(fig, use_container_width=True)

    # species PIF_Watchlist & Regional_Stewardship
    st.subheader("🐦🛡️ Species Watchlist & Stewardship Overlap")
    values = [filtered_df[(filtered_df['PIF_Watchlist_Status'] == 0) & (filtered_df['Regional_Stewardship_Status'] == 0)].shape[0],
            filtered_df[(filtered_df['PIF_Watchlist_Status'] == 0) & (filtered_df['Regional_Stewardship_Status'] == 1)].shape[0],
            filtered_df[(filtered_df['PIF_Watchlist_Status'] == 1) & (filtered_df['Regional_Stewardship_Status'] == 0)].shape[0],
            filtered_df[(filtered_df['PIF_Watchlist_Status']== 1) & (filtered_df['Regional_Stewardship_Status'] == 1)].shape[0]]
    labels = ['Neither', 'Regional Only', 'PIF Only', 'Both']
    colors = ["#924081", "#66f41f", "#f82a05", "#4c2dc5"]
    fig = go.Figure(data=[go.Pie(labels=labels,values=values,marker=dict(colors=colors),textinfo='label+percent',
                        hoverinfo='label+value',sort=False)])
    fig.update_layout(height=600,width=900,showlegend=True,)
    st.plotly_chart(fig, use_container_width=False)


    # Show species list under each category
    categories = {
    "Neither": filtered_df[(filtered_df['PIF_Watchlist_Status'] == 0) & (filtered_df['Regional_Stewardship_Status'] == 0)],
    "Regional Only": filtered_df[(filtered_df['PIF_Watchlist_Status'] == 0) & (filtered_df['Regional_Stewardship_Status'] == 1)],
    "PIF Only": filtered_df[(filtered_df['PIF_Watchlist_Status'] == 1) & (filtered_df['Regional_Stewardship_Status'] == 0)],
    "Both": filtered_df[(filtered_df['PIF_Watchlist_Status'] == 1) & (filtered_df['Regional_Stewardship_Status'] == 1)]}
    st.markdown("### 🐦🧾 Species in Each Conservation Category")
    for title, group in categories.items():
        unique_species = group['Common_Name'].dropna().unique()
        species_df = pd.DataFrame(unique_species, columns=["Common Name"])
        with st.expander(f"{title} ({len(unique_species)} species)", expanded=False):
            st.dataframe(species_df, use_container_width=True)


    # most observerd species in PIF & regional
    watchlist_df = filtered_df[filtered_df['PIF_Watchlist_Status'] == 1]
    regional_df = filtered_df[filtered_df['Regional_Stewardship_Status'] == 1]

    def get_most_common_species(df, label):
        if not df.empty and not df['Common_Name'].empty:
            species_counts = df['Common_Name'].value_counts()
            most_common = species_counts.idxmax()
            count = species_counts.max()
            st.subheader(f"🔍 Most Frequently Observed {label} Species")
            st.markdown(f"**{most_common}** was observed **{count}** times.")
        else:
            st.warning(f"⚠️ No {label} species observations found.")
    get_most_common_species(watchlist_df, "PIF Watchlist")
    get_most_common_species(regional_df, "Regional Stewardship")



# Ratio for male to female
def show_ratio_chart():
    st.subheader("📊 Ratio for Male to Female")
    sex_counts = filtered_df.groupby(['Common_Name', 'Sex']).size().unstack(fill_value=0)
    sex_counts['Male'] = sex_counts.get('Male', 0)
    sex_counts['Female'] = sex_counts.get('Female', 0)
    sex_counts['Male_to_Female_Ratio'] = sex_counts['Male'] / sex_counts['Female'].replace(0, float('nan'))
    top_species = sex_counts.sort_values('Male_to_Female_Ratio', ascending=False).head(20).reset_index()
    fig = px.bar(top_species, x="Common_Name", y="Male_to_Female_Ratio", text='Male_to_Female_Ratio')
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(yaxis_range=[0, top_species['Male_to_Female_Ratio'].max()*1.1])
    st.plotly_chart(fig, use_container_width=True)

    # Count of Male & Female by Location
    st.subheader("🧮 Count of Male & Female by Location")
    sex_loca = (filtered_df.groupby(['Location_Type', 'Sex']).size().reset_index(name="count")
                .pivot(index="Location_Type", columns="Sex", values="count").fillna(0))
    fig_count = px.imshow(sex_loca, color_continuous_scale="YlGnBu",
                          labels={"x": "Gender", "y": "Location", "color": "Count"})
    st.plotly_chart(fig_count, use_container_width=True)
                


# Sightings Over Interval & Distance
def show_Interval_Distance():
    # Average Observation Distance
    st.subheader("🧮Species by Average Observation Distance (Closest & Farthest)")
    distance_summary = (filtered_df.groupby('Common_Name')['Distance_Mid'].mean().sort_values())
    closest_species = distance_summary
    farthest_species = distance_summary
    combined = pd.concat([closest_species, farthest_species]).reset_index()
    combined.columns = ['Common_Name', 'Distance_Mid']
    fig = px.bar(combined,x='Distance_Mid',y='Common_Name',orientation='h',color_continuous_scale='Viridis',color='Distance_Mid')
    fig.update_layout(xaxis_title='Avg Observation Distance',yaxis_title='Common Name',width=5000,height=800)
    st.plotly_chart(fig, use_container_width=True)

    #species by interval duration
    st.subheader("⏱️Species Activity Types by Interval Duration")
    count_data = (filtered_df.groupby(['ID_Method', 'Interval_Duration']).size().reset_index(name='Count'))
    fig = px.bar(count_data,x='ID_Method',y='Count',color='Interval_Duration')
    fig.update_layout(xaxis_title='ID Method',yaxis_title='Count',
                      legend_title='Interval Duration',width=1000,height=600)
    st.plotly_chart(fig) 

   
    

sections = {
    "📅 Sightings Over Month": show_time_series,
    "🕊️ Top Species": show_top_species,
    "🌡️ Sightings Over Temp": show_temperature_vs_sightings,
    "🌦️ Environmental Conditions": show_environmental_conditions,
    "🧭 Sightings Over Observer": show_observer_heatmap,
    "📈 High-Activity Regions": show_high_activity_regions,
    "⏱️ Sightings Over Interval & Distance": show_Interval_Distance,
    "📊 Ratio for Male to Female": show_ratio_chart,
}

selected = st.sidebar.radio("Go to Section:", list(sections.keys()))
try:
    sections[selected]()  # Call the selected section
except Exception as e:
    st.error(f"🚨 Error in '{selected}' section: {e}")


