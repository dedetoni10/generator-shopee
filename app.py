import streamlit as st

# Mengatur tampilan halaman agar rapi
st.set_page_config(page_title="Generator Prompt Shopee", page_icon="📝", layout="wide")

st.title("🛍️ Generator Prompt Thumbnail (Arsitektur 3 Gambar)")
st.write("Masukkan data produk, atur efek, dan tentukan detail ide kompetitor untuk merakit teks prompt otomatis.")

# --- FITUR RIWAYAT WATERMARK ---
if 'riwayat_watermark' not in st.session_state:
    st.session_state['riwayat_watermark'] = ["NAURA ULFA"]

st.write("---")

# Bagian 1: Pengaturan Watermark Toko
st.subheader("1. Pengaturan Watermark Toko")
opsi_watermark = st.radio(
    "Apakah Anda ingin menambahkan watermark teks buatan AI pada gambar?",
    options=[
        "A. Ya, tambahkan watermark teks transparan", 
        "B. Tidak perlu (Produk sudah ada logo fisik / Biarkan bersih)"
    ]
)

watermark_final = ""
if "Ya" in opsi_watermark:
    pilihan_sejarah = st.selectbox(
        "Pilih dari Riwayat (Opsional):",
        options=["(Ketik Baru)"] + st.session_state['riwayat_watermark']
    )

    if pilihan_sejarah == "(Ketik Baru)":
        watermark_final = st.text_input("Nama Watermark:", placeholder="Ketik nama toko di sini...")
    else:
        watermark_final = st.text_input("Nama Watermark:", value=pilihan_sejarah)

st.write("---")

# Bagian 2: Data Produk Baru
st.subheader("2. Data Produk Baru")
judul_produk = st.text_input("Judul Produk", placeholder="Contoh: Kapasitor Bulat Kabel Kapasitor Pompa Air 6uf...")
deskripsi_produk = st.text_area("Deskripsi / Detail Produk", placeholder="Contoh:\nHarga per 1 biji\nTersedia ukuran 6uf, 8uf, dan 10uf\n450v\nBrand Lazaro")

st.write("---")

# Bagian 3: Detail Ide Spesifik dari Gambar 2
st.subheader("3. Detail Ide Spesifik dari Gambar 2 (Foto Kompetitor)")
ide_gambar2 = st.text_area(
    "Ketik ide, detail teknis, atau komponen spesifik apa yang mau diambil dari Gambar 2:",
    placeholder="Contoh: Ambil ide posisi tata letak kabel yang melingkar rapi di samping produk, serta perjelas detail terminal sekrup presisinya..."
)

st.write("---")

# Bagian 4: Efek Visual Tambahan
st.subheader("4. Efek Visual Tambahan (Opsional)")
pilihan_efek = st.multiselect(
    "Centang efek estetika untuk background foto (bisa pilih lebih dari satu):",
    options=[
        "Asap putih tipis (wispy white smoke)",
        "Pantulan kaca/air di bawah produk (Glossy reflection)",
        "Cahaya neon halus (Subtle neon glow)",
        "Percikan air segar (Water splashes)",
        "Bayangan daun estetik (Aesthetic leaf shadow/Gobo)"
    ]
)

efek_manual = st.text_input("Atau ketik manual efek lainnya:", placeholder="Contoh: Taburan serpihan emas di udara...")

semua_efek = pilihan_efek.copy()
if efek_manual.strip() != "":
    semua_efek.append(efek_manual.strip())

teks_efek_tambahan = ""
if len(semua_efek) > 0:
    gabungan_efek = ", ".join(semua_efek)
    teks_efek_tambahan = f"\n\nEFEK VISUAL TAMBAHAN:\nTambahkan elemen estetika berupa: {gabungan_efek}. Aplikasikan efek ini pada area background atau di sekitar produk secara halus, proporsional, dan elegan. Efek ini berfungsi untuk mempercantik suasana (mood) foto TANPA menutupi, mendistraksi, atau merusak detail fisik dari produk utama."

st.write("---")

# Bagian 5: Opsi Sudut Pandang (Angle)
st.subheader("5. Opsi Sudut Pandang (Angle) Produk")
pilihan_angle = st.radio(
    "Pilih perlakuan angle untuk produk Anda:",
    options=[
        "A. Gunakan Angle Asli (Paling Aman, anti berubah bentuk)", 
        "B. Ubah Angle Dinamis (Beresiko, cocok untuk bentuk sederhana)"
    ]
)

if "Gunakan Angle Asli" in pilihan_angle:
    teks_angle_instruksi = "Pertahankan sudut pandang (angle) produk PERSIS SAMA seperti pada Gambar 1. JANGAN memutar, memiringkan, atau mengubah perspektif produk sedikit pun untuk menghindari distorsi bentuk."
else:
    teks_angle_instruksi = "Ubah sedikit sudut pandang (angle) produk agar lebih dinamis (misalnya agak dimiringkan atau diputar sedikit) dengan mengikuti tata letak dari Gambar 2. PERINGATAN KERAS: Saat mengubah angle, Anda WAJIB mempertahankan geometri 3D, anatomi, dan bentuk asli produk secara mutlak seperti pada Gambar 1. JANGAN menambah atau mengurangi komponen fisik apa pun. Jika perubahan angle memicu distorsi bentuk, prioritaskan keaslian bentuk daripada angle."

st.write("---")

# Bagian 6: Pilihan Jenis Prompt
st.subheader("6. Pilih Jenis Prompt")
jenis_prompt = st.radio(
    "Mau merakit prompt untuk gambar yang mana?",
    options=[
        "1. Thumbnail Utama", 
        "2. Foto Detail Pendukung (Close-up)"
    ]
)

st.write("---")

# Tombol Eksekusi
if st.button("Rakit Teks Prompt", type="primary"):
    # Validasi input
    if "Ya" in opsi_watermark and not watermark_final:
        st.warning("Mohon isi Nama Watermark terlebih dahulu.")
    elif not judul_produk:
        st.warning("Mohon isi Judul Produk terlebih dahulu.")
    elif not ide_gambar2:
        st.warning("Mohon isi detail ide spesifik dari Gambar 2 terlebih dahulu.")
    else:
        # Menyimpan nama baru ke riwayat secara otomatis jika menggunakan watermark
        if "Ya" in opsi_watermark and watermark_final not in st.session_state['riwayat_watermark']:
            st.session_state['riwayat_watermark'].append(watermark_final)
            
        # --- PERSIAPAN LOGIKA WATERMARK ---
        if "Ya" in opsi_watermark:
            teks_watermark_prompt1 = f"""4. Watermark:
Tambahkan watermark transparan bertuliskan “{watermark_final}” tepat di area tengah (center) produk. Buat tipis, elegan, dan semi-transparan (opacity rendah) agar menyatu dengan desain. Watermark tidak boleh merusak tampilan produk, namun tetap cukup terbaca sebagai penanda kepemilikan."""
            
