var HEADER1 = [];
var HEADER2 = [];

async function header_file_1(){
    headers = await eel.get_file_1()();
    document.getElementById("choosen_file_1").innerHTML = headers[0]
    HEADER1 = headers
}

async function header_file_2(){
    headers = await eel.get_file_2()();
    document.getElementById("choosen_file_2").innerHTML = headers[0]
    HEADER2 = headers
}

function showamount1(newAmount){
    document.getElementById('amount1').innerHTML = newAmount
}

function create_column_list(){
    //File1
    s = '<select class="form-select" id="choose_fuzzy_col_1"><option selected>Select Fuzzy Column from File1</option>'
    for(var i=1; i<HEADER1.length; i++){
        s = s + `<option value="${HEADER1[i]}">${HEADER1[i]}</option>`
    }
    s = s + '</select>'
    document.getElementById("selected_file_1").innerHTML = s

    //File2
    s = '<select class="form-select" id="choose_fuzzy_col_2"><option selected>Select Fuzzy Column from File2</option>'
    for(var i=1; i<HEADER2.length; i++){
        s = s + `<option value="${HEADER2[i]}">${HEADER2[i]}</option>`
    }
    s = s + '</select>'
    document.getElementById("selected_file_2").innerHTML = s

    //Slider
    document.getElementById("slider").innerHTML = `<label for="slider"><b>Range Slider:</b></label>  
    <div class="slidecontainer">
    <input type="range" id="range" min=25 max=99 value=80 class="slider" oninput="showamount1(this.value)">
    <label><p>Value:<span id="amount1">80</span></p></label>`

    //Submit Button
    document.getElementById("submit").innerHTML = '<button type="button" class="btn btn-secondary" onclick="run_fuzzy()">Run Fuzzy</button>'
}

async function run_fuzzy(){
    document.getElementById("indicator").innerHTML = "Fuzzy Started";
    fuzzy_col_from_file_1  = document.getElementById("choose_fuzzy_col_1").value;
    fuzzy_col_from_file_2  = document.getElementById("choose_fuzzy_col_2").value;
    range = document.getElementById("range").value;

    if (fuzzy_col_from_file_1 == "Select Fuzzy Column from File1"){
        alert("Please Select Valid Column from File1 to perform fuzzy");
        return false;
    }

    if (fuzzy_col_from_file_2 == "Select Fuzzy Column from File2"){
        alert("Please Select Valid Column from File2 to perform fuzzy");
        return false;
    }

    R = await eel.perform_fuzzy(fuzzy_col_from_file_1, fuzzy_col_from_file_2, range)(()=>{
        document.getElementById("indicator").innerHTML = "Fuzzy Completed";
    });
};