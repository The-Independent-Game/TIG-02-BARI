# =============================================================
# CONTROLLO ESC CON RASPBERRY PI PICO 2
# Programma semplice per controllare un ESC tramite PWM
# =============================================================
from machine import Pin, PWM
import time

# =============================================================
# CONFIGURAZIONE
# =============================================================

# Pin utilizzato per il segnale PWM all'ESC
ESC_PIN = 28  # Usa GPIO 28 per il segnale dell'ESC
MIN_PULSE=610
MID_PULSE=1500
FREQ_PULSE= 50    # Frequenza del pwd
PERIOD_PULSE= (1/FREQ_PULSE)*1e6
MAX_16BIT_CON= 65535

PULSE= 610

# Inizializza il PWM per l'ESC
def inizializza_esc():
    pwm = PWM(Pin(ESC_PIN)) 
    pwm.freq(FREQ_PULSE)  # 50Hz è la frequenza standard per gli ESC
    return pwm

# Imposta la velocità dell'ESC
def set_speed(pwm, pulse):
    
    # Converti microsecondi in duty cycle (0-65535)
    duty = int((pulse / PERIOD_PULSE) * MAX_16BIT_CON)
    
    # Imposta il duty cycle
    pwm.duty_u16(duty)

# Sequenza di inizializzazione dell'ESC
def arma_esc(pwm):
    print("\n=== INIZIALIZZAZIONE ESC ===")
    print("Inviando segnale di minimo...")
    
    # Imposta valore minimo
    duty_min = int((MIN_PULSE / PERIOD_PULSE) * MAX_16BIT_CON)
    pwm.duty_u16(duty_min)
    time.sleep(1)
    
    # Imposta valore neutro
    print("Inviando segnale neutro...")
    duty_mid = int((MID_PULSE / PERIOD_PULSE) * MAX_16BIT_CON)
    pwm.duty_u16(duty_mid)
    time.sleep(1)
    
    print("ESC armato e pronto!\n")
    




pwm=inizializza_esc()

# Arma l'ESC
#arma_esc(pwm)

set_speed(pwm, PULSE)
time.sleep(2)
set_speed(pwm, 0)
        