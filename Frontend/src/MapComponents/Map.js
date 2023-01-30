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
    const popupContentRef = useRef(null);
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
        const allDaFeatures = function(pixel) {
            let features = [];
            map.forEachFeatureAtPixel(pixel, function(feature, layer){
                features.push(feature);
                console.log(feature)
            })
        }

        map.on("click", (event) => {

            allDaFeatures(event.pixel);

            let features = map.getFeaturesAtPixel(event.pixel);


            if (features && features.length > 0) {
               // if (features[0].get("label") === "place name") {
                    popup.setPosition(features[0].get("geometry").flatCoordinates);
                    popupContentRef.current.innerHTML =
                        "Location: " + features[0].get("instance") + "\n" +
                        "Coordinates: " + features[0].get("geometry").flatCoordinates + "\n" +
                        "Impact: "

               // }
            }
        });


    }, []);


    return (
        <div>
            <div ref={mapElement} className="map-container"/>
            <div ref={popupRef} className="popupContainer">
                <div ref={popupContentRef} className="popup-content"/>
            </div>

        </div>
    );
}

export default MapComponent;
