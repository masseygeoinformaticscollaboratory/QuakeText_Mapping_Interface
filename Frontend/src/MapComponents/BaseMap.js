import './MapStyle.css';
import React, {useEffect, useRef, useState} from 'react';
import 'ol/ol.css';
import TileWMS from 'ol/source/TileWMS';
import Map from 'ol/Map';
import View from 'ol/View';
import 'ol/ol.css';
import OSM from 'ol/source/OSM';
import {Tile as TileLayer} from 'ol/layer';


const base = new TileLayer({
    source: new OSM(),
});


const layer = new TileLayer({
    extent: [-13884991, 2870341, -7455066, 6338219],
    source: new TileWMS({
        url: 'http://localhost:8080/geoserver/wms?service=WMS',
        params: {'LAYERS': 'topp:states', 'TILED': true},
        serverType: 'geoserver',
        //crossOrigin: 'anonymous',
        // Countries have transparency, so do not fade tiles:
        transition: 0,
    }),
})


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