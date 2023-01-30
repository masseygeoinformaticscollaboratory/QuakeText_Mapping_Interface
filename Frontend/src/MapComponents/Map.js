import React, {useEffect, useRef, useState} from "react";
import Map from "ol/Map";
import base from "./Layers/BaseLayer"
import vectorLayer from "./Layers/VectorLayer";
import view from "./MapStyle/mapView";
import './MapStyle/MapStyle.css';
import 'ol/ol.css';
import {Overlay} from "ol";


function MapComponent() {
    const [map, setMap] = useState();
    const mapElement = useRef();
    const mapRef = useRef();
    const popupRef = useRef(null);
    mapRef.current = map;

    useEffect(() => {
        const map = new Map({
            target: mapElement.current,
            layers: [base, vectorLayer],
            view: view
        });
        setMap(map)

        const popup = new Overlay({
            element: popupRef.current,
            autoPan: true,
            autoPanAnimation: {
                duration: 250
            }
        });

        map.addOverlay(popup);

        map.on('click', event => {
            const { coordinate } = event;
            popup.setPosition(coordinate);
            popupRef.current.innerHTML = coordinate;
        });

    }, []);


    return (
        <div>
            <div ref={mapElement} className="map-container"/>
            <div
                ref={popupRef}
                className= "coord-popup"
                style={{ position: 'absolute', bottom: '20px', left: '20px' }} >
            </div>
        </div>
    );
}
export default MapComponent;
