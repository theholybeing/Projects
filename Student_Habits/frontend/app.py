import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

df = pd.read_csv("C:/Users/Mystic/Desktop/Student_Habits/data/student_habits_performance.csv")

st.title("📊 Student Habits & Exam Performance Dashboard")

if st.checkbox("🔍 Show Raw Data"):
    st.write(df)

habit = st.selectbox(
    "📌 Select Habit to Explore by Gender",
    ["study_hours_per_day", "social_media_hours", "sleep_hours"]
)

st.subheader(f"📦 {habit.replace('_', ' ').title()} by Gender")
fig1, ax1 = plt.subplots()
sns.boxplot(x='gender', y=habit, data=df, ax=ax1)
st.pyplot(fig1)

st.subheader("🔗 Correlation Heatmap")
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm', ax=ax2)
st.pyplot(fig2)

st.subheader("📈 Explore Relationships Between Two Features")
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
x_axis = st.selectbox("X-Axis", numeric_cols, index=0)
y_axis = st.selectbox("Y-Axis", numeric_cols, index=1)

fig3, ax3 = plt.subplots()
sns.scatterplot(x=df[x_axis], y=df[y_axis], hue=df['gender'], ax=ax3)
ax3.set_xlabel(x_axis.replace("_", " ").title())
ax3.set_ylabel(y_axis.replace("_", " ").title())
st.pyplot(fig3)

st.subheader("🧠 Student Clustering with PCA")

features = df.drop(columns=['student_id', 'exam_score'])
features = pd.get_dummies(features, drop_first=True)
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(features_scaled)
df['cluster'] = clusters

pca = PCA(n_components=2)
pca_components = pca.fit_transform(features_scaled)

fig4, ax4 = plt.subplots()
scatter = ax4.scatter(pca_components[:, 0], pca_components[:, 1], c=clusters, cmap='viridis')
ax4.set_title("PCA View of Student Clusters")
ax4.set_xlabel("PCA Component 1")
ax4.set_ylabel("PCA Component 2")
st.pyplot(fig4)