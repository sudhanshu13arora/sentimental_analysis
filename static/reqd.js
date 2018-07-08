/**
 * Created by Dell on 28-04-2018.
 */
function require() {
    console.log("called");
    var empt = document.forms["login_form"]["username"].value;
    var empt2 = document.forms["login_form"]["password"].value;
    if (empt === "" && empt2 === "") {
        alert("Please input a value");
        return false;
    }
    else if(empt === ""){
        alert("Please enter the username");
        return false;
    }
    else if(empt2 === ""){
        alert("Please enter the password");
        return false;
    }
    else {
        return true;
    }

}

function atLeastOneRadio() {
    console.log("radio called");
    var radios = document.getElementsByTagName('input');
    var value;
    var flag = 0;
    for (var i = 0; i < radios.length; i++) {
        if (radios[i].type === 'radio' && radios[i].checked) {
            // get value, set checked flag or do whatever you need to
            value = radios[i].value;
            flag = 1;
            return true;
        }

    }
    if (flag === 0) {
        alert("Please give a rating");
        return false;
    }

}