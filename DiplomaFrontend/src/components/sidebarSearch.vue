<template>
    <div>
        <img id="searchIconDark" class="searchIcon" src="../assets/search.png">
        <img id="searchIconLight" class="searchIcon" src="../assets/searchLight.png">


        <div class="tab tab1 sideCol" id="tab2">
            <a @click="makeFront"> 
                <img id="searchIconDark1" src="../assets/search.png" class="tab_icon"> 
                <img id="searchIconLight1" src="../assets/searchLight.png" class="tab_icon" style="display:none;"> 
            </a>
        </div>
        <div id="sidebarSearch" class="sidebarSearch sideCol">
            <a href="javascript:void(0)" class="closebtn textCol" @click="closeMenu">&times;</a>
            <div class='searchContent'>

                <p class="textWhere textCol">Искать в:</p>
                <div class="select labelCol">
                    <select id='chooseTable' class="textCol labelCol"></select>
                </div>
                
                <p class='textWhere textCol'>Атрибут:</p>
                <div class="select labelCol">
                    <select id='chooseValue' class="textCol labelCol"></select>
                </div>

                <input type="text" id='searchText' class="textCol labelCol">
                <input type="button" value="Поиск" class='searchButton textCol labelCol' id='searchButton'>
            </div>

            <hr>
            <p class="foundedHeader textCol">Найдено:</p>
            <div class="founded textCol" id='foundedDiv'>
                <ul id='foundedList'>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
import { global_map } from '../api/global';

import {Control} from 'ol/control';

export default {
    data() {
        return {
            tables: {
                "foundation": [
                    'name', 'type', 'address',
                    'holder_num', 'square', 'describe',
                ],
                "company": [
                    'name', 'type', 'address',
                    'holder_num', 'square', 'describe',
                ],
                "housingstock": [
                    'type', 'address', 'holder_num',
                    'square', 'describe', 'floors',
                ],
                "munitipalland": [
                    'name', 'purpose', 'holder_num',
                    'square', 'describe'
                ]
            },
            tableNames: {
                "учреждениях": [
                    'название', 'тип', 'адрес',
                    'балансодержатель', 'площадь', 'описание',
                ],
                "предприятиях": [
                    'название', 'тип', 'адрес',
                    'балансодержатель', 'площадь', 'описание',
                ],
                "помещениях": [
                    'тип', 'адрес', 'балансодержатель',
                    'площадь', 'описание', 'этажность',
                ],
                "муниципальных землях": [
                    'название', 'назначение', 'балансодержатель',
                    'площадь', 'описание'
                ]
            },
            tempFound: Array
        }
    },
    mounted() { 
        this.$nextTick(() => {
            this.initControls(global_map);
        });

        for(let i = 0; i < Object.keys(this.tables).length; i++) {
            let tableKey = Object.keys(this.tables)[i];
            let tableNamesKey = Object.keys(this.tableNames)[i];

            let newOption = new Option(tableNamesKey, tableKey);
            chooseTable.append(newOption);
        }
        chooseTable.onchange = (e) => {
            this.updateAttributes(e.target.value);
            searchText.value = null;
        };
        chooseValue.onchange = function() {
            searchText.value = null;
        };
        this.updateAttributes(chooseTable.value);

        searchButton.onclick = () => {
            this.$emit('make-search', chooseTable.value, chooseValue.value, searchText.value);
        }
    },
    methods: {
        //открываем менюшку справа
        openMenu() {
            sidebarSearch.style.borderRightWidth = "1px";
            sidebarSearch.style.width = "300px";
            tab2.style.left = "300px";
        },

        //закрываем менюшку справа
        closeMenu() {
            sidebarSearch.style.borderRightWidth = "0";
            sidebarSearch.style.width = "0";
            tab2.style.left = "-50px";
        },
        initControls(map) {
            //добавляем кнопку для включения менюшки поиска
            var button = document.createElement('button');

            button.title = "поиск актива";
            button.id = "searchIconButton";
            button.appendChild(searchIconDark);
            button.appendChild(searchIconLight);
            button.addEventListener('click', this.openMenu, false);

            var element = document.createElement('div');
            element.id = "searchMapButton";
            element.className = 'openSidebarSearch ol-unselectable ol-control';
            element.appendChild(button);

            var myControl = new Control({element: element});

            map.addControl(myControl);
        },

        removeOptions(selectbox) {
            let i;
            for(i = selectbox.options.length - 1 ; i >= 0 ; i--){
                selectbox.remove(i);
            }
        },
        updateAttributes(table) {
            this.removeOptions(chooseValue);

            let values = this.tables[table];
            let valNumber = Object.keys(this.tables).indexOf(table);
            let tempName = Object.keys(this.tableNames)[valNumber];
            let valueNames = this.tableNames[tempName];

            for(let i = 0; i < values.length; i++) {
                let newOption = new Option(valueNames[i], values[i]);
                chooseValue.append(newOption);
            }
        },
        makeFront() {
            this.$emit('make-front', 'search');
        },
        searchResult(features) {
            while(foundedList.firstChild) {
                foundedList.removeChild(foundedList.firstChild);
            }

            if(features.length == 0) {
                if(!document.getElementById("tempNotFound")) {
                    let newP = document.createElement("p");
                    newP.id = "tempNotFound";
                    newP.innerHTML = 'Ничего не найдено';
                    foundedDiv.appendChild(newP);
                }
                this.tempFound = [];
            }
            else {
                this.tempFound = features;
                if(document.getElementById("tempNotFound")) {
                    foundedDiv.removeChild(tempNotFound);
                }

                for(let feature in features) {
                    let newLi = document.createElement("li");
                    let props = features[feature].getProperties();
                    if('name' in props) {
                        newLi.innerHTML = '<a href=javascript:void(0)>' + props['name'] + '</a>';
                    }
                    else {
                        newLi.innerHTML = '<a href=javascript:void(0)>' + props['type'] + " - " + props['address']+ '</a>';
                    }
                    newLi.onclick = this.resultClick;
                    foundedList.appendChild(newLi);
                }
            }
        },
        resultClick(e) {
            let coords = [];

            let searchText = e.target.text;

            if(!searchText) {
                searchText = e.target.innerText;
            }

            for(let feature in this.tempFound) {
                let props = this.tempFound[feature].getProperties();
                if ('name' in props) {
                    if(props['name'] == searchText) {
                        coords = props['geometry'].flatCoordinates;
                        this.$emit('emit-selection', this.tempFound[feature], chooseTable.value);
                    }
                }
                else { //если искали помещения, у них нет имен
                    let stockID = props['type'] + " - " + props['address'];
                    if(stockID == searchText) {
                        coords = props['geometry'].flatCoordinates;
                        this.$emit('emit-selection', this.tempFound[feature], chooseTable.value);
                    }
                }
            }
            
            let new_zoom = global_map.getView().getZoom();
            if(new_zoom < 14) {
                new_zoom = 14;
            }

            global_map.getView().animate({
                center: coords,
                zoom: new_zoom,
                duration: 1000
            });
        }
    }
}
</script>

<style>
.openSidebarSearch {
    top: 4.7em;
    left: .5em;
    transition: 0.2s;
}

.sidebarSearch {
    border-right: 0 solid #6f6f6f;
    width: 0;
    height: 100%;
    position: fixed;
    z-index: 5000;
    top: 0;
    left: 0;
    overflow-x: hidden;
    padding-top: 40px;
    transition: 0.2s;
}

.closebtn {
    position: absolute;
    display: inline-block;  
    top: 15px;
    left: 20px;
    font-size: 22px;
    color: #343434;
    text-decoration: none;
    transition: 0.2s;
}

.closebtn:hover {
    transform: scale(1.25);
    color: black;
}

.closebtn:active {
    border: none;
}

.searchIcon {
    margin-top: 1px;
    margin-left: 2px;
    width: 20px;
    height: 20px;
}

.tab1 {
    top: 120px;
    z-index: 5001;
}

.tab_icon {
    width: 20px;
    height: 20px;
    margin-top: 10px;
}

.textWhere {
    display: inline-block;
    margin-right: 5px;
}

.searchContent {
    margin-left: 10px;
}

.searchButton {
    margin-top: 8px;
    margin-left: 185px;
}

#searchText {
    width: 260px;
}

.foundedHeader {
    text-align: center;
    margin: 5px 0;
}

.founded {
    overflow: auto;
    height: 26em;
    margin: 0 5px;
}

.founded ul {
    margin: 0;
    padding: 0;
}

.founded li {
    padding: 5px;
    margin: 5px;
    width: 268px;
    list-style-type: none; 
    cursor: pointer;
    transition: 0.15s;
    background: rgba(200,200,200,0.2);
}

.founded li:hover {
    background: rgb(230, 228, 228);
}

.founded li > a {
    display: block;
    text-decoration: none;
    text-align: center;
    color: #181818;
}

</style>