import React, {useEffect, useRef, useState} from "react";
import Map from "ol/Map";
import base from "./Layers/BaseLayer"
import view from "./MapStyle/mapView";
import './MapStyle/MapStyle.css';
import 'ol/ol.css';
import {Overlay} from "ol";
import {setText, formatPopup} from "./MapStyle/PopUpStyle";

import impactLayers from "./Layers/AllImpacts"


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
                layers: [base, impactLayers],
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
                    popupRef.current.style.display = "block"

                    let text = "";
                    let {location, coordinates, tweet, impact} = setText()

                    for (let i = 0; i < features.length; i++) {
                        //features[i].get("placename") for JSON
                        //features[i].get("instance") for CSV
                        text = text +
                            location + features[i].get("placename") + "\n" +
                            coordinates + features[i].get("geometry").flatCoordinates + "\n" +
                            tweet + features[i].get("tweet_text") + "\n" +
                            impact + features[i].get("impact_type") +
                            "\n \n"
                    }

                    popup.setPosition(features[0].get("geometry").flatCoordinates);
                    popupContentRef.current.innerHTML = text;
                    formatPopup(mapElement, popupRef);


                }


            });
        },
        []);


    function closePopup() {
        popupRef.current.style.display = "none";
    }

    return (
        <main style={{display: "flex"}}>
            <div ref={mapElement} className="map">
                <div ref={popupRef} className="popupContainer">
                    <button className="popup-closer" onClick={closePopup}></button>
                    <div ref={popupContentRef} className="popup-content"/>
                </div>

                    <fieldset className="layer-switcher">
                        <legend>Select Layers:</legend>
                        <div>
                            <input type="radio" id="huey" name="drone" value="huey" checked/>
                                <label htmlFor="huey">Huey</label>
                        </div>

                        <div>
                            <input type="radio" id="dewey" name="drone" value="dewey"/>
                                <label htmlFor="dewey">Dewey</label>
                        </div>

                        <div>
                            <input type="radio" id="louie" name="drone" value="louie"/>
                                <label htmlFor="louie">Louie</label>
                        </div>
                    </fieldset>


            </div>


        </main>
);
}

export default MapComponent;

