
"""
Created on Sun Nov  8 16:41:07 2026

@author: Sofia
"""



import tkinter as tk


class Time:
    def __init__(self, hour=0, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second

def time_to_int(t):
    minutes = t.hour * 60 + t.minute
    seconds = minutes * 60 + t.second
    return seconds

def int_to_time(seconds):
    t = Time()
    minutes, t.second = divmod(seconds, 60)
    t.hour, t.minute = divmod(minutes, 60)
    return t


class PomodoroApp(tk.Tk):
    def __init__(self):
        super().__init__()

      
        self.title("Método Pomodoro")
        self.geometry("450x620")
        self.configure(bg="#FFB6C1")  
        self.resizable(False, False)

       
        self.minutos_foco = 25
        self.minutos_pausa = 5
        self.modo_atual = "foco"
        self.tempo_total = self.minutos_foco * 60   
        self.tempo_restante = self.tempo_total
        self.rodando = False
        self.timer_id = None
        self.ultimo_espaco = 0

     
        self.lbl_status = tk.Label(
            self,
            text="SESSÃO DE FOCO",
            font=("Helvetica", 16, "bold"),
            fg="#4A0E17",             
            bg="#FFB6C1"              
        )
        self.lbl_status.pack(pady=15)

      
        self.canvas = tk.Canvas(self, width=260, height=260, bg="#FFB6C1", highlightthickness=0)
        self.canvas.pack(pady=10)

        
        self.canvas.create_oval(15, 15, 245, 245, outline="#FFB6C1", width=14)

        
        self.arc_progresso = self.canvas.create_arc(
            15, 15, 245, 245,
            start=90,
            extent=360,
            outline="#4A0E17",    
            width=14,
            style=tk.ARC
        )

  
        self.txt_tempo = self.canvas.create_text(
            130, 130,
            text="25:00",
            font=("Helvetica", 36, "bold"),
            fill="#4A0E17"          
        )

        
        self.frame_config = tk.Frame(self, bg="#FFB6C1")  
        self.frame_config.pack(pady=10)

        self.lbl_foco = tk.Label(
            self.frame_config, text="Foco (min):", font=("Helvetica", 11, "bold"), fg="#4A0E17", bg="#FFB6C1"
        )
        self.lbl_foco.grid(row=0, column=0, padx=5, pady=2, sticky="e")

        self.ent_foco = tk.Entry(self.frame_config, width=6, font=("Helvetica", 11), justify="center")
        self.ent_foco.insert(0, "25")
        self.ent_foco.grid(row=0, column=1, padx=5, pady=2)

        self.lbl_pausa = tk.Label(
            self.frame_config, text="Pausa (min):", font=("Helvetica", 11, "bold"), fg="#4A0E17", bg="#FFB6C1"
        )
        self.lbl_pausa.grid(row=1, column=0, padx=5, pady=2, sticky="e")

        self.ent_pausa = tk.Entry(self.frame_config, width=6, font=("Helvetica", 11), justify="center")
        self.ent_pausa.insert(0, "5")
        self.ent_pausa.grid(row=1, column=1, padx=5, pady=2)

        self.btn_definir = tk.Button(
            self.frame_config,
            text="Definir",
            font=("Helvetica", 10, "bold"),
            bg="#DB7093",
            fg="white",
            command=self.definir_tempo_customizado
        )
        self.btn_definir.grid(row=0, column=2, rowspan=2, padx=8, sticky="ns")

     
        self.frame_botoes = tk.Frame(self, bg="#FFB6C1")  
        self.frame_botoes.pack(pady=15)

        self.btn_iniciar = tk.Button(
            self.frame_botoes,
            text="Iniciar (Espaço)",
            font=("Helvetica", 12, "bold"),
            bg="GREEN",
            fg="white",
            width=14,
            command=self.alternar_timer
        )
        self.btn_iniciar.grid(row=0, column=0, padx=8)

        self.btn_resetar = tk.Button(
            self.frame_botoes,
            text="Resetar (R)",
            font=("Helvetica", 12, "bold"),
            bg="#DC143C",
            fg="white",
            width=10,
            command=self.resetar_timer
        )
        self.btn_resetar.grid(row=0, column=1, padx=8)

        self.btn_fim = tk.Button(
            self.frame_botoes,
            text="Fim",
            font=("Helvetica", 12, "bold"),
            bg="#4A0E17",
            fg="white",
            width=6,
            command=self.parar_ciclo
        )
        self.btn_fim.grid(row=0, column=2, padx=8)

     
        self.frame_modos = tk.Frame(self, bg="#FFB6C1") 
        self.frame_modos.pack(pady=5)

        self.btn_foco = tk.Button(
            self.frame_modos, text="Modo Foco (25m)", font=("Helvetica", 10, "bold"), bg="#DB7093", fg="white",
            command=lambda: self.set_modo("foco")
        )
        self.btn_foco.grid(row=0, column=0, padx=5)

        self.btn_descanso = tk.Button(
            self.frame_modos, text="Pausa Curta (5m)", font=("Helvetica", 10, "bold"), bg="#DB7093", fg="white",
            command=lambda: self.set_modo("pausa")
        )
        self.btn_descanso.grid(row=0, column=1, padx=5)

       
        self.lbl_dica = tk.Label(
            self, text="Atalhos: [Espaço] Iniciar/Pausar | [R] Resetar\n[Espaço x2] ou botão Fim: Encerrar ciclo",
            font=("Helvetica", 9, "bold"), fg="#4A0E17", bg="#FFB6C1"
        )
        self.lbl_dica.place(relx=0.5, rely=0.94, anchor=tk.CENTER)

      
        self.bind("<space>", self.ao_pressionar_espaco)
        self.bind("<r>", self.ao_pressionar_r)
        self.bind("<R>", self.ao_pressionar_r)

 

    def atualizar_interface(self):
        t_obj = int_to_time(self.tempo_restante)

        texto_str = f"{t_obj.minute:02d}:{t_obj.second:02d}"
        self.canvas.itemconfig(self.txt_tempo, text=texto_str)

        if self.tempo_total > 0:
            proporcao = self.tempo_restante / self.tempo_total
            extensao_arco = proporcao * 360
        else:
            extensao_arco = 0

        self.canvas.itemconfig(self.arc_progresso, extent=extensao_arco)

    def ciclo_timer(self):
        if self.rodando and self.tempo_restante > 0:
            self.tempo_restante -= 1
            self.atualizar_interface()
            self.timer_id = self.after(1000, self.ciclo_timer)
        elif self.tempo_restante == 0:
            self.rodando = False
           
            proximo = "pausa" if self.modo_atual == "foco" else "foco"
            self.set_modo(proximo)
            self.alternar_timer()

    def alternar_timer(self):
        if not self.rodando:
            if self.tempo_restante > 0:
                self.rodando = True
                self.btn_iniciar.configure(text="Pausar (Espaço)", bg="#FFFDD0", fg="#4A0E17")
                self.ciclo_timer()
        else:
            self.rodando = False
            if self.timer_id:
                self.after_cancel(self.timer_id)
            self.btn_iniciar.configure(text="Continuar (Espaço)", bg="#FDFD96")

    def resetar_timer(self):
        self.rodando = False
        if self.timer_id:
            self.after_cancel(self.timer_id)
        self.tempo_restante = self.tempo_total
        self.btn_iniciar.configure(text="Iniciar (Espaço)", bg="green", fg="white")
        self.atualizar_interface()

    def set_modo(self, modo):
        self.resetar_timer()
        self.modo_atual = modo

        if modo == "foco":
            minutos = self.minutos_foco
            titulo = "SESSÃO DE FOCO"
        else:
            minutos = self.minutos_pausa
            titulo = "HORA DO DESCANSO!"

        self.tempo_total = minutos * 60
        self.tempo_restante = self.tempo_total
        self.lbl_status.configure(text=titulo, fg="#4A0E17")
        self.atualizar_interface()

    def definir_tempo_customizado(self):
        try:
            foco = int(self.ent_foco.get())
            pausa = int(self.ent_pausa.get())
        
            if not (1 <= foco <= 59) or not (1 <= pausa <= 59):
                raise ValueError("Os tempos devem estar entre 1 e 59 minutos.")

            self.minutos_foco = foco
            self.minutos_pausa = pausa

            
            self.btn_foco.configure(text=f"Modo Foco ({foco}m)")
            self.btn_descanso.configure(text=f"Pausa Curta ({pausa}m)")

            
            self.set_modo(self.modo_atual)
        except ValueError:
            self.lbl_status.configure(text="ERRO: Digite minutos válidos (1-59)!", fg="#DC143C")

    def ao_pressionar_espaco(self, event):
      
        if event.time - self.ultimo_espaco < 500:
            self.ultimo_espaco = 0
            self.parar_ciclo()
        else:
            self.ultimo_espaco = event.time
            self.alternar_timer()

    def parar_ciclo(self):
        self.set_modo("foco")
        self.lbl_status.configure(text="CICLO ENCERRADO", fg="#DC143C")

    def ao_pressionar_r(self, event):
        self.resetar_timer()

if __name__ == "__main__":
    app = PomodoroApp()
    app.mainloop()