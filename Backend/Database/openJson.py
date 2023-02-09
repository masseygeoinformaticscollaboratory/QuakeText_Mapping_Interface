import pandas as pd

data = pd.read_json('../jsonData/singleJsonData.json', lines=True)
ner = data.get("ner")
sentences = data.get("sentences")
for row in ner:
    placeNames=[]
    mod=[]
    item=[]
    impact=[]
    sev = []
    for column in row:
        for item in column:

            if item[0] == item[1]:
                start =item[0]
                match item[2]:
                    case "place name":
                        placeNames.append(sentences.get(0)[0][start])
                    case "location modifier":
                        mod.append(sentences.get(0)[0][start])
                    case "severity or quantity":
                        sev.append(sentences.get(0)[0][start])
                    case "item affected":
                        item.append(sentences.get(0)[0][start])
                    case "type of impact":
                        impact.append(sentences.get(0)[0][start])
                    case "severity or quantity":
                        sev.append(sentences.get(0)[0][start])


    """
    for i in ner[index]:
        
    print(sentences[rowNer])
    for columns in rowNer:
        for items in columns:
            start = items[0]
            end = items[1]
            taggedType = items[2]



"""