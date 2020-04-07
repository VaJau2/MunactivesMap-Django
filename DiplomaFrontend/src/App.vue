<template>
    <div id="app">
        <MyMap
            ref="myMap"

            v-bind:styles="styles"
            v-on:created-selection="loadSelection"
            v-on:active-click="activeClick"
            v-on:search-found="searchFound"
            v-on:close-actives="closeActives"
            v-on:found-delete-value="foundDeleteValue"
            v-on:select-add="selectAddFeature"
         />
        <sidebar-left 
            ref="sidebarLeft"

            v-on:make-front="makeFront"
            v-on:find_and_delete_value="findAndDeleteValue"
            v-on:close-menu="closeSidebarLeft"
            v-on:check-change="checkChange"
            v-on:change-selection="changeSelection"
            v-on:delete-active="deleteActive"
        />
        <sidebar-search 
            ref="sidebarSearch"
            v-on:make-front="makeFront"
            v-on:make-search="makeSearch"
            v-on:emit-selection="emitSelection"
        />
        <sidebar-right
            v-on:hide-layer="hideLayer"
            v-on:change-color="changeColor"
            v-on:switch-theme="switchTheme"
        />
        <draw-menu 
            ref="drawMenu"
            v-bind:defaultTypes="defaultTypes"
            v-on:get-source="getSource"
            v-on:change-selection="changeSelection"
            v-on:emit-selection="emitSelection"
            v-on:check-change="checkChange"
            v-on:update-default-types="updateDefaultTypes"
            v-on:continue-save="saveData2"
        />
    </div>
</template>

<script>
import {Modcolor} from './api/modcolor';
import { global_map } from './api/global';
import {Circle as CircleStyle, Fill, Stroke, Style} from 'ol/style';
import {Control} from 'ol/control';
import * as olColor from 'ol/color';

import MyMap from './components/map'
import sidebarRight from './components/sidebarRight'
import sidebarLeft from './components/sidebarLeft'
import sidebarSearch from './components/sidebarSearch'
import drawMenu from './components/drawMenu'

export default {
    name: 'app',
    components: {
        MyMap,
        sidebarLeft,
        sidebarRight,
        sidebarSearch,
        drawMenu,
    },
    data () {
        return {
            showFounds: true,
            showCompanies: true,
            showStocks: true,
            showMunlands: true,

            styles: {
                'foundation': this.initStyle('foundation', "#201dcf"),
                'company': this.initStyle('company', "#02e15f"),
                'housingstock': this.initStyle('housingstock', "#020202"),
                'munitipalland': this.initStyle('munitipalland', "#C10900"),
            },
            select: null,

            maySave: false,
            defaultTypes: {},

            darkTheme: false,
            menuColor: null,
        }
    },
    mounted() {
        this.menuColor = document.createElement('style');
        this.menuColor.innerHTML = this.getCSS();
        document.head.appendChild(this.menuColor);

        this.$nextTick(() => {
            this.initControls(global_map);
        });
        document.addEventListener("keydown", (e) => {
            if ((window.navigator.platform.match("Mac") ? e.metaKey : e.ctrlKey)  && e.keyCode == 83) {
                e.preventDefault();
                if(this.maySave) {
                    this.saveData();
                }
            }
        }, false);
    },
    methods: {
        initControls(map) {
            var button = document.createElement('button');
            button.title = "сохранить изменения";
            button.style = "padding-top: 5px;";
            button.innerHTML = '🖬';
            button.addEventListener('click', this.saveData1, false);

            var element = document.createElement('div');
            element.id = "saveDataButton";
            element.className = 'saveDataButton ol-unselectable ol-control';
            element.appendChild(button);

            var myControl = new Control({element: element});

            map.addControl(myControl);
        },
        saveData1() { //слишком сложно проводить асинхронность, когда изменяешь еще не созданный актив
            //сначала мы его должны создать
            this.$refs.drawMenu.saveData(); 
        },
        saveData2() { //а уже потом изменять
            this.$refs.sidebarLeft.saveData();
            this.maySave = false;
            window.onbeforeunload = null;
            document.title = "Munactives map";
            saveDataButton.style.left = "-2em";
            console.log("data saved");
        },
        initStyle(style, temp_color) {
            var strokeColor = Modcolor.pSBC(-0.6, temp_color);

            var fillColor = olColor.asArray(temp_color);
            fillColor = fillColor.slice();
            fillColor[3] = 0.4;

            var newStyle = new Style({
                fill: new Fill({
                    color: fillColor
                }),
                stroke: new Stroke({
                    color: strokeColor,
                    width: 2
                }),
                image: new CircleStyle({
                    radius: 7,
                    fill: new Fill({
                        color: temp_color
                    })
                })
            });
            return newStyle;
        },

        hideLayer(hide, layer) {
            this.$refs.myMap.hideLayer(layer, hide);
        },
        changeColor(color, layer) {
            var strokeColor = Modcolor.pSBC(-0.6, color);
            this.styles[layer].setStroke(new Stroke({
                color: strokeColor,
                width: 2
            }));

            this.styles[layer].setImage(new CircleStyle({
                radius: 7,
                fill: new Fill({
                    color: color
                })
            }))

            if(layer == "munitipalland") {
                var fillColor = olColor.asArray(color);
                fillColor = fillColor.slice();
                fillColor[3] = 0.4;

                this.styles['munitipalland'].setFill(new Fill({
                    color: fillColor
                }));
            }
            this.$refs.myMap.changeLayer(layer);
        },
        loadSelection(select) {
            this.select = select;
        },
        changeSelection(change, on=true) {
            if(change == "clear") {
                this.select.getFeatures().clear();
            }
            else if(change == "on") {
                this.select.setProperties({
                    "active": on
                });
            }
            else if(change == "add") {
                this.changeSelection("on", !on);
                this.$refs.myMap.selectAdd = on;
                if(!on) {
                    this.$refs.myMap.unselectFeatures();
                }
            }
        },
        activeClick(activeName, feature) {
            this.$refs.sidebarLeft.openMenu(activeName, feature, this.select);
            this.makeFront("sidebar");
        },
        closeActives() {
            this.$refs.sidebarLeft.closeMenu();
        },
        makeFront(name) {
            if(name === "sidebar") {
                document.getElementById("tab1").style.zIndex = 5003;
                document.getElementById("sidebarLeft").style.zIndex = 5002;
                document.getElementById("tab2").style.zIndex = 5001;
                document.getElementById("sidebarSearch").style.zIndex = 5000;
            }
            else {
                document.getElementById("tab2").style.zIndex = 5003;
                document.getElementById("sidebarSearch").style.zIndex = 5002;
                document.getElementById("tab1").style.zIndex = 5001;
                document.getElementById("sidebarLeft").style.zIndex = 5000;
            }
        },
        makeSearch(table, valueName, value) {
            this.$refs.myMap.search(table, valueName, value);
        },
        searchFound(features) {
            this.$refs.sidebarSearch.searchResult(features);
        },
        emitSelection(feature, layerName) {
            this.$refs.myMap.emitSelection(feature, layerName);
        },
        findAndDeleteValue(valueName, value, firstTypeReplace=null, source=null) {
            this.$refs.myMap.findAndDeleteValue(valueName, value, firstTypeReplace, source);
        },
        foundDeleteValue(feature, active_name) {
            this.$refs.sidebarLeft.foundDeleteValue(feature, active_name);
        },
        closeSidebarLeft() {
            this.$refs.myMap.clearModify();
        },
        getSource(sourceName) {
            let source = this.$refs.myMap.getSource(sourceName);
            this.$refs.drawMenu.source = source;
        },
        updateDefaultTypes() {
            let allTypes = this.$refs.sidebarLeft.sprs;
            for(let typeI in allTypes) {
                let firstKey = Object.keys(allTypes[typeI])[0];
                this.defaultTypes[typeI] = allTypes[typeI][firstKey].type;
            }
        },
        selectAddFeature(feature) {
            let sideLeft = this.$refs.sidebarLeft;
            if(sideLeft.modify != null) {
                sideLeft.addEditFeature(feature);
            }
        },
        deleteActive(sourceName, feature) {
            let source = this.$refs.myMap.getSource(sourceName);
            source.removeFeature(feature);
            this.$refs.drawMenu.removeActive(sourceName, feature);
        },

        checkChange() {
            document.title = "Munactives map (*)";
            saveDataButton.style.left = ".5em";
            this.maySave = true;
            window.onbeforeunload = function() {
                return 'Внимание, изменения не сохранены. Покинуть страницу?';
            };
        },

        getCSS() {
            let darkCol = "rgb(52,52,52)";
            let lightCol = "rgb(248,248,248)";
            let contrBackCol = "rgba(38,38,38,0.4)";
            let butCol = "#66757f";
            let butColHov = "#373f44";
            let whiteCol = "#FFFFFF";

            if(this.darkTheme) {
                lightCol = "rgb(52,52,52)";
                darkCol = "rgb(248,248,248)"
                contrBackCol = "rgb(200,200,200,0.4)";
                butCol = "#d4dee4";
                butColHov = "#97a1a7";
                whiteCol = "#151515";
            }

            return `.sideCol {
                        background-color: `+ lightCol +`;
                    }
                    .textCol {
                        color: `+ darkCol +`;
                    }
                    .labelCol {
                        background-color: `+ whiteCol +`;
                    }
                    .buttonCol {
                        background-color: `+ butCol +`;
                    }
                    .buttonCol:hover {
                        background-color: `+ butColHov +`;
                    }

                    .ol-control {
                        background-color:  `+ contrBackCol +`;
                    }
                    .ol-control:hover {
                        background-color: `+ contrBackCol +`;
                    }
                    .ol-control button {
                        color: `+ butCol +`;
                        background-color: `+ lightCol +`;
                    }
                    .ol-control button:hover {
                        color: `+ butColHov +`;
                        background-color: rgb(167, 167, 167);
                    }
                    .ol-control button:active {
                        background-color: rgb(136, 136, 136);
                    }
                    .ol-control button:focus {
                        background-color: rgb(200, 200, 200);
                    }`
        },

        switchTheme() {
            this.darkTheme = !this.darkTheme;
            this.$refs.myMap.switchTheme(this.darkTheme);
            this.menuColor.innerHTML = this.getCSS();
            if(this.darkTheme) {
                this.switchIcons(searchIconDark, searchIconLight);
                this.switchIcons(searchIconDark1, searchIconLight1);
                this.switchIcons(mapMarkerIconDark, mapMarkerIconLight);
                this.switchIcons(optionsIconDark, optionsIconLight);
            }
            else {
                this.switchIcons(searchIconLight, searchIconDark);
                this.switchIcons(searchIconLight1, searchIconDark1);
                this.switchIcons(mapMarkerIconLight, mapMarkerIconDark);
                this.switchIcons(optionsIconLight, optionsIconDark);
            }
            localStorage.setItem("dark-theme", this.darkTheme);
        },
        switchIcons(oldIcon, newIcon){
            oldIcon.style.display = "none";
            newIcon.style.display = "block";
        },
    }
}
</script>

<style>
body {
    margin: 0;
    padding: 0;
}

#app {
    height: 100vh;
}

* {
    font-size: 15px;
    font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
}

.saveDataButton {
    top: 8.9em;
    left: -2em;
    transition: 0.2s;
}

input {
    border: #8d8d8d solid 1px;
    border-radius: 5px;
    padding: 6px;
}

input:hover {
    border: #1385f0 solid 1px;
}

textarea {
    border: #8d8d8d solid 1px;
    border-radius: 5px;
    padding: 6px 0;
}

textarea:hover {
    border: #1385f0 solid 1px;
}

/* Reset Select */
select {
    -webkit-appearance: none;
    -moz-appearance: none;
    -ms-appearance: none;
    appearance: none;
    outline: 0;
    box-shadow: none;
    border: 0 !important;
    background-image: none;
}
/* Remove IE arrow */
select::-ms-expand {
    display: none;
}
/* Custom Select */
.select {
    position: relative;
    display: inline-block;
    width: 200px;
    height: 30px;
    line-height: 2;
    overflow: hidden;
    border-radius: .25em;
    border: #8d8d8d 1px solid;
    top: 10px;
}

select {
    height: 100%;
    width: 100%;
    padding: 0 .5em;
    cursor: pointer;
    display: block;
}

select:focus {
    border: none;
}

/* Arrow */
.select::after {
    content: '\25BC';
    position: absolute;
    top: 0;
    right: 0;
    padding: 0 1px;
    cursor: pointer;
    pointer-events: none;
    -webkit-transition: .25s all ease;
    -o-transition: .25s all ease;
    transition: .25s all ease;
}
.select::after:hover {
    border: #1385f0 1px solid;
}
/* Transition */
.select:hover::after {
    color: #1385f0;
}
</style>
