import {Fill, Stroke, Style} from "ol/style";

const selectStyle = new Style({
    fill: new Fill({
        color: '#eeeeee',
    }),
    stroke: new Stroke({
        color: 'rgba(255, 255, 255, 0.7)',
        width: 2,
    }),
});

function addHover(map) {
    let selected = null;
    map.on('pointermove', function (e) {
        if (selected !== null) {
            selected.setStyle(undefined);
            selected = null;
        }

        map.forEachFeatureAtPixel(e.pixel, function (f) {
            selected = f;
            selectStyle.getFill().setColor(f.get('COLOR') || '#eeeeee');
            f.setStyle(selectStyle);
            return true;
        });

    });
}

export default addHover;