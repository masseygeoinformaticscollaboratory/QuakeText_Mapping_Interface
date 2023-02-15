import VectorLayer from "ol/layer/Vector";
import VectorSource from "ol/source/Vector";
import {GeoJSON} from "ol/format";
import {Icon, Style} from "ol/style";
import iconImage from "./icons/injuryLayer.png";

const injury_layer = new VectorLayer({
    source: new VectorSource({
        url: 'http://localhost:8080/geoserver/quaketext/ows?service=WFS&version=1.0.0' +
            '&request=GetFeature&typeName=quaketext:Injury&maxFeatures=1000&output' +
            'Format=application/json',
        format: new GeoJSON(),
    }),
    style: new Style({
        image: new Icon({
            src: iconImage,
            scale: 0.05,
            anchor: [0.5, 1.1],
        }),
    }),

});


export default injury_layer;

