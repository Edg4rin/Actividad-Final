from umqtt.simple import MQTTClient
import machine
import time
import network
import dht

# Configuración de MQTT
mqtt_host = "mqtt3.thingspeak.com"
mqtt_channel_id = "2776829"  # Reemplaza con tu Channel ID
mqtt_publish_topic = f"channels/{mqtt_channel_id}/publish"
mqtt_client_id = "Dy8mOx02NDYsABAiIyMSFjo"  # Client ID proporcionado
mqtt_username = "Dy8mOx02NDYsABAiIyMSFjo"  # Username proporcionado
mqtt_password = "DiFOK8FwcUs7GwA4YBa+NCdT"  # Reemplaza con tu password completo

# Configuración de DHT11
dht_pin = machine.Pin(6)  # Pin en el que está conectado el sensor DHT11
dht_sensor = dht.DHT11(dht_pin)

# Conexión a WiFi
def connect_wifi():
    print('Conectando a WiFi...')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('INFINITUM3146', 'Ee5Fb9Pj8w')  # Reemplaza con tus credenciales WiFi
    while not wlan.isconnected():
        pass
    print('Conectado a WiFi')
    print('IP address:', wlan.ifconfig()[0])

# Conexión a MQTT
def connect_mqtt():
    print('Conectando a MQTT...')
    try:
        client = MQTTClient(
            client_id=mqtt_client_id,
            server=mqtt_host,
            port=1883,
            user=mqtt_username,
            password=mqtt_password
        )
        client.connect()
        print('Conectado a MQTT')
        return client
    except Exception as e:
        print(f'Error de conexión MQTT: {e}')
        return None

# Función para publicar datos a ThingSpeak
def publish_data(client, temperature, humidity):
    try:
        # Crear el mensaje como un string simple
        message = f"field1={temperature}&field2={humidity}"
        
        client.publish(mqtt_publish_topic, message)  # Publicar el mensaje en el tema de ThingSpeak
        print(f"Mensaje publicado a ThingSpeak: {message}")
    except Exception as e:
        print(f"Error al publicar datos: {e}")

# Función para leer los datos del sensor DHT11
def read_dht11():
    try:
        dht_sensor.measure()  # Toma la lectura del sensor
        temperature = dht_sensor.temperature()  # Temperatura en grados Celsius
        humidity = dht_sensor.humidity()  # Humedad en porcentaje
        print("Temperatura: {} C, Humedad: {} %".format(temperature, humidity))
        return temperature, humidity
    except Exception as e:
        print("Error al leer el sensor:", e)
        return None, None

# Función para guardar los datos en un archivo de texto
def save_data_to_file(temperature, humidity):
    try:
        with open('/datos_dht11.txt', 'a') as file:  # Guarda en la memoria flash interna
            file.write("Temperatura: {} C, Humedad: {} %\n".format(temperature, humidity))
            print("Datos guardados en el archivo.")
    except Exception as e:
        print(f"Error al guardar los datos en el archivo: {e}")

# Main
if __name__ == "__main__":
    connect_wifi()  # Conectarse a WiFi
    client = connect_mqtt()  # Conectarse al servidor MQTT

    if client:
        while True:
            temperature, humidity = read_dht11()  # Leer datos del sensor
            if temperature is not None and humidity is not None:
                publish_data(client, temperature, humidity)  # Publicar datos a ThingSpeak
                save_data_to_file(temperature, humidity)  # Guardar datos en archivo
            time.sleep(10)  # Espera de 10 segundos antes de tomar otra lectura
    else:
        print("No se pudo conectar al servidor MQTT")