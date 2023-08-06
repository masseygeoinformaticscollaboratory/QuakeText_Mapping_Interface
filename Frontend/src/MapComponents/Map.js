import React, {useEffect, useRef, useState} from "react";
import Map from "ol/Map";
import base from "./Layers/BaseLayer"
import view from "./MapStyle/mapView";
import './MapStyle/MapStyle.css';
import 'ol/ol.css';
import {setText, setPopUpHeight, createPopUpOverlay} from "./MapStyle/PopUpStyle";
import impactLayers from "./Layers/AllImpacts"
import LayerSwitcher from "./Layers/LayerSwitcher/LayerSwitcher";
import {setSwitcherHeight} from "./Layers/LayerSwitcher/LayerSwitcherStyles/LayerSwitcherStyle";
import {impactLabels} from "./Layers/LayerSwitcher/LayerSwitcherStyles/labels";

//This component handles and creates the main map component,
//and adds layers such as pop-ups and the layer switcher
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

            //Sets the layer switcher height based on how many number of impact categories
            setSwitcherHeight(impactLabels.length);

            const popup = createPopUpOverlay(popupRef);
            map.addOverlay(popup);

            map.on("click", (event) => {
                // If the user clicks on an icon, a pop-up will be displayed
                let features = map.getFeaturesAtPixel(event.pixel);

                //Must be a point where an icon is located
                if (features && features.length > 0) {
                    popupRef.current.style.display = "block"
                    let target = features[0].getId();
                    let impactString = target.substring(0, target.indexOf("."));

                    let {title, location, coordinates, tweet, impact} = setText(impactString)
                    let text = title + '\n \n';
                    for (let i = 0; i < features.length; i++) {
                        //features[i].get("placename") for JSON
                        //features[i].get("instance") for CSV
                        let target = features[i].getId()
                        if (impactString === target.substring(0, target.indexOf("."))) {
                            text = text +
                                impact + features[i].get("impact_type") + "\n" +
                                location + features[i].get("place_name") + "\n" +
                                coordinates + features[i].get("geometry").flatCoordinates + "\n" +
                                tweet + features[i].get("tweet_text") + "\n" +
                                "\n \n"
                        }
                    }
                    //Generates popup and sets text and location
                    popup.setPosition(features[0].get("geometry").flatCoordinates);
                    popupContentRef.current.innerHTML = text;
                    setPopUpHeight(mapElement, popupRef);

                } else {
                    //When the user clicks away from the pop-up, it will close
                    popupRef.current.style.display = "none"
                }
            });
        },
        []);

    function closePopup() {
        // Closes pop-up when exit button is clicked
        popupRef.current.style.display = "none";
    }

    return (
        <main style={{display: "flex"}}>
            <div ref={mapElement} className="map">
                <div ref={popupRef} className="popupContainer">
                    <button className="popup-closer" onClick={closePopup}></button>
                    <div ref={popupContentRef} className="popup-content"/>
                </div>
                <LayerSwitcher className="layer-switcher" impactLayers={impactLayers} popup={popupRef}/>
            </div>
        </main>
    );
}

export default MapComponent;

