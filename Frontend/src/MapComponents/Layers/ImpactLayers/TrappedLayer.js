import VectorLayer from "ol/layer/Vector";
import VectorSource from "ol/source/Vector";
import {GeoJSON} from "ol/format";
import {Icon, Style} from "ol/style";
import iconImage from "./icons/trappedLayer.png";


const trapped_layer = new VectorLayer({
        source: new VectorSource({
            url: 'http://localhost:8080/geoserver/quaketext/ows?service=WFS&version=1.0.0' +
                '&request=GetFeature&typeName=quaketext:Trapped&maxFeatures=1000&output' +
                'Format=application/json',
            format: new GeoJSON(),
        }),

        style: new Style({
            image: new Icon({
                src: iconImage,
                scale: 0.06,
                anchor: [0.4, 1.1],
            }),
        }),
    })
;


export default trapped_layer;
