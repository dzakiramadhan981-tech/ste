import streamlit as st
import pandas as pd
import re
import os
import json
import time
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Tuple
import hashlib
import random

# KELAS DASAR & ENKAPSULASI

class Mahasiswa:
    """Kelas untuk merepresentasikan data mahasiswa dengan enkapsulasi"""
    def __init__(self, nim: str, nama: str, jurusan: str = "Teknik Informatika", angkatan: str = "2024"):
        self.__nim = nim  # Private attribute
        self.__nama = nama  # Private attribute
        self.__jurusan = jurusan  # Private attribute
        self.__angkatan = angkatan  # Private attribute
    
    # Getter methods
    @property
    def nim(self) -> str:
        return self.__nim
    
    @property
    def nama(self) -> str:
        return self.__nama
    
    @property
    def jurusan(self) -> str:
        return self.__jurusan
    
    @property
    def angkatan(self) -> str:
        return self.__angkatan
    
    # Setter methods
    @nim.setter
    def nim(self, nim: str):
        if self._validasi_nim(nim):
            self.__nim = nim
        else:
            raise ValueError("NIM tidak valid")
    
    @nama.setter
    def nama(self, nama: str):
        if self._validasi_nama(nama):
            self.__nama = nama
        else:
            raise ValueError("Nama tidak valid")
    
    @jurusan.setter
    def jurusan(self, jurusan: str):
        self.__jurusan = jurusan
    
    @angkatan.setter
    def angkatan(self, angkatan: str):
        self.__angkatan = angkatan
    
    # Validasi private methods
    def _validasi_nim(self, nim: str) -> bool:
        """Validasi NIM menggunakan regex"""
        pattern = r'^\d{9,12}$'
        return bool(re.match(pattern, nim))
    
    def _validasi_nama(self, nama: str) -> bool:
        """Validasi nama menggunakan regex"""
        pattern = r'^[A-Za-z\s\.\,]{3,50}$'
        return bool(re.match(pattern, nama))
    
    def to_dict(self) -> Dict:
        """Mengembalikan data mahasiswa sebagai dictionary"""
        return {
            'nim': self.__nim,
            'nama': self.__nama,
            'jurusan': self.__jurusan,
            'angkatan': self.__angkatan
        }
    
    def __str__(self) -> str:
        return f"{self.__nim} - {self.__nama} - {self.__jurusan}"

# ==============================
# INHERITANCE & POLYMORPHISM
# ==============================

class DataMahasiswa(ABC):
    """Abstract Base Class untuk manajemen data mahasiswa"""
    
    @abstractmethod
    def tambah(self, mahasiswa: Mahasiswa) -> bool:
        pass
    
    @abstractmethod
    def hapus(self, nim: str) -> bool:
        pass
    
    @abstractmethod
    def cari(self, keyword: str) -> List[Mahasiswa]:
        pass

class ManajemenMahasiswa(DataMahasiswa):
    """Kelas untuk mengelola data mahasiswa menggunakan array dan pointer"""
    
    def __init__(self):
        self.__data = []  # Private array untuk menyimpan data
        self.__pointer = 0  # Pointer untuk iterasi
    
    # Implementasi metode abstract
    def tambah(self, mahasiswa: Mahasiswa) -> bool:
        """Menambahkan mahasiswa ke dalam array"""
        try:
            # Cek duplikasi NIM
            for m in self.__data:
                if m.nim == mahasiswa.nim:
                    raise ValueError(f"Mahasiswa dengan NIM {mahasiswa.nim} sudah ada")
            
            self.__data.append(mahasiswa)
            return True
        except Exception as e:
            raise e
    
    def hapus(self, nim: str) -> bool:
        """Menghapus mahasiswa berdasarkan NIM"""
        for i, m in enumerate(self.__data):
            if m.nim == nim:
                del self.__data[i]
                return True
        return False
    
    def cari(self, keyword: str) -> List[Mahasiswa]:
        """Mencari mahasiswa berdasarkan keyword (NIM atau Nama)"""
        hasil = []
        for m in self.__data:
            if keyword.lower() in m.nim.lower() or keyword.lower() in m.nama.lower():
                hasil.append(m)
        return hasil
    
    # Metode tambahan
    def edit(self, nim_lama: str, mahasiswa_baru: Mahasiswa) -> bool:
        """Mengedit data mahasiswa"""
        for i, m in enumerate(self.__data):
            if m.nim == nim_lama:
                # Cek jika NIM baru sudah ada (kecuali NIM sama)
                if nim_lama != mahasiswa_baru.nim:
                    for m2 in self.__data:
                        if m2.nim == mahasiswa_baru.nim:
                            raise ValueError(f"Mahasiswa dengan NIM {mahasiswa_baru.nim} sudah ada")
                
                self.__data[i] = mahasiswa_baru
                return True
        return False
    
    def get_semua(self) -> List[Mahasiswa]:
        """Mengembalikan semua data mahasiswa"""
        return self.__data.copy()
    
    def get_by_nim(self, nim: str) -> Optional[Mahasiswa]:
        """Mengembalikan mahasiswa berdasarkan NIM"""
        for m in self.__data:
            if m.nim == nim:
                return m
        return None
    
    def jumlah(self) -> int:
        """Mengembalikan jumlah mahasiswa"""
        return len(self.__data)
    
    def __iter__(self):
        """Mengimplementasikan iterator"""
        self.__pointer = 0
        return self
    
    def __next__(self):
        """Mengembalikan elemen berikutnya dalam iterasi"""
        if self.__pointer < len(self.__data):
            result = self.__data[self.__pointer]
            self.__pointer += 1
            return result
        else:
            raise StopIteration

# ==============================
# ALGORITMA PENCARIAN
# ==============================

class AlgoritmaPencarian:
    """Kelas untuk implementasi berbagai algoritma pencarian"""
    
    @staticmethod
    def linear_search(data: List[Mahasiswa], keyword: str, by: str = 'nama') -> List[Mahasiswa]:
        """
        Linear Search - O(n)
        Mencari data secara sequential
        """
        hasil = []
        for m in data:
            if by == 'nama' and keyword.lower() in m.nama.lower():
                hasil.append(m)
            elif by == 'nim' and keyword in m.nim:
                hasil.append(m)
        return hasil
    
    @staticmethod
    def binary_search(data: List[Mahasiswa], nim: str) -> Optional[Mahasiswa]:
        """
        Binary Search - O(log n)
        Hanya bekerja pada data yang sudah terurut berdasarkan NIM
        """
        # Pastikan data terurut berdasarkan NIM
        data_sorted = sorted(data, key=lambda x: x.nim)
        
        low = 0
        high = len(data_sorted) - 1
        
        while low <= high:
            mid = (low + high) // 2
            if data_sorted[mid].nim == nim:
                return data_sorted[mid]
            elif data_sorted[mid].nim < nim:
                low = mid + 1
            else:
                high = mid - 1
        return None
    
    @staticmethod
    def sequential_search(data: List[Mahasiswa], keyword: str) -> List[Mahasiswa]:
        """
        Sequential Search - O(n)
        Variasi dari linear search
        """
        hasil = []
        i = 0
        n = len(data)
        
        while i < n:
            if keyword.lower() in data[i].nama.lower() or keyword in data[i].nim:
                hasil.append(data[i])
            i += 1
        return hasil

# ==============================
# ALGORITMA PENGURUTAN
# ==============================

class AlgoritmaPengurutan:
    """Kelas untuk implementasi berbagai algoritma pengurutan"""
    
    @staticmethod
    def bubble_sort(data: List[Mahasiswa], by: str = 'nim', ascending: bool = True) -> List[Mahasiswa]:
        """
        Bubble Sort - O(n²)
        Mengurutkan data dengan metode bubble sort
        """
        n = len(data)
        data_copy = data.copy()
        
        for i in range(n):
            for j in range(0, n - i - 1):
                if by == 'nim':
                    condition = data_copy[j].nim > data_copy[j + 1].nim if ascending else data_copy[j].nim < data_copy[j + 1].nim
                else:  # by == 'nama'
                    condition = data_copy[j].nama > data_copy[j + 1].nama if ascending else data_copy[j].nama < data_copy[j + 1].nama
                
                if condition:
                    data_copy[j], data_copy[j + 1] = data_copy[j + 1], data_copy[j]
        
        return data_copy
    
    @staticmethod
    def selection_sort(data: List[Mahasiswa], by: str = 'nim', ascending: bool = True) -> List[Mahasiswa]:
        """
        Selection Sort - O(n²)
        Mengurutkan data dengan metode selection sort
        """
        n = len(data)
        data_copy = data.copy()
        
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if by == 'nim':
                    condition = data_copy[j].nim < data_copy[min_idx].nim if ascending else data_copy[j].nim > data_copy[min_idx].nim
                else:  # by == 'nama'
                    condition = data_copy[j].nama < data_copy[min_idx].nama if ascending else data_copy[j].nama > data_copy[min_idx].nama
                
                if condition:
                    min_idx = j
            
            data_copy[i], data_copy[min_idx] = data_copy[min_idx], data_copy[i]
        
        return data_copy
    
    @staticmethod
    def insertion_sort(data: List[Mahasiswa], by: str = 'nim', ascending: bool = True) -> List[Mahasiswa]:
        """
        Insertion Sort - O(n²)
        Mengurutkan data dengan metode insertion sort
        """
        data_copy = data.copy()
        
        for i in range(1, len(data_copy)):
            key = data_copy[i]
            j = i - 1
            
            while j >= 0:
                if by == 'nim':
                    condition = data_copy[j].nim > key.nim if ascending else data_copy[j].nim < key.nim
                else:  # by == 'nama'
                    condition = data_copy[j].nama > key.nama if ascending else data_copy[j].nama < key.nama
                
                if condition:
                    data_copy[j + 1] = data_copy[j]
                    j -= 1
                else:
                    break
            
            data_copy[j + 1] = key
        
        return data_copy
    
    @staticmethod
    def merge_sort(data: List[Mahasiswa], by: str = 'nim', ascending: bool = True) -> List[Mahasiswa]:
        """
        Merge Sort - O(n log n)
        Mengurutkan data dengan metode merge sort (rekursif)
        """
        if len(data) <= 1:
            return data.copy()
        
        mid = len(data) // 2
        left = AlgoritmaPengurutan.merge_sort(data[:mid], by, ascending)
        right = AlgoritmaPengurutan.merge_sort(data[mid:], by, ascending)
        
        return AlgoritmaPengurutan._merge(left, right, by, ascending)
    
    @staticmethod
    def _merge(left: List[Mahasiswa], right: List[Mahasiswa], by: str, ascending: bool) -> List[Mahasiswa]:
        """Helper method untuk merge sort"""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if by == 'nim':
                condition = left[i].nim < right[j].nim if ascending else left[i].nim > right[j].nim
            else:  # by == 'nama'
                condition = left[i].nama < right[j].nama if ascending else left[i].nama > right[j].nama
            
            if condition:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    @staticmethod
    def shell_sort(data: List[Mahasiswa], by: str = 'nim', ascending: bool = True) -> List[Mahasiswa]:
        """
        Shell Sort - O(n log n) sampai O(n²)
        Mengurutkan data dengan metode shell sort
        """
        n = len(data)
        data_copy = data.copy()
        gap = n // 2
        
        while gap > 0:
            for i in range(gap, n):
                temp = data_copy[i]
                j = i
                
                while j >= gap:
                    if by == 'nim':
                        condition = data_copy[j - gap].nim > temp.nim if ascending else data_copy[j - gap].nim < temp.nim
                    else:  # by == 'nama'
                        condition = data_copy[j - gap].nama > temp.nama if ascending else data_copy[j - gap].nama < temp.nama
                    
                    if condition:
                        data_copy[j] = data_copy[j - gap]
                        j -= gap
                    else:
                        break
                
                data_copy[j] = temp
            gap //= 2
        
        return data_copy

# ==============================
# FILE I/O OPERATIONS
# ==============================

class FileHandler:
    """Kelas untuk menangani operasi file I/O"""
    
    @staticmethod
    def simpan_ke_file(data: List[Mahasiswa], filename: str = 'data_mahasiswa.json'):
        """Menyimpan data mahasiswa ke file JSON"""
        try:
            data_dict = [m.to_dict() for m in data]
            with open(filename, 'w') as file:
                json.dump(data_dict, file, indent=4)
            return True
        except Exception as e:
            raise Exception(f"Gagal menyimpan ke file: {str(e)}")
    
    @staticmethod
    def baca_dari_file(filename: str = 'data_mahasiswa.json') -> List[Mahasiswa]:
        """Membaca data mahasiswa dari file JSON"""
        try:
            if not os.path.exists(filename):
                return []
            
            with open(filename, 'r') as file:
                data_dict = json.load(file)
            
            data_mahasiswa = []
            for item in data_dict:
                try:
                    mahasiswa = Mahasiswa(
                        nim=item['nim'],
                        nama=item['nama'],
                        jurusan=item.get('jurusan', 'Teknik Informatika'),
                        angkatan=item.get('angkatan', '2024')
                    )
                    data_mahasiswa.append(mahasiswa)
                except Exception as e:
                    print(f"Error parsing data: {item} - {str(e)}")
            
            return data_mahasiswa
        except Exception as e:
            raise Exception(f"Gagal membaca dari file: {str(e)}")

# ==============================
# AUTHENTICATION SYSTEM
# ==============================

class AuthSystem:
    """Sistem autentikasi untuk login"""
    
    def __init__(self):
        self.__users = {
            'admin': self._hash_password('admin123'),
            'dosen': self._hash_password('dosen123'),
            'mahasiswa': self._hash_password('mahasiswa123')
        }
    
    def _hash_password(self, password: str) -> str:
        """Hash password menggunakan SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self, username: str, password: str) -> bool:
        """Memvalidasi login"""
        if username in self.__users:
            return self.__users[username] == self._hash_password(password)
        return False

# ==============================
# STREAMLIT GUI APPLICATION
# ==============================

class AplikasiManajemenMahasiswa:
    """Kelas utama untuk aplikasi Streamlit"""
    
    def __init__(self):
        self.manajemen = ManajemenMahasiswa()
        self.auth = AuthSystem()
        self.file_handler = FileHandler()
        
        # Inisialisasi state session
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        if 'user_role' not in st.session_state:
            st.session_state.user_role = None
        if 'data_mahasiswa' not in st.session_state:
            st.session_state.data_mahasiswa = []
        
        # Load data dari file saat aplikasi dimulai
        self._load_data()
    
    def _load_data(self):
        """Memuat data dari file"""
        try:
            data = self.file_handler.baca_dari_file()
            for m in data:
                self.manajemen.tambah(m)
            st.session_state.data_mahasiswa = self.manajemen.get_semua()
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
    
    def _save_data(self):
        """Menyimpan data ke file"""
        try:
            self.file_handler.simpan_ke_file(self.manajemen.get_semua())
        except Exception as e:
            st.error(f"Error saving data: {str(e)}")
    
    def login_page(self):
        """Halaman login dengan desain modern"""
        # Background gradient animation
        self._animated_background()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Glassmorphism login card
            st.markdown("""
            <div class="glass-card login-card">
                <div class="login-header">
                    <h1 style="margin-bottom: 0;">🎓</h1>
                    <h2 style="margin-top: 0;">Sistem Manajemen Mahasiswa</h2>
                    <p>Silakan login untuk melanjutkan</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.container():
                st.markdown('<div class="glass-form">', unsafe_allow_html=True)
                
                username = st.text_input("👤 **Username**", placeholder="Masukkan username Anda")
                password = st.text_input("🔒 **Password**", type="password", placeholder="Masukkan password Anda")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("🚀 **Login**", use_container_width=True, type="primary"):
                        if self.auth.login(username, password):
                            st.session_state.logged_in = True
                            st.session_state.user_role = username
                            st.success("✅ Login berhasil!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Username atau password salah")
                
                with col_btn2:
                    if st.button("🔄 **Reset**", use_container_width=True):
                        st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Demo accounts
                with st.expander("📋 **Akun Demo**"):
                    st.markdown("""
                    | Role | Username | Password |
                    |------|----------|----------|
                    | Administrator | `admin` | `admin123` |
                    | Dosen | `dosen` | `dosen123` |
                    | Mahasiswa | `mahasiswa` | `mahasiswa123` |
                    """)
                
                # Stats
                st.markdown("""
                <div class="stats-card">
                    <div class="stat-item">
                        <span class="stat-icon">📊</span>
                        <span class="stat-text">Total Data: <strong>{}</strong></span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-icon">⏱️</span>
                        <span class="stat-text">Terakhir Update: <strong>{}</strong></span>
                    </div>
                </div>
                """.format(self.manajemen.jumlah(), datetime.now().strftime("%d/%m/%Y")), unsafe_allow_html=True)
    
    def main_page(self):
        """Halaman utama aplikasi"""
        # Header dengan gradient
        st.markdown("""
        <div class="main-header">
            <div class="header-content">
                <h1>🎓 <span class="gradient-text">Sistem Manajemen Data Mahasiswa</span></h1>
                <p>Mengelola data akademik dengan algoritma pencarian dan pengurutan</p>
            </div>
            <div class="user-badge">
                <span class="user-icon">👤</span>
                <span class="user-role">{}</span>
            </div>
        </div>
        """.format(st.session_state.user_role.upper()), unsafe_allow_html=True)
        
        # Stats bar
        self._display_stats_bar()
        
        # Sidebar menu dengan glassmorphism
        with st.sidebar:
            st.markdown("""
            <div class="sidebar-header">
                <h2>📋 Menu</h2>
            </div>
            """, unsafe_allow_html=True)
            
            menu_options = [
                ("📊 Dashboard", "dashboard"),
                ("➕ Tambah Data", "tambah"),
                ("✏️ Edit Data", "edit"),
                ("🗑️ Hapus Data", "hapus"),
                ("🔍 Pencarian", "pencarian"),
                ("📈 Pengurutan", "pengurutan"),
                ("📊 Visualisasi", "visualisasi"),
                ("ℹ️ Analisis Algoritma", "analisis"),
                ("🚪 Logout", "logout")
            ]
            
            selected_menu = st.radio(
                "Pilih Menu:",
                [opt[0] for opt in menu_options],
                label_visibility="collapsed"
            )
            
            # Get menu key
            menu_key = [opt[1] for opt in menu_options if opt[0] == selected_menu][0]
            
            st.markdown("---")
            
            # Quick actions
            st.markdown("### ⚡ Quick Actions")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Simpan", use_container_width=True):
                    self._save_data()
                    st.toast("✅ Data berhasil disimpan!", icon="✅")
            with col2:
                if st.button("🔄 Muat Ulang", use_container_width=True):
                    self._load_data()
                    st.toast("🔄 Data berhasil dimuat ulang!", icon="🔄")
            
            # Real-time stats
            st.markdown("---")
            st.markdown("### 📈 Statistik Real-time")
            
            data = self.manajemen.get_semua()
            if data:
                jurusan_counts = {}
                for m in data:
                    jurusan_counts[m.jurusan] = jurusan_counts.get(m.jurusan, 0) + 1
                
                most_common_jurusan = max(jurusan_counts, key=jurusan_counts.get)
                
                st.metric("👥 Total Mahasiswa", self.manajemen.jumlah())
                st.metric("🎓 Jurusan Terbanyak", most_common_jurusan)
                st.metric("📅 Tahun Aktif", "2024")
        
        # Konten berdasarkan menu
        if menu_key == "dashboard":
            self._dashboard()
        elif menu_key == "tambah":
            self._tambah_data()
        elif menu_key == "edit":
            self._edit_data()
        elif menu_key == "hapus":
            self._hapus_data()
        elif menu_key == "pencarian":
            self._pencarian_data()
        elif menu_key == "pengurutan":
            self._pengurutan_data()
        elif menu_key == "visualisasi":
            self._visualisasi_data()
        elif menu_key == "analisis":
            self._analisis_kompleksitas()
        elif menu_key == "logout":
            self._logout_page()
    
    def _display_stats_bar(self):
        """Menampilkan statistik bar"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stat-card blue-card">
                <div class="stat-icon">👥</div>
                <div class="stat-content">
                    <div class="stat-value">{self.manajemen.jumlah()}</div>
                    <div class="stat-label">Total Mahasiswa</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            data = self.manajemen.get_semua()
            jurusan_count = len(set([m.jurusan for m in data])) if data else 0
            st.markdown(f"""
            <div class="stat-card green-card">
                <div class="stat-icon">🎓</div>
                <div class="stat-content">
                    <div class="stat-value">{jurusan_count}</div>
                    <div class="stat-label">Jurusan</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            if data:
                angkatan_count = len(set([m.nim[:4] for m in data if len(m.nim) >= 4]))
            else:
                angkatan_count = 0
            st.markdown(f"""
            <div class="stat-card orange-card">
                <div class="stat-icon">📅</div>
                <div class="stat-content">
                    <div class="stat-value">{angkatan_count}</div>
                    <div class="stat-label">Angkatan</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            last_update = datetime.now().strftime("%H:%M")
            st.markdown(f"""
            <div class="stat-card purple-card">
                <div class="stat-icon">⏱️</div>
                <div class="stat-content">
                    <div class="stat-value">{last_update}</div>
                    <div class="stat-label">Terakhir Update</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def _dashboard(self):
        """Dashboard tampilan data dengan visualisasi"""
        st.markdown("## 📊 Dashboard Data Mahasiswa")
        
        # Quick filter
        with st.container(border=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_nim = st.text_input("🔍 Filter NIM", placeholder="Cari berdasarkan NIM...")
            with col2:
                filter_nama = st.text_input("🔍 Filter Nama", placeholder="Cari berdasarkan nama...")
            with col3:
                filter_jurusan = st.selectbox(
                    "🎓 Filter Jurusan",
                    ["Semua Jurusan"] + list(sorted(set([m.jurusan for m in self.manajemen.get_semua()])))
                )
        
        # Data tabel
        data = self.manajemen.get_semua()
        
        # Filter data
        if filter_nim:
            data = [m for m in data if filter_nim in m.nim]
        if filter_nama:
            data = [m for m in data if filter_nama.lower() in m.nama.lower()]
        if filter_jurusan != "Semua Jurusan":
            data = [m for m in data if m.jurusan == filter_jurusan]
        
        if data:
            # Tampilkan data dalam card grid
            st.subheader(f"📋 Data Mahasiswa ({len(data)} ditemukan)")
            
            # Grid layout untuk cards
            cols = st.columns(3)
            for idx, mahasiswa in enumerate(data[:12]):  # Tampilkan maksimal 12 card
                with cols[idx % 3]:
                    self._display_mahasiswa_card(mahasiswa)
            
            # Jika ada lebih dari 12 data, tampilkan tabel
            if len(data) > 12:
                with st.expander("📋 Lihat Semua Data dalam Tabel"):
                    df_data = []
                    for m in data:
                        df_data.append({
                            'NIM': m.nim,
                            'Nama': m.nama,
                            'Jurusan': m.jurusan,
                            'Angkatan': m.nim[:4] if len(m.nim) >= 4 else 'N/A'
                        })
                    
                    df = pd.DataFrame(df_data)
                    st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Visualisasi data
            st.markdown("---")
            self._visualize_data(data)
            
        else:
            st.markdown("""
            <div class="empty-state">
                <h3>📭 Tidak ada data ditemukan</h3>
                <p>Coba ubah filter pencarian atau tambahkan data baru</p>
            </div>
            """, unsafe_allow_html=True)
    
    def _display_mahasiswa_card(self, mahasiswa: Mahasiswa):
        """Menampilkan card untuk satu mahasiswa"""
        colors = ["#4CC9F0", "#4361EE", "#3A0CA3", "#7209B7", "#F72585"]
        color = random.choice(colors)
        
        st.markdown(f"""
        <div class="mahasiswa-card" style="border-left: 5px solid {color};">
            <div class="card-header">
                <span class="card-nim">{mahasiswa.nim}</span>
                <span class="card-badge">{mahasiswa.jurusan[:3]}</span>
            </div>
            <div class="card-body">
                <h4>{mahasiswa.nama}</h4>
                <p><strong>Jurusan:</strong> {mahasiswa.jurusan}</p>
                <p><strong>Angkatan:</strong> {mahasiswa.nim[:4] if len(mahasiswa.nim) >= 4 else 'N/A'}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def _visualize_data(self, data: List[Mahasiswa]):
        """Visualisasi data dengan Plotly"""
        st.subheader("📊 Visualisasi Data")
        
        tab1, tab2, tab3 = st.tabs(["Distribusi Jurusan", "Distribusi Angkatan", "Statistik"])
        
        with tab1:
            # Jurusan distribution
            jurusan_counts = {}
            for m in data:
                jurusan_counts[m.jurusan] = jurusan_counts.get(m.jurusan, 0) + 1
            
            if jurusan_counts:
                fig = go.Figure(data=[
                    go.Pie(
                        labels=list(jurusan_counts.keys()),
                        values=list(jurusan_counts.values()),
                        hole=.3,
                        marker=dict(colors=px.colors.qualitative.Set3)
                    )
                ])
                fig.update_layout(
                    title="Distribusi Mahasiswa per Jurusan",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Angkatan distribution
            angkatan_counts = {}
            for m in data:
                angkatan = m.nim[:4] if len(m.nim) >= 4 else "Unknown"
                angkatan_counts[angkatan] = angkatan_counts.get(angkatan, 0) + 1
            
            if angkatan_counts:
                fig = go.Figure(data=[
                    go.Bar(
                        x=list(angkatan_counts.keys()),
                        y=list(angkatan_counts.values()),
                        marker_color='#4361EE',
                        text=list(angkatan_counts.values()),
                        textposition='auto'
                    )
                ])
                fig.update_layout(
                    title="Distribusi Mahasiswa per Angkatan",
                    xaxis_title="Angkatan",
                    yaxis_title="Jumlah",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                avg_name_len = sum(len(m.nama) for m in data) / len(data) if data else 0
                st.metric("📝 Rata-rata Panjang Nama", f"{avg_name_len:.1f} karakter")
            
            with col2:
                jurusan_unique = len(set(m.jurusan for m in data))
                st.metric("🎓 Jumlah Jurusan Unik", jurusan_unique)
            
            with col3:
                if data:
                    latest_nim = max(data, key=lambda x: x.nim).nim[:4] if len(data[0].nim) >= 4 else "N/A"
                    st.metric("🆕 Angkatan Terbaru", latest_nim)
    
    def _tambah_data(self):
        """Form tambah data mahasiswa dengan desain modern"""
        st.markdown("## ➕ Tambah Data Mahasiswa Baru")
        
        with st.container(border=True):
            col1, col2 = st.columns(2)
            
            with col1:
                nim = st.text_input("**📝 NIM**", placeholder="Contoh: 24101140099", 
                                   help="Masukkan 9-12 digit angka")
                nama = st.text_input("**👤 Nama Lengkap**", placeholder="Contoh: Azka Insan Robbani",
                                    help="Hanya huruf, spasi, titik, dan koma")
            
            with col2:
                jurusan = st.selectbox(
                    "**🎓 Jurusan**",
                    ["Teknik Informatika", "Sistem Informasi", "Teknik Komputer", 
                     "Manajemen Informatika", "Ilmu Komputer", "Teknologi Informasi"]
                )
                
                angkatan_options = [str(year) for year in range(2018, 2026)]
                angkatan = st.selectbox("**📅 Angkatan**", angkatan_options, index=6)
            
            # Preview card
            if nim and nama:
                st.markdown("### 👁️ Preview Data")
                col_preview1, col_preview2, col_preview3 = st.columns([2, 1, 1])
                with col_preview1:
                    st.info(f"**Nama:** {nama}")
                with col_preview2:
                    st.info(f"**NIM:** {nim}")
                with col_preview3:
                    st.info(f"**Jurusan:** {jurusan}")
            
            # Submit button dengan styling
            col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])
            with col_btn1:
                if st.button("🚀 **Simpan Data**", type="primary", use_container_width=True):
                    self._process_tambah_data(nim, nama, jurusan, angkatan)
            
            with col_btn2:
                if st.button("🔄 **Reset Form**", use_container_width=True):
                    st.rerun()
            
            with col_btn3:
                if st.button("📋 **Template**", use_container_width=True):
                    st.code("NIM: 24101140099\nNama: Azka Insan Robbani\nJurusan: Teknik Informatika")
    
    def _process_tambah_data(self, nim: str, nama: str, jurusan: str, angkatan: str):
        """Memproses penambahan data"""
        try:
            if not nim or not nama:
                st.error("❌ NIM dan Nama wajib diisi!")
                return
            
            if not re.match(r'^\d{9,12}$', nim):
                st.error("❌ NIM harus terdiri dari 9-12 digit angka!")
                return
            
            if not re.match(r'^[A-Za-z\s\.\,]{3,50}$', nama):
                st.error("❌ Nama hanya boleh mengandung huruf, spasi, titik, dan koma!")
                return
            
            mahasiswa_baru = Mahasiswa(nim=nim, nama=nama, jurusan=jurusan, angkatan=angkatan)
            self.manajemen.tambah(mahasiswa_baru)
            st.session_state.data_mahasiswa = self.manajemen.get_semua()
            
            # Success animation
            st.success(f"✅ Data **{nama}** berhasil ditambahkan!")
            st.balloons()
            
            # Auto redirect ke dashboard setelah 2 detik
            time.sleep(2)
            st.rerun()
            
        except ValueError as e:
            st.error(f"❌ Error: {str(e)}")
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan: {str(e)}")
    
    def _edit_data(self):
        """Form edit data mahasiswa"""
        st.markdown("## ✏️ Edit Data Mahasiswa")
        
        data = self.manajemen.get_semua()
        if not data:
            st.info("📭 Tidak ada data mahasiswa yang dapat diedit.")
            return
        
        # Pilih mahasiswa dengan search
        search_col1, search_col2 = st.columns([3, 1])
        with search_col1:
            search_term = st.text_input("🔍 Cari mahasiswa:", placeholder="Masukkan NIM atau nama...")
        
        filtered_data = data
        if search_term:
            filtered_data = [m for m in data if search_term.lower() in m.nama.lower() or search_term in m.nim]
        
        if filtered_data:
            pilihan = {f"{m.nim} - {m.nama} ({m.jurusan})": m.nim for m in filtered_data}
            selected = st.selectbox("Pilih Mahasiswa:", list(pilihan.keys()))
            
            if selected:
                nim_lama = pilihan[selected]
                mahasiswa = self.manajemen.get_by_nim(nim_lama)
                
                if mahasiswa:
                    with st.form("form_edit", border=True):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            nim_baru = st.text_input("NIM Baru*", value=mahasiswa.nim, max_chars=12)
                            nama_baru = st.text_input("Nama Lengkap Baru*", value=mahasiswa.nama, max_chars=50)
                        
                        with col2:
                            jurusan_baru = st.selectbox(
                                "Jurusan Baru*",
                                ["Teknik Informatika", "Sistem Informasi", "Teknik Komputer", 
                                 "Manajemen Informatika", "Ilmu Komputer"],
                                index=["Teknik Informatika", "Sistem Informasi", "Teknik Komputer", 
                                       "Manajemen Informatika", "Ilmu Komputer"].index(mahasiswa.jurusan)
                                if mahasiswa.jurusan in ["Teknik Informatika", "Sistem Informasi", "Teknik Komputer", 
                                                         "Manajemen Informatika", "Ilmu Komputer"]
                                else 0
                            )
                            
                            angkatan_baru = st.selectbox(
                                "Angkatan Baru",
                                [str(year) for year in range(2018, 2026)],
                                index=int(mahasiswa.angkatan) - 2018 if mahasiswa.angkatan.isdigit() and 2018 <= int(mahasiswa.angkatan) <= 2025 else 6
                            )
                        
                        col_btn1, col_btn2 = st.columns(2)
                        with col_btn1:
                            submitted = st.form_submit_button("💾 **Update Data**", type="primary", use_container_width=True)
                        with col_btn2:
                            if st.form_submit_button("❌ **Batal**", use_container_width=True):
                                st.rerun()
                        
                        if submitted:
                            self._process_edit_data(nim_lama, nim_baru, nama_baru, jurusan_baru, angkatan_baru)
        else:
            st.warning("🔍 Tidak ditemukan mahasiswa dengan kriteria tersebut.")
    
    def _process_edit_data(self, nim_lama: str, nim_baru: str, nama_baru: str, jurusan_baru: str, angkatan_baru: str):
        """Memproses edit data"""
        try:
            if not nim_baru or not nama_baru:
                st.error("❌ NIM dan Nama wajib diisi!")
                return
            
            if not re.match(r'^\d{9,12}$', nim_baru):
                st.error("❌ NIM harus terdiri dari 9-12 digit angka!")
                return
            
            if not re.match(r'^[A-Za-z\s\.\,]{3,50}$', nama_baru):
                st.error("❌ Nama hanya boleh mengandung huruf, spasi, titik, dan koma!")
                return
            
            mahasiswa_baru = Mahasiswa(nim=nim_baru, nama=nama_baru, jurusan=jurusan_baru, angkatan=angkatan_baru)
            self.manajemen.edit(nim_lama, mahasiswa_baru)
            st.session_state.data_mahasiswa = self.manajemen.get_semua()
            
            st.success("✅ Data mahasiswa berhasil diupdate!")
            st.balloons()
            time.sleep(1)
            st.rerun()
            
        except ValueError as e:
            st.error(f"❌ Error: {str(e)}")
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan: {str(e)}")
    
    def _hapus_data(self):
        """Form hapus data mahasiswa"""
        st.markdown("## 🗑️ Hapus Data Mahasiswa")
        
        data = self.manajemen.get_semua()
        if not data:
            st.info("📭 Tidak ada data mahasiswa yang dapat dihapus.")
            return
        
        pilihan = {f"{m.nim} - {m.nama}": m.nim for m in data}
        selected = st.selectbox("Pilih Mahasiswa yang akan dihapus:", list(pilihan.keys()))
        
        if selected:
            nim_hapus = pilihan[selected]
            mahasiswa = self.manajemen.get_by_nim(nim_hapus)
            
            if mahasiswa:
                # Warning card
                st.markdown("""
                <div class="warning-card">
                    <h3>⚠️ PERINGATAN: Penghapusan Data</h3>
                    <p>Data yang dihapus tidak dapat dikembalikan. Pastikan data yang dipilih benar.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Data preview
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**NIM:** {mahasiswa.nim}")
                    st.info(f"**Jurusan:** {mahasiswa.jurusan}")
                with col2:
                    st.info(f"**Nama:** {mahasiswa.nama}")
                    st.info(f"**Angkatan:** {mahasiswa.angkatan}")
                
                # Confirmation
                confirm = st.checkbox("✅ Saya yakin ingin menghapus data ini")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("🗑️ **Hapus Permanen**", type="primary", disabled=not confirm, use_container_width=True):
                        try:
                            if self.manajemen.hapus(nim_hapus):
                                st.session_state.data_mahasiswa = self.manajemen.get_semua()
                                st.error(f"🗑️ Data **{mahasiswa.nama}** berhasil dihapus!")
                                time.sleep(2)
                                st.rerun()
                            else:
                                st.error("❌ Gagal menghapus data mahasiswa.")
                        except Exception as e:
                            st.error(f"❌ Terjadi kesalahan: {str(e)}")
                
                with col_btn2:
                    if st.button("↩️ **Batal**", use_container_width=True):
                        st.rerun()
    
    def _pencarian_data(self):
        """Halaman pencarian data dengan visualisasi"""
        st.markdown("## 🔍 Pencarian Data Mahasiswa")
        
        # Search input dengan styling
        with st.container(border=True):
            keyword = st.text_input(
                "Masukkan keyword pencarian:",
                placeholder="Cari berdasarkan NIM atau Nama...",
                help="Anda dapat mencari berdasarkan NIM (angka) atau Nama (teks)"
            )
        
        if keyword:
            data = self.manajemen.get_semua()
            
            # Tabs untuk berbagai algoritma
            tab1, tab2, tab3 = st.tabs([
                "🔍 Linear Search", 
                "⚡ Binary Search", 
                "📊 Perbandingan"
            ])
            
            with tab1:
                st.markdown("### 🔍 Linear Search")
                st.caption("**Kompleksitas:** O(n) | **Keuntungan:** Dapat mencari berdasarkan NIM atau Nama")
                
                col1, col2 = st.columns(2)
                with col1:
                    by = st.radio("Cari berdasarkan:", ["Nama", "NIM"], horizontal=True)
                
                with st.spinner("Sedang mencari..."):
                    start_time = time.time()
                    hasil = AlgoritmaPencarian.linear_search(data, keyword, by.lower())
                    end_time = time.time()
                    exec_time = end_time - start_time
                
                self._display_search_results(hasil, exec_time, "Linear Search")
            
            with tab2:
                st.markdown("### ⚡ Binary Search")
                st.caption("**Kompleksitas:** O(log n) | **Persyaratan:** Data harus terurut berdasarkan NIM")
                
                if re.match(r'^\d+$', keyword):
                    data_sorted = sorted(data, key=lambda x: x.nim)
                    
                    with st.spinner("Sedang mencari dengan binary search..."):
                        start_time = time.time()
                        hasil_binary = AlgoritmaPencarian.binary_search(data_sorted, keyword)
                        end_time = time.time()
                        exec_time = end_time - start_time
                    
                    if hasil_binary:
                        self._display_search_results([hasil_binary], exec_time, "Binary Search")
                    else:
                        st.info("ℹ️ Tidak ditemukan hasil.")
                        st.metric("⏱️ Waktu Eksekusi", f"{exec_time:.6f} detik")
                else:
                    st.warning("⚠️ Binary Search hanya bisa mencari berdasarkan NIM (angka)")
            
            with tab3:
                st.markdown("### 📊 Perbandingan Algoritma")
                
                # Benchmark comparison
                comparison_data = []
                
                # Linear Search benchmark
                start_time = time.time()
                linear_results = AlgoritmaPencarian.linear_search(data, keyword, 'nama')
                linear_time = time.time() - start_time
                
                comparison_data.append({
                    'Algoritma': 'Linear Search',
                    'Waktu (ms)': linear_time * 1000,
                    'Hasil': len(linear_results),
                    'Kompleksitas': 'O(n)'
                })
                
                # Sequential Search benchmark
                start_time = time.time()
                seq_results = AlgoritmaPencarian.sequential_search(data, keyword)
                seq_time = time.time() - start_time
                
                comparison_data.append({
                    'Algoritma': 'Sequential Search',
                    'Waktu (ms)': seq_time * 1000,
                    'Hasil': len(seq_results),
                    'Kompleksitas': 'O(n)'
                })
                
                # Binary Search benchmark (jika NIM)
                if re.match(r'^\d+$', keyword):
                    data_sorted = sorted(data, key=lambda x: x.nim)
                    start_time = time.time()
                    binary_result = AlgoritmaPencarian.binary_search(data_sorted, keyword)
                    binary_time = time.time() - start_time
                    
                    comparison_data.append({
                        'Algoritma': 'Binary Search',
                        'Waktu (ms)': binary_time * 1000,
                        'Hasil': 1 if binary_result else 0,
                        'Kompleksitas': 'O(log n)'
                    })
                
                df_comparison = pd.DataFrame(comparison_data)
                
                # Visualisasi perbandingan
                col_chart, col_table = st.columns(2)
                with col_chart:
                    fig = px.bar(
                        df_comparison,
                        x='Algoritma',
                        y='Waktu (ms)',
                        color='Algoritma',
                        title='Perbandingan Waktu Eksekusi',
                        text='Waktu (ms)',
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig.update_traces(texttemplate='%{text:.3f}ms', textposition='outside')
                    st.plotly_chart(fig, use_container_width=True)
                
                with col_table:
                    st.dataframe(
                        df_comparison,
                        column_config={
                            "Waktu (ms)": st.column_config.ProgressColumn(
                                "Waktu (ms)",
                                format="%.3f",
                                min_value=0,
                                max_value=max(df_comparison['Waktu (ms)']) * 1.1
                            )
                        },
                        hide_index=True,
                        use_container_width=True
                    )
    
    def _display_search_results(self, hasil: List[Mahasiswa], exec_time: float, algorithm: str):
        """Menampilkan hasil pencarian"""
        if hasil:
            st.success(f"✅ Ditemukan **{len(hasil)}** hasil dengan {algorithm} ({exec_time:.6f} detik)")
            
            # Tampilkan dalam grid
            cols = st.columns(2)
            for idx, m in enumerate(hasil[:6]):  # Tampilkan maksimal 6
                with cols[idx % 2]:
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-nim">{m.nim}</div>
                        <div class="result-name">{m.nama}</div>
                        <div class="result-major">{m.jurusan}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Jika lebih dari 6, tampilkan tabel
            if len(hasil) > 6:
                with st.expander(f"📋 Lihat Semua {len(hasil)} Hasil"):
                    df_data = []
                    for m in hasil:
                        df_data.append({
                            'NIM': m.nim,
                            'Nama': m.nama,
                            'Jurusan': m.jurusan
                        })
                    df = pd.DataFrame(df_data)
                    st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("ℹ️ Tidak ditemukan hasil.")
            st.metric("⏱️ Waktu Eksekusi", f"{exec_time:.6f} detik")
    
    def _pengurutan_data(self):
        """Halaman pengurutan data dengan visualisasi"""
        st.markdown("## 📈 Pengurutan Data Mahasiswa")
        
        # Configuration panel
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                by = st.selectbox("**Urutkan berdasarkan:**", ["NIM", "Nama"])
            
            with col2:
                order = st.selectbox("**Urutan:**", ["Ascending (A-Z/0-9)", "Descending (Z-A/9-0)"])
            
            with col3:
                algorithm = st.selectbox(
                    "**Algoritma:**",
                    ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Shell Sort"]
                )
            
            with col4:
                sample_size = st.slider("**Jumlah Data:**", 10, 100, 50, 10)
        
        if st.button("🚀 **Jalankan Pengurutan**", type="primary"):
            data = self.manajemen.get_semua()
            if len(data) == 0:
                st.warning("📭 Tidak ada data untuk diurutkan.")
                return
            
            # Ambil sample data
            sample_data = data[:min(sample_size, len(data))]
            ascending = order.startswith("Ascending")
            
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Eksekusi algoritma
            status_text.text(f"🔄 Menjalankan {algorithm}...")
            
            start_time = time.time()
            
            if algorithm == "Bubble Sort":
                complexity = "O(n²)"
                hasil = AlgoritmaPengurutan.bubble_sort(sample_data, by.lower(), ascending)
            elif algorithm == "Selection Sort":
                complexity = "O(n²)"
                hasil = AlgoritmaPengurutan.selection_sort(sample_data, by.lower(), ascending)
            elif algorithm == "Insertion Sort":
                complexity = "O(n²)"
                hasil = AlgoritmaPengurutan.insertion_sort(sample_data, by.lower(), ascending)
            elif algorithm == "Merge Sort":
                complexity = "O(n log n)"
                hasil = AlgoritmaPengurutan.merge_sort(sample_data, by.lower(), ascending)
            elif algorithm == "Shell Sort":
                complexity = "O(n log n) sampai O(n²)"
                hasil = AlgoritmaPengurutan.shell_sort(sample_data, by.lower(), ascending)
            
            end_time = time.time()
            exec_time = end_time - start_time
            
            progress_bar.progress(100)
            status_text.text("✅ Pengurutan selesai!")
            
            # Results
            st.success(f"✅ Data berhasil diurutkan menggunakan **{algorithm}** ({complexity})")
            
            # Metrics
            col_metric1, col_metric2, col_metric3 = st.columns(3)
            with col_metric1:
                st.metric("⏱️ Waktu Eksekusi", f"{exec_time:.6f} detik")
            with col_metric2:
                st.metric("📊 Jumlah Data", len(sample_data))
            with col_metric3:
                st.metric("⚡ Kecepatan", f"{len(sample_data)/exec_time:.1f} data/detik")
            
            # Tampilkan hasil
            st.subheader("📋 Hasil Pengurutan")
            
            tab_table, tab_chart = st.tabs(["Tabel Data", "Visualisasi"])
            
            with tab_table:
                df_data = []
                for m in hasil:
                    df_data.append({
                        'NIM': m.nim,
                        'Nama': m.nama,
                        'Jurusan': m.jurusan
                    })
                
                df = pd.DataFrame(df_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
            
            with tab_chart:
                # Visualisasi pengurutan
                values = [m.nim if by == 'NIM' else m.nama for m in hasil]
                indices = list(range(len(values)))
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=indices,
                        y=values if by == 'NIM' else [1] * len(values),
                        text=values,
                        marker_color='#4361EE',
                        textposition='outside'
                    )
                ])
                
                fig.update_layout(
                    title=f"Hasil Pengurutan Berdasarkan {by}",
                    xaxis_title="Posisi",
                    yaxis_title=by,
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    def _visualisasi_data(self):
        """Halaman visualisasi data lengkap"""
        st.markdown("## 📊 Visualisasi Data Lengkap")
        
        data = self.manajemen.get_semua()
        if not data:
            st.info("📭 Tidak ada data untuk divisualisasikan.")
            return
        
        tab1, tab2, tab3 = st.tabs(["📈 Distribusi", "📅 Timeline", "🎯 Insights"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Jurusan distribution
                jurusan_counts = {}
                for m in data:
                    jurusan_counts[m.jurusan] = jurusan_counts.get(m.jurusan, 0) + 1
                
                fig1 = px.pie(
                    values=list(jurusan_counts.values()),
                    names=list(jurusan_counts.keys()),
                    title="Distribusi Jurusan",
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # Angkatan distribution
                angkatan_counts = {}
                for m in data:
                    angkatan = m.nim[:4] if len(m.nim) >= 4 else "Unknown"
                    angkatan_counts[angkatan] = angkatan_counts.get(angkatan, 0) + 1
                
                fig2 = px.bar(
                    x=list(angkatan_counts.keys()),
                    y=list(angkatan_counts.values()),
                    title="Distribusi Angkatan",
                    color=list(angkatan_counts.values()),
                    color_continuous_scale=px.colors.sequential.Viridis
                )
                st.plotly_chart(fig2, use_container_width=True)
        
        with tab2:
            # Timeline visualization
            st.subheader("📅 Timeline Data Mahasiswa")
            
            # Create timeline data
            timeline_data = []
            for m in data:
                angkatan = m.nim[:4] if len(m.nim) >= 4 else "2024"
                timeline_data.append({
                    'Tahun': int(angkatan),
                    'Nama': m.nama,
                    'Jurusan': m.jurusan,
                    'NIM': m.nim
                })
            
            df_timeline = pd.DataFrame(timeline_data)
            
            if not df_timeline.empty:
                fig = px.scatter(
                    df_timeline,
                    x='Tahun',
                    y='Jurusan',
                    color='Jurusan',
                    size=[10] * len(df_timeline),
                    hover_data=['Nama', 'NIM'],
                    title="Distribusi Mahasiswa per Tahun dan Jurusan",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Data insights
            st.subheader("🎯 Data Insights")
            
            insights_col1, insights_col2 = st.columns(2)
            
            with insights_col1:
                # Statistik
                total = len(data)
                jurusan_count = len(set([m.jurusan for m in data]))
                avg_name_len = sum(len(m.nama) for m in data) / total
                
                st.metric("👥 Total Mahasiswa", total)
                st.metric("🎓 Jurusan Unik", jurusan_count)
                st.metric("📝 Rata-rata Panjang Nama", f"{avg_name_len:.1f} karakter")
            
            with insights_col2:
                # Additional insights
                if data:
                    # Find most common first name
                    first_names = [m.nama.split()[0] for m in data if m.nama]
                    if first_names:
                        most_common_name = max(set(first_names), key=first_names.count)
                        st.metric("👤 Nama Depan Terbanyak", most_common_name)
                    
                    # NIM patterns
                    nim_lengths = [len(m.nim) for m in data]
                    avg_nim_len = sum(nim_lengths) / len(nim_lengths)
                    st.metric("🔢 Rata-rata Panjang NIM", f"{avg_nim_len:.1f} digit")
    
    def _analisis_kompleksitas(self):
        """Halaman analisis kompleksitas algoritma"""
        st.markdown("## ℹ️ Analisis Kompleksitas Algoritma")
        
        # Theory section
        with st.expander("📚 Teori Kompleksitas Waktu", expanded=True):
            st.markdown("""
            ### ⏱️ Notasi Big-O
            
            Notasi Big-O digunakan untuk menggambarkan performa algoritma dalam hal waktu eksekusi 
            atau penggunaan memori relatif terhadap ukuran input.
            
            | Notasi | Nama | Deskripsi | Contoh |
            |--------|------|-----------|--------|
            | **O(1)** | Constant Time | Waktu eksekusi konstan | Akses array dengan index |
            | **O(log n)** | Logarithmic Time | Waktu bertambah secara logaritmik | Binary Search |
            | **O(n)** | Linear Time | Waktu bertambah linear dengan input | Linear Search |
            | **O(n log n)** | Linearithmic Time | Kombinasi linear dan logaritmik | Merge Sort, Quick Sort |
            | **O(n²)** | Quadratic Time | Waktu bertambah secara kuadratik | Bubble Sort, Selection Sort |
            | **O(2ⁿ)** | Exponential Time | Waktu bertambah secara eksponensial | Brute Force |
            """)
        
        # Algorithm comparison
        st.markdown("### ⚡ Perbandingan Algoritma")
        
        col_alg1, col_alg2, col_alg3 = st.columns(3)
        
        with col_alg1:
            st.markdown("""
            <div class="alg-card">
                <h4>🔍 Pencarian</h4>
                <ul>
                    <li><strong>Linear Search:</strong> O(n)</li>
                    <li><strong>Binary Search:</strong> O(log n)</li>
                    <li><strong>Sequential Search:</strong> O(n)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col_alg2:
            st.markdown("""
            <div class="alg-card">
                <h4>📈 Pengurutan</h4>
                <ul>
                    <li><strong>Bubble Sort:</strong> O(n²)</li>
                    <li><strong>Selection Sort:</strong> O(n²)</li>
                    <li><strong>Insertion Sort:</strong> O(n²)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col_alg3:
            st.markdown("""
            <div class="alg-card">
                <h4>⚡ Advanced</h4>
                <ul>
                    <li><strong>Merge Sort:</strong> O(n log n)</li>
                    <li><strong>Shell Sort:</strong> O(n log n) - O(n²)</li>
                    <li><strong>Quick Sort:</strong> O(n log n)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Performance test
        st.markdown("### 🧪 Benchmark Performance")
        
        if st.button("🚀 Jalankan Benchmark", type="primary"):
            data = self.manajemen.get_semua()
            if len(data) < 10:
                st.warning("⚠️ Minimal 10 data untuk benchmark yang akurat.")
                return
            
            # Prepare test data
            test_sizes = [10, 50, 100, 500]
            test_data = data[:500]  # Max 500 data untuk benchmark
            
            results = []
            
            for size in test_sizes:
                if size <= len(test_data):
                    sample = test_data[:size]
                    
                    # Test Linear Search
                    start = time.time()
                    AlgoritmaPencarian.linear_search(sample, "a", 'nama')
                    linear_time = time.time() - start
                    
                    # Test Binary Search (requires sorted data)
                    sorted_sample = sorted(sample, key=lambda x: x.nim)
                    start = time.time()
                    if sorted_sample:
                        AlgoritmaPencarian.binary_search(sorted_sample, sorted_sample[0].nim)
                    binary_time = time.time() - start
                    
                    # Test Bubble Sort
                    start = time.time()
                    AlgoritmaPengurutan.bubble_sort(sample, 'nim', True)
                    bubble_time = time.time() - start
                    
                    # Test Merge Sort
                    start = time.time()
                    AlgoritmaPengurutan.merge_sort(sample, 'nim', True)
                    merge_time = time.time() - start
                    
                    results.append({
                        'Data Size': size,
                        'Linear Search': linear_time * 1000,
                        'Binary Search': binary_time * 1000,
                        'Bubble Sort': bubble_time * 1000,
                        'Merge Sort': merge_time * 1000
                    })
            
            # Display results
            df_results = pd.DataFrame(results)
            
            # Plot comparison
            fig = go.Figure()
            
            for col in ['Linear Search', 'Binary Search', 'Bubble Sort', 'Merge Sort']:
                fig.add_trace(go.Scatter(
                    x=df_results['Data Size'],
                    y=df_results[col],
                    mode='lines+markers',
                    name=col
                ))
            
            fig.update_layout(
                title='Benchmark Algoritma vs Ukuran Data',
                xaxis_title='Ukuran Data',
                yaxis_title='Waktu (ms)',
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show data table
            st.dataframe(df_results, use_container_width=True, hide_index=True)
    
    def _logout_page(self):
        """Halaman logout"""
        st.markdown("""
        <div class="logout-container">
            <h2>👋 Logout</h2>
            <p>Apakah Anda yakin ingin keluar dari sistem?</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("✅ Ya, Keluar", type="primary", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.user_role = None
                st.success("👋 Anda telah berhasil logout!")
                time.sleep(1)
                st.rerun()
            
            if st.button("❌ Tidak, Kembali", use_container_width=True):
                st.rerun()
    
    def _animated_background(self):
        """Background animation untuk login page"""
        st.markdown("""
        <style>
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .stApp {
            background: linear-gradient(-45deg, #0c2461, #1e3799, #4a69bd, #6a89cc);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            min-height: 100vh;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def run(self):
        """Menjalankan aplikasi"""
        st.set_page_config(
        page_title="Manajemen Data Mahasiswa",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
        )

        
        # Inject custom CSS
        self._inject_custom_css()
        
        # Routing berdasarkan status login
        if not st.session_state.logged_in:
            self.login_page()
        else:
            self.main_page()
    
    def _inject_custom_css(self):
        """Menyuntikkan CSS kustom ke aplikasi"""
        st.markdown("""
        <style>
        /* Reset dan base styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        /* Animasi background untuk login */
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .stApp {
            background: linear-gradient(-45deg, #f5f7fa, #e4e8f0, #c3cfe2, #a8b6d6);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        /* PERUBAHAN: Input text color to black */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {
            color: #000000 !important;  /* Warna hitam */
        }
        
        /* PERUBAHAN: Placeholder color */
        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder {
            color: #666666 !important;  /* Warna abu-abu gelap untuk placeholder */
        }
        
        /* PERUBAHAN: Text color for labels */
        .stTextInput label,
        .stSelectbox label,
        .stTextArea label,
        .stNumberInput label,
        .stRadio label,
        .stCheckbox label {
            color: #000000 !important;  /* Warna hitam untuk label */
        }
        
        /* PERUBAHAN: Login form input text color */
        .glass-form input {
            color: #000000 !important;
        }
        
        .glass-form input::placeholder {
            color: #666666 !important;
        }
        
        .glass-form label {
            color: #000000 !important;
        }
        
        /* Header styling */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        }
        
        .header-content h1 {
            font-size: 2.2rem;
            margin-bottom: 0.5rem;
            font-weight: 700;
        }
        
        .header-content p {
            opacity: 0.9;
            font-size: 1rem;
        }
        
        .gradient-text {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .user-badge {
            background: rgba(255, 255, 255, 0.2);
            padding: 0.5rem 1rem;
            border-radius: 25px;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            backdrop-filter: blur(10px);
        }
        
        /* Stat cards */
        .stat-card {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
            display: flex;
            align-items: center;
            gap: 1rem;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 1px solid rgba(0, 0, 0, 0.05);
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.12);
        }
        
        .blue-card { border-top: 4px solid #4361EE; }
        .green-card { border-top: 4px solid #4CAF50; }
        .orange-card { border-top: 4px solid #FF9800; }
        .purple-card { border-top: 4px solid #9C27B0; }
        
        .stat-icon {
            font-size: 2.5rem;
            width: 60px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 12px;
            background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%);
        }
        
        .stat-content {
            flex: 1;
        }
        
        .stat-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #2c3e50;
            line-height: 1;
        }
        
        .stat-label {
            font-size: 0.9rem;
            color: #7f8c8d;
            margin-top: 0.25rem;
        }
        
        /* Mahasiswa card */
        .mahasiswa-card {
            background: white;
            border-radius: 12px;
            padding: 1.2rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            transition: all 0.3s ease;
            border: 1px solid #e0e0e0;
        }
        
        .mahasiswa-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
        }
        
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }
        
        .card-nim {
            font-family: 'Courier New', monospace;
            font-weight: 600;
            color: #4361EE;
            font-size: 0.9rem;
        }
        
        .card-badge {
            background: #4361EE;
            color: white;
            padding: 0.2rem 0.6rem;
            border-radius: 20px;
            font-size: 0.7rem;
            font-weight: 600;
        }
        
        .card-body h4 {
            color: #2c3e50;
            margin-bottom: 0.5rem;
            font-size: 1.1rem;
        }
        
        .card-body p {
            color: #7f8c8d;
            font-size: 0.85rem;
            margin: 0.2rem 0;
        }
        
        /* Login card */
        .glass-card {
            background: rgba(255, 255, 255, 0.95); /* PERUBAHAN: lebih opaque untuk kontras */
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin-bottom: 2rem;
        }
        
        .login-card {
            text-align: center;
            color: #000000; /* PERUBAHAN: warna hitam */
        }
        
        .login-header h1 {
            font-size: 3.5rem;
            margin-bottom: 0.5rem;
            color: #000000; /* PERUBAHAN: warna hitam */
        }
        
        .login-header h2 {
            font-size: 1.8rem;
            margin-bottom: 0.5rem;
            font-weight: 600;
            color: #000000; /* PERUBAHAN: warna hitam */
        }
        
        .login-header p {
            opacity: 0.9;
            font-size: 1rem;
            color: #333333; /* PERUBAHAN: warna abu-abu gelap */
        }
        
        .glass-form {
            background: rgba(255, 255, 255, 0.98); /* PERUBAHAN: lebih solid */
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
        }
        
        /* Stats card di login */
        .stats-card {
            background: rgba(255, 255, 255, 0.95); /* PERUBAHAN: lebih solid */
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 1.5rem;
            margin-top: 2rem;
            color: #000000; /* PERUBAHAN: warna hitam */
            border: 1px solid rgba(0, 0, 0, 0.1); /* PERUBAHAN: border lebih gelap */
        }
        
        .stat-item {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1rem;
        }
        
        .stat-item:last-child {
            margin-bottom: 0;
        }
        
        .stat-icon {
            font-size: 1.5rem;
            color: #000000; /* PERUBAHAN: warna hitam */
        }
        
        .stat-text {
            font-size: 0.95rem;
            color: #000000; /* PERUBAHAN: warna hitam */
        }
        
        .stat-text strong {
            color: #4361EE; /* Warna biru untuk emphasis */
        }
        
        /* Result card untuk pencarian */
        .result-card {
            background: white;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
            border-left: 4px solid #4361EE;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
        }
        
        .result-nim {
            font-family: 'Courier New', monospace;
            color: #4361EE;
            font-weight: 600;
            font-size: 0.9rem;
        }
        
        .result-name {
            font-size: 1.1rem;
            font-weight: 600;
            color: #2c3e50;
            margin: 0.3rem 0;
        }
        
        .result-major {
            color: #7f8c8d;
            font-size: 0.85rem;
        }
        
        /* Warning card */
        .warning-card {
            background: linear-gradient(135deg, #FFEAA7 0%, #fab1a0 100%);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 2px solid #e17055;
        }
        
        .warning-card h3 {
            color: #d63031;
            margin-bottom: 0.5rem;
        }
        
        .warning-card p {
            color: #636e72;
        }
        
        /* Empty state */
        .empty-state {
            text-align: center;
            padding: 4rem 2rem;
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
        }
        
        .empty-state h3 {
            color: #2c3e50;
            margin-bottom: 1rem;
        }
        
        .empty-state p {
            color: #7f8c8d;
        }
        
        /* Algorithm card */
        .alg-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
            height: 100%;
            border-top: 4px solid #4361EE;
        }
        
        .alg-card h4 {
            color: #2c3e50;
            margin-bottom: 1rem;
            font-size: 1.2rem;
        }
        
        .alg-card ul {
            list-style: none;
            padding: 0;
        }
        
        .alg-card li {
            padding: 0.5rem 0;
            border-bottom: 1px solid #f0f0f0;
            color: #34495e;
        }
        
        .alg-card li:last-child {
            border-bottom: none;
        }
        
        .alg-card li strong {
            color: #4361EE;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%) !important;
            color: white !important;
        }
        
        [data-testid="stSidebar"] .stRadio div {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 0.5rem;
        }
        
        [data-testid="stSidebar"] label {
            color: white !important;
        }
        
        .sidebar-header {
            padding: 1rem 0;
            border-bottom: 2px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 1rem;
        }
        
        .sidebar-header h2 {
            color: white;
            font-size: 1.5rem;
        }
        
        /* PERUBAHAN: Radio button di sidebar tetap putih */
        [data-testid="stSidebar"] .stRadio span {
            color: white !important;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }
        
        /* PERUBAHAN: Button text tetap putih */
        .stButton > button span {
            color: white !important;
        }
        
        /* Input styling */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select {
            background: white !important;
            border: 2px solid #e0e0e0 !important;
            border-radius: 10px !important;
            padding: 0.75rem 1rem !important;
            font-size: 0.95rem !important;
            transition: border-color 0.3s ease !important;
            color: #000000 !important; /* PERUBAHAN: tambahan untuk memastikan warna hitam */
        }
        
        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        }
        
        /* Metric styling */
        [data-testid="stMetricValue"] {
            font-size: 2rem !important;
            font-weight: 700 !important;
            color: #2c3e50 !important;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 0.9rem !important;
            color: #7f8c8d !important;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            background: transparent;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: white !important;
            border-radius: 10px 10px 0 0 !important;
            padding: 0.75rem 1.5rem !important;
            font-weight: 600 !important;
            color: #7f8c8d !important;
            border: 1px solid #e0e0e0 !important;
            border-bottom: none !important;
            transition: all 0.3s ease !important;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            color: #667eea !important;
            background: #f8f9fa !important;
        }
        
        .stTabs [aria-selected="true"] {
            background: white !important;
            color: #667eea !important;
            border-color: #667eea !important;
            box-shadow: 0 -2px 0 #667eea inset !important;
        }
        
        /* Alert styling */
        .stAlert {
            border-radius: 12px !important;
            border: none !important;
            padding: 1rem 1.5rem !important;
        }
        
        .stAlert.stSuccess {
            background: linear-gradient(135deg, #a8e6cf 0%, #dcedc1 100%) !important;
            color: #2d3436 !important;
        }
        
        .stAlert.stError {
            background: linear-gradient(135deg, #ffafbd 0%, #ffc3a0 100%) !important;
            color: #2d3436 !important;
        }
        
        .stAlert.stInfo {
            background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%) !important;
            color: #2d3436 !important;
        }
        
        .stAlert.stWarning {
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%) !important;
            color: #2d3436 !important;
        }
        
        /* Container styling */
        .stContainer {
            background: white;
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
        }
        
        /* Progress bar */
        .stProgress > div > div > div {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background: white !important;
            border-radius: 10px !important;
            border: 2px solid #e0e0e0 !important;
            font-weight: 600 !important;
            color: #2c3e50 !important;
        }
        
        .streamlit-expanderHeader:hover {
            border-color: #667eea !important;
        }
        
        /* Logout container */
        .logout-container {
            text-align: center;
            padding: 4rem 2rem;
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
            margin: 2rem auto;
            max-width: 500px;
        }
        
        .logout-container h2 {
            color: #2c3e50;
            margin-bottom: 1rem;
            font-size: 2rem;
        }
        
        .logout-container p {
            color: #7f8c8d;
            margin-bottom: 2rem;
            font-size: 1.1rem;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .main-header {
                flex-direction: column;
                text-align: center;
                gap: 1rem;
            }
            
            .user-badge {
                align-self: center;
            }
        }
        </style>
        """, unsafe_allow_html=True)

# ==============================
# INISIALISASI DATA CONTOH
# ==============================

def inisialisasi_data_contoh():
    """Menginisialisasi data mahasiswa contoh"""
    data_contoh = [
        ("24101140099", "Azka Insan Robbani"),
        ("241011401958", "Bagus ardiansyah"),
        ("241011401713", "Fathur Rachman"),
        ("241011400087", "Tumpal Sinaga"),
        ("241011401650", "Vina Aulia"),
        ("241011400103", "Satria Apriza Fajar"),
        ("241011400085", "Davrielle saddad"),
        ("241012402295", "JANDRI HARTAT GEA"),
        ("241011400094", "Walman pangaribuan"),
        ("24011400075", "Rafli"),
        ("241011401866", "Jason Cornelius Chandra"),
        ("241011402663", "Ahmad Rasyid"),
        ("241011400068", "Ferda Ayi Sukaesih Sutanto"),
        ("241011402896", "M. Ikram Maulana"),
        ("241011400091", "Nazril Supriyadi"),
        ("241011402829", "Ade jahwa aulia"),
        ("241011400092", "Maulana ikhsan fadhillah"),
        ("241011400089", "Dea Amellya"),
        ("241011402427", "Risqi Eko Trianto"),
        ("241011400098", "Rizki Ramadani"),
        ("241011402197", "muhammad alif fajriansyah"),
        ("241011400097", "dzaki ramadhan"),
        ("241011400076", "Servatius Hasta Kristanto"),
        ("241011401761", "Ahmad Firdaus"),
        ("241011402338", "Ade sofyan"),
        ("241011402835", "Dimas Ahmad"),
        ("241011401470", "Adam Darmansyah"),
        ("241011400079", "Muhammad Noer Alam P"),
        ("241011403269", "Azmi Al Fahriza"),
        ("241011402053", "Ahmad Irfan"),
        ("241011402382", "Gregorius Gilbert Ieli Sarjana")
    ]
    
    return data_contoh

# ==============================
# MAIN EXECUTION
# ==============================

if __name__ == "__main__":
    try:
        # Buat instance aplikasi
        app = AplikasiManajemenMahasiswa()
        
        # Tambahkan data contoh jika file belum ada
        if not os.path.exists('data_mahasiswa.json'):
            data_contoh = inisialisasi_data_contoh()
            for nim, nama in data_contoh:
                try:
                    # Generate random angkatan between 2020-2024
                    angkatan = str(random.randint(2020, 2024))
                    mahasiswa = Mahasiswa(nim=nim, nama=nama, angkatan=angkatan)
                    app.manajemen.tambah(mahasiswa)
                except Exception as e:
                    print(f"Error menambahkan {nama}: {str(e)}")
            
            # Simpan ke file
            app.file_handler.simpan_ke_file(app.manajemen.get_semua())
            print("✅ Data contoh berhasil diinisialisasi!")
        
        # Jalankan aplikasi
        app.run()
        
    except Exception as e:
        st.error(f"❌ Terjadi kesalahan fatal: {str(e)}")
