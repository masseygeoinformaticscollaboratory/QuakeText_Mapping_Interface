import './MapStyle.css';
import React, {useEffect, useRef, useState} from 'react';
import {Map, View} from 'ol';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import 'ol/ol.css';

function BaseMap() {
    const [map, setMap] = useState();
    const mapElement = useRef();
    const mapRef = useRef();
    mapRef.current = map;

    useEffect(() => {
        const initialMap = new Map({
            target: mapElement.current,
            layers: [
                new TileLayer({
                    source: new OSM(),
                }),
            ],
            view: new View({
                center: [0, 0],
                zoom: 0,
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
