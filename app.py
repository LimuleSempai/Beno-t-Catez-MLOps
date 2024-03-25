import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
@st.cache
def load_data():
    df = pd.read_csv('housing.csv')
    return df

# Preprocessing
def preprocess_data(df):
    df = df[df['total_bedrooms'].notnull()]
    for element in df['ocean_proximity'].unique():
        df[element]= df['ocean_proximity'].apply(lambda x: 1 if x == element else 0)
    df = df.drop('ocean_proximity', axis=1)
    return df

# Visualizations
def show_histogram(df):
    st.subheader('Histogram of Median House Value')
    plt.figure(figsize=(8, 6))
    sns.histplot(df['median_house_value'], bins=30, kde=True)
    st.pyplot()

def show_scatterplot(df):
    st.subheader('Scatterplot of Latitude vs Longitude')
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='longitude', y='latitude', data=df, alpha=0.5)
    st.pyplot()

def show_correlation_heatmap(df):
    st.subheader('Correlation Heatmap')
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
    st.pyplot()

def main():
    st.title('California Housing Data Exploration')
    st.write("""
    ## Exploring California Housing Data
    """)
    
    df = load_data()
    df = preprocess_data(df)

    st.write("### Sample of the Dataset")
    st.write(df.head())

    st.write("### Dataset Description")
    st.write(df.describe())

    st.write("### Dataset Information")
    st.write(df.info())

    # Visualization
    show_histogram(df)
    show_scatterplot(df)
    show_correlation_heatmap(df)

if __name__ == "__main__":
    main()
