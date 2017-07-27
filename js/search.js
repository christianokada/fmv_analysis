function filter_results() {
    var input = document.getElementById("input");
    var query = input.value.toUpperCase();
    var div = document.getElementById("fh5co-main");
    var list = div.getElementsByTagName('a');

    // get list of frame filenames in images.json
    $.getJSON('images.json', function(data) {
        for (i = 0; i < list.length; i++) {
            var contains;
            // get frame[i] and compare tags with input query
            $.getJSON('data/' + parse_json(data[i], ".json"), function(json_data) {
                element = parse_json(json_data.frame, "");
                // console.log("init = " + i, element)
                contains = false;
                tags = json_data.description.tags;
                for (j = 0; j < tags.length; j++) {
                    if(tags[j].toUpperCase().includes(query)) {
                        contains = true;
                        break;
                    }
                }
            }).then(function() {
                // console.log("post = " + element + i)
                // make hidden or visible if bool is false
                if (contains == false && query != "") {
                    console.log(element + " hidden")
                    document.getElementById(element).setAttribute('style', 'display:none');
                    // document.getElementById(element).setAttribute('style','visibility:hidden');
                }
                else {
                    console.log(element + " visibile")
                    document.getElementById(element).setAttribute('style', 'display:block');
                    // document.getElementById(element).setAttribute('style','visibility:visible');
                }
            });
        }
    });
}

function parse_json(text, ext) {
    var str = text.split(".");
    return str[0] + ext;
}
