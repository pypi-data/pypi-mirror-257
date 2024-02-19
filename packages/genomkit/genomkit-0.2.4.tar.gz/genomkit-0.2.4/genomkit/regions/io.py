import os


###########################################################################
# IO functions
###########################################################################
def load_BED(filename: str):
    from genomkit import GRegion, GRegions
    if not os.path.exists(filename):
        raise FileNotFoundError(f"The file '{filename}' does not exist.")
    else:
        res = GRegions()
        with open(filename, 'r') as file:
            for line in file:
                if not line.startswith("#"):
                    infos = line.strip().split()
                    res.add(GRegion(sequence=infos[0],
                                    start=int(infos[1]), end=int(infos[2]),
                                    orientation=infos[5],
                                    name=infos[3], score=infos[4]))
        return res
