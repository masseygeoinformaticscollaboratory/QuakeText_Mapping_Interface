import './MapStyle.css';
import React, {useEffect, useRef, useState} from 'react';
import {Map, View} from 'ol';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import 'ol/ol.css';
import VectorLayer from "ol/layer/Vector";
import VectorSource from "ol/source/Vector";

const base = new TileLayer({
    source: new OSM(),
});


const layer = new VectorLayer({
    source: new VectorSource(),
    url: 'https://localhost:8080/geoserver/wms',
    params: {'LAYERS': 'ne:countries', 'TILED': true},
    serverType: 'geoserver',
    crossOrigin: 'anonymous'
});

function BaseMap() {
    const [map, setMap] = useState();
    const mapElement = useRef();
    const mapRef = useRef();
    mapRef.current = map;

    useEffect(() => {
        const initialMap = new Map({
            target: mapElement.current,
            layers: [base, layer],
            view: new View({
                center: [0, 0],
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
