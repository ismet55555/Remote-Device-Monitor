// Create a XMLHttpRequest object to handle REST calls
// TODO: Switch to fetch API
let request = new XMLHttpRequest();  


///////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////

// Clear the UI 
clear_ui()

// Update the UI 
update_ui()

// Start the Update UI timer
start_polling_status()

///////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////


function http_request_helper(method, ip, port, endpoint, args_dict){
    ////////////////////////////////////////////////
    // Usage:
    //      GET
    //          let time = http_request_helper('GET', picell_ip, '5000', 'get_time')
    //      POST
    //          let response = http_request_helper('POST', null, '', apc_on_off, {'fixture_euid':fixture_euid_selected})
    ////////////////////////////////////////////////

    // Adding any passed arguments in key:value dict format
    argText = ''
    if (args_dict != null){
        argText += '?'
        for(let key in args_dict){
            let value = args_dict[key]
            argText = argText + key + '=' + value + '&'
        }
    }
    argText = argText.substring(0, argText.length - 1);

    // Forming the request
    if (ip != null){
        // Sending request to remote location (picell)
        request_url = 'http://' + ip + ':' + port + '/' + endpoint + argText
    } else {
        // Sending request to local flask server
        request_url = endpoint + argText
    }
    console.log('Sending Request: ' + request_url)

    // Sending the request
    try {
        request.open(method.toUpperCase(), request_url, false);
        request.setRequestHeader('Access-Control-Allow-Origin', '*')
        request.send();
        return request.responseText;
    } catch(error) {
        console.warn("ERROR: Failed to send request. Response: " + error)
        return null;
    }
    
}


///////////////////////////////////////////////////////////////////////////////////////////////////


function start_monitor() {
    console.log('Starting monitor')
    let response = http_request_helper('POST', null, '7777', 'start_monitor_scan')
}

function stop_monitor() {
    console.log('Starting monitor')
    let response = http_request_helper('POST', null, '7777', 'stop_monitor_scan')
}

///////////////////////////////////////////////////////////////////////////////////////////////////

function clear_ui() {
    console.log("CLEARING UI")

    document.getElementById("ip").innerText = '-';
    document.getElementById("port").innerText = '-';
    document.getElementById("online-status").innerText = '-';
    document.getElementById("date").innerText = '-';
    document.getElementById("time").innerText = '-';
    document.getElementById("slack-channel").innerText = '-';
    // document.getElementById("email-addresses").innerText = '-';
}



function start_polling_status() {
    // If clear_and_update_ui is already doing, stop doing it
    if ((typeof update_ui_timer !== 'undefined')) {
        clearInterval(update_ui_timer);  
    }
    // Start status data polling timer at regular integral
    update_ui_timer = setInterval(function() { update_ui() }, 3000);
}
function stop_polling_status() {
    // Stop any status data polling
    clearInterval(doing_stuff_timer);
}
function update_ui() {
    // Clear and update the UI
    let response = http_request_helper('GET', null, '7777', 'tc_status')

    success = (response != null) ? JSON.parse(response)['success'] : false;
    if (success) {
        document.getElementById("name").innerText = JSON.parse(response)['status']['name'];

        document.getElementById("ip").innerText = JSON.parse(response)['status']['ip_address'];
        document.getElementById("port").innerText = JSON.parse(response)['status']['port'];

        let status_text = 'Currently Unknown'
        if (JSON.parse(response)['status']['status'] == 0) {
            status_text = 'ONLINE'
        } else {
            status_text = 'OFFLINE'
        }
        document.getElementById("online-status").innerText = status_text;

        document.getElementById("date").innerText = JSON.parse(response)['status']['date'];
        document.getElementById("time").innerText = JSON.parse(response)['status']['time'];
        document.getElementById("slack-channel").innerText = JSON.parse(response)['status']['slack_channel'];
        // document.getElementById("email-addresses").innerText = JSON.parse(response)['status']['email_addresses'];
    } else {
        clear_ui()
    }
}


///////////////////////////////////////////////////////////////////////////////////////////////////

// Setting Inner texts of element
// document.getElementById("picell-name").innerText = '-';

//////////////////////////////////////////////////////////////////

// Disabling element
// document.getElementById("btn-reboot-picell").disabled = true;

//////////////////////////////////////////////////////////////////

// Removing all listed in a select menu
// let fixture_power_select = document.getElementById("picell-power-fixture");
// let length = fixture_power_select.options.length;
// for (i = 0; i < length; i++) {
//     fixture_power_select.options[i] = null;
// }
// let length = fixture_power_select.options.length = 0;
// fixture_power_select.disabled = true;  // Disabling select

//////////////////////////////////////////////////////////////////

// Populating a select menu
// for(let i in fixture_sm_firmware){
//     if (!(isNaN(fixture_sm_firmware[i][0]))) {  // Omit any falsh binary that does not start with a number
//         let flash_version_option = document.createElement("option");  // Creating a select option
//         flash_version_option.text = fixture_sm_firmware[i];  // Adding the fixture name to the option
//         flash_version_select.add(flash_version_option);  // Adding the option to the select
//     }
// }
// flash_version_select.disabled = false

//////////////////////////////////////////////////////////////////

// Do something on the expension of a accordian panel
// $('#accordion3').on('show.bs.collapse', function () {
//     // When accordion panel expands do stuff ...
// });

//////////////////////////////////////////////////////////////////

// Do something at a regular interval
// function start_doing_stuff() {
//     // If doing_stuff is already doing, stop doing it
//     if ((typeof doing_stuff_timer !== 'undefined')) {
//         clearInterval(doing_stuff_timer);  
//     }
//     // Start data acquisition timer at regular integral
//     doing_stuff_timer = setInterval(function() { doing_stuff() }, 500);
// }
// function stop_doing_stuff() {
//     // Stopping PyBoard dim value data acquisition
//     clearInterval(doing_stuff_timer);
// }
// function doing_stuff() {
//     // do stuff here
// }

//////////////////////////////////////////////////////////////////

// // Showing  modal, then do something after it appears
// let apc_on_off_text = (apc_on_off == 'apc_on') ? 'up' : 'down'
// document.getElementById('modalLoader-text').innerText = '<Modal Message Here>'
// $('#modalLoader').modal('show');

// // After loading modal has appeared, proceed to send request
// $('#modalLoader').on('shown.bs.modal', async function (e) {
//     let success = false
//     // Define the function
//     async function do_something(){
//         // Do something here
//         // success = ?
//     };

//     // Execute the function
//     await do_something();

//     // Hiding loading modal after execution
//     setTimeout(function () { 
//         $('#modalLoader').modal('hide');
//     }, 2000);

//     // Show a warning modal if request has failed
//     $('#modalLoader').on('hide.bs.modal', async function (e) {
//         if (success == false){
//             document.getElementById('modalWarning-text').innerText = '<Error Message Here>'
//             $('#modalWarning').modal('show');
//         }
//     })
// })