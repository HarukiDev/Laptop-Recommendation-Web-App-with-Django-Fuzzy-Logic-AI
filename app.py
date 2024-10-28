from flask import Flask, render_template, request, jsonify
import pandas as pd
from logika_fuzzy import hitung_kecepatan 

app = Flask(__name__)

# Data awal
df = pd.read_csv("laptop_price.csv", encoding='latin-1')
df = df.drop(['laptop_ID', 'Inches', 'ScreenResolution', 'Cpu', 'Gpu', 'OpSys', 'Weight', 'Price_euros'], axis=1)
df = df.dropna()

# Fungsi untuk menormalisasi kolom Memory ke GB
def normalis_memory(memory_str):
    try:
        if 'TB' in memory_str:
            return int(memory_str.replace('TB SSD', '').replace('TB Flash Storage', '').replace('TB HDD', '').strip()) * 1024
        elif 'GB' in memory_str:
            return int(memory_str.replace('GB SSD', '').replace('GB Flash Storage', '').replace('GB HDD', '').strip())
        else:
            raise ValueError("Format memory tidak dikenal: " + memory_str)
    except ValueError as e:
        return None

df['Memory_GB'] = df['Memory'].apply(normalis_memory)
df = df.dropna(subset=['Memory_GB'])
df = df.drop(['Memory'], axis=1)

# Fungsi untuk konversi RAM dari objek ke int
def ram_to_int(ram_str):
    return int(ram_str.replace('GB', '').strip())

df['Ram_int'] = df['Ram'].apply(ram_to_int)
df = df.drop(['Ram'], axis=1)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ram_value = int(request.form['ram'])
        memory_value = int(request.form['memory'])
        kecepatan = hitung_kecepatan(ram_value, memory_value)

        # Konversi kecepatan ke string
        if kecepatan < 20:
            kecepatan_str = "Lambat"
        elif kecepatan >= 40 and kecepatan < 60:
            kecepatan_str = "Sedang"
        elif kecepatan >= 60 and kecepatan < 80:
            kecepatan_str = "Cepat"
        else:
            kecepatan_str = "Sangat Cepat"

        # Filter laptop berdasarkan RAM dan Memory yang dipilih
        laptop_serupa = df[(df['Ram_int'] == ram_value) & (df['Memory_GB'] == memory_value)]

        return jsonify({'kecepatan': kecepatan_str, 'laptop_serupa': laptop_serupa.to_dict(orient='records')})
    return render_template('index.html', kecepatan=None)

if __name__ == '__main__':  
    app.run(debug=True)
