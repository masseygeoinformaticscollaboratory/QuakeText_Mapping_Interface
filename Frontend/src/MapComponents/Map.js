import React, {useEffect, useRef, useState} from "react";
import Map from "ol/Map";
import base from "./Layers/BaseLayer"
import vectorLayer from "./Layers/VectorLayer";
import view from "./MapStyle/mapView";
import './MapStyle/MapStyle.css';
import 'ol/ol.css';
import popup from "./Functionality/popupInfo";

function BaseMap() {
    const [map, setMap] = useState();
    const mapElement = useRef();
    const mapRef = useRef();
    mapRef.current = map;

    useEffect(() => {
        const initialMap = new Map({
            target: mapElement.current,
            layers: [base, vectorLayer],
            view: view
        });
        popup(initialMap);
        setMap(initialMap)
    }, []);
    return (
        <div ref={mapElement} className="map-container"/>
    );
}

export default BaseMap;