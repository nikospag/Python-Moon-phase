#!/usr/bin/python3

import ephem
import math
from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

moonpath = "/home/nikospag/Downloads/conky-weather-master/moon.png" #Input (full moon) image file path
phasepath = "/home/nikospag/.cache/conky/phase.png" #Output image file path
textpath = "/home/nikospag/.cache/conky/moon.txt" # Output text file path
m = ephem.Moon()
s = ephem.Sun()
m.compute()
s.compute()
sun_glon = ephem.degrees(s.hlon + math.pi).norm
moon_glon = m.hlon
age = ephem.degrees(moon_glon - sun_glon).norm
age = age / (2 * math.pi) * 100
au = ephem.meters_per_au
m_au = m.earth_distance
dist = m_au * au / 1000
a = m.elong
dt = ephem.next_full_moon(ephem.now())
dtlocal = ephem.localtime(dt)
fullmoon = dtlocal.strftime('%d %b, %H:%M')
phase = m.moon_phase
illum = phase * 100
phase = 1 - phase
if a > 0:
    phase = -phase

with Image(filename=moonpath) as img:
    radius = img.height // 2
    with Drawing() as draw:
        draw.fill_color = Color("rgba(0, 0, 0, 0.7)")
        if phase < 0:
            phase = abs(phase)
            for y in range(radius):
                x = math.sqrt(radius**2 - y**2)
                x = round(x)
                X = radius - x
                Y = radius - y
                Y_mirror = radius + y
                moon_width = 2 * (radius - X)
                shade = moon_width * phase
                shade = round(shade)
                x_shade = X + shade
                draw.line((X, Y), (x_shade, Y))
                if Y_mirror != Y:
                    draw.line((X, Y_mirror), (x_shade, Y_mirror))
            draw(img)
            img.save(filename=phasepath)

        elif phase > 0:
            phase = abs(phase)
            for y in range(radius):
                x = math.sqrt(radius**2 - y**2)
                x = round(x)
                X = radius + x
                Y = radius - y
                Y_mirror = radius + y
                moon_width = 2 * (radius - X)
                shade = moon_width * phase
                shade = round(shade)
                x_shade = X + shade
                draw.line((X, Y), (x_shade, Y))
                if Y_mirror != Y:
                    draw.line((X, Y_mirror), (x_shade, Y_mirror))
            draw(img)
            img.save(filename=phasepath)

with open(textpath, "w") as file:
    file.write("{:.2f}\n".format(age))
    file.write("{:.2f}\n".format(illum))
    file.write("{:.0f}\n".format(dist))
    file.write("{}\n".format(fullmoon))
