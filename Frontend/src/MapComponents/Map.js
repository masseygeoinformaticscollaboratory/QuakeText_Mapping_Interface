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


        map.on("click", (event) => {

            let features = map.getFeaturesAtPixel(event.pixel);


            if (features && features.length > 0) {

                let coordinates, location, impact, count_place = 0;
                for (let i = 0; i < features.length; i++) {

                    if (features[i].get("label") === "place name" && count_place === 0) {
                        location = features[i].get("instance")
                        coordinates = features[i].get("geometry").flatCoordinates
                        count_place++;
                    }
                    /*
                    if (features[i].get("label") === "type of impact") {
                        impact = features[i].get("instance")
                    }
                     */
                }
                console.log(features)
                popup.setPosition(coordinates);
                popupContentRef.current.innerHTML =
                    "Location: " + location + "\n" +
                    "Coordinates: " + coordinates + "\n" +
                   // "Impact: " + impact + "\n" +
                    "Tweet: " + features[0].get("tweetText")
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
