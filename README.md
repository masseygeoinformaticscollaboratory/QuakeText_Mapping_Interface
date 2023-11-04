# Quake Text Mapping Interface and Place Name Disambiguation

This Repository contains all components for the Mapping Interface and Place Name Disambiguation research.

---
Directory Components:
---
### Frontend:
Contains all the content for the visualisation of the mapping application.
This is created with a React Frame work.
#### File Structure:

```
   -- Frontend
      |-- package-lock.json
      |-- package.json
      |-- public
      |   |-- index.html
      |   |-- robots.txt
      |-- src
          |-- App.css
          |-- App.js
          |-- index.css
          |-- index.js
          |-- MapComponents
              |-- Map.js
              |-- Layers
              |   |-- AllImpacts.js
              |   |-- BaseLayer.js
              |   |-- ImpactLayers
              |   |   |-- DamageLayer.js
              |   |   |-- DeathLayer.js
              |   |   |-- FireLayer.js
              |   |   |-- FloodLayer.js
              |   |   |-- InjuryLayer.js
              |   |   |-- MissingLayer.js
              |   |   |-- OtherLayer.js
              |   |   |-- TerrorismLayer.js
              |   |   |-- TrappedLayer.js
              |   |   |-- icons
              |   |       |-- damageLayer.png
              |   |       |-- deathLayer.png
              |   |       |-- fireLayer.png
              |   |       |-- floodLayer.png
              |   |       |-- injuryLayer.png
              |   |       |-- missingLayer.png
              |   |       |-- otherLayer.png
              |   |       |-- terrorismLayer.png
              |   |       |-- trappedLayer.png
              |   |-- LayerSwitcher
              |       |-- LayerSwitcher.js
              |       |-- LayerSwitcherStyles
              |           |-- LayerSwitcherStyle.js
              |           |-- labels.css
              |           |-- labels.js
              |           |-- icons
              |               |-- damageIcon.png
              |               |-- deathIcon.png
              |               |-- fireIcon.png
              |               |-- floodIcon.png
              |               |-- injuryIcon.png
              |               |-- missingIcon.png
              |               |-- otherIcon.png
              |               |-- terrorismIcon.png
              |               |-- trappedIcon.png
              |-- MapStyle
                  |-- MapStyle.css
                  |-- PopUpStyle.js
                  |-- mapView.js
```
The structure of the frontend is consistent with that of a standard react app. 
Refer to the comments within the code for specification about what each component does.

---
### Backend:
A file containing all source code components related to the back end processes. 
The processing of data to be used within the FrontEnd Application. Data is added
to a PostGreSQL database which is connected to GeoServer.
#### File Structure:
```
|-- quake-text
    |-- CSV
    |   |-- handleDBForCSV.py
    |   |-- readCSVData.py
    |   |-- dataFiles
    |       |-- data.csv
    |-- Database
    |   |-- configDB.py
    |   |-- connectDB.py
    |   |-- database.ini
    |   |-- handleDBForJSON.py
    |   |-- readJSONData.py
    |-- dataFiles
        |-- quaketext.json
```
#### <u> CSV </u>
- Code components for using CSV files as input data.

#### <u> Database </u>
This folder contains the most recent version of the data handling - using JSON input
- `configDB.py` configures the database details on the virtual sever with the information specified in `database.ini`
- `connectDB.py` where the data scripts are run for inorder to connect to the database
- `handleDBForJSON.py` handles the queries to the PostGreSQL DB for the Data formatted in JSON
- `readJSONData.py` reads in and cleans the data ready to be plotted on the interface

---
### Place_Name_Disambiguation:
A file containing the source code and generated data for testing our Place Name Disambiguation method. 
#### File Structure:
```
|-- quake-text
    |-- .DS_Store
    |-- Annotation
    |   |-- annotationProcess.py
    |   |-- Annotation_Complete
    |   |   |-- GeorgiaFullSet.csv
    |   |   |-- SophieFullSet.csv
    |   |-- Annotation_Evaluation
    |       |-- CohenKappaCalc.py
    |-- CleanedNERData
    |   |-- CleanedNERData_Bio.csv
    |   |-- bio5000NERCleaned.csv
    |   |-- nerNPLDataCleaned.csv
    |   |-- quake_text_prepped_data.csv
    |-- Coordinates
    |   |-- coordinate_retrival.py
    |   |-- Completed_Coordinate_Data
    |       |-- LGLProcessed.csv
    |       |-- LGLProcessed512.csv
    |       |-- NPLCoordinateCompleted.csv
    |       |-- bio5000CompletedCoordinates.csv
    |-- DataPrepScripts
    |   |-- prepare_NPL_Data.py
    |   |-- prepare_biological_data.py
    |   |-- prepare_quaketext_data.py
    |   |-- processLGL.py
    |-- DocumentStats
    |   |-- documentStats.py
    |-- Embeddings
    |   |-- embeddings_retrevial.py
    |   |-- CompletedEmbeddings
    |   |   |-- Bio5000-CompleteEmbeddings.csv
    |   |   |-- LGL50-CompletedEmbeddings.csv
    |   |   |-- LGL512-CompletedEmbeddings.csv
    |   |   |-- NLP-CompletedEmbeddings.csv
    |   |   |-- QuadTred-CompletedEmbeddings.csv
    |   |-- Embedding Evaluation
    |       |-- embeddingMetricsCalc.py
    |-- MainComponents
    |   |-- config.py
    |   |-- configDB.py
    |   |-- connectDB.py
    |   |-- database.ini
    |-- MultiThreadedAttempt
    |   |-- coordinatesMultiThreaded.py
    |   |-- mutliThreadedEmbeddings.py
    |-- OriginalData
    |   |-- BioWhere.csv
    |   |-- lgl.xml
    |   |-- NLP_Data
    |       |-- 2014_California_Earthquake.csv
    |       |-- 2014_Chile_Earthquake_en.csv
    |       |-- 2014_Hurricane_Odile_Mexico_en.csv
    |       |-- 2014_Iceland_Volcano_en.csv
    |       |-- 2014_Malaysia_Airline_MH370_en.csv
    |       |-- 2014_Middle_East_Respiratory_Syndrome_en.csv
    |       |-- 2014_Typhoon_Hagupit_en.csv
    |       |-- 2015_Cyclone_Pam_en.csv
    |       |-- 2015_Nepal_Earthquake_en.csv
    |       |-- Landslides_Worldwide_en.csv
```

#### <u> Annotation: </u>
Contains the following:
- Completed annotations by our annotators Sophie and Georgia in the `Annotation_Complete` directory
- The calculation `CohensKappaCalc.py` script located in `Annotation_Evaluation\CohenKappCalc.py`
- The annotationProcess.py script for processing, cleaning and retrieval of the coordinates of the annotated data

#### <u> CleanedNERData: </u>
Contains the NER Data extracted by Flair or another NER Tool

#### <u> Coordinates: </u>
Contains the following:
- Folder containing the completed coordinate retrieval data files for each data set
- `coordinate_retrival.py` script used to retrieve the coordinates

#### <u> DataPrepScripts: </u>
Contains scripts to process each of the original data sets

#### <u> DocumentStats: </u>
Contains the script to calculate the statistics of each of the data sets

#### <u> Embeddings: </u>
Contains the following:
- A folder `Completedembeddings` containing the Completed Embedding data in a csv file for each of the data sets
- A folder `EmbeddingEvaluation` cotaining the script `embeddingsMeticCalc.py` used to determine how accurate our results from our method were 
- `embeddings_retrival.py` a script to process, retrieve and find the predicted instance using Large Language Models

#### <u> MultiThreadedAttempt: </u>
Contains two files attempting to speed up the process of coordinate retrieval and embedding retrieval using multithreading. These were however unsuccessful, but I thought it may be useful for future work

#### <u> MainComponents: </u>
Contains the main components for running the Place Name Disambiguation method
- `config.py` specifies the openAI Key and is not added to any repositories
- `configDB.py` configures the database details on the virtual sever with the information specified in `database.ini`
- `connectDB.py` where the data scripts are run for inorder to connect to the database

#### <u> Original Data: </u>
Contains the original data files we used before processing

---

## Running Components:

### To Populate Datebase:
1. Ensure PostGIS database server is connected and running 
2. Navigate to `Backend/Database/connectDB.py` and run the `connectDB.py` script. New incoming data should be place within the `Backend/dataFiles` directory

This should any new data PostGreSQL Database. This is automatically linked to GeoServer. 

### To Start Web Application:
1. Ensure TomCat is running and GeoServer can be accessed
2. Go to the `Frontend` directory and start the interface with `npm start`
---
## Useful Resources:
- See [ServerAppInstructions.pdf](Resources/ServerAppInstructions.pdf) for more detailed instructions

- See [A_Web_Application_to_Map_Disaster_Impacts_from_Text.pdf](Resources/A_Web_Application_to_Map_Disaster_Impacts_from_Text.pdf) for further details regarding the operation of the web application component

- See [Exploring Toponym Disambiguation with Large Language Models: Insights and Challenges](Resources/ToponymDisambiguationReport) for further details on the Place Name Disambiguation method and results