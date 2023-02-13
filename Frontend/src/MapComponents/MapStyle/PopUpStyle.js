export function formatPopup(mapElement, popupRef) {
    const mapHeight = mapElement.current.getBoundingClientRect();
    const popRect = popupRef.current.getBoundingClientRect();

    const topMap = mapHeight.top;
    const bottomPop = popRect.bottom;
    const maxHeight = bottomPop - (topMap + 20);

    popupRef.current.style.maxHeight = `${maxHeight}px`;
}

export function setText(){
    let location = '<span class= "bold">Location: </span>';
    let coordinates = '<span class= "bold">Coordinates: </span>';
    let tweet = '<span class= "bold">Tweet: </span>';
    let impact ='<span class= "bold">Impact Type: </span>';


    return {location, coordinates, tweet,impact}
}
