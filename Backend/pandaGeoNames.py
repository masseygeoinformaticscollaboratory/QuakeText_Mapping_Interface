import pandas as pd
import geocoder
import time

start = time.time()
df = pd.read_csv('data/1000RowData.csv')
print("Time Taken Reading File")
print("% s seconds" % (time.time() - start))

df = df[['label', 'instance', 'tweetText', 'tweetId']].copy()
place_name_df = df[df.label == 'place name']
newdf = df[df['label'].str.contains("place name")==False]

latlist = []
lnglist = []
place_name_df = place_name_df.reset_index(drop=True)

for index, row in place_name_df.iterrows():
    g = geocoder.geonames(row['instance'], key='QuakeText')
    latlist.append(g.lat)
    lnglist.append(g.lng)

place_name_df['latitude'] = latlist
place_name_df['longitude'] = lnglist

result = pd.concat([place_name_df, newdf])

result.sort_values(by=['tweetId'])

result = result.reset_index(drop=True)

writingtime = time.time()

result.to_csv('data/newData.csv')


print("Time taken writing to file")
print("% s seconds" % (time.time() - writingtime))

print("TotalTime Consumed")
print("% s seconds" % (time.time() - start))

