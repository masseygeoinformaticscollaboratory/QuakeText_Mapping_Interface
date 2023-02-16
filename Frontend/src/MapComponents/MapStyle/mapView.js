import View from "ol/View";
//View for Map Component
export default new View({
    projection: 'EPSG:4326',
    center: [0, 0],
    zoom: 3,
    minZoom: 2,
    maxZoom: 18,
});