import VectorLayer from "ol/layer/Vector";
import VectorSource from "ol/source/Vector";
import {GeoJSON} from "ol/format";
import {Fill, Icon, Stroke, Style} from "ol/style";




const vectorLayer = new VectorLayer({
    source: new VectorSource({
        url: 'http://localhost:8080/geoserver/quaketext/ows?service=' +
            'WFS&version=1.0.0&request=GetFeature&typeName=quaketext:quake_text' +
            '&maxFeatures=50&outputFormat=application/json',
        format: new GeoJSON(),
    }),
    style: new Style({
        fill: new Fill({
            color: 'rgba(255, 0, 0, 0.2)'
        }),
        stroke: new Stroke({
            color: '#343434',
            width: 2
        }),
        image: new Icon( {
            anchor: [0.5, 46],
            anchorXUnits: 'fraction',
            anchorYUnits: 'pixels',
            opacity: 0.95,
            src: 'Resources/green-marker.png'
        })
    })

});



export default vectorLayer;

/*When getting a vector layer in GeoJson from Geoserver in openlayers, how can I customise all the icons to use a png store locally ?*/