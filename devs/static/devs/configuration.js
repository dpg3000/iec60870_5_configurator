$(document).ready(function(){
    var device_list = [];
    var lastDeviceName;

    jQuery('#add-center-btn').click(function() {
        var num = jQuery('.repeat-center').length;
        var newNum = new Number(num + 1);
        var previousDom = jQuery('#repeat-center-' + num);
        var newElem = jQuery('#repeat-center-' + num).clone().attr('id', 'repeat-center-' + newNum);                    // cloning the previous element
        var numOfInputCards = newElem.children('#center').children('.enable-input-cards-section').children('.repeat-'+
        'input-card').length;
        var numOfOutputCards = newElem.children('#center').children('.enable-output-cards-section').children('.repeat-'+
        'output-card').length;
        var numOfDevices = newElem.children('#center').children('.enable-devices-section').children('.repeat-'+
        'device').length;

        /*PREVIOUS CENTER*/
        previousDom.children('#center').children('#table-cards').children('#body-cards').children('#row-'+              // disabling the "enable cards" checkbox
        'cards').children('#cell-cards').children('.enable-cards').prop("disabled", true);

        previousDom.children('#center').children('.enable-cards-section').children('#table-input-'+                     // disabling the "enable input cards" checkbox
        'cards').children('#body-input-cards').children('#row-input-cards').children('#cell-input-'+
        'cards').children('.enable-input-cards').prop("disabled", true);

        previousDom.children('#center').children('.enable-cards-section').children('#table-output-'+                    // disabling the "enable output cards" checkbox
        'cards').children('#body-output-cards').children('#row-output-cards').children('#cell-output-'+
        'cards').children('.enable-output-cards').prop("disabled", true);

        previousDom.children('#center').children('#table-devices').children('#body-devices').children('#row-'+          // disabling the "enable devices" checkbox
        'devices').children('#cell-devices').children('.enable-devices').prop("disabled", true);

        previousDom.children('#center').css("background", "url(../static/admin/img/icon-yes.svg) 100px 11px no-repeat");// Adding "validated" icon

        $(this).attr('disabled', true);                                                                                 // disabling the "add center" button

        $('#generate').attr('disabled', true);                                                                          // disabling "generate" button

        /*NEW CENTER*/
        newElem.children('#center').children('#table-center').children('#body-center').children('#row-'+                // cleaning center name
        'center').children('#cell-center-name').children('#center-name').val("");

        newElem.children('#center').children('#table-cards').children('#body-cards').children('#row-'+                  // Unchecking the "enable cards" checkbox
        'cards').children('#cell-cards').children('.enable-cards').prop("checked", false);

        newElem.children('#center').children('.enable-cards-section').children('#table-input-'+                         // Unchecking the "enable input card" checkbox
        'cards').children('#body-input-cards').children('#row-input-cards').children('#cell-input-'+
        'cards').children('.enable-input-cards').prop("checked", false);

        newElem.children('#center').children('.enable-cards-section').children('#table-output-'+                        // Unchecking the "enable output card" checkbox
        'cards').children('#body-output-cards').children('#row-output-cards').children('#cell-output-'+
        'cards').children('.enable-output-cards').prop("checked", false);

        for (i = numOfInputCards; i > 1; i--) {                                                                         // Removing all input cards but the first
            newElem.children('#center').children('.enable-cards-section').children('.enable-input-cards-'+
            'section').children('#repeat-input-card-' + i).remove();
        }

        for (i = numOfOutputCards; i > 1; i--) {                                                                        // Removing all output cards but the first
            newElem.children('#center').children('.enable-cards-section').children('.enable-output-cards-'+
            'section').children('#repeat-output-card-' + i).remove();
        }

        newElem.children('#center').children('.enable-cards-section').children('.enable-input-cards-section').hide();   //hide the input card configurator dialog
        newElem.children('#center').children('.enable-cards-section').children('.enable-output-cards-section').hide();  //hide the output card configurator dialog
        newElem.children('#center').children('.enable-cards-section').hide();                                           //hide the card configurator dialog

        newElem.children('#center').children('.enable-cards-section').children('.enable-input-cards-'+                  //Enable the selector of the input card left in the last loop
        'section').children('#repeat-input-card-1').children('.selector-input-card').attr('disabled', false);
        newElem.children('#center').children('.enable-cards-section').children('.enable-output-cards-'+                 //Enable the selector of the output card left in the last loop
        'section').children('#repeat-output-card-1').children('.selector-input-card').attr('disabled', false);

        newElem.children('#center').children('.enable-cards-section').children('.enable-input-cards-'+                  //Initialize the number of input cards
        'section').children('#repeat-input-card-1').children('.selector-num-input-card').val(1);
        newElem.children('#center').children('.enable-cards-section').children('.enable-output-cards-'+                 //Initialize the number of output cards
        'section').children('#repeat-output-card-1').children('.selector-num-output-card').val(1);

        newElem.children('#center').children('.enable-cards-section').children('.enable-input-cards-'+                  //Enable add input card button
        'section').children('#add-input-card-btn').attr('disabled', false);
        newElem.children('#center').children('.enable-cards-section').children('.enable-output-cards-'+                 //Enable add output card button
        'section').children('#add-output-card-btn').attr('disabled', false);

        newElem.children('#center').children('.enable-cards-section').children('.enable-input-cards-'+                  //Disable remove input card button
        'section').children('#remove-input-card-btn').attr('disabled', true);
        newElem.children('#center').children('.enable-cards-section').children('.enable-output-cards-'+                 //Disable remove output card button
        'section').children('#remove-output-card-btn').attr('disabled', true);

        /*Cleaning devices*/
        newElem.children('#center').children('#table-devices').children('#body-devices').children('#row-'+              //Uncheck the add device checkbox
        'devices').children('#cell-devices').children('.enable-devices').prop("checked", false);

        newElem.children('#center').children('.enable-devices-section').hide();                                         //hide the device configurator dialog

        for (i = numOfDevices; i > 1; i--) {                                                                            //Remove any devices but first
            newElem.children('#center').children('.enable-devices-section').children('#repeat-device-' + i).remove();
        }

        newElem.children('#center').children('.enable-devices-section').children('#repeat-'+                            //Enable the selector of the device left in the last loop
        'device-1').children('.selector-device').attr('disabled', false);

        newElem.children('#center').children('.enable-devices-section').children('#repeat-'+                            //Initialize the number of devices
        'device-1').children('.selector-num-device').val(1);

        newElem.children('#center').children('.enable-devices-section').children('#add-device-'+                        //Enable add device button
        'btn').attr('disabled', false);

        newElem.children('#center').children('.enable-devices-section').children('#remove-devices-'+                    //Disable remove device button
        'btn').attr('disabled', true);

        previousDom.after(newElem);                                                                                     // Adding the new element after the previous
        jQuery('#remove-center-btn').attr('disabled', false);                                                           // Enabling 'remove center' possibility
    });

    jQuery('#remove-center-btn').click(function() {
        var num = jQuery('.repeat-center').length;
        var newNum = new Number(num - 1);
        var actualDom = jQuery('#repeat-center-' + newNum);

        actualDom.children('#center').css("background", "");

        actualDom.children('#center').children('#table-cards').children('#body-cards').children('#row-'+                // enable the add card checkbox
        'cards').children('#cell-cards').children('.enable-cards').prop("disabled", false);

        actualDom.children('#center').children('.enable-cards-section').children('#table-input-'+                       // enable the add input card checkbox
        'cards').children('#body-input-cards').children('#row-input-cards').children('#cell-input-'+
        'cards').children('.enable-input-cards').prop("disabled", false);

        actualDom.children('#center').children('.enable-cards-section').children('#table-output-'+                      // enable the add output card checkbox
        'cards').children('#body-output-cards').children('#row-output-cards').children('#cell-output-'+
        'cards').children('.enable-output-cards').prop("disabled", false);

        actualDom.children('#center').children('#table-devices').children('#body-devices').children('#row-'+            // enable the add device checkbox
        'devices').children('#cell-devices').children('.enable-devices').prop("disabled", false);

        if(actualDom.children('#center').children('.enable-cards-section').children('#table-input-'+                    // logic to control ADD CENTER and GENERATE
        'cards').children('#body-input-cards').children('#row-input-cards').children('#cell-input-'+
        'cards').children('.enable-input-cards').prop('checked') || actualDom.children('#center').children('.enable-'+
        'cards-section').children('#table-output-cards').children('#body-output-cards').children('#row-output-'+
        'cards').children('#cell-output-cards').children('.enable-output-'+
        'cards').prop('checked') || actualDom.children('#center').children('#table-devices').children('#body-'+
        'devices').children('#row-devices').children('#cell-devices').children('.enable-devices').prop('checked')) {
            $('#add-center-btn').attr('disabled', false);
            $('#generate').attr('disabled', false);
        } else {
            $('#add-center-btn').attr('disabled', true);
            $('#generate').attr('disabled', true);
        }

        jQuery('#repeat-center-' + num).remove();                                                                       // Removing the last element

        if (newNum == 1) {
            jQuery('#remove-center-btn').attr('disabled', true);                                                        // Last element can not be removed
        }
    });

    $(document).on('click', '.enable-cards', function() {                                                               // Hide or show card section based on checkbox
        if(this.checked) {
            $(this).parent().parent().parent().parent().siblings('.enable-cards-section').show();
        } else {
            $(this).parent().parent().parent().parent().siblings('.enable-cards-section').hide();
        }
    });

    $(document).on('click', '.enable-input-cards', function() {                                                         // Hide or show input card section based on checkbox
        if(this.checked) {
            $(this).parent().parent().parent().parent().siblings('.enable-input-cards-section').show();
        } else {
            $(this).parent().parent().parent().parent().siblings('.enable-input-cards-section').hide();
        }
    });

    $(document).on('click', '.enable-output-cards', function() {                                                         // Hide or show output card section based on checkbox
        if(this.checked) {
            $(this).parent().parent().parent().parent().siblings('.enable-output-cards-section').show();
        } else {
            $(this).parent().parent().parent().parent().siblings('.enable-output-cards-section').hide();
        }
    });

    $(document).on('click', '.enable-devices', function() {
        var deviceName = $(this).parent().parent().parent().parent().siblings('.enable-devices-'+
        'section').children('#repeat-device-1').children('.selector-device').val();
        var root = $(this).parent().parent().parent().parent().siblings('.enable-devices-section').children('#repeat-'+
        'device-1')

        if (this.checked) {
            $('#device-list').show();
            ajax_processing(deviceName, root);
            console.log(device_list);
            $(this).parent().parent().parent().parent().siblings('.enable-devices-section').show();
            $('#add-center-btn').attr('disabled', false);
            $('#generate').attr('disabled', false);
        } else {
            $('#device-list').hide();
            $(this).parent().parent().parent().parent().siblings('.enable-devices-section').hide();
            $('#add-center-btn').attr('disabled', true);
            $('#generate').attr('disabled', true);
        }

        if($(this).parent().parent().parent().parent().siblings('#table-cards').children('#body-'+
        'cards').children('#row-cards').children('#cell-cards').children('.enable-cards').prop('checked')) {

            if($(this).parent().parent().parent().parent().siblings('.enable-cards-section').children('#table-input-'+
            'cards').children('#body-input-cards').children('#row-input-cards').children('#cell-input-'+
            'cards').children('.enable-input-cards').prop('checked')) {
                $('#add-center-btn').attr('disabled', false);
                $('#generate').attr('disabled', false);
            }

            if($(this).parent().parent().parent().parent().siblings('.enable-cards-section').children('#table-output-'+
            'cards').children('#body-output-cards').children('#row-output-cards').children('#cell-output-'+
            'cards').children('.enable-output-cards').prop('checked')) {
                $('#add-center-btn').attr('disabled', false);
                $('#generate').attr('disabled', false);
            }
        }
    });

    $(document).on('click', '#add-input-card-server', function() {
        if($(this).prop('checked') == false) {
            $(this).siblings('#add-input-card-io').prop('checked', true)
        }
    });

    $(document).on('click', '#add-output-card-server', function() {
        if($(this).prop('checked') == false) {
            $(this).siblings('#add-output-card-io').prop('checked', true)
        }
    });

    $(document).on('click', '#add-input-card-io', function() {
        if($(this).prop('checked') == false) {
            $(this).siblings('#add-input-card-server').prop('checked', true)
        }
    });

    $(document).on('click', '#add-output-card-io', function() {
        if($(this).prop('checked') == false) {
            $(this).siblings('#add-output-card-server').prop('checked', true)
        }
    });

    $(document).on('click', '#add-device-server', function() {
        if($(this).prop('checked') == false) {
            $(this).siblings('#add-device-client').prop('checked', true)
        }
    });

    $(document).on('click', '#add-device-client', function() {
        if($(this).prop('checked') == false) {
            $(this).siblings('#add-device-server').prop('checked', true)
        }
    });

    $(document).on('click', '#add-input-card-btn', function() {
        var num = $(this).siblings('.repeat-input-card').length;
        var newNum = new Number(num + 1);
        var previousDom = $(this).siblings('#repeat-input-card-' + num);
        var newElem = $(this).siblings('#repeat-input-card-' + num).clone().attr('id', 'repeat-input-card-' + newNum);

        if (newNum >= $("#hidden-input-cards-num").val()) {
            $(this).attr('disabled', true);
        } else {
            newElem.children(".selector-input-card").children("option[value='"+ previousDom.children(".selector-input-"
            + "card").val() +"']").attr('disabled', true);

            newElem.children(".selector-input-card").children('option:not(:disabled)').each(function() {
                $(this).prop('selected', true);
            });

            newElem.children(".selector-num-input-card").val(1);

            newElem.children("#add-input-card-server").prop('checked', true);
            newElem.children("#add-input-card-io").prop('checked', true);

            previousDom.children(".selector-input-card").attr('disabled', true);

            previousDom.after(newElem);
            $(this).siblings('#remove-input-card-btn').attr('disabled', false);
        }
    });

    $(document).on('click', '#add-output-card-btn', function() {
        var num = $(this).siblings('.repeat-output-card').length;
        var newNum = new Number(num + 1);
        var previousDom = $(this).siblings('#repeat-output-card-' + num);
        var newElem = $(this).siblings('#repeat-output-card-' + num).clone().attr('id', 'repeat-output-card-' + newNum);

        if (newNum >= $("#hidden-output-cards-num").val()) {
            $(this).attr('disabled', true);
        } else {
            newElem.children(".selector-output-card").children("option[value='"+ previousDom.children(".selector-"+
            "output-card").val() +"']").attr('disabled', true);

            newElem.children(".selector-output-card").children('option:not(:disabled)').each(function() {
                $(this).prop('selected', true);
            });

            newElem.children(".selector-num-output-card").val(1);

            newElem.children("#add-output-card-server").prop('checked', true);
            newElem.children("#add-output-card-io").prop('checked', true);

            previousDom.children(".selector-output-card").attr('disabled', true);

            previousDom.after(newElem);
            $(this).siblings('#remove-output-card-btn').attr('disabled', false);
        }
    });

    $(document).on('click', '#remove-input-card-btn', function() {
        var num = $(this).siblings('.repeat-input-card').length;
        var newNum = new Number(num - 1);
        var previousDom = $(this).siblings('#repeat-input-card-' + newNum);
        var actualDom = $(this).siblings('#repeat-input-card-' + num);

        if (newNum == 1) {
            $(this).attr('disabled', true);                                                                             // if only one element remains, disable the remove button
        } else {
            actualDom.remove();                                                                                         // remove the last element
            $(this).siblings('#add-input-card-btn').attr('disabled', false);                                            // enable the "add" button
            previousDom.children(".selector-input-card").attr('disabled', false);                                       // enable input card selection
        }
    });

    $(document).on('click', '#remove-output-card-btn', function() {
        var num = $(this).siblings('.repeat-output-card').length;
        var newNum = new Number(num - 1);
        var previousDom = $(this).siblings('#repeat-output-card-' + newNum);
        var actualDom = $(this).siblings('#repeat-output-card-' + num);

        if (newNum == 1) {
            $(this).attr('disabled', true);                                                                             // if only one element remains, disable the remove button
        } else {
            actualDom.remove();                                                                                         // remove the last element
            $(this).siblings('#add-output-card-btn').attr('disabled', false);                                           // enable the "add" button
            previousDom.children(".selector-output-card").attr('disabled', false);                                      // enable output card selection
        }
    });

    $(document).on('focus', '.selector-device', function() {
        lastDeviceName = this.value;
    }).change(function() {
        lastDeviceName = this.value;
    });

    $(document).on('change', '.selector-device', function() {
        var deviceName = $(this).val()
        var root = $(this).parent()

        $("#device-list").children('#' + lastDeviceName).remove();
        const index = device_list.indexOf(lastDeviceName);
        if (index > -1) {
            device_list.splice(index, 1);
        }

        ajax_processing(deviceName, root);
        console.log(device_list);
    });

    $(document).on('click', '#add-device-btn', function() {
        var num = $(this).siblings('.repeat-device').length;
        var newNum = new Number(num + 1);
        var previousDom = $(this).siblings('#repeat-device-' + num);
        var newElem = $(this).siblings('#repeat-device-' + num).clone().attr('id', 'repeat-device-' + newNum);

        newElem.children(".selector-device").children("option[value='"+ previousDom.children(".selector-"                 // unable the previous choice
        + "device").val() +"']").attr('disabled', true);

        newElem.children(".selector-num-device").val(1);

        newElem.children(".selector-device").children('option:not(:disabled)').each(function() {
            $(this).prop('selected', true);
        });

        var deviceName = newElem.children(".selector-device").val()
        var root = newElem

        ajax_processing(deviceName, root);
        console.log(device_list);

        previousDom.children(".selector-device").attr('disabled', true);

        previousDom.after(newElem);
        $(this).siblings('#remove-device-btn').attr('disabled', false);

        if (newNum == $("#hidden-devices-num").val()) {
            $(this).attr('disabled', true);
        }
    });

    $(document).on('click', '#remove-device-btn', function() {
        var num = $(this).siblings('.repeat-device').length;
        var newNum = new Number(num - 1);
        var previousDom = $(this).siblings('#repeat-device-' + newNum);
        var actualDom = $(this).siblings('#repeat-device-' + num);
        var deviceName = actualDom.children('.selector-device').val();

        $("#device-list").children('#' + deviceName).remove();
        const index = device_list.indexOf(deviceName);
        if (index > -1) {
            device_list.splice(index, 1);
        }
        console.log(device_list);

        actualDom.remove();                                                                                                 // remove the last element
        $(this).siblings('#add-device-btn').attr('disabled', false);                                                        // enable the "add" button
        previousDom.children(".selector-device").attr('disabled', false);                                                   // enable device selection

        if (newNum == 1) {
            $(this).attr('disabled', true);                                                                                 // if only one element remains, disable the "remove" button
        }
    });

    $(document).on('click', '.enable-cards', function() {
        if(this.checked) {
            if($(this).parent().parent().parent().parent().siblings('.enable-cards-section').children('#table-input-'+
            'cards').children('#body-input-cards').children('#row-input-cards').children('#cell-input-'+
            'cards').children('.enable-input-cards').prop('checked') ||
            $(this).parent().parent().parent().parent().siblings('.enable-cards-section').children('#table-output-'+
            'cards').children('#body-output-cards').children('#row-output-cards').children('#cell-output-'+
            'cards').children('.enable-output-cards').prop('checked') ||
            $(this).parent().parent().parent().parent().siblings('#table-devices').children('#body-'+
            'devices').children('#row-devices').children('#cell-devices').children('.enable-devices').prop('checked')) {
                $('#add-center-btn').attr('disabled', false);
                $('#generate').attr('disabled', false);
            } else {
                $('#add-center-btn').attr('disabled', true);
                $('#generate').attr('disabled', true);
            }
        } else {
            if($(this).parent().parent().parent().parent().siblings('#table-devices').children('#body-'+
            'devices').children('#row-devices').children('#cell-devices').children('.enable-devices').prop('checked')) {
                $('#add-center-btn').attr('disabled', false);
                $('#generate').attr('disabled', false);
            } else {
                $('#add-center-btn').attr('disabled', true);
                $('#generate').attr('disabled', true);
            }
        }

    });

    $(document).on('click', '.enable-input-cards', function() {
        if(this.checked) {
            $('#add-center-btn').attr('disabled', false);
            $('#generate').attr('disabled', false);
        } else {
            $('#add-center-btn').attr('disabled', true);
            $('#generate').attr('disabled', true);
        }

        if($(this).parent().parent().parent().parent().siblings('#table-output-cards').children('#body-output-'+
        'cards').children('#row-output-cards').children('#cell-output-cards').children('.enable-output-'+
        'cards').prop('checked')) {
            $('#add-center-btn').attr('disabled', false);
            $('#generate').attr('disabled', false);
        }

        if($(this).parent().parent().parent().parent().parent().siblings('#table-devices').children('#body-'+
        'devices').children('#row-devices').children('#cell-devices').children('.enable-devices').prop('checked')) {
            $('#add-center-btn').attr('disabled', false);
            $('#generate').attr('disabled', false);
        }
    });

    $(document).on('click', '.enable-output-cards', function() {
        if(this.checked) {
            $('#add-center-btn').attr('disabled', false);
            $('#generate').attr('disabled', false);
        } else {
            $('#add-center-btn').attr('disabled', true);
            $('#generate').attr('disabled', true);
        }

        if($(this).parent().parent().parent().parent().siblings('#table-input-cards').children('#body-input-'+
        'cards').children('#row-input-cards').children('#cell-input-cards').children('.enable-input-'+
        'cards').prop('checked')) {
            $('#add-center-btn').attr('disabled', false);
            $('#generate').attr('disabled', false);
        }

        if($(this).parent().parent().parent().parent().parent().siblings('#table-devices').children('#body-'+
        'devices').children('#row-devices').children('#cell-devices').children('.enable-devices').prop('checked')) {
            $('#add-center-btn').attr('disabled', false);
            $('#generate').attr('disabled', false);
        }
    });

    $(document).on('click', '.enable-device', function() {
        if (this.checked) {
            $(this).siblings(".object-section").show();
        } else {
            $(this).siblings(".object-section").hide();
        }
    });

    $(document).on('click', '.enable-monitor-objects', function() {
        if (this.checked) {
            $(this).siblings(".monitor-objects-section").show();
        } else {
            $(this).siblings(".monitor-objects-section").hide();
        }
    });

    $(document).on('click', '.enable-control-objects', function() {
        if (this.checked) {
            $(this).siblings(".control-objects-section").show();
        } else {
            $(this).siblings(".control-objects-section").hide();
        }
    });

    $(document).on('click', '.enable-signals', function() {
        if (this.checked) {
            $(this).siblings(".signals-section").show();
        } else {
            $(this).siblings(".signals-section").hide();
        }
    });

    function ajax_processing(deviceName, root) {
        $.ajax({
            url: '/ajax/validate_parameters/',
            data: {
              'device_name': deviceName
            },
            dataType: 'json',
            success: function (data) {
                if (!data.is_client) {
                    root.children('#add-device-client').prop('checked', false)
                    root.children('#add-device-client').prop('disabled', true)
                    root.children('#add-device-server').prop('checked', true)
                    root.children('#add-device-server').prop('disabled', true)
                } else {
                    root.children('#add-device-client').prop('checked', true)
                    root.children('#add-device-client').prop('disabled', false)
                    root.children('#add-device-server').prop('checked', true)
                    root.children('#add-device-server').prop('disabled', false)
                }
                if (!data.is_do) {
                    root.children('.selector-operation').children().each(function() {
                        if ($(this).val() == "DO") {
                            $(this).prop('disabled', true)
                        }
                    });
                } else {
                    root.children('.selector-operation').children().each(function() {
                        if ($(this).val() == "DO") {
                            $(this).prop('disabled', false)
                        }
                    });
                }
                if (!data.is_sbo) {
                    root.children('.selector-operation').children().each(function() {
                        if ($(this).val() == "SBO") {
                            $(this).prop('disabled', true)
                        }
                    });
                    root.children('.selector-operation').val("DO");
                } else {
                    root.children('.selector-operation').children().each(function() {
                        if ($(this).val() == "SBO") {
                           $(this).prop('disabled', false)
                        }
                    });
                }

                if (!device_list.includes(deviceName)) {
                    //Add element to list
                    device_list.push(deviceName);
                    device_processing(deviceName, data.device_data);
                }
            }
        });
    }

    function device_processing(deviceName, data) {
        var device = '';

        //Create drop-down menu
        device += '<div class="actionlist" id="' + deviceName + '">\n';
        device += '\t<input type="checkbox" class="enable-device" id="' + deviceName + '-cbx">\n';
        device += '\t<label>' + deviceName + '</label>\n';
        device += '\t<div class="object-section" style="display:none;">\n';
        $.each(data, function(key, value){
            if (key == 'monitor') {
                device += '\t\t<div class="monitor-section">\n';
                device += '\t\t\t<input type="checkbox" class="enable-monitor-objects" id="monitor-cbx" style="position:relative; left:15px;">\n';
                device += '\t\t\t<label style="position:relative; left:15px;">monitor objects</label>\n';
                device += '\t\t\t<div class="monitor-objects-section" style="display:none;">\n';
                $.each(value, function(key, value){
                    device += '\t\t\t\t<div class="monitor-object" id="' + key + '">\n';
                    device += '\t\t\t\t\t<input class="enable-signals" type="checkbox" id="' + key + '-cbx" style="position:relative; left:30px;">\n';
                    device += '\t\t\t\t\t<label style="position:relative; left:30px;">' + key + '</label>\n';
                    device += '\t\t\t\t\t<div class="signals-section" style="display:none;">\n';
                    $.each(value, function(index, value){
                        device += '\t\t\t\t\t\t<div class="signal">\n';
                        device += '\t\t\t\t\t\t\t<input type="checkbox" id="' + value + '-cbx" value="' + value + '" style="position:relative; left:45px;" checked>\n';
                        device += '\t\t\t\t\t\t\t<label style="position:relative; left:45px;">' + value + '</label>\n';
                        device += '\t\t\t\t\t\t</div>\n';
                    });
                    device += '\t\t\t\t\t</div>\n';
                    device += '\t\t\t\t</div>\n';
                });
                device += '\t\t\t</div>\n';
                device += '\t\t</div>\n';
            }
            if (key == 'control') {
                device += '\t\t<div class="control-section">\n';
                device += '\t\t\t<input type="checkbox" class="enable-control-objects" id="control-cbx" style="position:relative; left:15px;">\n';
                device += '\t\t\t<label style="position:relative; left:15px;">control objects</label>\n';
                device += '\t\t\t<div class="control-objects-section" style="display:none;">\n';
                $.each(value, function(key, value){
                    device += '\t\t\t\t<div class="control-object" id="' + key + '">\n';
                    device += '\t\t\t\t\t<input class="enable-signals" type="checkbox" id="' + key + '-cbx" style="position:relative; left:30px;">\n';
                    device += '\t\t\t\t\t<label style="position:relative; left:30px;">' + key + '</label>\n';
                    device += '\t\t\t\t\t<div class="signals-section" style="display:none;">\n';
                    $.each(value, function(index, value){
                        device += '\t\t\t\t\t\t<div class="signal">\n';
                        device += '\t\t\t\t\t\t\t<input type="checkbox" id="' + value + '-cbx" value="' + value + '" style="position:relative; left:45px;" checked>\n';
                        device += '\t\t\t\t\t\t\t<label style="position:relative; left:45px;">' + value + '</label>\n';
                        device += '\t\t\t\t\t\t</div>\n';
                    });
                    device += '\t\t\t\t\t</div>\n';
                    device += '\t\t\t\t</div>\n';
                });
                device += '\t\t\t</div>\n';
                device += '\t\t</div>\n';
            }
        });

        device += '\t</div>\n';
        device += '</div>\n';

        $("#device-list").append(device);
    }

    $('#form-data').submit(function(event) {
        var xmlString = "";

        xmlString += '<?xml version="1.0" encoding="UTF-8"?>';
        xmlString += "<root>";
        $('.repeat-center').each(function() {
            xmlString += "<center name='";
            xmlString += $(this).children('#center').children("#table-center").children("#body-"+
            "center").children("#row-center").children("#cell-center-name").children("#center-name").val();
            xmlString += "'>";

            if($(this).children('#center').children('#table-cards').children('#body-cards').children('#row-'+
            'cards').children('#cell-cards').children('.enable-cards').prop('checked')) {
                if($(this).children('#center').children('.enable-cards-section').children("#table-input-"+
                "cards").children("#body-input-cards").children("#row-input-cards").children('#cell-input-'+
                'cards').children('.enable-input-cards').prop('checked')) {
                    $(this).children('#center').children('.enable-cards-section').children('.enable-input-cards-'+
                    'section').children('.repeat-input-card').each(function() {
                        xmlString += "<input-card ";
                        xmlString += "number='";
                        xmlString += $(this).children('.selector-num-input-card').val();
                        xmlString += "' ";
                        xmlString += "server='";
                        if($(this).children('#add-input-card-server').prop('checked')) {
                            xmlString += "yes";
                        } else {
                            xmlString += "no";
                        }
                        xmlString += "'";
                        xmlString += " io='";
                        if($(this).children('#add-input-card-io').prop('checked')) {
                            xmlString += "yes";
                        } else {
                            xmlString += "no";
                        }
                        xmlString += "'>";
                        xmlString += $(this).children('.selector-input-card').val();
                        xmlString += "</input-card>";
                    });
                }

                if($(this).children('#center').children('.enable-cards-section').children("#table-output-"+
                "cards").children("#body-output-cards").children("#row-output-cards").children('#cell-output-'+
                'cards').children('.enable-output-cards').prop('checked')) {
                    $(this).children('#center').children('.enable-cards-section').children('.enable-output-cards-'+
                    'section').children('.repeat-output-card').each(function() {
                        xmlString += "<output-card ";
                        xmlString += "number='";
                        xmlString += $(this).children('.selector-num-output-card').val();
                        xmlString += "' ";
                        xmlString += "server='";
                        if($(this).children('#add-output-card-server').prop('checked')) {
                            xmlString += "yes";
                        } else {
                            xmlString += "no";
                        }
                        xmlString += "'";
                        xmlString += " io='";
                        if($(this).children('#add-output-card-io').prop('checked')) {
                            xmlString += "yes";
                        } else {
                            xmlString += "no";
                        }
                        xmlString += "'>";
                        xmlString += $(this).children('.selector-output-card').val();
                        xmlString += "</output-card>";
                    });
                }
            }

            if($(this).children('#center').children("#table-devices").children("#body-devices").children("#row-"+
            "devices").children('#cell-devices').children('.enable-devices').prop('checked')) {
                $(this).children('#center').children(".enable-devices-section").children('.repeat-'+
                'device').each(function() {
                    xmlString += "<device ";
                    xmlString += "operation='";
                    xmlString += $(this).children('.selector-operation').val();
                    xmlString += "' ";
                    xmlString += "number='";
                    xmlString += $(this).children('.selector-num-device').val();
                    xmlString += "' ";
                    xmlString += "server='";
                    if($(this).children('#add-device-server').prop('checked')) {
                        xmlString += "yes";
                    } else {
                        xmlString += "no";
                    }
                    xmlString += "'";
                    xmlString += " client='";
                    if($(this).children('#add-device-client').prop('checked')) {
                        xmlString += "yes";
                    } else {
                        xmlString += "no";
                    }
                    xmlString += "'>";
                    xmlString += $(this).children('.selector-device').val();
                    xmlString += "</device>";
                });
            }
            xmlString += "</center>";
        });
        xmlString += "</root>";

        $('#hidden-request-data').val(xmlString);
    });
});
