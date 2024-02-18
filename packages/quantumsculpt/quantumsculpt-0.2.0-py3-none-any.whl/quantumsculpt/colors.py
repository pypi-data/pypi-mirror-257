def adjust_lightness(color, amount=0.5):
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])

red = '#f54e42'
blue = '#1487b8'

gray = '#555555'
grey = '#555555'
black = '#000000'

red_dark = '#941338'
blue_dark = '#134f94'