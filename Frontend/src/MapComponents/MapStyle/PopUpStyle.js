import {Overlay} from "ol";
import {getIcon} from "../Layers/LayerSwitcher/LayerSwitcherStyles/LayerSwitcherStyle";

//Sets the Pop up Max Height so it doesn't extend the map
export function setPopUpHeight(mapElement, popupRef) {
    const mapHeight = mapElement.current.getBoundingClientRect();
    const popRect = popupRef.current.getBoundingClientRect();

    const topMap = mapHeight.top;
    const bottomPop = popRect.bottom;
    const maxHeight = bottomPop - (topMap + 30);

    popupRef.current.style.maxHeight = `${maxHeight}px`;
}

//Sets the text for the pop up and formats it
export function setText(layer) {
    let title = `<h4 id = "title" >${layer}</h4><img id = "title-image" src="${getIcon(layer)}" alt="">`;
    let location = '<span class= "bold">Location: </span>';
    let coordinates = '<span class= "bold">Coordinates: </span>';
    let tweet = '<span class= "bold">Tweet: </span>';
    let impact = '<span class= "bold">Impact Type: </span>';


    return {title, location, coordinates, tweet, impact}
}

//Creates the pop-up overlay for the map
export function createPopUpOverlay(popupRef) {
    return new Overlay({
        element: popupRef.current,
        autoPan: true,
        autoPanAnimation: {
            duration: 250
        }
    });
}