# 🎮 OBS Remoto: Controla OBS con Arduino

Conecta botones a Arduino para controlar las escenas y comenzar y parar las grabaciones.
El código de arduino es básico. Cada vez que se pulsa un botón, imprime en el Serial B0, B1, B2, B3, etc (corresponden con los identificadores de los botones).
El código python lee los mensajes del serial y cada vez que lee que un botón ha sido pulsado, ejecuta la acción configurada

Algunos botones ejecutan acciones como reproducir sonido o para reproduccion de sonido. Estas acciones se conectan por http a otro servidor instalado en otra máquina (yo configuro este OBS remoto lo tengo en mi PC de grabación, y ese otro servidor en mi PC main). El otro servidor es la ejecución de este repositorio: https://github.com/MarcosNoDeFotos/yt_utils
