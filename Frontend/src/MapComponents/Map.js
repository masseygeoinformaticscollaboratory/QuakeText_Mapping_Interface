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
    const mapElement = useRef(null);
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
                    let text = "";
                    let location = '<span class= "bold">Location: </span>';
                    let coordinates = '<span class= "bold">Coordinates: </span>';
                    let tweet = '<span class= "bold">Tweet: </span>';

                    for (let i = 0; i < features.length; i++) {
                        console.log(features[i]);
                        features[i].get()

                        text = text +
                            location + features[i].get("instance") + "\n" +
                            coordinates + features[i].get("geometry").flatCoordinates + "\n" +
                            tweet + features[i].get("tweetText") + "\n \n"
                    }

                    popup.setPosition(features[0].get("geometry").flatCoordinates);
                    popupContentRef.current.innerHTML = text;
                    const mapHeight = mapElement.current.getBoundingClientRect();
                    const popRect = popupRef.current.getBoundingClientRect();

                    const topMap = mapHeight.top;
                    const bottomPop = popRect.bottom;
                    const maxHeight =  bottomPop - (topMap+20);

                    popupRef.current.style.maxHeight = `${maxHeight}px`;



                }
            });
        },
        []);


    return (
        <div>
            <div ref={mapElement} className="map-container">
                <div ref={popupRef} className="popupContainer">
                    <div ref={popupContentRef} className="popup-content"/>
                </div>
            </div>

        </div>
    );
}

export default MapComponent;

/*if (features && features.length > 0) {

                console.log(features)
                popup.setPosition(event.coordinates);
                let text = "";
                for (let i = 0; i < features.length; i++) {
                    text = text + "\n" +
                        "Location: " + features[i].get("instance") + "\n" +
                        "Coordinates: " + features[i].get("geometry").flatCoordinates + "\n" +
                        "Tweet: " + features[0].get("tweetText")
                }

                popupContentRef.current.innerHTML = text;

            }*/