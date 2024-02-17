from pathlib import Path
from pyPhases import PluginAdapter
from pyPhasesRecordloader import RecordLoader


class Plugin(PluginAdapter):
    def initPlugin(self):
        RecordLoader.registerRecordLoader("RecordLoaderMrOS", "pyPhasesRecordloaderMrOS.recordLoaders")
        RecordLoader.registerRecordLoader("MrOSAnnotationLoader", "pyPhasesRecordloaderMrOS.recordLoaders")
        mrosPath = Path(self.getConfig("mros-path"))

        self.project.setConfig("loader.mros.filePath", mrosPath.as_posix())
        self.project.setConfig("loader.mros.dataset.downloader.basePath", mrosPath.as_posix())
        self.project.setConfig(
            "loader.mros.dataset.downloader.basePathExtensionwise",
            [
                (mrosPath / "polysomnography/edfs/visit1/").as_posix(),
                (mrosPath / "polysomnography/annotations-events-nsrr/visit1/").as_posix(),
                (mrosPath / "polysomnography/edfs/visit2/").as_posix(),
                (mrosPath / "polysomnography/annotations-events-nsrr/visit2/").as_posix(),
            ],
        )
