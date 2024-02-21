import pathlib
import tempfile


class SketchInfo:
    # a class that holds useful sketch information
    def __init__(self, sketchPath: pathlib.Path):
        self.path = sketchPath
        self.folder = self.path.parent
        self.barename = self.path.stem
        self.namejs = self.path.with_suffix(".js").name

        self._targetFolder = tempfile.TemporaryDirectory(prefix=f".{self.barename}_", dir=self.folder)
        self.targetFolder = pathlib.Path(self._targetFolder.name)

        self.outputFolder = self.targetFolder / "__target__"
        self.indexFile = self.targetFolder / "index.html"
