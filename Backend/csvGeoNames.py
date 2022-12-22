import csv
import geocoder
import time

start = time.time()
with open('data/10RowData.csv', 'r') as file:
    reader = csv.reader(file)
    print("Time Taken Reading File")
    print("% s seconds" % (time.time() - start))
    writingtime = time.time()
    with open('data/newdata.csv', 'w') as newfile:
        writer = csv.writer(newfile)
        header = ['place name', 'tweetText', 'lat', 'lon']
        writer.writerow(header)
        for row in reader:
            if row[3] == 'place name':
                g = geocoder.geonames(row[4], key='QuakeText')
                newrow = [row[4], row[7], g.lat, g.lng]
                writer.writerow(newrow)

print("Time taken writing to file")
print("% s seconds" % (time.time() - writingtime))

print("TotalTime Consumed")
print("% s seconds" % (time.time() - start))

