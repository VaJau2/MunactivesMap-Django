<template>
    <div id="map" class="map sideCol" />
</template>

<script>
//компонент карты
//загружает карту в приложение
//добавляет кнопки controls на карту

import { set_global_map, global_map } from '../api/global';
import {Active} from '../api/actives'

import 'ol/ol.css';
import Map from 'ol/Map';
import View from 'ol/View';
import {OSM, XYZ, Vector as VectorSource} from 'ol/source';
import {Tile as TileLayer, Vector as VectorLayer} from 'ol/layer';
import {Fill, Stroke, Style} from 'ol/style';
import GeoJSON from 'ol/format/GeoJSON';
import {Select} from 'ol/interaction';

export default {
    name: 'MyMap',
    props: {
        styles: Object,
    },
    data() {
        return {
            zoom: 2,
            center: [0, 0],

            sources: {
                'company': new VectorSource(),
                'foundation': new VectorSource(),
                'housingstock': new VectorSource(),
                'munitipalland': new VectorSource(),
            },
            layers: {
                'company': new VectorLayer(),
                'foundation': new VectorLayer(),
                'housingstock': new VectorLayer(),
                'munitipalland': new VectorLayer(),
            },

            selection: null,
            featsSelected: [],
            programmaryLayer: null, //если выделяем selection объект программно, он не может вытащить слой
            selectAdd: false,

            lightLayer: null,
            darkLayer: null
        }
    },
    mounted() {
        var myMap = this.initMap();
        this.initLayers(myMap);
        this.initControls(myMap);
    },
    methods: {
        initMap() {
            var openStreetMapLayer = new TileLayer({
                source: new OSM({
                    attributions: ['All maps © <a href="http://www.openstreetmap.org/">OpenStreetMap</a>'],
                    opaque: false,
                    url: 'https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png'
                })
            });

            this.lightLayer = new TileLayer({
                source: new XYZ({
                    attributions: ['All maps © <a href="http://www.openstreetmap.org/">OpenStreetMap</a>'],
                    opaque: false,
                    url: 'https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoidmFqYTcyIiwiYSI6ImNqaHEyMmlndzFlOXAzNnMzdm9weW4wenAifQ.pi99dVLPiG4oF7rSlwzS5A'
                })
            });

            this.darkLayer = new TileLayer({
                source: new XYZ({
                    attributions: ['All maps © <a href="http://www.openstreetmap.org/">OpenStreetMap</a>'],
                    opaque: false,
                    url: 'https://api.mapbox.com/styles/v1/mapbox/dark-v10/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoidmFqYTcyIiwiYSI6ImNqaHEyMmlndzFlOXAzNnMzdm9weW4wenAifQ.pi99dVLPiG4oF7rSlwzS5A'
                })
            });

            var map = new Map({
                layers: [
                    this.lightLayer
                ],
                target: 'map',
                view: new View({
                    zoom: this.zoom,
                    center: this.center,
                })
            });
            set_global_map(map);

            return map;
        },
        initLayers(map) {
            let counter = 4;
            for(let source in this.sources) {
                Active.get(source).then(data => {
                    var newFeatures = (new GeoJSON()).readFeatures(data);
                    this.sources[source].addFeatures(newFeatures);
                }); 
                
                this.layers[source].setSource(this.sources[source]);
                this.layers[source].setStyle(this.styles[source]);
                this.layers[source].setZIndex(counter);
                counter -= 1;
                
                map.addLayer(this.layers[source]);
            }
        },
        switchTheme(darkTheme) {
            if(darkTheme) {
                global_map.removeLayer(this.lightLayer);
                global_map.addLayer(this.darkLayer);
            }
            else {
                global_map.addLayer(this.lightLayer);
                global_map.removeLayer(this.darkLayer);
            }
        },

        getLayerName(layer) {
            for (let layer_name in this.layers) {
                if (this.layers[layer_name] == layer) {
                    return layer_name;
                }
            }
            return "[layer_not_found]"
        },
        initControls(map) {
            this.selection = new Select();

            map.addInteraction(this.selection);
            this.selection.on('select', (e) => {
                let featureSelected = e.selected[0];

                if (featureSelected) {
                    let layer = this.selection.getLayer(featureSelected);
                    if(layer) {
                        layer = this.getLayerName(layer);
                    }
                    else {
                        layer = this.programmaryLayer;
                    }
                    this.$emit('active-click', layer, featureSelected);
                }
                else {
                    this.$emit('close-actives');
                }

            });
            this.$emit("created-selection", this.selection);


            var highlightStyle = new Style({
                fill: new Fill({
                    color: 'rgba(255,255,255,0.7)'
                }),
                stroke: new Stroke({
                    color: '#3399CC',
                    width: 3
                })
            });

            map.on('singleclick', (e) => {
                if(this.selectAdd) {
                    map.forEachFeatureAtPixel(e.pixel, (f) => {
                        var selIndex = this.featsSelected.indexOf(f);
                        if (selIndex < 0) {
                            this.$emit("select-add", f);
                            this.featsSelected.push(f);
                            f.setStyle(highlightStyle);
                        } else {
                            this.featsSelected.splice(selIndex, 1);
                            f.setStyle(undefined);
                        }
                    });
                }
            });
        },

        unselectFeatures() {
            for(let featI in this.featsSelected) {
                let feature = this.featsSelected[featI];
                feature.setStyle(undefined);
            }
            this.featsSelected = [];
        },

        changeLayer(layer) {
            this.layers[layer].changed();
        },

        hideLayer(layer, hide) {
            this.layers[layer].setVisible(hide);
        },

        search(table, valueName, value) {
            let features = [];
            if(value.length === 0) {
                this.$emit('search-found', []);
                return;
            }
            if(valueName == "holder_num") {
                let need_continue = false;
                for(let holder_i = 0; holder_i < holdersSelect.options.length - 1; holder_i += 1) {
                    let holder_option = holdersSelect.options[holder_i];

                    if(holder_option.text.includes(value.toLowerCase())) {
                        value = holder_option.value;
                        need_continue = true;
                    }
                }
                if(!need_continue) {
                    this.$emit('search-found', []);
                    return;
                }
            }
            for(let feature in this.sources[table].getFeatures()) {
                feature = this.sources[table].getFeatures()[feature];
                let valueCompare = feature.getProperties()[valueName];

                if (typeof(valueCompare) == "string") {
                    valueCompare = valueCompare.toLowerCase();
                    if(typeof(value) == "string") {
                        value = value.toLowerCase();

                        if(valueCompare.includes(value)) {
                            features.push(feature);
                        } 
                    }
                }
                else {
                    valueCompare = feature.getProperties()[valueName];
                    if(valueCompare == value) {
                        features.push(feature);
                    } 
                }
            }
            this.$emit('search-found', features);
        }, 
        emitSelection(feature, layerName) {
            this.programmaryLayer = layerName;

            var selected_collection = this.selection.getFeatures();
            selected_collection.clear();
            selected_collection.push(feature);

            this.selection.dispatchEvent({
                type: 'select',
                selected: [feature],
                deselected: []
            });
        },
        //когда удаляется холдер или тип, нужно найти другие активы, которые ему принадлежали
        findAndDeleteValue(valueName, value, firstTypeReplace=null, source=null) {
            for(let source_num in this.sources) {
                if(source != null) {
                    if(source != source_num) {
                        continue;
                    }
                }

                let features_array = this.sources[source_num].getFeatures();
                for(let feature_num in features_array) {
                    let feature = features_array[feature_num];
                    if(feature.getProperties()[valueName] == value) {
                        //и удалить его там
                        let props = feature.getProperties();
                        props[valueName] = firstTypeReplace;
                        feature.setProperties(props);
                        //а затем сказать sidebarLeft сохранить эти изменения
                        this.$emit("found-delete-value", feature, source_num);
                    }
                }
            }
        },
        getSource(sourceName) {
            return this.sources[sourceName];
        },
    }
}
</script>

<style>
.map {
    width: 100%;
    height:100vh; 
}

.ol-zoom {
    top: 1em;
}

.ol-control {
    padding: 1px;
}

.ol-control:hover {
    padding: 1px;
}
</style>