import VectorLayer from "ol/layer/Vector";
import VectorSource from "ol/source/Vector";
import {GeoJSON} from "ol/format";
import {Icon, Style} from "ol/style";
import iconImage from "./icons/injuryLayer.png";

//Injury Impact Category Layer

const injury_layer = new VectorLayer({
    source: new VectorSource({
        url: 'http://localhost:8080/geoserver/quaketext/ows?service=WFS&version=1.0.0' +
            '&request=GetFeature&typeName=quaketext:Injury&maxFeatures=1000&output' +
            'Format=application/json',
        format: new GeoJSON(),
    }),
    // add appropriate icon image and offset position slighty
    style: new Style({
        image: new Icon({
            src: iconImage,
            scale: 0.055,
            anchor: [-0.5,0.5],
        }),
    }),

});


export default injury_layer;

