import './MapStyle.css';
import React, {useEffect, useRef, useState} from 'react';
import {Map, View} from 'ol';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import 'ol/ol.css';
import {TileWMS} from "ol/source";

const layer = new TileLayer({
    source: new TileWMS({
        url: "",
    })
})

const base = new TileLayer({
    source: new OSM(),
});

function BaseMap() {
    const [map, setMap] = useState();
    const mapElement = useRef();
    const mapRef = useRef();
    mapRef.current = map;

    useEffect(() => {
        const initialMap = new Map({
            target: mapElement.current,
            layers: [base,layer],
            view: new View({
                center: [-8908887.277395891, 5381918.072437216],
                zoom: 12,
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
