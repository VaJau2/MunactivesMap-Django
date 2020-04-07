<template>
    <div>
        <div class="delete_check_backgroud" id="delete_check_background">
            <div class="delete_check sideCol">
                <p id="delete_check_text" class="delete_check_header textCol labelCol">Удалить балансодержателя?</p>
                <p class="textCol">Вы уверены?</p>
                <input id="delete_check_yes" class="labelCol textCol" type="button" value="да">
                <input id="delete_check_cancel" class="labelCol textCol" type="button" value="нет">
            </div>
        </div>

        <div id="editHeaderBackgr" class="headerMenu editHeader">
            <input type="button" value="отмена" v-on:click="cancelEdit">
            <input type="button" value="сохранить" v-on:click="saveEdit">
            <p class="headerMenuText">Редактирование</p>
        </div>

        <div class="tab sideCol" id="tab1">
            <a @click="makeFront"> 
                <img id="optionsIconDark" src="../assets/options.png" class="tab_icon"> 
                <img id="optionsIconLight" src="../assets/optionsLight.png" class="tab_icon" style="display:none"> 
            </a>
        </div>
        <div id="sidebarLeft" class="sidebarLeft sideCol">
            <a href="javascript:void(0)" class="closebtn textCol" @click="closeMenu">&times;</a>

            <!-- менюшка изменения типов -->
            <div class="type_menu sideCol" id="type_menu">
                <div class="select labelCol property" style="width:223px; margin-bottom: 5px;">
                    <select id='typeSelect' class="labelCol textCol holder_property" v-on:change="checkActiveChange"></select>
                   
                </div>

                <a href="javascript:void(0)" class="closebtn textCol" @click="closeTypeMenu">&times;</a>
               
                <p class="property_head textCol">Название:</p>
                <input class="property holder_property labelCol textCol" id="type_name">
                <p class="property_head textCol">Описание:</p>
                <textarea 
                    id="type_explain" class="property holder_property textCol labelCol" 
                    rows="3" style="width: 220px; resize: none;"
                    v-on:change="checkActiveChange">
                </textarea> 
                <div id="typePurposeDiv">
                    <p class="property_head textCol">Предназначение:</p>
                    <input class="property holder_property labelCol textCol" id="type_purpose" v-on:change="checkActiveChange">
                </div>
                <input id="delete_type" class="delete_holder labelCol textCol" type="button" value="удалить тип">
            </div>


            <!-- менюшка балансодержателей -->
            <div class="holder_menu sideCol" id="holder_menu">
                <div class="select labelCol property" style="width:223px; margin-bottom: 5px;">
                    <select id='holdersSelect' class="labelCol textCol holder_property" v-on:change="checkActiveChange"></select>
                </div>

                <a href="javascript:void(0)" class="closebtn textCol" @click="closeHolderMenu">&times;</a>
                <p class="property_head textCol">Название:</p>
                <input class="property holder_property textCol labelCol" id="holder_name" v-on:change="checkActiveChange">
                <p class="property_head textCol">Контактный номер:</p>
                <input class="property holder_property textCol labelCol" id="holder_phone" v-on:change="checkActiveChange">
                <p class="property_head textCol">Адрес:</p>
                <input class="property holder_property textCol labelCol" id="holder_address" v-on:change="checkActiveChange">
                <p class="property_head textCol">ФИО:</p>
                <input class="property holder_property textCol labelCol" id="holder_fio" v-on:change="checkActiveChange">
                <input id="delete_holder" class="delete_holder textCol labelCol" type="button" value="удалить балансодержателя">
            </div>

            <p id='activeNameLabel' class="textCol">Тип актива</p>

            <a href="javascript:void(0)" class="changePosButton textCol" title="редактировать положение актива на карте" @click="startEdit">
                <img id="mapMarkerIconDark" class="searchIcon" src="../assets/map-marker.png">
                <img id="mapMarkerIconLight" class="searchIcon" src="../assets/map-markerLight.png" style="display: none;">
            </a>
            <hr>
            <!--отдельный div нужен, чтоб его можно было вырубать-->
            <div id='typeDiv' class="active_properties">
                <p class="property_head textCol">Тип:</p>
                <input id='type_button' class="property textCol labelCol" type="button" value='type' style="width:265px">
            </div>

            <ul id="active_properties" class="active_properties">
                <li>
                    <p class="property_head textCol">Балансодержатель:</p>
                    <input id='holder_button' class="property textCol labelCol" type="button" value='holder' style="width:265px">
                </li>

                <li v-for="(fc_value, name) in properties">
                    <p class="property_head textCol">{{name}}:</p>
                    <input v-bind:id="fc_value[1]" class="property textCol labelCol" v-model='fc_value[0]' v-on:change="checkActiveChange">
                </li>
            </ul>
            <hr>
            <input id="delete_active_button" class="property delete_active_button textCol labelCol" type="button" value="удалить актив">
        </div>
    </div>
</template>

<script>
import { global_map } from '../api/global';
import {Active} from '../api/actives'

import GeoJSON from 'ol/format/GeoJSON';
import {Modify, Snap} from 'ol/interaction';
import Collection from 'ol/Collection';

export default {
    data() {
        return {
            map_feature: null,
            activeName: "",
            properties: {},
            sprs: {
                "foundation": {},
                "company": {},
                'stock': {},
            },
            activeSpr: "",
            holders: {},
            deleted_holders: {"data": [], "deleted": []}, 
            changedHolders: [],
            createdHolders: [],

            createdTypes: [],
            changedTypes: [],
            deleted_types: {"data": [], "deleted": [], "name": []},

            changedActives: {},
            geometryChanged: false,
            editingGeometry: null,
            multiplyGeometry: false,
            editingGeometries: null,

            modify: null,
            snap: null,
            featsCollection: null,
        }
    },
    mounted() {
        //загружаем с сервера типы активов
        for(let active_type in this.sprs) {
            Active.get("sprtype"+active_type).then(data => {
                this.sprs[active_type] = data;
            });
        };
        //загружаем с сервера холдеров
        Active.get("holder").then(data => {
            data.sort(function(a,b) {
                if(a["holder_num"] > b["holder_num"]) {
                    return 1;
                }
                if(b["holder_num"] > a["holder_num"]) {
                    return -1;
                }
                return 0;
            });

            for(let temp_holder in data) {
                this.holders[data[temp_holder].holder_num] = data[temp_holder];
                let newOption = new Option(data[temp_holder].name, data[temp_holder].holder_num);
                holdersSelect.append(newOption);
            }

            let optionNewHolder = new Option("Новый балансодержатель", -1);
            holdersSelect.append(optionNewHolder);
        });

        //обрабатываем изменения типа актива (тк он есть всегда)
        typeSelect.onchange = (e) => {
            if(e.target.value == "-1") {
                //код - почти копия кода чуть ниже, его комменты точно подойдут сюда
                let new_type_num = Object.keys(this.sprs[this.activeSpr]).length;

                if(this.deleted_types.data.length > 0) {
                    let typeID = this.deleted_types.data[0];
                    typeID = typeID.split("_")[1];
                    new_type_num = typeID;
                    this.deleted_types.data.shift();
                    this.deleted_types.deleted.shift();
                    this.deleted_types.name.shift();
                }

                let new_type = {
                    "type": "название",
                    "description": "описание"
                }
                if(this.activeSpr == "foundation") {
                    new_type.purpose = "предназначение";
                }

                type_button.value = new_type.type;
                this.sprs[this.activeSpr][new_type_num] = new_type;

                this.updateTypeSelect();
                typeSelect.value = new_type_num;
                this.loadTypeValues();
                this.changeActiveValues("type", new_type.type);

                let typeId = this.activeSpr + "_" + new_type_num;
                this.createdTypes.push(typeId);
            }
            else {
                this.loadTypeValues();
                type_button.value = e.target.options[e.target.value].label;
            }
        }

        holdersSelect.onchange = (e) => {
            //добавляем холдера
            if(e.target.value == "-1") {
                //стандартное место - в конец списка
                let new_holder_num = Object.keys(this.holders).length;

                //но если где-то в списке есть пустое место - добавляем туда
                if(this.deleted_holders.data.length > 0) {
                    new_holder_num = this.deleted_holders.data[0];
                    this.deleted_holders.data.shift(); //убираем элемент из начала списка
                    this.deleted_holders.deleted.shift();
                }

                let new_holder = {
                    "holder_num": new_holder_num,
                    "name": "название",
                    "phone": "000",
                    "address": "адрес",
                    "fio": "ФИО"
                }
                holder_button.value = new_holder.name;
                this.holders[new_holder_num] = new_holder;
                //очищаем select, чтоб опция "новый балансодержатель" переместилась вниз при добавлении
                this.updateHoldersSelect();
    
                //вытаскиваем значения нового холдера
                this.loadHolderValues(new_holder);
                this.changeActiveValues("holder_num", new_holder_num);

                this.createdHolders.push(new_holder_num);
                return;
            }

            let new_holder = this.holders[e.target.value];
            this.loadHolderValues(new_holder);
            holder_button.value = new_holder.name;
            let props = this.map_feature.getProperties();
            props.holder_num = new_holder.holder_num;
            this.map_feature.setProperties(props);
        }

        holder_name.onchange = function(e) {
            if(holdersSelect.value) {
                holdersSelect.options[holdersSelect.value].text = e.target.value;
                holder_button.value = e.target.value;
            }
        }

        delete_holder.onclick = () => {
            delete_check_background.style.display = "block";
            this.deleteAsk("Удалить балансодержателя?", (e) => {
                delete_check_background.style.display = "none";
                //вытаскиваем его номер
                let props = this.map_feature.getProperties();
                let temp_num = props.holder_num;

                //убираем его из списка
                this.delete(this.holders, temp_num);

                this.updateHoldersSelect();
                this.loadHolderValues(null);

                //убираем его из map_feature
                props.holder_num = null;
                this.map_feature.setProperties(props);
                holder_button.value = null;
                //this.updateMapFeature();

                //добавляем в список удаленных холдеров
                this.deleted_holders.data.push(temp_num);
                this.deleted_holders.deleted.push(false); //удален ли холдер в БД

                //убираем из других списков
                if(this.createdHolders.includes(temp_num)) {
                    this.removeValue(this.createdHolders, temp_num);
                }
                if(this.changedHolders.includes(temp_num)) {
                    this.removeValue(this.changedHolders, temp_num);
                }

                this.checkActiveChange(e);

                //проходим по всем активам и убираем холдера, если там стоял удаленный
                this.$emit("find_and_delete_value", 'holder', temp_num);
            })
        }

        delete_check_cancel.onclick = function() {
            delete_check_background.style.display = "none";
        }

        type_name.onchange = (e) => {
            let dict = this.sprs[this.activeSpr];
            for(let i in dict) {
                if(dict[i].type == e.target.value) {
                    alert("Внимание: это название типа уже существует, выберите другое.");
                    type_name.value = type_button.value;
                    return;
                }
            }
            typeSelect.options[typeSelect.selectedIndex].text = e.target.value;
            type_button.value = e.target.value;
            this.checkActiveChange(e); //надо, чтоб оно происходило позже, поэтому оно здесь, а не наверху
        }

        type_button.onclick = function() {
            type_menu.style.left = "20px";
        }

        delete_type.onclick = () => {
            let sprArr = this.sprs[this.activeSpr];
            if(Object.keys(sprArr).length <= 1) {
                alert("Внимание: невозможно удалить последний оставшийся тип.");
                return;
            }

            this.deleteAsk("Удалить тип актива?", (e) => {
                delete_check_background.style.display = "none";
                let props = this.map_feature.getProperties();

                let old_type_num = this.findId(sprArr, props.type, "type");
                let typeId = this.activeSpr + "_" + old_type_num;

                this.deleted_types.data.push(typeId);
                this.deleted_types.deleted.push(false);
                this.deleted_types.name.push(props.type);

                if(this.createdTypes.includes(typeId)) {
                    this.removeValue(this.createdTypes, typeId);
                }
                if(this.changedTypes.includes(typeId)) {
                    this.removeValue(this.changedTypes, typeId);
                }

                this.delete(this.sprs[this.activeSpr], old_type_num);
                let new_type_num = sprArr[Object.keys(sprArr)[0]].type;

                this.$emit("find_and_delete_value", 'type', props.type, new_type_num, this.activeName);

                props.type = new_type_num;
                this.map_feature.setProperties(props);

                this.setType(this.activeSpr);
                this.checkActiveChange(e);
            });
        }

        //удаление актива
        delete_active_button.onclick = () => {
            this.deleteAsk("Удалить актив?", (e) => { 
                delete_check_background.style.display = "none";
                this.$emit("delete-active", this.activeName, this.map_feature);
                this.closeMenu();
                let activeID = this.activeName + "_" + this.map_feature.getId();
                if(activeID in this.changedActives) {
                    delete this.changedActives[activeID];
                }
                //this.checkActiveChange(e);
                this.$emit("check-change");
            });
        }

        let loaded_deleted_holders = JSON.parse(localStorage.getItem("deleted_holders"));
        if(loaded_deleted_holders) {
            this.deleted_holders = loaded_deleted_holders;
        }

        let loaded_deleted_types = JSON.parse(localStorage.getItem("deleted_types"));
        if(loaded_deleted_types) {
            this.deleted_types = loaded_deleted_types;
        }
    },
    methods:
    {
        //методы для управления словарями
        delete(container, key) {
            if (key in container) {
                delete container[key];
                return true;
            }
            return false;
        },
        removeOptions(selectbox) {
            let i;
            for(i = selectbox.options.length - 1 ; i >= 0 ; i--){
                selectbox.remove(i);
            }
        },
        removeValue(arr) {
            var what, a = arguments, L = a.length, ax;
            while (L > 1 && arr.length) {
                what = a[--L];
                while ((ax= arr.indexOf(what)) !== -1) {
                    arr.splice(ax, 1);
                }
            }
            return arr;
        },
        findId(dict, value, compare=null) {
            for(let id in dict) {
                if(compare) {
                    if(dict[id][compare] == value) {
                        return id;
                    }
                }
                else {
                    if(dict[id] == value) {
                        return id;
                    }
                }
            }
            console.log("couldn't find value -> " + value);
            return null;
        },
        changeActiveValues(valueName, value) {
            //меняем объекту переменную
            let feature_options = this.map_feature.getProperties();
            feature_options[valueName] = value;
            this.map_feature.setProperties(feature_options);

            //обновляем значение измененного актива, чтоб там не стояло -1
            let activeID = this.activeName + "_" + this.map_feature.getId();
            this.changedActives[activeID] = (new GeoJSON()).writeFeatureObject(this.map_feature);
        },

        deleteAsk(askText, yesFunc) {
            delete_check_background.style.display = "block";
            delete_check_text.innerText = askText;
            delete_check_yes.onclick = yesFunc;
        },
        setType(typeName) {
            this.activeSpr = typeName;
            this.updateTypeSelect();
            type_button.value = this.map_feature.getProperties().type;
            typeSelect.value = this.findId(this.sprs[this.activeSpr], type_button.value, "type");
            
            this.loadTypeValues();
        },
        updateTypeSelect(){
            this.removeOptions(typeSelect);
            let sprArr = this.sprs[this.activeSpr];
            for(let found_type in sprArr) {
                let type_name = sprArr[found_type].type;
                let newOption = new Option(type_name, found_type);
                typeSelect.append(newOption);
            }
            typeSelect.append(new Option("Новый тип", -1));
        },
        loadTypeValues() {
            let active_type = this.sprs[this.activeSpr][typeSelect.value];
            type_name.value = active_type.type;
            type_explain.value = active_type.description;
            if(this.activeSpr == "foundation") {
                typePurposeDiv.style.display = "block";
                type_purpose.value = active_type.purpose;
            }
            else {
                typePurposeDiv.style.display = "none";
            }
        },
        //добавляем в список измененных активов другие, у которых был удаляемый холдер или тип
        foundDeleteValue(feature, active_name) {
            let activeID = active_name + "_" + feature.getId();
            this.changedActives[activeID] = (new GeoJSON()).writeFeatureObject(feature);
        },

        //обновление списка холдеров
        updateHoldersSelect() {
            this.removeOptions(holdersSelect);
            for(let temp_holder in this.holders) {
                let newOption = new Option(this.holders[temp_holder].name, this.holders[temp_holder].holder_num);
                holdersSelect.append(newOption);
            }
            let optionNewHolder = new Option("Новый балансодержатель", -1);
            holdersSelect.append(optionNewHolder);
        },


        //вызываем менюшку и передаем ей параметры
        openMenu(activeName, feature) {
            this.map_feature = feature;
            this.activeName = activeName;

            feature = feature.getProperties();
            typeDiv.style.display = "block";

            //добавляем в значения словаря массив данных
            //чтоб и выводить можно было, и запросы составлять по их значениям
            this.properties = {
                "Название": [feature.name, 'name'],
                "Адрес": [feature.address, 'address'],
                "Площадь": [feature.square,'square'],
                "Описание": [feature.describe,'describe']
            }

            if(activeName === "foundation") {
                activeNameLabel.innerHTML = "Учреждение";
                this.setType('foundation');
            }
            else if(activeName === "company") {
                activeNameLabel.innerHTML = "Предприятие";
                this.setType('company');
            }
            else if(activeName === "housingstock") {
                activeNameLabel.innerHTML = "Помещение";
                this.setType('stock');

                this.delete(this.properties, "Название");
                this.properties["Этажность"] = [feature.floors, 'floors'];
            }
            else if(activeName === "munitipalland") {
                activeNameLabel.innerHTML = "Муниципальная земля";

                typeDiv.style.display = "none";

                this.delete(this.properties, "Адрес");
                this.properties["Назначение"] = [feature.purpose, 'purpose'];
            }

            if(this.holders[feature.holder_num]) {
                holder_button.value = this.holders[feature.holder_num].name;
            }
            else {
                holder_button.value = null;
            }
            holder_button.onclick = () => {
                this.openHolderMenu();
            }
            this.loadHolderValues(this.holders[feature.holder_num]);
            this.closeHolderMenu();
            this.closeTypeMenu();
            
            sidebarLeft.style.borderRightWidth = "1px";
            sidebarLeft.style.width = "300px";
            tab1.style.left = "300px";
        },

        compareDicts(dict1, dict2) {
            for(let key in dict1) {
                if(dict1[key] !== dict2[key]) {
                    return false;
                }
            }
            return true;
        },

        updateMapFeature() {
            let options = (new GeoJSON()).writeFeatureObject(this.map_feature);

            for(let property in this.properties) {
                let value = this.properties[property];
                options.properties[value[1]] = value[0];
            }

            //тип актива отсутствует в munlands, поэтому берем отдельно
            if(typeDiv.style.display === "block") {
                options.properties["type"] = typeSelect.options[typeSelect.selectedIndex].label;
            }
            options.properties["holder_num"] = parseInt(holdersSelect.value);

            //если объект передвинули, его в любом случае надо сохранить
            if(this.geometryChanged) {
                options.properties["geometry"] = this.map_feature.getGeometry();
                this.geometryChanged = false;
            }
            else if(this.compareDicts(options.properties, this.map_feature.getProperties())) {
                return;
            }
            this.map_feature.setProperties(options.properties);

            let activeID = this.activeName + "_" + this.map_feature.getId();
            this.changedActives[activeID] = (new GeoJSON()).writeFeatureObject(this.map_feature);
        },

        closeMenu() {
            this.$emit("change-selection", "clear");

            sidebarLeft.style.borderRightWidth = "0";
            sidebarLeft.style.width = "0";
            tab1.style.left = "-50px";

            this.closeHolderMenu();
            this.closeTypeMenu();
        },
        
        makeFront() {
            this.$emit('make-front', 'sidebar');
        },

        loadHolderValues(holder) {
            if(holder) {
                holdersSelect.value = holder.holder_num;
                holder_name.value = holder.name;
                holder_phone.value = holder.phone;
                holder_address.value = holder.address;
                holder_fio.value = holder.fio;
            }
            else {
                holdersSelect.value = null;
                holder_name.value = "";
                holder_phone.value = "";
                holder_address.value = "";
                holder_fio.value = "";
            }
        },

        openHolderMenu() {
            holder_menu.style.left = "20px";
        },
        closeHolderMenu() {
            holder_menu.style.left = "-280px";
        },
        closeTypeMenu() {
            type_menu.style.left = "-280px";
        },

        saveTypesData() {
            let options = {}
            options.type = type_name.value;
            options.description = type_explain.value;
            if(this.activeSpr == "foundation") {
                options.purpose = type_purpose.value;
            }
            let typeID = typeSelect.value;
            if(!(typeID in this.sprs[this.activeSpr]) || this.compareDicts(options, this.sprs[this.activeSpr][typeID])) {
                return;
            }
            this.sprs[this.activeSpr][typeID] = options;

            this.updateMapFeature();

            typeID = this.activeSpr + "_" + typeSelect.value;
            if(!this.changedTypes.includes(typeID) && !this.createdTypes.includes(typeID)) {
                this.changedTypes.push(typeID);
            }
        },
        saveHoldersData() {
            let options = {};
            options["holder_num"] = parseInt(this.map_feature.getProperties().holder_num);
            options["name"] = holder_name.value;
            options["phone"] = holder_phone.value;
            options["address"] = holder_address.value;
            options["fio"] = holder_fio.value;

            let holderID = options["holder_num"];

            if(!(holderID in this.holders) || this.compareDicts(options, this.holders[holderID])) {
                return;
            }
            this.holders[holderID] = options;

            if(!this.changedHolders.includes(holderID) && !this.createdHolders.includes(holderID)) {
                this.changedHolders.push(holderID);
            }
        },
        

        checkActiveChange(e) {
            if(e) {
                if(e.target.id.includes("holder") && e.target.id != "holdersSelect") {
                    if(holdersSelect.value) {
                        this.saveHoldersData();
                        this.$emit("check-change");
                    }
                    else {
                        alert("Балансодержатель не найден. Выберите или создайте владельца, чтобы менять его атрибуты");
                        e.target.value = "";
                    }
                }
                else if(e.target.id.includes("type") && e.target.id != "typeSelect" && e.target.id != "delete_type") {
                    this.saveTypesData();
                    this.$emit("check-change");
                }
                else {
                    this.updateMapFeature();
                    this.$emit("check-change");
                }
            }
        },

        saveData() {
            //создаем типы в БД
            for(let typeI in this.createdTypes) {
                typeI = this.createdTypes[typeI].split("_");
                let new_type = this.sprs[typeI[0]][typeI[1]];
                Active.create("sprtype" + typeI[0], new_type);
            }

            //удаляем типы в БД
            for(let typeI in this.deleted_types.data) {
                if(!this.deleted_types.deleted[typeI]) {
                    let typeArr = this.deleted_types.data[typeI].split("_");
                    Active.delete("sprtype" + typeArr[0], this.deleted_types.name[typeI]);
                    this.deleted_types.deleted[typeI] = true;
                }
            }
            localStorage.setItem("deleted_types", JSON.stringify(this.deleted_types));

            //изменяем значения типов
            for(let typeI in this.changedTypes) {
                typeI = this.changedTypes[typeI].split("_");
                let new_type = this.sprs[typeI[0]][typeI[1]];
                Active.update("sprtype" + typeI[0], new_type.type, new_type);
            }

            //создаем холдеров в БД
            for(let holderI in this.createdHolders) {
                holderI = this.createdHolders[holderI];
                let new_holder = this.holders[holderI];
                Active.create("holder", new_holder);
            }
            
            //удаляем холдеров в БД
            for(let holderI in this.deleted_holders.data) {
                if(!this.deleted_holders.deleted[holderI]) {
                    Active.delete("holder", this.deleted_holders.data[holderI]);
                    this.deleted_holders.deleted[holderI] = true;
                }
            }
            localStorage.setItem("deleted_holders", JSON.stringify(this.deleted_holders));

            //изменяем значения холдеров
            for(let holderI in this.changedHolders) {
                holderI = this.changedHolders[holderI];
                let options = this.holders[holderI];
                Active.update("holder", holderI, options);
            }

            //изменяем значения активов
            for(let activeI in this.changedActives) {
                let options = this.changedActives[activeI];
 
                activeI = activeI.split("_");
                let activeName = activeI[0];
                let activeID = activeI[1];
                Active.update(activeName, activeID, options);
            }
            this.createdTypes = [];
            this.changedTypes = [];
            this.createdHolders = []; //очищаем словари 
            this.changedHolders = [];
            this.changedActives = { };
        },
        startEdit() {
            this.editingGeometry = (new GeoJSON()).writeFeature(this.map_feature);
            this.featsCollection = new Collection([this.map_feature]);
            this.modify = new Modify({features: this.featsCollection});
            this.modify.on("modifyend", () => {
                this.geometryChanged = true;
            });
            global_map.addInteraction(this.modify);

            editHeaderBackgr.style.top = "0";
            sidebarLeft.style.borderRightWidth = "0";
            sidebarLeft.style.width = "0";
            tab1.style.left = "-50px";
            searchMapButton.style.left = "-2em";
            drawMapButton.style.left = "-2em";

            if(this.activeName == "munitipalland") {
                this.snap = new Snap({features: this.featsCollection});
                global_map.addInteraction(this.snap);
                this.$emit("change-selection", "add", true);
            }
            else {
               this.$emit("change-selection", "on", false); 
            }
        },
        addEditFeature(feature) {
            this.featsCollection.push(feature);
            this.editingGeometries = (new GeoJSON()).writeFeatures(this.featsCollection.getArray());
            this.multiplyGeometry = true;
        },
        stopEdit() {
            this.clearModify();

            editHeaderBackgr.style.top = "-15px";
            sidebarLeft.style.borderRightWidth = "1px";
            sidebarLeft.style.width = "300px";
            tab1.style.left = "300px";
            searchMapButton.style.left = ".5em";
            drawMapButton.style.left = ".5em";

            if(this.activeName == "munitipalland") {
                this.$emit("change-selection", "add", false);
            }
            else {
                this.$emit("change-selection", "on");
            }
        },
        cancelEdit() {
            if(this.multiplyGeometry) {
                let feats = (new GeoJSON()).readFeatures(this.editingGeometries);
                let featsArr = this.featsCollection.getArray();

                for(let i = 0; i < featsArr.length; i++) {
                    let feature = feats[i];
                    featsArr[i].setGeometry(feature.getGeometry());
                }
            }
            else {
                let feature = (new GeoJSON()).readFeature(this.editingGeometry);
                this.map_feature.setGeometry(feature.getGeometry());
            }

            this.stopEdit();
        },
        saveEdit() {
            if(this.geometryChanged) {
                this.$emit("check-change");
                document.title = "Munactives map (*)";
                this.updateMapFeature();

                let featsArr = this.featsCollection.getArray();
                if(this.multiplyGeometry) {
                    for(let i = 0; i < featsArr.length; i++) {
                        let feature = featsArr[i];
                        let activeID = this.activeName + "_" + feature.getId();
                        this.changedActives[activeID] = (new GeoJSON()).writeFeatureObject(feature);
                    }

                    this.multiplyGeometry = false;
                }
            }

            this.stopEdit();
        },
        clearModify() {
            if(this.modify != null) {
                global_map.removeInteraction(this.modify);
                global_map.removeInteraction(this.snap);
                this.modify = null;
                this.snap = null;
            }
        },
    }
}
</script>

<style>
.sidebarLeft {
    border-right: 0 solid #6f6f6f;
    width: 0;
    height: 100%;
    position: fixed;
    z-index: 5002;
    top: 0;
    left: 0;
    background-color: rgb(248, 248, 248);
    overflow-x: hidden;
    padding-top: 20px;
    transition: 0.2s;
}

.sidebarLeft .closebtn {
    position: absolute;
    display: inline-block;  
    top: 15px;
    left: 20px;
    font-size: 22px;
    text-decoration: none;
    transition: 0.2s;
}

.sidebarLeft .closebtn:hover {
    transform: scale(1.25);
    color: black;
}

.sidebarLeft .closebtn:active {
    border: none;
}

#activeNameLabel {
    margin-top: 2px;
    margin-bottom: 15px;
    text-align: center;
    font-size: 16px;
}

.active_properties {
    padding-left: 2px;
    margin: 0;
}

.property_head {
    display: inline-block;
    margin: 2px 10px;
}

.property {
    margin: 0 8px;
    width: 250px;
    font-size: 12px;
}

.holder_property {
    width: 210px;
    text-align: center;
}

#typeDiv .property {
    width: 265px;
}


.tab {
    position: absolute;
    left:-50px;
    top: 55px;
    height: 45px;
    width: 20px;
    background: white;
    border: 1px solid #6f6f6f; 
    border-left: none;
    margin: 8px 0;
    border-radius: 0 4px 4px 0;
    transition: 0.2s;
    z-index: 5003;
    cursor: pointer;
}

.tab_icon {
    width: 20px;
    height: 20px;
    margin-top: 10px;
}

.holder_menu {
    position: absolute;
    background: rgb(248,248,248);
    width: 250px;
    left: -280px;
    top: 120px;
    transition: 0.2s;
    padding: 5px 0;
    box-shadow: 0 0 10px rgba(0,0,0,0.5);
}

.delete_holder {
    width: 220px;
    padding: 5px 0;
    margin-top: 15px;
    margin-left: 10px;
    margin-bottom: 8px;
}

.delete_check_backgroud {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    background:rgba(10,10,10,0.6);
    display: none;
    z-index: 5004;
}

.delete_check {
    position: absolute;
    top: 30%;
    left: 40%;
    border: 1px solid #383838;
    text-align: center;
    padding-bottom: 8px;
}

.delete_check_header {
    margin: 0;
    padding: 8px;
}

.editHeader {
    top: -15px;
    background-color: #3aa510;
    border-bottom: #141b0d solid 1px;
}

.editHeader input {
    height: 14px;
    border: 0;
    padding: 0 15px;
    margin-left: 5px;
}

.editHeader input:hover {
    background-color: #73e247;
}

.changePosButton {
    position: absolute;
    top: 15px;
    left: 250px;
    transition: 0.2s;
}

.changePosButton:hover {
    transform: scale(1.2);
}

.type_menu {
    position: absolute;
    background: rgb(248,248,248);
    top: 75px;
    padding: 5px 0;
    width: 250px;
    left: -280px;
    transition: 0.2s;
    box-shadow: 0 0 10px rgba(0,0,0,0.5);
}

#delete_active_button {
    width: 265px;
    margin-top: 6px;
}
</style>