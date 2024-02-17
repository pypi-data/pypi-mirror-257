from math import ceil

from pyPhasesRecordloader.downloader.Downloader import Downloader
from pyPhasesRecordloader.recordLoaders.CSVMetaLoader import CSVMetaLoader
from pyPhasesRecordloaderSHHS.recordLoaders.RecordLoaderSHHS import RecordLoaderSHHS


class RecordLoaderMrOS(RecordLoaderSHHS):
    def isVisit1(self, recordName):
        return recordName[:11] == "mros-visit1"

    def getFilePathSignal(self, recordName):
        dl = self.getDownloader()
        pathEdfV1, _, pathEdfV2, _ = dl.basePathExtensionwise

        path = pathEdfV1 if self.isVisit1(recordName) else pathEdfV2

        return path + "/" + recordName + ".edf"

    def getFilePathAnnotation(self, recordId):
        isVisit1 = recordId[:11] == "mros-visit1"
        dl = self.getDownloader()
        _, pathXmlV1, _, pathXmlV2 = dl.basePathExtensionwise

        path = pathXmlV1 if isVisit1 else pathXmlV2

        return path + "/" + recordId + "-nsrr.xml"

    def groupBy(self, name: str, recordIds, metadata=None):
        groupedRecords = {}
        if name == "patient":
            for recordId in recordIds:
                id = recordId[12:]

                if id not in groupedRecords:
                    groupedRecords[id] = []

                groupedRecords[id].append(recordId)
        return groupedRecords

    def getMetaData(self, recordName):
        metaData = super().getMetaData(recordName, loadMetadataFromCSV=False)
        metaData["recordId"] = recordName
        ageKey = "vsage1" if self.isVisit1(recordName) else "vs2age1"
        bpdiaKey = "bpbpdiam" if self.isVisit1(recordName) else "vs2age1"
        bpsysKey = "bpbpsysm" if self.isVisit1(recordName) else "bpbpsysm"
        relevantRows = {
            "gender": lambda row: "male" if row["gender"] == 2 else "female",
            "age": ageKey,
            "bmi": "hwbmi",
            "tst": "poslprdp",
            # therapy / diagnostics
            "sLatency": "posllatp",
            "rLatency": "poremlat",  # REM Sleep Latency: the interval between the first sleep epoch and REM sleep including wake from type II polysomnography
            "waso": "powaso",
            "sEfficiency": "poslpeff",  # REM Sleep Latency: the interval between the first sleep epoch and REM sleep including wake from type II polysomnography
            "indexArousal": lambda r: r["poai_all"] if r["poai_all"] != "M" else None,
            # % N1, N2, N3, R
            # PLMSI
            "indexPlms": "poavgplm",
            "indexPlmsArousal": "poavplma",
            # AHI
            "ahi": lambda r: r["poahi4a"] if r["poahi4a"] != "M" else None,
            # Diagnosis
            "bp_diastolic": bpdiaKey,
            "bp_systolic": bpsysKey,
            "race": "race",
        }
        visit = 1 if self.isVisit1(recordName) else 2
        csvLoader = CSVMetaLoader(
            f"{self.filePath}/datasets/mros-visit{visit}-dataset-0.6.0.csv", idColumn="nsrrid", relevantRows=relevantRows
        )

        csvMetaData = csvLoader.getMetaData(recordName[12:].upper())
        metaData.update(csvMetaData)

        if "tst" in metaData and metaData["indexArousal"] is not None and metaData["tst"] is not None:
            metaData["countArousal"] = ceil(float(metaData["indexArousal"]) * float(metaData["tst"]) / 60)

        return metaData
