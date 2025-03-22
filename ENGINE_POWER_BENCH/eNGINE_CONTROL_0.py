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

# Valori PWM (in microsecondi)
MIN_PULSE = 1000  # Minimo throttle (1ms)
MID_PULSE = 1500  # Posizione neutra (1.5ms)
MAX_PULSE = 2000  # Massimo throttle (2ms)

# Velocità attuale (valore da 0 a 100)
# MODIFICA QUESTO VALORE PER CAMBIARE LA VELOCITÀ
VELOCITA = 1  # Imposta da 0 a 100 (0=fermo, 50=metà velocità, 100=massima velocità)

# LED di stato (LED integrato nel Pico)
led = Pin(25, Pin.OUT)

# =============================================================
# FUNZIONI
# =============================================================

# Inizializza il PWM per l'ESC
def inizializza_esc():
    pwm = PWM(Pin(ESC_PIN))
    pwm.freq(50)  # 50Hz è la frequenza standard per gli ESC
    return pwm

# Converte la velocità (0-100) in valore PWM (1000-2000μs)
def velocita_a_pwm(velocita_percentuale):
    # Limita la velocità tra 0 e 100
    velocita_percentuale = max(0, min(100, velocita_percentuale))
    
    # Se la velocità è 0, impostiamo il valore neutro (1500μs)
    if velocita_percentuale == 0:
        return MID_PULSE
    
    # Altrimenti, mappiamo la velocità da 1-100 al range 1500-2000μs
    return MID_PULSE + (velocita_percentuale * (MAX_PULSE - MID_PULSE) // 100)

# Imposta la velocità dell'ESC
def set_speed(pwm, velocita_percentuale):
    # Ottieni il valore PWM dalla velocità percentuale
    pulse_width_us = velocita_a_pwm(velocita_percentuale)
    
    # Converti microsecondi in duty cycle (0-65535)
    duty = int((pulse_width_us / 20000) * 65535)
    
    # Imposta il duty cycle
    pwm.duty_u16(duty)
    
    # Visualizzazione
    print(f"Velocità: {velocita_percentuale}%, PWM: {pulse_width_us}μs")
    
    # Fai lampeggiare il LED per indicare che la velocità è cambiata
    led.value(1)
    time.sleep(0.05)
    led.value(0)

# Sequenza di inizializzazione dell'ESC
def arma_esc(pwm):
    print("\n=== INIZIALIZZAZIONE ESC ===")
    print("Inviando segnale di minimo...")
    
    # Imposta valore minimo
    duty_min = int((MIN_PULSE / 20000) * 65535)
    pwm.duty_u16(duty_min)
    time.sleep(1)
    
    # Imposta valore neutro
    print("Inviando segnale neutro...")
    duty_mid = int((MID_PULSE / 20000) * 65535)
    pwm.duty_u16(duty_mid)
    time.sleep(1)
    
    print("ESC armato e pronto!\n")

# =============================================================
# PROGRAMMA PRINCIPALE
# =============================================================

def main():
    # Inizializza il PWM
    esc_pwm = inizializza_esc()
    
    # Arma l'ESC
    arma_esc(esc_pwm)
    
    print("=== CONTROLLO VELOCITÀ ===")
    print("VELOCITÀ impostata al valore:", VELOCITA)
    print("Per cambiare la velocità, modifica il valore 'VELOCITA' nel codice")
    print("e riavvia il programma.\n")
    
    # Imposta la velocità iniziale
    set_speed(esc_pwm, VELOCITA)
    
    try:
        # Mantieni questa velocità fino all'interruzione
        while True:
            # Fai lampeggiare il LED lentamente per indicare che il programma è in esecuzione
            led.value(1)
            time.sleep(0.5)
            led.value(0)
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        # Ferma il motore in caso di interruzione
        print("\nProgramma interrotto. Fermando il motore...")
        set_speed(esc_pwm, 0)  # Imposta velocità a 0 (neutro)

# =============================================================
# AVVIO DEL PROGRAMMA
# =============================================================

if __name__ == "__main__":
    main()