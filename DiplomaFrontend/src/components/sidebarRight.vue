<template>
    <div id="sidebarRight" class="sidebarRight sideCol">
        <a href="javascript:void(0)" class="closebtn textCol" @click="closeMenu">&times;</a>
        <p class="themeSwitch_text textCol">Темная тема</p>
        <label class="themeSwitch">
            <input id='themeButton' type="checkbox">
            <span class="themeSlider"></span>
        </label>
        <div class="layersChoose">
            <label class="layerContainer textCol">Учреждения
                <input type="checkbox" checked id="check_foundation">
                <span class="checkmark"></span>
            </label>
            <input 
                class="color-check" 
                id="founds_color" 
                type="color"
                value="#201dcf"
            >
            <label class="layerContainer textCol">Предприятия
                <input type="checkbox" checked id="check_company">
                <span class="checkmark"></span>
            </label>
            <input 
                class="color-check" 
                id="companies_color" 
                type="color"
                value="#02e15f"
            >
            <label class="layerContainer textCol">Помещения
                <input type="checkbox" checked id="check_stock">
                <span class="checkmark"></span>
            </label>
            <input 
                class="color-check" 
                id="stocks_color" 
                type="color"
                value="#020202"
            >
            <label class="layerContainer textCol">Муниципальные земли
                <input type="checkbox" checked id="check_munland">
                <span class="checkmark"></span>
            </label>
            <input 
                class="color-check"
                id="munland_color" 
                type="color"
                value="#C10900"
            >
        </div>
       <!-- <input type="button" class="textCol labelCol" value="экспорт" @click="pngExport">
        <a id="image-download" download="map.png"></a>-->
    </div>
</template>

<script>
//файл менюшки справа, которая отвечает за управление слоями
import { global_map } from '../api/global';
import Map from 'ol/Map';
import {Control} from 'ol/control';

export default {
    data() {
        return {
            menuColor: null,
        }
    },
    mounted() {
        this.$nextTick(() => {
            let darking = localStorage.getItem("dark-theme");
            if(darking != "false") {
                this.$emit("switch-theme");
                themeButton.checked = true;
            }

            this.initControls(global_map);
        });

        check_foundation.onclick = () => {
            this.$emit('hide-layer', check_foundation.checked, "foundation");
        };
        check_company.onclick = () => {
            this.$emit('hide-layer', check_company.checked, "company");
        };
        check_stock.onclick = () => {
            this.$emit('hide-layer', check_stock.checked, "housingstock");
        };
        check_munland.onclick = () => {
            this.$emit('hide-layer', check_munland.checked, "munitipalland");
        };

        founds_color.onchange = () => {
            this.$emit('change-color', founds_color.value, "foundation");
            this.saveColor("foundsColor", founds_color.value);
        }
        companies_color.onchange = () => {
            this.$emit('change-color', companies_color.value, "company");
            this.saveColor("companiesColor", companies_color.value);
        }
        stocks_color.onchange = () => {
            this.$emit('change-color', stocks_color.value, "housingstock");
            this.saveColor("stocksColor", stocks_color.value);
        }
        munland_color.onchange = () => {
            this.$emit('change-color', munland_color.value, "munitipalland");
            this.saveColor("munlandsColor", munland_color.value);
        }

        this.loadColors();
    },
    computed: {
        checkLocalStorage: function() {
            try {
                return 'localStorage' in window && window['localStorage'] !== null;
            } catch (e) {
                return false;
            }
        },
    },
    methods: {
        //открываем менюшку справа
        openMenu() {
            sidebarRight.style.borderLeftWidth = "1px";
            sidebarRight.style.width = "260px";
        },

        //закрываем менюшку справа
        closeMenu() {
            sidebarRight.style.borderLeftWidth = "0";
            sidebarRight.style.width = "0";
        },

        initControls(map) {
            //добавляем кнопку для включения менюшки слоев
            var button = document.createElement('button');
            button.title="открыть меню опций";
            button.style = "padding-top: 5px;";
            button.innerHTML = '⚙️';
            button.addEventListener('click', this.openMenu, false);

            var element = document.createElement('div');
            element.className = 'openSidebarRight ol-unselectable ol-control';
            element.appendChild(button);

            var myControl = new Control({element: element});

            map.addControl(myControl);

            themeButton.onclick = (e) => {
                this.$emit("switch-theme");
            }
        },

        saveColor(layer, color) {
            if(this.checkLocalStorage) { 
                localStorage.setItem(layer, color);
            }
        },

        loadColors() {
            if(this.checkLocalStorage) {
                var foundsColor = localStorage.getItem("foundsColor");
                var companiesColor = localStorage.getItem("companiesColor");
                var stocksColor = localStorage.getItem("stocksColor");
                var munlandsColor = localStorage.getItem("munlandsColor");

                if(foundsColor) {
                    founds_color.value = foundsColor;
                    founds_color.onchange();
                }
                if(companiesColor) {
                    companies_color.value = companiesColor;
                    companies_color.onchange();
                }
                if(stocksColor) {
                    stocks_color.value = stocksColor;
                    stocks_color.onchange();
                }
                if(munlandsColor) {
                    munland_color.value = munlandsColor;
                    munland_color.onchange();
                }
            }
        },

        // pngExport() {
        //     global_map.once('rendercomplete', function() {
        //         var mapCanvas = document.createElement('canvas');
        //         var size = global_map.getSize();
        //         mapCanvas.width = size[0];
        //         mapCanvas.height = size[1];
        //         var mapContext = mapCanvas.getContext('2d');
        //         Array.prototype.forEach.call(document.querySelectorAll('.ol-layer canvas'), function(canvas) {
        //         if (canvas.width > 0) {
        //             var opacity = canvas.parentNode.style.opacity;
        //             mapContext.globalAlpha = opacity === '' ? 1 : Number(opacity);
        //             var transform = canvas.style.transform;
        //             // Get the transform parameters from the style's transform matrix
        //             var matrix = transform.match(/^matrix\(([^\(]*)\)$/)[1].split(',').map(Number);
        //             // Apply the transform to the export map context
        //             CanvasRenderingContext2D.prototype.setTransform.apply(mapContext, matrix);
        //             mapContext.drawImage(canvas, 0, 0);
        //         }
        //         });
        //         if (navigator.msSaveBlob) {
        //             // link download attribuute does not work on MS browsers
        //             navigator.msSaveBlob(mapCanvas.msToBlob(), 'map.png');
        //         } else {
        //             var link = document.getElementById('image-download');
        //             link.href = mapCanvas.toDataURL();
        //             link.click();
        //         }
        //     });
        //     global_map.renderSync();
        // }
    }
}
</script>

<style>
.sidebarRight {
    border-left: 0 solid #6f6f6f;
    width: 0;
    height: 100%;
    position: fixed;
    z-index: 5000;
    top: 0;
    right: 0;
    overflow-x: hidden;
    padding-top: 40px;
    transition: 0.2s;
}

.sidebarRight .closebtn {
    position: absolute;
    display: inline-block;  
    top: 15px;
    right: 20px;
    left: 227px;
    font-size: 22px;
    text-decoration: none;
    transition: 0.2s;
}

.sidebarRight .closebtn:hover {
    transform: scale(1.25);
    color: black;
}

.sidebarRight .closebtn:active {
    border: none;
}

.layerContainer {
    text-decoration: none;
    display: inline-block;
    position: relative;
    padding-left: 35px;
    margin-bottom: 5px;
    cursor: pointer;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}

.layersChoose {
    margin-top: 30px;
}

.color-check {
    display: inline-block;
    border: none;
    width: 26px;
    height: 26px;
    margin-top: 12px;
    margin-left: 5px;
    background-color: rgba(1,1,1,0);
}

.color-check:hover {
    border: none;
}

.layerContainer input {
    position: absolute;
    opacity: 0;
    cursor: pointer;
    height: 0;
    width: 0;
    left: 0;
}

.checkmark {
    position: absolute;
    top: 0;
    left: 10px;
    height: 18px;
    width: 18px;
    background-color: #343434;
}

.checkmark:after {
    content: "";
    position: absolute;
    display: none;
}

.layerContainer input:checked ~ .checkmark:after {
    display: block;
}

.layerContainer .checkmark:after {
    left: 5px;
    top: 2px;
    width: 5px;
    height: 10px;
    border: solid white;
    border-width: 0 3px 3px 0;
    -webkit-transform: rotate(45deg);
    -ms-transform: rotate(45deg);
    transform: rotate(45deg);
}

.openSidebarRight {
    top: 1em;
    right: .7em;
}

.themeSwitch {
    position: relative;
    display: inline-block;
    width: 30px;
    height: 17px;
    top: 5px;
}

.themeSwitch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.themeSlider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    -webkit-transition: .4s;
    transition: .4s;
    border-radius: 17px;
}

.themeSlider:before {
    position: absolute;
    content: "";
    height: 13px;
    width: 13px;
    left: 2px;
    bottom: 2px;
    background-color: white;
    -webkit-transition: .4s;
    transition: .4s;
    border-radius: 50%;
}

input:checked + .themeSlider {
    background-color: #2196F3;
}

input:focus + .themeSlider {
    box-shadow: 0 0 1px #2196F3;
}

input:checked + .themeSlider:before {
    -webkit-transform: translateX(13px);
    -ms-transform: translateX(13px);
    transform: translateX(13px);
}

.themeSwitch_text {
    display: inline-block;
    margin: 0 5px 0 100px;
}
</style>