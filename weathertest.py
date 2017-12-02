import pyowm
owm = pyowm.OWM('ae594305a07bf60780bb6bb61cce49a8')
observation = owm.weather_at_place("Cambridge,us")
w = observation.get_weather()
print(w)
temperature = w.get_temperature('fahrenheit')['temp']
print(temperature)