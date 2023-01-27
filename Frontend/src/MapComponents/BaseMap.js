import './MapStyle.css';
import React, {useEffect, useRef, useState} from 'react';
import 'ol/ol.css';
//import TileWMS from 'ol/source/TileWMS';
import Map from 'ol/Map';
import View from 'ol/View';
import 'ol/ol.css';
import OSM from 'ol/source/OSM';
import {Tile as TileLayer} from 'ol/layer';
import {ImageWMS} from "ol/source";
import {Group} from "ol/layer";
import {Image} from "ol/layer"

const base = new Group({
    'title': 'Base maps',
    layers: [
        new TileLayer({
            title: 'OSM',
            type: 'base',
            visible: true,
            source: new OSM()
        })
    ]
});


const overlays = new Group({
    'title': 'Overlays',
    layers: [
        new Image({
            title: 'aus1',
            visible: true,
            // extent: [-180, -90, -180, 90],
            source: new ImageWMS({
                url: 'http://localhost:8080/geoserver/wms',
                params: {'LAYERS': 'aussie:aus1'},
                ratio: 1,
                serverType: 'geoserver'
            })
        }),
        new Image({
            title: 'aus2',
            visible: true,
            // extent: [-180, -90, -180, 90],
            source: new ImageWMS({
                url: 'http://localhost:8080/geoserver/wms',
                params: {'LAYERS': 'aussie:aus2'},
                ratio: 1,
                serverType: 'geoserver'
            })
        }),
        new Image({
            title: 'aus3',
            visible: true,
            // extent: [-180, -90, -180, 90],
            source: new ImageWMS({
                url: 'http://localhost:8080/geoserver/wms',
                params: {'LAYERS': 'aussie:aus3'},
                ratio: 1,
                serverType: 'geoserver'
            })
        })

    ]
});


function BaseMap() {
    const [map, setMap] = useState();
    const mapElement = useRef();
    const mapRef = useRef();
    mapRef.current = map;

    useEffect(() => {
        const initialMap = new Map({
            target: mapElement.current,
            layers: [base, overlays],
            view: new View({
                projection: 'EPSG:4326',
                center: [78.0, 23.0],
                zoom: 5,
                minZoom: 2,
                maxZoom: 18,
            }),
        });
        setMap(initialMap)
    }, []);
    return (
        <div ref={mapElement} className="map-container"/>
    );
}

export default BaseMap;