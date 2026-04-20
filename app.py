import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Konfigurasi Halaman
st.set_page_config(page_title="Simulasi Pembagian Lembar Jawaban", page_icon="📝")

st.title("📝 Simulasi Discrete Event: Pembagian Lembar Jawaban")
st.markdown("""
Aplikasi ini mensimulasikan proses pembagian lembar jawaban ujian secara antrian (FIFO).
Silakan masukkan parameter di samping kiri untuk melihat hasil simulasi, verifikasi, dan validasi sederhana.
""")

# Sidebar Input
st.sidebar.header("Parameter Simulasi")
n_mahasiswa = st.sidebar.slider("Jumlah Mahasiswa (N)", 1, 100, 30)
min_durasi = st.sidebar.number_input("Durasi Minimum (menit)", 0.5, 5.0, 1.0)
max_durasi = st.sidebar.number_input("Durasi Maksimum (menit)", 1.0, 10.0, 3.0)
random_seed = st.sidebar.number_input("Random Seed (untuk Reproduksibilitas)", 0, 1000, 42)

if min_durasi >= max_durasi:
    st.error("Durasi Minimum harus lebih kecil dari Durasi Maksimum!")
    st.stop()

# Fungsi Simulasi (Sama seperti di Notebook)
def run_sim(n, min_t, max_t, seed):
    np.random.seed(seed)
    services = np.random.uniform(min_t, max_t, n)
    current_time = 0
    data = []
    for i in range(n):
        start = current_time
        end = start + services[i]
        data.append({
            'Mahasiswa': i+1,
            'Durasi': services[i],
            'Mulai': start,
            'Selesai': end
        })
        current_time = end
    df = pd.DataFrame(data)
    total_time = df['Selesai'].max()
    avg_wait = 0 # Dalam model FIFO ketat tanpa gap kedatangan, wait time relatif terhadap server busy
    # Namun untuk visualisasi, kita bisa hitung waktu tunggu kumulatif jika ada gap, 
    # tapi di kasus ini server selalu busy jadi wait time = 0 relative to previous finish.
    # Kita tampilkan Total Time dan Utilisasi.
    utilization = df['Durasi'].sum() / total_time if total_time > 0 else 0
    return df, total_time, utilization

# Jalankan Simulasi
df_res, total_t, util = run_sim(n_mahasiswa, min_durasi, max_durasi, random_seed)

# Tampilan Hasil Utama
col1, col2, col3 = st.columns(3)
col1.metric("Total Waktu Selesai", f"{total_t:.2f} Menit")
col2.metric("Rata-rata Durasi/Orang", f"{df_res['Durasi'].mean():.2f} Menit")
col3.metric("Utilisasi Dosen", f"{util*100:.1f}%")

st.subheader("📊 Tabel Detail Antrian (5 Data Pertama)")
st.dataframe(df_res.head())

st.subheader("📈 Grafik Waktu Selesai Kumulatif")
fig, ax = plt.subplots()
ax.plot(df_res['Mahasiswa'], df_res['Selesai'], marker='o', linestyle='-', color='b')
ax.set_xlabel("Urutan Mahasiswa")
ax.set_ylabel("Waktu Selesai (Menit)")
ax.set_title("Progres Pembagian Lembar Jawaban")
ax.grid(True)
st.pyplot(fig)

st.subheader("✅ Analisis Verifikasi & Validasi Singkat")
st.info(f"""
- **Verifikasi Logika**: Antrian berjalan FIFO. Mahasiswa ke-{n_mahasiswa} selesai pada menit {total_t:.2f}.
- **Validasi Teoritis**: Dengan rentang [{min_durasi}, {max_durasi}], rata-rata teoritis adalah {(min_durasi+max_durasi)/2:.2f} menit.
  Estimasi kasar total waktu: {n_mahasiswa * ((min_durasi+max_durasi)/2):.2f} menit.
  Hasil Simulasi: {total_t:.2f} menit. (Selisih akibat variasi acak).
""")

st.markdown("---")
st.caption("Dibuat untuk Tugas Modsim 2026 - [Fanesha Dwi Fanny Br.Silalahi]")