from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData, Fog, PerspectiveLens, DirectionalLight, AmbientLight
from direct.gui.OnscreenText import OnscreenText
import buildSettings
from modules import launcherUpdater

loadPrcFileData('', 'win-size 1024 640 \n'
                    'window-title %name%\n'
                    'show-frame-rate-meter %debug%\n'
                    'load-file-type p3assimp\n'
                    'model-path /client/content\n'
                    'gl-coordinate-system default'
                .replace('%name%', buildSettings.CLIENT_NAME)
                .replace('%debug%', str(buildSettings.DEBUG)))


class Launcher(ShowBase):
    def __init__(self):
        super().__init__()

        player_model = self.loader.loadModel("content/steve-model/steve.obj")
        scene_model = self.loader.loadModel("content/test/environment")

        player_model.setPos(0, -150, 15)
        player_model.setR(-45)
        player_model.setP(90)
        player_model.setScale(0.025, 0.025, 0.025)

        player_model.reparentTo(self.render)

        # TODO Player nickname display
        textObject = OnscreenText(text='Test scene', pos=(-1.33, 0.9), scale=0.07, style=3)

        scene_model.setPos(0, 0, 0)
        scene_model.reparentTo(self.render)

        playerVec = player_model.getPos()
        playerDist = playerVec.length()
        x = player_model.getX() + playerDist / 2.0

        self.camera.setX(x)

        self.set_background_color(149 / 255, 200 / 255, 216 / 255, 0)

        self.fog = Fog("Outside Fog")
        self.fog.setColor(149 / 255, 200 / 255, 216 / 255)
        self.fog.setExpDensity(0.0025)

        # Cool lens
        sunLens = PerspectiveLens()
        sunLens.setFilmSize(50)
        sunLens.setNearFar(25, 45)

        # Directional light
        sun = DirectionalLight("sun")
        sun.setShadowCaster(True, 512, 512)
        sun.setColor((1, 1, 1, 1))

        self.sunNp = self.render.attachNewNode(sun)
        self.sunNp.setPos(-50, -200, 60)
        self.sunNp.lookAt(0, 0, 0)

        # Ambient light
        alight = AmbientLight('alight')
        alight.setColor((0.5, 0.5, 0.5, 0.25))

        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)

        self.render.setLight(self.sunNp)
        self.render.setFog(self.fog)
        self.render.setShaderAuto()


if __name__ == "__main__":
    launcherWindow = Launcher()
    # TODO Инициализация сетки

    updater = launcherUpdater.ClientUpdater(buildSettings.SERVER_IP, buildSettings.FILE_PATH)
    updater.download_to_temp_dir()

    launcherWindow.run()
