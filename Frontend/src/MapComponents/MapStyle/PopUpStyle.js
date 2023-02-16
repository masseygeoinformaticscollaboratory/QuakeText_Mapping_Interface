import {Overlay} from "ol";
import {getIcon} from "../Layers/LayerSwitcher/LayerSwitcherStyles/LayerSwitcherStyle";
export function formatPopup(mapElement, popupRef) {
    const mapHeight = mapElement.current.getBoundingClientRect();
    const popRect = popupRef.current.getBoundingClientRect();

    const topMap = mapHeight.top;
    const bottomPop = popRect.bottom;
    const maxHeight = bottomPop - (topMap + 20);

    popupRef.current.style.maxHeight = `${maxHeight}px`;
}

export function setText(layer) {
    console.log(layer)
    let title =  `<h4 id = "title" >${layer}</h4><img id = "title-image" src="${getIcon(layer)}" alt="">`;
    let location = '<span class= "bold">Location: </span>';
    let coordinates = '<span class= "bold">Coordinates: </span>';
    let tweet = '<span class= "bold">Tweet: </span>';
    let impact = '<span class= "bold">Impact Type: </span>';


    return {title, location, coordinates, tweet, impact}
}

export function createPopUpOverlay(popupRef) {
    return new Overlay({
        element: popupRef.current,
        autoPan: true,
        autoPanAnimation: {
            duration: 250
        }
    });
}