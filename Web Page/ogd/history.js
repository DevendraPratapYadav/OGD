var data_email_glob;

window.onload = function() {
    var parent_window = window.opener;
    data_email_glob = parent_window.data_email_glob;

    console.log("i am alive");

    generateUserHistoryView();
};

function findPositionElement(obj) {
    var currenttop = 0;
    if (obj.offsetParent) {
        do {
            currenttop += obj.offsetTop;
        } while (obj = obj.offsetParent);
    return [currenttop];
    }
}

//gets user data from python service
//TODO: implement http://localhost:5000/getUserData
//      input: json object which has userId
//      output: json object which is of type {"result":[datasetName, io, param, colNames]}
function getUserDataFromServer(){
    var userId = data_email_glob;
    var user = {"input":userId};
    var jqXHR_Data = $.ajax({
                    type: "POST",
                    url: "http://localhost:5000/getUserData",
                    data: JSON.stringify(user, null, '\t'),
                    async: false,
                    crossDomain: true,
                    contentType: 'application/json;charset=UTF-8',
                    success: function(data){
                        // console.log(data);
                    }
                });
    console.log(jqXHR_Data);
    return jqXHR_Data.responseJSON;
}

//makes and returns a new div element with some default styling
function getNewDivElement(){
    // margin: auto;width: 80%; padding: 5px;background-color:#eeeeee;"
    var div = document.createElement("div");
    div.style.width = "80%";
    div.style.margin = "auto";
    div.style.padding = "5px";
    div.style.backgroundColor = "#eeeeee";

    return div;
}

//generates a users history view
//TODO: implement http://localhost:5000/runMLComponentFromHistory
//      input: json object which has all user session data
//      output: json object which contains predictions and its visualization image link
function generateUserHistoryView(){
    var userData = JSON.parse(getUserDataFromServer())["result"];
    // console.log(userData);

    var parentDiv = getNewDivElement();
    parentDiv.style.backgroundColor = "#ffffff"

    for (var i = userData.length - 1; i >= 0; i--) {
        var view = JSON.parse(userData[i][3]);
        console.log(view);

        var datasetName = view[1];
        var selectionInput = view[2][0];
        var selectionOutput = view[2][1];   
        var inputParam = view[3][0].toString();
        var colNames = getColumnNamesFromUserData(view[4]);

        var para = document.createElement("p");
        para.innerHTML = "<pre><b>Dataset Name</b>       "+datasetName.toString()+"<br>";
        para.innerHTML += "<pre><b>Input Columns</b>     "+getColNames(selectionInput,colNames)+"<br>";
        para.innerHTML += "<pre><b>Output Columns</b>     "+ getColNames(selectionOutput,colNames)+"<br>";
        para.innerHTML += "<pre><b>Input Parameters</b>   "+ inputParam.toString()+"</per>";

        // hpara.style.float = "left";

        // para.innerHTML += colNames.toString()+"<br>";

        console.log(para.innerHTML);

        var button = document.createElement("input");
        button.setAttribute("type", "button");
        button.setAttribute("value", "View");
        button.onclick = (function(arg,ioSelection,colNames){

            return function(){

                window.scroll(0,findPositionElement(document.getElementById("visualizationImage")));
                // document.body.scrollTop = document.body.scrollHeight;

                var jqXHR_Data = $.ajax({
                    type: "POST",
                    url: "http://localhost:5000/runMLComponentFromHistory",
                    data: JSON.stringify(arg, null, '\t'),
                    async: false,
                    crossDomain: true,
                    contentType: 'application/json;charset=UTF-8',
                    success: function(data){
                        //implement display functions
                    }
                });

                pyData = jqXHR_Data.responseJSON;

                console.log("shit before");

                var img_url = "/ogd/visual.jpg";
                console.log(img_url);
                // console.log(data);
                document.getElementById("visualizationImage").src = img_url+'?random='+new Date().getTime();
                populateResult(pyData.result,ioSelection,colNames);
            }


        })({"input":userData[i]},view[2],colNames);

        var div = getNewDivElement();
        div.appendChild(para);
        // div.appendChild(hpara);
        div.appendChild(button);

        parentDiv.appendChild(div);
        parentDiv.appendChild(document.createElement("br"));
    }

    console.log("hell");
    document.getElementById("history-content").appendChild(parentDiv);
}

function getColumnNamesFromUserData(data){
    names = [];
    for (var i = 0; i <data.length; i++) {
        names.push([data[i]["title"]]);
    }
    return names;
}

function getColNames(indices,names){
    nmstr = "";
    for (var i = 0; i < indices.length; i++) {
        nmstr += names[indices[i]]+",    "
    }
    return nmstr;
}

function populateResult(result,ioSelection,colNames){
    var i=0;
    var j=0;

    row_data = [];

    for(i=0;i<result.length;i++){
        row_ar = [];
        for (j=0;j<result[i].length;j++){
            if(result[i][j] == ','){

            }
            else {
                row_ar.push(result[i][j]);
            }
        }
        row_data.push(row_ar);
    } 

    col_data = [];

    for(i=0;i<ioSelection[0].length;i++){
        var temp = ioSelection[0][i];
        col_data.push(colNames[temp]);
    }

    for(i=0;i<ioSelection[1].length;i++){
        var temp = ioSelection[i];
        col_data.push(colNames[temp]);
    }

    console.log("******   Row_data Col_data  ******");
    // console.log(data_col_select_glob);
    // console.log(data_col_names_glob);
    console.log(row_data);
    console.log(col_data);

    generateResultTable(row_data,col_data);
}

function generateResultTable(row_data,col_data){
    document.getElementById("contain-result-table").innerHTML = '<div style="background-color: #FFFFFF;border-color: #000000;padding: 20px;border-radius: 13px;box-shadow: 0px 0px 15px #888888;"><table id="resultDataTable" class="display" style="min-width: 100%"></table></div>';

    console.log(row_data);
    console.log(col_data);

    var table = $('#resultDataTable').DataTable({
        data: row_data,
        columns: col_data,
        "scrollX": true
    });
    console.log("complete data");
    console.log(table.rows().data().toArray());

    var i=0;
    var j=0;
    arobj = [];
    for(i=0;i<row_data.length;i++){
        temp = {};
        for(j=0;j<col_data.length;j++){
            arobj[col_data[j]] = row_data[i][j];
        }
    }
    console.log(arobj);
}