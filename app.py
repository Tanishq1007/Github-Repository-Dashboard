import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


df = pd.read_csv('github_dataset.csv')


st.set_page_config(page_title='GitHub Repository Dashboard', layout='wide')


st.sidebar.header('Filters')


languages = df['language'].unique().tolist() if 'language' in df.columns else []
selected_languages = st.sidebar.multiselect('Select Repository Languages', languages, default=languages)


min_stars = int(df['stars_count'].min()) if 'stars_count' in df.columns else 0
max_stars = int(df['stars_count'].max()) if 'stars_count' in df.columns else 100
stars_range = st.sidebar.slider('Select Star Range', min_stars, max_stars, (min_stars, max_stars))


filtered_df = df[(df['language'].isin(selected_languages)) & 
                 (df['stars_count'].between(stars_range[0], stars_range[1]))]


st.header('Key Metrics')
total_repositories = len(filtered_df)
total_stars = filtered_df['stars_count'].sum()
average_forks = filtered_df['forks_count'].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Total Repositories", total_repositories)
col2.metric("Total Stars", total_stars)
col3.metric("Average Forks", f"{average_forks:.2f}")


st.subheader('Filtered Dataset Overview')
st.write(filtered_df.head())

st.subheader('Repository Language Distribution')
if 'language' in filtered_df.columns:
    language_counts = filtered_df['language'].value_counts()
    fig1 = px.pie(values=language_counts.values, names=language_counts.index, 
                  title='Languages Used in Repositories',
                  color_discrete_sequence=px.colors.sequential.Rainbow)
    st.plotly_chart(fig1)


st.subheader('Star Distribution')

if 'stars_count' in filtered_df.columns:
    # Create bins for star counts
    bins = [0, 5, 10, 20, 50, 100, 200, 500, 1000]  # Define bin edges
    labels = ['0-5', '6-10', '11-20', '21-50', '51-100', '101-200', '201-500', '501-1000']  # Labels for bins
    filtered_df['stars_bins'] = pd.cut(filtered_df['stars_count'], bins=bins, labels=labels, right=False)

    # Count the number of repositories in each bin
    star_distribution = filtered_df['stars_bins'].value_counts().sort_index()

    # Create a bar graph
    fig2 = px.bar(
        x=star_distribution.index,
        y=star_distribution.values,
        labels={'x': 'Stars Count', 'y': 'Number of Repositories'},
        title='Star Distribution',
        color=star_distribution.values,
        color_continuous_scale=px.colors.sequential.Viridis,
    )

    # Update layout
    fig2.update_layout(
        height=500,
        xaxis_title='Stars Count',
        yaxis_title='Number of Repositories',
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
    )

    st.plotly_chart(fig2)


st.subheader('3D Scatter Plot: Forks vs Stars vs Issues')

if 'stars_count' in filtered_df.columns and 'forks_count' in filtered_df.columns and 'issues_count' in filtered_df.columns:
    fig3d = px.scatter_3d(
        filtered_df,
        x='stars_count',
        y='forks_count',
        z='issues_count',
        color='language',
        title='3D Visualization of Forks vs Stars vs Issues',
        hover_name='repositories',
        hover_data={
            'stars_count': True,
            'forks_count': True,
            'issues_count': True
        },
        size_max=10,
    )

   
    fig3d.update_layout(
        scene=dict(
            xaxis_title='Stars Count',
            yaxis_title='Forks Count',
            zaxis_title='Issues Count'
        ),
        title_font_size=20,
        title_x=0.5,  
    )

    st.plotly_chart(fig3d)

st.subheader('Search Repositories by Name')
search_term = st.text_input('Enter Repository Name:')
if search_term:
    search_results = filtered_df[filtered_df['repositories'].str.contains(search_term, case=False, na=False)]
    st.write(search_results)


st.sidebar.markdown("**Dashboard created by Tanishq**")
