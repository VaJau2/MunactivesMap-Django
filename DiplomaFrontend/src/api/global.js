var global_map = null;

var set_global_map = function(new_map) {
    global_map = new_map;
    console.log("set new global map");
}

export {global_map, set_global_map};