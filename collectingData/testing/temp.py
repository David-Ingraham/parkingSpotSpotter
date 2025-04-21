with open('./cmdLineAppd/listOffileNamesGoodCamera.txt') as file:
    for f in files:
        file.write(f"{f}\n")