<template>
    <div>
        <div id="createHeaderBackgr" class="headerMenu createHeader">
            <label class="layerContainer drawMultiplyLeftMargin">Множественное создание
                <input type="checkbox" id="draw_check_multiply">
                <span class="drawCheckmarker checkmark"></span>
            </label>

            <p class="headerMenuText">Создание</p>
        </div>
        <div id="askTypeDraw" class="sideCol">
            <a href="javascript:void(0)" class="closebtn textCol" @click="closeAsk">&times;</a>
            <p class="textCol">Выберите тип актива</p>
            <ul>
            <li><input class="textCol labelCol" type='button' value="Учреждения" id="create_foundation"></li>
            <li><input class="textCol labelCol" type='button' value="Предприятия" id="create_company"></li>
            <li><input class="textCol labelCol" type='button' value="Помещения" id="create_housingstock"></li>
            <li><input class="textCol labelCol" type='button' value="Муниципальные земли" id="create_munitipalland"></li>
            </ul>
        </div>
    </div>
</template>

<script>
import { global_map } from '../api/global';
import {Active} from '../api/actives'

import GeoJSON from 'ol/format/GeoJSON';
import {Control} from 'ol/control';
import {Draw, Snap} from 'ol/interaction';

export default {
    props: {
        defaultTypes: Object
    },
    data() {
        return {
            source: null,
            draw: null,
            snap: null,

            createdActives: {
                "props": {},
                "geometry": {}
            },
            deletedActives: {
                "data": [], 
                "deleted": []
            }
        }
    },
    mounted() { 
        this.$nextTick(() => {
            this.initControls(global_map);
        });

        let actives = ['company', 'foundation', 'housingstock', 'munitipalland'];
        for(let active_num in actives) {
            let active_name = actives[active_num];
            let temp_button = document.getElementById("create_" + active_name);

            temp_button.onclick = () => {
                this.$emit("change-selection", "on", false);
                //this.$emit("change-selection", "add", true);
                this.openMenu();
                this.closeAsk();

                this.$emit("get-source", active_name);
                let type = "Point";
                let addSnap = false;
                if(active_name == "munitipalland") {
                    type = "Polygon";
                    addSnap = true;
                }
                this.draw = new Draw({
                    source: this.source,
                    type: type
                })
                this.draw.on("drawend", (e) => {
                    let props = e.feature.getProperties();

                    if(active_name != "munitipalland") {
                        this.$emit("update-default-types");
                        let type_name = active_name;
                        if(type_name == "housingstock") {
                            type_name = "stock";
                        }
                        props.type = this.defaultTypes[type_name]; 
                        e.feature.setProperties(props);
                    }

                    if(active_name != "housingstock") {
                        props.name = "Название актива";
                    }
                    props.address = "Адрес актива";
                    props.square = "0";
                    props.describe = "Описание актива";
                    if(active_name == "housingstock") {
                        props.floors = "0";
                    }
                    if(active_name == "munitipalland") {
                        props.purpose = "Назначение актива";
                    }
                    props.holder_num = null;

                    e.feature.setProperties(props);

                    let newID = this.source.getFeatures().length;
                    if(this.deletedActives.data.length > 0) {
                        for(let i in this.deletedActives.data) {
                            let activeID = this.deletedActives.data[i];
                            activeID = activeID.split("_");
                            if(activeID[0] == active_name) {
                                newID = activeID[1];
                                this.deletedActives.data.splice(i, 1);
                                this.deletedActives.deleted.splice(i, 1);
                                break;
                            }
                        }
                    }
                    e.feature.setId(newID);

                    let activeID = active_name + "_" + newID;
                    this.createdActives.props[activeID] = e.feature.getProperties();
                    this.createdActives.geometry[activeID] = e.feature.getGeometry();

                    if(!draw_check_multiply.checked) {
                        this.cancelMenu();
                        this.$emit('emit-selection', e.feature, active_name);
                    }

                    this.$emit("check-change");
                });
                global_map.addInteraction(this.draw);
                if(addSnap) {
                    this.snap = new Snap({source: this.source});
                    global_map.addInteraction(this.snap);
                }
            };

        }
    },
    methods: {
        initControls(map) {
            this.createButton(map, "drawMapButton", "openDrawMenu", "создать актив", '🖉', this.openAsk);
            this.createButton(map, "cancelDrawButton", "cancelDrawMenu", "отменить создание", "X", this.cancelMenu);
        },
        createButton(map, buttonID, buttonClass, buttonText, icon, func) {
            var buttonStart = document.createElement('button');
            buttonStart.title = buttonText;
            buttonStart.style = "padding-top: 5px;";
            buttonStart.innerHTML = icon;
            buttonStart.addEventListener('click', func, false);

            var elementStart = document.createElement('div');
            elementStart.id = buttonID;
            elementStart.className = buttonClass + ' ol-unselectable ol-control';
            elementStart.appendChild(buttonStart);

            var myControlStart = new Control({element: elementStart});

            map.addControl(myControlStart);
        },
        openAsk() {
            askTypeDraw.style.left = "0.5em";
        },
        closeAsk() {
            askTypeDraw.style.left = "-20em";
        },
        openMenu() {
            createHeaderBackgr.style.top = "0px";
            searchMapButton.style.left = "-2em";
            drawMapButton.style.left = "-2em";
            cancelDrawButton.style.left = ".5em";
        },
        cancelDraw() {
            if(this.snap) {
                global_map.removeInteraction(this.snap);
                this.snap = null;
            }
            if(this.draw) {
                this.$emit("change-selection", "on");
                //this.$emit("change-selection", "add", false);
                global_map.removeInteraction(this.draw);
                this.draw = null;
            }
        },
        cancelMenu() {
            createHeaderBackgr.style.top = "-15px";
            searchMapButton.style.left = ".5em";
            drawMapButton.style.left = ".5em";
            cancelDrawButton.style.left = "-2em";
            this.cancelDraw();
        },
        removeActive(activeName, feature) {
            let activeID = activeName + "_" + feature.getId();
            this.deletedActives.data.push(activeID);
            this.deletedActives.deleted.push(false);

            if(activeID in this.createdActives) {
                delete this.createdActives.props[activeID];
                delete this.createdActives.geometry[activeID];
            }
        },

        saveData() {
            let count = 0;
            for(let activeI in this.createdActives.props) {
                let activeData = this.createdActives.props[activeI];
                delete activeData.geometry;

                let activeGeom = this.createdActives.geometry[activeI];
                activeGeom = (new GeoJSON).writeGeometry(activeGeom);

                activeI = activeI.split("_");
                let activeName = activeI[0];

                let savedActiveData = {};
                savedActiveData.id = activeI[1]; //приводим данные в вид, читаемый в post запросах
                savedActiveData.name = "create"; //ведь эти запросы такие привереды, шо капец
                if(activeName != "munitipalland") {
                    savedActiveData.type = activeData.type;
                }
                for(let i in activeData) {
                    savedActiveData[i] = activeData[i];
                }
                savedActiveData.coordinates = activeGeom;     

                Active.create(activeName, savedActiveData).then(() => {
                    if(count < this.createdActives.props.length - 1) {
                        count += 1;
                    } else { //доходим до последнего созданного актива и отправляем app сигнал о том, что все созданы
                        this.$emit("continue-save");
                    }
                });
            }
            
            if(Object.keys(this.createdActives.props).length == 0) { //если созданных активов не оказалось, сохранять дальше все равно надо
                this.$emit("continue-save");
            }

            this.createdActives = {
                "props": {},
                "geometry": {}
            };
            

            for(let i in this.deletedActives.data) {
                if(!this.deletedActives.deleted[i]) {
                    let activeArr = this.deletedActives.data[i].split("_");
                    Active.delete(activeArr[0], activeArr[1]);
                    this.deletedActives.deleted[i] = true;
                }
            }
            localStorage.setItem("deleted_actives", JSON.stringify(this.deletedActives));
        }
    }
}
</script>

<style>
.headerMenu {
    position: absolute;
    width: 100%;
    height: 14px;
    transition: 0.5s;
}

.createHeader {
    top: -15px;
    background-color: #f56e00;
    border-bottom: #271200 solid 1px;
}

.openDrawMenu {
    top: 6.8em;
    left: .5em;
    transition: 0.2s;
}

.cancelDrawMenu {
    top: 6.8em;
    left: -2em;
    transition: 0.2s;
}

.headerMenuText {
    margin: 0 2%;
    color: #fff3e9;
    display: inline-block;
}

#askTypeDraw {
    position: absolute;
    top: 6.8em;
    left: -20em;
    border: rgba(38, 38, 38, 0.4) solid 2px;
    border-radius: 5px;
    transition: 0.5s;
}

#askTypeDraw ul {
    padding: 0 5px;
    margin: 5px 0;
}

#askTypeDraw li {
    list-style-type: none; 
    cursor: pointer;
}

#askTypeDraw .closebtn {
    top: 1px;
    left: 6px;
}

#askTypeDraw p {
    text-align: center;
    border-bottom: rgba(38, 38, 38, 0.4) solid 1px;
    margin: 8px 0;
}

#askTypeDraw input {
    width: 190px;
    cursor: pointer;
    border-radius: 5px;
    margin-bottom: 5px;
}

.drawMultiplyLeftMargin {
    margin-left: 5px;
    color: #fff3e9;
}

.drawCheckmarker {
    height: 14px;
    width: 14px;
}

.drawCheckmarker::after {
    left: 4px !important;
    top: 1px !important;
    width: 3px !important;
    height: 8px !important;
}

</style>