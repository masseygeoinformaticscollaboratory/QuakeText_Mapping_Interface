import {Tile as TileLayer} from "ol/layer";
import OSM from "ol/source/OSM";

//Base OSM Layer for Map
const base = new TileLayer({
    title: 'OSM',
    type: 'base',
    visible: true,
    source: new OSM()
});

export default base