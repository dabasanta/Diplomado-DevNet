import mapboxgl from "mapbox-gl";

const addMainSourceLayer = (map: any, coordinates: any) => {
  // Add a data source containing GeoJSON data.
  map.addSource("maine", {
    type: "geojson",
    data: {
      type: "Feature",
      //geometry,
      geometry: {
        type: "Polygon",
        coordinates: coordinates.value,
      },
    },
  });

  // Add a new layer to visualize the polygon.
  map.addLayer({
    id: "maine",
    type: "fill",
    source: "maine", // reference the data source
    layout: {},
    paint: {
      "fill-color": "#0080ff", // blue color fill
      "fill-opacity": 0,
    },
  });
  // Add a black outline around the polygon.
  map.addLayer({
    id: "outline",
    type: "line",
    source: "maine",
    layout: {},
    paint: {
      "line-color": "#000",
      "line-width": 2,
    },
  });
};

const addMainControls = (map: any) => {
  // Add zoom and rotation controls to the map.
  map.addControl(
    new mapboxgl.NavigationControl({
      showCompass: false,
    }),
    "bottom-right"
  );

  map.on("mouseenter", "states-layer", () => {
    map.getCanvas().style.cursor = "pointer";
  });
};

const addBarriosLayer = (map: any, barrios: any) => {
  const newBarrios = barrios.value.filter((x: any) => x.limite != null);
  newBarrios.map((barrio: any) => {
    map.addSource(barrio.id, {
      type: "geojson",
      data: {
        type: "Feature",
        //geometry,
        geometry: {
          type: "Polygon",
          coordinates: barrio.limite.coordinates[0],
        },
      },
    });

    map.addLayer({
      id: barrio.id,
      type: "fill",
      source: barrio.id, // reference the data source
      layout: {},
      paint: {
        "fill-color": getRandomColor(), // blue color fill
        "fill-opacity": 0.5,
      },
    });

    /* Map on click */
    map.on("click", [barrio.id], (e: any) => {
      new mapboxgl.Popup({ className: "map-popup" })
        .setLngLat(e.lngLat)
        .setHTML(`<div>${barrio.name}</div>`)
        .addTo(map);
    });
  });
};

const removeBarriosLayer = (map: any, barrios: any) => {
  const newBarrios = barrios.value.filter((x: any) => x.limite != null);
  newBarrios.map((barrio: any) => {
    map.removeLayer(barrio.id);
    map.removeSource(barrio.id);
  });
};

export {
  addMainSourceLayer,
  addMainControls,
  addBarriosLayer,
  removeBarriosLayer,
};
