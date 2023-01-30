function getInfo(map) {

    map.on("click", (event) => {

        let features = map.getFeaturesAtPixel(event.pixel);
        if (features && features.length > 0) {
            if (features[0].get("label") === "place name") {
                console.log(features[0].get("instance"));
                console.log(features[0].get("geometry").flatCoordinates);
            }
        }
    });
}

export default getInfo;