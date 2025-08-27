import tkinter as tk
from tkinter import messagebox, ttk
import os
import pandas as pd

def aggiungi_voce(tipo_voce):
    """Aggiunge una spesa o un'entrata e aggiorna l'interfaccia."""
    descrizione = descrizione_entry.get()
    importo_str = importo_entry.get()
    categoria = categoria_entry.get()

    if not descrizione or not importo_str or not categoria:
        messagebox.showerror("Errore", "Per favore, compila tutti i campi.")
        return

    try:
        importo = float(importo_str)
    except ValueError:
        messagebox.showerror("Errore", "L'importo deve essere un numero valido.")
        return

    file_name = "spese.txt" if tipo_voce == "spesa" else "entrate.txt"
    with open(file_name, "a") as file:
        file.write(f"{descrizione},{importo},{categoria}\n")
    
    pulisci_campi()
    aggiorna_treeview()
    aggiorna_saldo_visibile()
    nascondi_campi_input()
    messagebox.showinfo("Successo", f"{tipo_voce.capitalize()} aggiunta con successo!")

def calcola_saldo():
    """Ritorna il saldo finanziario."""
    totale_spese = 0.0
    if os.path.exists("spese.txt") and os.path.getsize("spese.txt") > 0:
        with open("spese.txt", "r") as file:
            for riga in file:
                try:
                    _, importo_str, _ = riga.strip().split(',')
                    totale_spese += float(importo_str)
                except (ValueError, IndexError):
                    continue

    totale_entrate = 0.0
    if os.path.exists("entrate.txt") and os.path.getsize("entrate.txt") > 0:
        with open("entrate.txt", "r") as file:
            for riga in file:
                try:
                    _, importo_str, _ = riga.strip().split(',')
                    totale_entrate += float(importo_str)
                except (ValueError, IndexError):
                    continue

    return totale_entrate - totale_spese

def aggiorna_saldo_visibile():
    """Aggiorna la label del saldo."""
    saldo = calcola_saldo()
    saldo_label.config(text=f"Saldo Finale: {saldo:.2f}€")

def pulisci_campi():
    """Pulisce i campi di input."""
    descrizione_entry.delete(0, tk.END)
    importo_entry.delete(0, tk.END)
    categoria_entry.delete(0, tk.END)

def aggiorna_treeview():
    """Legge i dati e aggiorna la TreeView."""
    for item in tree.get_children():
        tree.delete(item)

    if os.path.exists("entrate.txt") and os.path.getsize("entrate.txt") > 0:
        with open("entrate.txt", "r") as file:
            for riga in file:
                try:
                    desc, imp, cat = riga.strip().split(',')
                    tree.insert("", "end", values=(desc, float(imp), cat, "Entrata"), tags=("entrata",))
                except (ValueError, IndexError):
                    continue

    if os.path.exists("spese.txt") and os.path.getsize("spese.txt") > 0:
        with open("spese.txt", "r") as file:
            for riga in file:
                try:
                    desc, imp, cat = riga.strip().split(',')
                    tree.insert("", "end", values=(desc, float(imp), cat, "Spesa"), tags=("spesa",))
                except (ValueError, IndexError):
                    continue

def esporta_in_excel():
    """Esporta i dati combinati in un file Excel."""
    try:
        spese_df = pd.read_csv("spese.txt", header=None, names=['Descrizione', 'Importo', 'Categoria'])
        spese_df['Tipo'] = 'Spesa'
    except (pd.errors.EmptyDataError, FileNotFoundError):
        spese_df = pd.DataFrame(columns=['Descrizione', 'Importo', 'Categoria', 'Tipo'])
    
    try:
        entrate_df = pd.read_csv("entrate.txt", header=None, names=['Descrizione', 'Importo', 'Categoria'])
        entrate_df['Tipo'] = 'Entrata'
    except (pd.errors.EmptyDataError, FileNotFoundError):
        entrate_df = pd.DataFrame(columns=['Descrizione', 'Importo', 'Categoria', 'Tipo'])

    dati_completi = pd.concat([spese_df, entrate_df], ignore_index=True)
    dati_completi['Importo'] = dati_completi.apply(lambda row: -abs(row['Importo']) if row['Tipo'] == 'Spesa' else abs(row['Importo']), axis=1)
    dati_completi.to_excel("resoconto_finanziario.xlsx", index=False)
    messagebox.showinfo("Esportazione Completata", "Dati esportati con successo in 'resoconto_finanziario.xlsx'")

def mostra_campi_input(tipo):
    """Mostra i campi di input e imposta il comando del pulsante 'Salva'."""
    nascondi_campi_input()
    input_frame.pack(pady=10)
    
    if tipo == "spesa":
        salva_button.config(text="Salva Spesa", command=lambda: aggiungi_voce("spesa"))
    else:
        salva_button.config(text="Salva Entrata", command=lambda: aggiungi_voce("entrata"))
    
    salva_button.pack(fill="x", padx=10, pady=5)
    pulisci_campi()
    
def nascondi_campi_input():
    """Nasconde i campi di input."""
    input_frame.pack_forget()
    salva_button.pack_forget()

# Configurazione della finestra principale
root = tk.Tk()
root.title("Gestore Finanze Personali")
root.geometry("900x600") # Larghezza totale ridotta di 300 pixel (da 1200 a 900)
# Per mantenere il layout più compatto, si può evitare l'opzione a tutto schermo
# root.state('zoomed') 

# Creazione dei frame
left_frame = tk.Frame(root, width=160, bg="#f0f0f0") # Larghezza del menu ridotta di 40 pixel (da 200 a 160)
right_frame = tk.Frame(root)
bottom_frame = tk.Frame(root, bg="#f0f0f0", pady=10)

left_frame.pack(side="left", fill="y")
right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
bottom_frame.pack(side="bottom", fill="x")

# Menu e pulsanti nel frame sinistro
tk.Label(left_frame, text="Menu", font=("Helvetica", 14, "bold"), bg="#f0f0f0").pack(pady=10)

tk.Button(left_frame, text="Aggiungi Spesa", command=lambda: mostra_campi_input("spesa")).pack(fill="x", padx=10, pady=5)
tk.Button(left_frame, text="Aggiungi Entrata", command=lambda: mostra_campi_input("entrata")).pack(fill="x", padx=10, pady=5)
tk.Button(left_frame, text="Esporta in Excel", command=esporta_in_excel).pack(fill="x", padx=10, pady=5)

# Frame per i campi di input (nascosto inizialmente)
input_frame = tk.Frame(left_frame, bg="#f0f0f0")
tk.Label(input_frame, text="Descrizione:", bg="#f0f0f0").pack(pady=2)
descrizione_entry = tk.Entry(input_frame)
descrizione_entry.pack(pady=2)
tk.Label(input_frame, text="Importo (€):", bg="#f0f0f0").pack(pady=2)
importo_entry = tk.Entry(input_frame)
importo_entry.pack(pady=2)
tk.Label(input_frame, text="Categoria:", bg="#f0f0f0").pack(pady=2)
categoria_entry = tk.Entry(input_frame)
categoria_entry.pack(pady=2)

# Pulsante Salva (nascosto inizialmente)
salva_button = tk.Button(left_frame)

# TreeView nel frame destro
columns = ('descrizione', 'importo', 'categoria', 'tipo')
tree = ttk.Treeview(right_frame, columns=columns, show='headings')
tree.heading('descrizione', text='Descrizione')
tree.heading('importo', text='Importo (€)')
tree.heading('categoria', text='Categoria')
tree.heading('tipo', text='Tipo')
tree.column('descrizione', width=350) # Larghezza della colonna 'descrizione' aumentata
tree.column('importo', width=120, anchor=tk.CENTER) # Larghezza della colonna 'importo' aumentata
tree.column('categoria', width=180) # Larghezza della colonna 'categoria' aumentata
tree.column('tipo', width=120, anchor=tk.CENTER) # Larghezza della colonna 'tipo' aumentata
tree.tag_configure('entrata', background='lightgreen')
tree.tag_configure('spesa', background='lightcoral')
tree.pack(fill="both", expand=True)

# Label per il saldo nel frame inferiore
saldo_label = tk.Label(bottom_frame, text="Saldo Finale: 0.00€", font=("Helvetica", 14, "bold"), bg="#f0f0f0")
saldo_label.pack(side="left", padx=10, expand=True)

# Aggiornamento iniziale e avvio
aggiorna_treeview()
aggiorna_saldo_visibile()
root.mainloop()