
#Wireless Communication using Access Point Mode of RPi Pico W 
#Libraries 

import network 
import socket 
import time 
import machine 
import math 

#Create an Access Point 

ssid = 'AAA_PICO_AP' 
password = 'Triple A' 
ap = network.WLAN(network.AP_IF) 
ap.config(essid=ssid, password=password) 
ap.active(True) # Activate the access point 

while ap.active() == False: 
    pass 

print('Connection is successful') 
print(ap.ifconfig()) # this line will print the IP address of the Pico board 

#Create a socket server 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind(('', 80)) 
s.listen(1)# maximum number of requests that can be queued 

#create a web page 

def web_page(light_state, tempvalue, temp_state, ac_state, occupancy, reserve_status): 
    
    html = """  

   <html>  
    <head>  
    <title>Triple A HVAC System</title>
    <meta charset="UTF-8">
    <script>
        function autoRefresh() {
            window.location.reload(true);
        }
        setInterval(autoRefresh, 5000); // Refresh every 5 seconds
        
        function updateClock() {
        var now = new Date();
        document.getElementById("clock").innerHTML = now.toLocaleTimeString();
        }
        setInterval(updateClock, 1000);
        updateClock();
    </script>
    </head>
    
    <body style="font-family: Arial; margin:0; background:#f4f6f9;">

      <!-- Nav bar -->
      <div style="background:#1a1a2e; color:white; padding:12px 24px; display:flex; justify-content:space-between; align-items:center;">
        <h2 style="margin:0;">Triple A Facilities</h2>
        <span id="clock" style="font-size:13px; color:#aaa;"></span>
      </div>

      <!-- Status banner -->
      <div id="banner" style="background:#28a745; color:white; text-align:center; padding:8px; font-size:14px;">
        All Systems Normal
      </div>

      <!-- Cards grid -->
      <div style="display:grid; grid-template-columns: repeat(2,1fr); gap:16px; padding:20px; max-width:800px; margin:auto;">

        <!-- Building Status card -->
        <div style="background:white; border-radius:12px; padding:20px; box-shadow:0 2px 8px rgba(0,0,0,0.08);">
          <div style="font-size:12px; color:#888; text-transform:uppercase;">Building Status</div>
          <div style="font-size:28px; font-weight:bold; margin:8px 0;" id="status">--</div>
        </div>

        <!-- Temperature card -->
        <div style="background:white; border-radius:12px; padding:20px; box-shadow:0 2px 8px rgba(0,0,0,0.08);">
          <div style="font-size:12px; color:#888; text-transform:uppercase;">Temperature</div>
          <div style="font-size:28px; font-weight:bold; margin:8px 0;" id="temp">--</div>
          <div id="tempstate" style="font-size:13px; color:#888;">TEMP_STATE</div>
        </div>

        <!-- Occupancy card -->
        <div style="background:white; border-radius:12px; padding:20px; box-shadow:0 2px 8px rgba(0,0,0,0.08);">
          <div style="font-size:12px; color:#888; text-transform:uppercase;">Occupancy</div>
          <div style="font-size:28px; font-weight:bold; margin:8px 0;" id="occ">OCCUPANCY</div>
          <div style="font-size:28px; font-weight:bold; margin:8px 0;" id="reservation">RESERVE_STATUS</div>
          <span id="occ_indicator" style="color:green; font-size:20px;">Reserved when motion is detected or manually reserved</span>
        </div>

        <!-- AC Status card -->
        <div style="background:white; border-radius:12px; padding:20px; box-shadow:0 2px 8px rgba(0,0,0,0.08);">
          <div style="font-size:12px; color:#888; text-transform:uppercase;">AC Status</div>
          <div style="font-size:28px; font-weight:bold; margin:8px 0;" id="ac">OFF</div>
          <span id="green" style="color:gray; font-size:20px;">AC is automatic</span>
        </div>
        
      </div>

      
      <!-- Buttons -->
      <div style="text-align:center; padding:0 20px 20px;">
        
        <!-- Occupancy Buttons -->
        
        <button onclick="window.location.href='/reserve'"
          style="padding:10px 24px; background:#28a745; color:white; border:none; border-radius:8px; margin:4px; font-size:14px; cursor:pointer;">
          Reserve Room
        </button>
        <button onclick="window.location.href='/unreserve'"
          style="padding:10px 24px; background:#6c757d; color:white; border:none; border-radius:8px; margin:4px; font-size:14px; cursor:pointer;">
          Cancel Reservation
        </button>
        
        <!-- AC Buttons -->
        
        <button onclick="window.location.href='/on'"
          style="padding:10px 24px; background:#007BFF; color:white; border:none; border-radius:8px; margin:4px; font-size:14px; cursor:pointer;">
          Turn AC ON
        </button>
        <button onclick="window.location.href='/off'"
          style="padding:10px 24px; background:#dc3545; color:white; border:none; border-radius:8px; margin:4px; font-size:14px; cursor:pointer;">
          Turn AC OFF
        </button>
    
      </div>

      <!-- Footer -->
      <div style="text-align:center; font-size:12px; color:#aaa; padding:12px;">
        Triple A HVAC System — Auto-refreshes every 5 seconds
      </div>
     
    <script>  

    // VARIABLES (replace with real sensor values)  
 
    var temperature = TEMP_VALUE;  
    var occupancy = 0;  
    var lightOn = LIGHT_VALUE;  
    var acOn = AC_STATE;  

    // MAIN FUNCTION  
    function updateSystem() {  
 
    // GET SENSOR VALUES HERE  
 
    // temperature = ...  
 
    // occupancy = ...  
 
    // lightOn = ...  
 
    // BASIC LOGIC   
 
    if (lightOn == true) {  
        document.getElementById("status").innerHTML = "Light ON";  

 
    } else {  
 
        document.getElementById("status").innerHTML = "Light OFF";  
    
        acOn = false;  
 
    }  
 
      
 
    // DISPLAY VALUES   
 
    document.getElementById("temp").innerHTML = temperature + " ˚C";  
  
      
 
    if (acOn == true) {  
 
        document.getElementById("ac").innerHTML = "ON";  
    
        document.getElementById("green").style.color = "green";  
 
    } else {  
 
        document.getElementById("ac").innerHTML = "OFF";  
    
        document.getElementById("green").style.color = "gray";  
 
    }  
 
      
    if (lightOn == false) {
        document.getElementById("occ_indicator").style.color = "gray";
        
    } else if (occupancy > 0) {
        document.getElementById("occ_indicator").style.color = "red";
        
    } else {
        document.getElementById("occ_indicator").style.color = "green";
    }
    if (lightOn == true) {
        document.getElementById("temp").innerHTML = temperature + " ˚C";  
    } else {
        document.getElementById("temp").style.textDecoration = "line-through";
    }

    }  

    // BUTTON FUNCTION  
    function toggleAC() {  
    acOn = !acOn;  

    // ===== SEND DATA TO MICROCONTROLLER HERE =====  
    // sendAC(acOn);  
    updateSystem();  
    }  
    // LOOP (updates every 2 secs)  
 
    updateSystem();  
    </script>  
    </body>  
    </html>  
    
        """ 
    return html 
  
#Matching sensors to correct pins on breadboard
lightsensor = machine.ADC(26) 
led1 = machine.Pin(16, machine.Pin.OUT)
temp_sensor = machine.ADC(28)
light_state = False
led2 = machine.Pin(17, machine.Pin.OUT)
ac_state = False
pir_sensor = machine.Pin(15, machine.Pin.IN)
            #            ^^---------------------------------------------------------------------------------------FIX!!!!!

            
occupancy = False
manual_on = False #manual override button on
manual_off = False #manual override button off
reserved = False


#Response when connection received 
while True: 
    
    try: 
        conn, addr = s.accept() 
    except OSError as e: 
        print("socket error:", e)
        continue 

    print('Got a connection from %s' % str(addr)) 
    request = conn.recv(1024)
    request_str = str(request)
    # Extract path from request
    path = request_str.split(' ')[1] if ' ' in request_str else '/'
    print("Path received:", path)  # ← add this
    
    print('\nRaspberry PICO Data:\n----------------------------') 

        
    #--------AC button code----------
    if path == "/on":
        led2.value(1)
        ac_state = True
        manual_on = True
        manual_off = False
        
    elif path == "/off":
        led2.value(0)
        ac_state = False
        manual_on = False
        manual_off = True
        
    elif path == "/reset":
        manual_on = False
        manual_off = False
        reserved = False
        print("All states reset")
        
        
    #--------Reservation button code----------
    elif path == "/reserve":
        reserved = True
        print("Room reserved")
        occupancy = False
        
    elif path == "/unreserve":
        reserved = False
        print("Reservation cancelled")
        
    elif path == "/":
        print("Normal page load")
        
    #Declarations of all sensors
    Sensor_out = lightsensor.read_u16() 
    tempsensorvalue = temp_sensor.read_u16() 

    #1.0 LIGHT webpage logic
    print("Raw light sensor value:", Sensor_out)
    
    if Sensor_out < 64000: 
        light_state = True
        led1.value(1)  
        print("light detected") 
    
    else: 
        light_state = False 
        led1.value(0)
        print("light not detected")  
    
    #reset independant AC control
    if light_state == False:
        manual_on = False
        manual_off = False
        led2.value(0)
        ac_state = False
        print("Building closed - AC reset")
    
    #2.0 temp_sensor
    print("Raw Temp:", tempsensorvalue) 
    tempvalue = round((1 / (1/298 + (1/3950) * math.log((65535 / tempsensorvalue) - 1))) - 212, 1)
    print("Temperature:", tempvalue, "˚C") 


    if tempvalue > 23: 
        temp_state = "Temperature is above thermal comfort maximum of 23˚C"
        print("Temperature is high") 

    elif tempvalue < 20: 
        temp_state = "Temperature is below thermal comfort minimum of 20˚C"
        print("Temperature is low")
        

    else: 
        temp_state = "In range"
        print("Temperature is in range")


    #3.0 PIR Sensor...
    # 3.0 PIR Sensor (FIXED)

    pir_value = pir_sensor.value()
    print("PIR raw value:", pir_value)

    if pir_value == 1:
        occupancy = True
        print("Occupancy detected")
    else:
        occupancy = False
        print("No motion")
    
    # reservation code
    if reserved == True and occupancy == True:
        reserve_status = "Room is Occupied"
        occupancy = False

        
    elif reserved == True and occupancy == False:
        reserve_status = "Reserved - Successful"
        occupancy_status = "Occupied" if occupancy else "Vacant"
        
    else:
        reserve_status = "---"
    
    #trouble shoot
    print("manual_off:", manual_off)
    print("manual_on:", manual_on)
    print("light_state:", light_state)
    print("tempvalue:", tempvalue)
        
    #4.0 AC LOGIC (manual override)
    if manual_off == True:
        led2.value(0) 
        ac_state = False
        print("AC manually forced off")

    elif manual_on == True:
        led2.value(1)
        ac_state = True
        print("AC manually forced on")

    else:
        if light_state == True and tempvalue > 23:
            led2.value(1)
            ac_state = True
            print("AC auto turned on")
        else:
            led2.value(0)
            ac_state = False
            print("AC auto turned off")

    print('----------------------------\n')
    time.sleep(0.2) 


    # Update webpage with correct light value and temperature value
    html = web_page(light_state, tempvalue, temp_state, ac_state, occupancy, reserve_status)
    html = html.replace("LIGHT_VALUE", str(light_state).lower())
    html = html.replace("TEMP_VALUE", str(tempvalue))
    html = html.replace("TEMP_STATE", str(temp_state))
    html = html.replace("AC_STATE", str(ac_state).lower())
    html = html.replace("OCCUPANCY", "Occupied" if occupancy else "Vacant")
    html = html.replace("RESERVE_STATUS", reserve_status)
    response = html
    
    conn.send("HTTP/1.1 200 OK\r\n") 
    conn.send("Content-Type: text/html\r\n") 
    conn.send("Connection: close\r\n\r\n") 
    conn.sendall(response) 
    conn.close() 

    print('Content = %s' % request)

