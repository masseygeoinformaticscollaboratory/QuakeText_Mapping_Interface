import VectorLayer from "ol/layer/Vector";
import VectorSource from "ol/source/Vector";
import {GeoJSON} from "ol/format";
import {Icon, Style} from "ol/style";
import iconImage from "./icons/missingLayer.png";

const missing_layer = new VectorLayer({
    source: new VectorSource({
        url: 'http://localhost:8080/geoserver/quaketext/ows?service=WFS&version=1.0.0' +
            '&request=GetFeature&typeName=quaketext:Missing&maxFeatures=1000&output' +
            'Format=application/json',
        format: new GeoJSON(),
    }),
    style: new Style({
        image: new Icon({
            src: iconImage,
            scale: 0.06,
            anchor: [0.6, 0.9],
        }),
    }),
});
export default missing_layer;

