import './MapStyle.css';
import React, {useEffect, useRef, useState} from 'react';
import {Map, View} from 'ol';
import TileLayer from 'ol/layer/Tile';
import ImageLayer from 'ol/layer/Image'
import ImageSource from "ol/source/ImageWMS";
import OSM from 'ol/source/OSM';
import 'ol/ol.css';

const base = new TileLayer({
    source: new OSM(),
});

const layer = new ImageLayer({
    source: new ImageSource({
        url: 'http://localhost:8080/geoserver/quaketext/wms',
        params: {'LAYERS':'quaketext'},
        serverType: 'geoserver'
    })
})

function BaseMap() {
    const [map, setMap] = useState();
    const mapElement = useRef();
    const mapRef = useRef();
    mapRef.current = map;

    useEffect(() => {
        const initialMap = new Map({
            target: mapElement.current,
            layers: [base],
            view: new View({
                center: [0, 0],
                zoom: 5,
                minZoom: 2,
                maxZoom: 18,
            }),
        });
        setMap(initialMap)
        initialMap.addLayer(layer)
    }, []);
    return (
        <div ref={mapElement} className="map-container"/>
    );
}

export default BaseMap;
