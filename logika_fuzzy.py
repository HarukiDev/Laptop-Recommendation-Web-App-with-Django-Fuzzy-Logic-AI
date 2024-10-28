import numpy as np
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Definisikan variabel input
ram = ctrl.Antecedent(np.arange(0, 33, 1), 'ram')
memory = ctrl.Antecedent(np.arange(0, 2049, 1), 'memory')

# Definisikan variabel output
kecepatan = ctrl.Consequent(np.arange(0, 101, 1), 'kecepatan')

# Batasan RAM
ram['low'] = fuzz.trimf(ram.universe, [0, 0, 16])
ram['medium'] = fuzz.trimf(ram.universe, [8, 16, 32])
ram['high'] = fuzz.trimf(ram.universe, [16, 32, 32])

# Batasan Memory
memory['low'] = fuzz.trimf(memory.universe, [0, 0, 512])
memory['medium'] = fuzz.trimf(memory.universe, [256, 512, 1024])
memory['high'] = fuzz.trimf(memory.universe, [512, 2048, 2048])

# Batasan kecepatan
kecepatan['slow'] = fuzz.trimf(kecepatan.universe, [0, 0, 50])
kecepatan['average'] = fuzz.trimf(kecepatan.universe, [25, 50, 75])
kecepatan['fast'] = fuzz.trimf(kecepatan.universe, [50, 100, 100])

# Buat aturan fuzzy
rule1 = ctrl.Rule(ram['low'] & memory['low'], kecepatan['slow'])
rule2 = ctrl.Rule(ram['medium'] & memory['medium'], kecepatan['average'])
rule3 = ctrl.Rule(ram['high'] & memory['high'], kecepatan['fast'])
rule4 = ctrl.Rule(ram['medium'] & memory['low'], kecepatan['slow'])
rule5 = ctrl.Rule(ram['low'] & memory['medium'], kecepatan['slow'])
rule6 = ctrl.Rule(ram['high'] & memory['medium'], kecepatan['average'])
rule7 = ctrl.Rule(ram['medium'] & memory['high'], kecepatan['average'])

# Sistem kontrol
kecepatan_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
kecepatan_simulasi = ctrl.ControlSystemSimulation(kecepatan_ctrl)

def hitung_kecepatan(ram_value, memory_value):
    kecepatan_simulasi.input['ram'] = ram_value
    kecepatan_simulasi.input['memory'] = memory_value
    kecepatan_simulasi.compute()
    return kecepatan_simulasi.output['kecepatan']