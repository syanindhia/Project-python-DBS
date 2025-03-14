import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Judul Dashboard
st.title("Nongzhanguan Air Quality Dashboard")

# Load dataset
file_path = "imputed_Nongzhanguan.csv"
df = pd.read_csv(file_path)

# Konversi ke datetime
df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])

# Sidebar
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Start Date", df['datetime'].min().date())
end_date = st.sidebar.date_input("End Date", df['datetime'].max().date())

# Sidebar - Time Frame
time_frame = st.sidebar.selectbox("Time Frame", ["Daily", "Weekly", "Monthly", "Yearly"])

# Sidebar - Parameter Polusi
selected_parameter = st.sidebar.selectbox("Parameter", ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3", "TEMP", "PRES", "DEWP", "RAIN", "WSPM"])

# Filter Data berdasarkan Tanggal
filtered_df = df[(df["datetime"].dt.date >= start_date) & (df["datetime"].dt.date <= end_date)].copy()

# Set datetime sebagai index sebelum resampling
filtered_df.set_index("datetime", inplace=True)

# Pastikan hanya kolom numerik yang diproses saat resampling
numeric_cols = filtered_df.select_dtypes(include="number").columns
filtered_df = filtered_df[numeric_cols]  # Ambil hanya kolom numerik

# Resampling Data sesuai Time Frame
if time_frame == "Daily":
    filtered_df = filtered_df.resample("D").mean()
elif time_frame == "Weekly":
    filtered_df = filtered_df.resample("W").mean()
elif time_frame == "Monthly":
    filtered_df = filtered_df.resample("ME").mean()
elif time_frame == "Yearly":
    filtered_df = filtered_df.resample("YE").mean()

# Reset index setelah resampling
filtered_df = filtered_df.reset_index()

# Rata-rata Polutan Secara Interaktif
st.subheader("Average Pollutant Levels Based on Selected Period")
col1, col2, col3, col4, col5 = st.columns(5)
polutan_list = ["PM2.5", "PM10", "NO2", "CO", "O3"]

filtered_means = {param: filtered_df[param].mean() for param in polutan_list if param in filtered_df.columns}

# Menampilkan nilai rata-rata dalam kolom
with col1:
    st.metric(label="PM2.5 (µg/m³)", value=f"{filtered_means.get('PM2.5', 0):.2f}")

with col2:
    st.metric(label="PM10 (µg/m³)", value=f"{filtered_means.get('PM10', 0):.2f}")

with col3:
    st.metric(label="NO2 (µg/m³)", value=f"{filtered_means.get('NO2', 0):.2f}")

with col4:
    st.metric(label="CO (µg/m³)", value=f"{filtered_means.get('CO', 0):.2f}")

with col5:
    st.metric(label="O3 (µg/m³)", value=f"{filtered_means.get('O3', 0):.2f}")

# Grafik Tren Waktu
st.subheader(f"Tren {selected_parameter} ({time_frame.lower()})")
fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(data=filtered_df, x="datetime", y=selected_parameter, ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# Heatmap Korelasi Interaktif
st.subheader("Heatmap Korelasi")

# Pilihan variabel untuk korelasi
selected_corr_columns = st.multiselect("Pilih variabel untuk korelasi:", df.columns, default=df.columns[:6])

# Pilihan colormap
colormap_options = ["coolwarm", "viridis", "plasma", "magma", "cividis"]
selected_colormap = st.selectbox("Pilih skema warna:", colormap_options, index=0)

# Checkbox untuk menampilkan nilai korelasi
show_corr_values = st.checkbox("Tampilkan nilai korelasi", value=True)

# Filter dataset berdasarkan pilihan pengguna
if selected_corr_columns:
    corr_matrix = filtered_df[selected_corr_columns].corr()

    # Plot heatmap
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(corr_matrix, annot=show_corr_values, cmap=selected_colormap, fmt=".2f", ax=ax)

    ax.set_title("Matriks Korelasi")

    # Tampilkan di Streamlit
    st.pyplot(fig)
else:
    st.warning("Pilih minimal dua variabel untuk menampilkan heatmap.")

st.caption('Dicoding Coding Camp powered by DBS Foundation')