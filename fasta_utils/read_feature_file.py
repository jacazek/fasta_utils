def read_feature_file(feature_file):
    with (open(feature_file) as file):
        line = file.readline().strip()
        while line != "":
            yield line
            line = file.readline().strip()
        file.close()