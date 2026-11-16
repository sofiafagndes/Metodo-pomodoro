# Método Pomodoro

Aplicativo de Pomodoro feito em Python com `tkinter`, usando programação orientada a objetos.
O programa alterna automaticamente entre **tempo de foco** e **tempo de pausa**, e só para quando o usuário encerra o ciclo.

## Funcionalidades

- Cronômetro com círculo de progresso (`Canvas`) e relógio digital.
- Tempos de foco e de pausa configuráveis (de 1 a 59 minutos). Padrão: 25 e 5 minutos.
- Troca automática entre foco e pausa, sem parar.
- Botões: Iniciar/Pausar/Continuar, Resetar, Fim, Modo Foco e Pausa Curta.
- Validação das entradas com `try/except`.

## Atalhos do teclado

| Tecla | Ação |
|---|---|
| Espaço | Iniciar / Pausar / Continuar |
| Espaço duas vezes seguidas | Encerrar o ciclo |
| R | Resetar o tempo |

O botão **Fim** também encerra o ciclo.

## Como executar

Requisitos: Python 3 com `tkinter` (já vem na instalação padrão do Python no Windows e no macOS).

```bash
python pomodoro.py
```

## Estrutura do código

- `Time`, `time_to_int` e `int_to_time`: representação do tempo em horas, minutos e segundos e conversão de/para segundos.
- `PomodoroApp(tk.Tk)`: interface gráfica e lógica do cronômetro.
  - `__init__`: monta a janela, os widgets (`pack`, `grid` e `place`) e os eventos de teclado (`.bind`).
  - `atualizar_interface`: atualiza o relógio e o arco de progresso.
  - `ciclo_timer`: loop de 1 segundo com `after()` e troca automática de modo.
  - `alternar_timer`, `resetar_timer`, `set_modo`, `parar_ciclo`: controle do cronômetro.
  - `definir_tempo_customizado`: lê e valida os tempos digitados.

## Autores

Sofia Fagundes
Sophia Graf
Isabella Miranda
