# Veo si existe la cancion que se pone en el menu principal
if os.path.exists('Canciones/Indie Rock'):
    if os.path.isfile('Canciones/Indie Rock/The Killers - Mr. Brightside.wav'):
        pass

    else:
        self.send.emit(['cancion inicio'])
else:
    self.send.emit(['cancion inicio'])