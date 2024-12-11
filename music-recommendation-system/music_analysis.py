from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import matplotlib.pyplot as plt

# Initialize a Spark session
spark = SparkSession.builder.appName("DataVisualization").getOrCreate()

# Load CSV files into PySpark DataFrames
file_by_year = "/public/data_by_year.csv"
file_by_genres = "/public/data_by_genres.csv"

df_by_year = spark.read.csv(file_by_year, header=True, inferSchema=True)
df_by_genres = spark.read.csv(file_by_genres, header=True, inferSchema=True)

# Data Exploration and Visualization
# Convert Spark DataFrames to Pandas for visualizations
pdf_by_year = df_by_year.toPandas()
pdf_by_genres = df_by_genres.toPandas()

# Visualization 1: Trend of Popularity Over Years
plt.figure(figsize=(12, 6))
plt.plot(pdf_by_year['year'], pdf_by_year['popularity'], marker='o')
plt.title('Trend of Popularity Over Years')
plt.xlabel('Year')
plt.ylabel('Popularity')
plt.grid()
plt.show()

# Visualization 2: Average Danceability of Genres
top_genres = pdf_by_genres.groupby('genres')['danceability'].mean().sort_values(ascending=False).head(10)
top_genres.plot(kind='bar', figsize=(12, 6))
plt.title('Top 10 Genres by Average Danceability')
plt.xlabel('Genres')
plt.ylabel('Average Danceability')
plt.xticks(rotation=45)
plt.grid()
plt.show()

# Visualization 3: Energy vs Popularity Scatter Plot (Yearly Data)
plt.figure(figsize=(12, 6))
plt.scatter(pdf_by_year['energy'], pdf_by_year['popularity'], alpha=0.6)
plt.title('Energy vs Popularity')
plt.xlabel('Energy')
plt.ylabel('Popularity')
plt.grid()
plt.show()

# Additional PySpark Processing Example
# Example: Calculate the average popularity by genre
avg_popularity_by_genre = df_by_genres.groupBy("genres").avg("popularity").orderBy(col("avg(popularity)").desc())
avg_popularity_by_genre.show(10)
