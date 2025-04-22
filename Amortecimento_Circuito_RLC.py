import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy import signal
import tkinter as tk
from tkinter import ttk

# Função principal que gera os gráficos
def simulate_rlc():
    # Obter valores da interface
    try:
        L = float(entry_L.get()) * 1e-6  # Converte µH para H
        C = float(entry_C.get()) * 1e-6  # Converte µF para F
        R = float(entry_R.get())
        V0 = float(entry_V0.get())
    except:
        tk.messagebox.showerror("Erro", "Valores inválidos! Use números.")
        return

    # Configurações de simulação
    t = np.linspace(0, 1e-3, 10000)  # Tempo: 0 a 1 ms

    # =============================================
    # 1. Simulação Temporal
    # =============================================
    # Circuito RLC Série
    def rlc_serie(y, t, R, L, C):
        i, vc = y
        di_dt = (vc - R * i) / L
        dvc_dt = -i / C
        return [di_dt, dvc_dt]

    y0_serie = [0, V0]  # I0 = 0, V0 definido pelo usuário
    sol_serie = odeint(rlc_serie, y0_serie, t, args=(R, L, C))
    i_L_serie, v_C_serie = sol_serie[:, 0], sol_serie[:, 1]

    # Circuito RLC Paralelo
    def rlc_paralelo(y, t, R, L, C):
        vc, il = y
        dvc_dt = - (vc / R + il) / C
        dil_dt = vc / L
        return [dvc_dt, dil_dt]

    y0_paralelo = [V0, 0]  # V0 definido pelo usuário, I0 = 0
    sol_paralelo = odeint(rlc_paralelo, y0_paralelo, t, args=(R, L, C))
    v_C_paralelo, i_L_paralelo = sol_paralelo[:, 0], sol_paralelo[:, 1]

    # =============================================
    # 2. Diagrama de Bode
    # =============================================
    frequencies = np.logspace(0, 6, 1000)
    w = 2 * np.pi * frequencies

    # Função de Transferência Série
    num_serie = [1/(L*C)]
    den_serie = [1, R/L, 1/(L*C)]
    sys_serie = signal.TransferFunction(num_serie, den_serie)

    # Função de Transferência Paralelo
    num_paralelo = [1/C, 0]
    den_paralelo = [1, 1/(R*C), 1/(L*C)]
    sys_paralelo = signal.TransferFunction(num_paralelo, den_paralelo)

    w, mag_serie, phase_serie = signal.bode(sys_serie, w)
    w, mag_paralelo, phase_paralelo = signal.bode(sys_paralelo, w)

    # =============================================
    # 3. Plotagem dos Resultados
    # =============================================
    plt.figure(figsize=(14, 10))
    plt.rc('font', size=9)

    # Subplot 1: Corrente no Indutor
    plt.subplot(3, 2, 1)
    plt.plot(t * 1e6, i_L_serie, 'b', label='Série', linewidth=1.2)
    plt.plot(t * 1e6, i_L_paralelo, 'r--', label='Paralelo', linewidth=1.2)
    plt.xlabel('Tempo (µs)')
    plt.ylabel('Corrente (A)')
    plt.title('Corrente no Indutor')
    plt.legend()
    plt.grid(alpha=0.5)

    # Subplot 2: Tensão no Capacitor
    plt.subplot(3, 2, 2)
    plt.plot(t * 1e6, v_C_serie, 'b', label='Série', linewidth=1.2)
    plt.plot(t * 1e6, v_C_paralelo, 'r--', label='Paralelo', linewidth=1.2)
    plt.xlabel('Tempo (µs)')
    plt.ylabel('Tensão (V)')
    plt.title('Tensão no Capacitor')
    plt.legend()
    plt.grid(alpha=0.5)

    # Subplot 3: Diagrama de Fase (Série)
    plt.subplot(3, 2, 3)
    plt.plot(i_L_serie, v_C_serie, 'g', linewidth=1.2)
    plt.xlabel('Corrente (A)')
    plt.ylabel('Tensão (V)')
    plt.title('Diagrama de Fase (Série)')
    plt.grid(alpha=0.5)

    # Subplot 4: Diagrama de Fase (Paralelo)
    plt.subplot(3, 2, 4)
    plt.plot(i_L_paralelo, v_C_paralelo, 'm', linewidth=1.2)
    plt.xlabel('Corrente (A)')
    plt.ylabel('Tensão (V)')
    plt.title('Diagrama de Fase (Paralelo)')
    plt.grid(alpha=0.5)

    # Subplot 5: Magnitude do Bode
    plt.subplot(3, 2, 5)
    plt.semilogx(frequencies, mag_serie, 'b', label='Série', linewidth=1.2)
    plt.semilogx(frequencies, mag_paralelo, 'r--', label='Paralelo', linewidth=1.2)
    plt.xlabel('Frequência (Hz)')
    plt.ylabel('Magnitude (dB)')
    plt.title('Diagrama de Bode - Magnitude')
    plt.legend()
    plt.grid(alpha=0.5)

    # Subplot 6: Fase do Bode
    plt.subplot(3, 2, 6)
    plt.semilogx(frequencies, phase_serie, 'b', label='Série', linewidth=1.2)
    plt.semilogx(frequencies, phase_paralelo, 'r--', label='Paralelo', linewidth=1.2)
    plt.xlabel('Frequência (Hz)')
    plt.ylabel('Fase (graus)')
    plt.title('Diagrama de Bode - Fase')
    plt.legend()
    plt.grid(alpha=0.5)

    plt.tight_layout()
    plt.show()

# =============================================
# Interface Gráfica (Tkinter)
# =============================================
root = tk.Tk()
root.title("Simulador RLC - Entrada de Valores")
root.geometry("400x300")
root.configure(bg='#f0f0f0')

# Estilo
style = ttk.Style()
style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
style.configure('TButton', font=('Arial', 10, 'bold'))
style.configure('TEntry', font=('Arial', 10))

# Frame principal
frame = ttk.Frame(root, padding="20")
frame.pack(fill=tk.BOTH, expand=True)

# Labels e Entradas
ttk.Label(frame, text="Indutância (µH):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
entry_L = ttk.Entry(frame)
entry_L.grid(row=0, column=1, padx=5, pady=5)
entry_L.insert(0, "11")  # Valor padrão

ttk.Label(frame, text="Capacitância (µF):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
entry_C = ttk.Entry(frame)
entry_C.grid(row=1, column=1, padx=5, pady=5)
entry_C.insert(0, "180")  # Valor padrão

ttk.Label(frame, text="Resistência (Ω):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
entry_R = ttk.Entry(frame)
entry_R.grid(row=2, column=1, padx=5, pady=5)
entry_R.insert(0, "0.085")  # Valor padrão

ttk.Label(frame, text="Tensão Inicial (V):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
entry_V0 = ttk.Entry(frame)
entry_V0.grid(row=3, column=1, padx=5, pady=5)
entry_V0.insert(0, "900")  # Valor padrão

# Botão de Simulação
button = ttk.Button(frame, text="Simular", command=simulate_rlc)
button.grid(row=4, column=0, columnspan=2, pady=20)

root.mainloop()