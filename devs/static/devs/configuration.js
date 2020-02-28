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

        newElem.children('#center').children('.enable-cards-section').children('.enable-input-cards-section').hide();   //hiding the "input card section"
        newElem.children('#center').children('.enable-cards-section').children('.enable-output-cards-section').hide();  //hiding the "output card section"
        newElem.children('#center').children('.enable-cards-section').hide();                                           //hiding the "global card section"

        newElem.children('#center').children('.enable-cards-section').children('.enable-input-cards-'+                  //Enabling the selector of the input card left in the last loop
        'section').children('#repeat-input-card-1').children('.selector-input-card').attr('disabled', false);
        newElem.children('#center').children('.enable-cards-section').children('.enable-output-cards-'+                 //Enabling the selector of the output card left in the last loop
        'section').children('#repeat-output-card-1').children('.selector-input-card').attr('disabled', false);

        newElem.children('#center').children('.enable-cards-section').children('.enable-input-cards-'+                  //Initializing the number of input cards
        'section').children('#repeat-input-card-1').children('.selector-num-input-card').val(1);
        newElem.children('#center').children('.enable-cards-section').children('.enable-output-cards-'+                 //Initializing the number of output cards
        'section').children('#repeat-output-card-1').children('.selector-num-output-card').val(1);

        newElem.children('#center').children('.enable-cards-section').children('.enable-input-cards-'+                  //Enabling the "add input card" button
        'section').children('#add-input-card-btn').attr('disabled', false);
        newElem.children('#center').children('.enable-cards-section').children('.enable-output-cards-'+                 //Enabling the "add output card" button
        'section').children('#add-output-card-btn').attr('disabled', false);

        newElem.children('#center').children('.enable-cards-section').children('.enable-input-cards-'+                  //Disabling the "remove input card" button
        'section').children('#remove-input-card-btn').attr('disabled', true);
        newElem.children('#center').children('.enable-cards-section').children('.enable-output-cards-'+                 //Disabling the "remove output card" button
        'section').children('#remove-output-card-btn').attr('disabled', true);

        newElem.children('#center').children('#table-devices').children('#body-devices').children('#row-'+              //Unchecking the "add device" checkbox
        'devices').children('#cell-devices').children('.enable-devices').prop("checked", false);

        newElem.children('#center').children('.enable-devices-section').hide();                                         //hiding the "device section"

        for (i = numOfDevices; i > 1; i--) {                                                                            //Removing any devices but first
            newElem.children('#center').children('.enable-devices-section').children('#repeat-device-' + i).remove();
        }

        newElem.children('#center').children('.enable-devices-section').children('#repeat-'+                            //Enabling the selector of the device left in the last loop
        'device-1').children('.selector-device').attr('disabled', false);

        newElem.children('#center').children('.enable-devices-section').children('#repeat-'+                            //Initializing the number of devices
        'device-1').children('.selector-num-device').val(1);

        newElem.children('#center').children('.enable-devices-section').children('#add-device-'+                        //Enabling the "add device" button
        'btn').attr('disabled', false);

        newElem.children('#center').children('.enable-devices-section').children('#remove-devices-'+                    //Disabling the "remove device" button
        'btn').attr('disabled', true);

        previousDom.after(newElem);                                                                                     // Adding the new element after the previous
        jQuery('#remove-center-btn').attr('disabled', false);                                                           // Enabling the "remove center" button
    });

    jQuery('#remove-center-btn').click(function() {
        var num = jQuery('.repeat-center').length;
        var newNum = new Number(num - 1);
        var actualDom = jQuery('#repeat-center-' + newNum);

        actualDom.children('#center').css("background", "");                                                            // Removing "validated" icon

        actualDom.children('#center').children('#table-cards').children('#body-cards').children('#row-'+                // Enabling the "add card" checkbox
        'cards').children('#cell-cards').children('.enable-cards').prop("disabled", false);

        actualDom.children('#center').children('.enable-cards-section').children('#table-input-'+                       // Enabling the "add input card" checkbox
        'cards').children('#body-input-cards').children('#row-input-cards').children('#cell-input-'+
        'cards').children('.enable-input-cards').prop("disabled", false);

        actualDom.children('#center').children('.enable-cards-section').children('#table-output-'+                      // Enabling the "add output card" checkbox
        'cards').children('#body-output-cards').children('#row-output-cards').children('#cell-output-'+
        'cards').children('.enable-output-cards').prop("disabled", false);

        actualDom.children('#center').children('#table-devices').children('#body-devices').children('#row-'+            // Enabling the "add device" checkbox
        'devices').children('#cell-devices').children('.enable-devices').prop("disabled", false);

        if(actualDom.children('#center').children('.enable-cards-section').children('#table-input-'+                    // Logic to control "add center" and "generate" buttons
        'cards').children('#body-input-cards').children('#row-input-cards').children('#cell-input-'+                    // They'll be enabled only in case there are any cards or devices selected
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

        jQuery('#repeat-center-' + num).remove();                                                                       // Removing the last center

        if (newNum == 1) {
            jQuery('#remove-center-btn').attr('disabled', true);                                                        // Last element can not be removed if there is only one left
        }
    });

    $(document).on('click', '.enable-cards', function() {                                                               // Card section behaviour
        if(this.checked) {
            $(this).parent().parent().parent().parent().siblings('.enable-cards-section').show();
        } else {
            $(this).parent().parent().parent().parent().siblings('.enable-cards-section').hide();
        }
    });

    $(document).on('click', '.enable-input-cards', function() {                                                         // Input card section behaviour
        if(this.checked) {
            $(this).parent().parent().parent().parent().siblings('.enable-input-cards-section').show();
        } else {
            $(this).parent().parent().parent().parent().siblings('.enable-input-cards-section').hide();
        }
    });

    $(document).on('click', '.enable-output-cards', function() {                                                        // Output card section behaviour
        if(this.checked) {
            $(this).parent().parent().parent().parent().siblings('.enable-output-cards-section').show();
        } else {
            $(this).parent().parent().parent().parent().siblings('.enable-output-cards-section').hide();
        }
    });

    $(document).on('click', '.enable-devices', function() {                                                             // Device section behaviour
        var deviceName = $(this).parent().parent().parent().parent().siblings('.enable-devices-'+
        'section').children('#repeat-device-1').children('.selector-device').val();
        var root = $(this).parent().parent().parent().parent().siblings('.enable-devices-section').children('#repeat-'+
        'device-1')

        if (this.checked) {
            $('#device-list').show();                                                                                   // Showing signal selection list
            ajax_processing(deviceName, root);                                                                          // ajax to process DB options of the first device
            $(this).parent().parent().parent().parent().siblings('.enable-devices-section').show();                     // Showing the "device section"
            $('#add-center-btn').attr('disabled', false);                                                               // "add center" button behaviour
            $('#generate').attr('disabled', false);                                                                     // "generate" button behaviour
        } else {
            $('#device-list').hide();                                                                                   // Hiding signal selection list
            $(this).parent().parent().parent().parent().siblings('.enable-devices-section').hide();
            $('#add-center-btn').attr('disabled', true);
            $('#generate').attr('disabled', true);
        }

        if($(this).parent().parent().parent().parent().siblings('#table-cards').children('#body-'+                      //"add center" and "generate" buttons behaviour
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

    $(document).on('click', '#add-input-card-server', function() {                                                      // Input card server / io rebound behaviour
        if($(this).prop('checked') == false) {
            $(this).siblings('#add-input-card-io').prop('checked', true)
        }
    });

    $(document).on('click', '#add-output-card-server', function() {                                                     // Output card server / io rebound behaviour
        if($(this).prop('checked') == false) {
            $(this).siblings('#add-output-card-io').prop('checked', true)
        }
    });

    $(document).on('click', '#add-input-card-io', function() {                                                          // Input card server / io rebound behaviour
        if($(this).prop('checked') == false) {
            $(this).siblings('#add-input-card-server').prop('checked', true)
        }
    });

    $(document).on('click', '#add-output-card-io', function() {                                                         // Output card server / io rebound behaviour
        if($(this).prop('checked') == false) {
            $(this).siblings('#add-output-card-server').prop('checked', true)
        }
    });

    $(document).on('click', '#add-device-server', function() {                                                          // Device server / client rebound behaviour
        if($(this).prop('checked') == false) {
            $(this).siblings('#add-device-client').prop('checked', true)
        }
    });

    $(document).on('click', '#add-device-client', function() {                                                          // Device server / client rebound behaviour
        if($(this).prop('checked') == false) {
            $(this).siblings('#add-device-server').prop('checked', true)
        }
    });

    $(document).on('click', '#add-input-card-btn', function() {                                                         // "Add input card" button behaviour
        var num = $(this).siblings('.repeat-input-card').length;
        var newNum = new Number(num + 1);
        var previousDom = $(this).siblings('#repeat-input-card-' + num);
        var newElem = $(this).siblings('#repeat-input-card-' + num).clone().attr('id', 'repeat-input-card-' + newNum);

        if (newNum > $("#hidden-input-cards-num").val()) {                                                              // Limiting the number of adds
            $(this).attr('disabled', true);
        } else {
            newElem.children(".selector-input-card").children("option[value='"+ previousDom.children(".selector-input-" // Disabling last choice
            + "card").val() +"']").attr('disabled', true);

            newElem.children(".selector-input-card").children('option:not(:disabled)').each(function() {                // Enabling the ones left
                $(this).prop('selected', true);
            });

            newElem.children(".selector-num-input-card").val(1);                                                        // Initializing the number of input cards
            newElem.children("#add-input-card-server").prop('checked', true);                                           // Initializing the server option
            newElem.children("#add-input-card-io").prop('checked', true);                                               // Initializing the io option

            previousDom.children(".selector-input-card").attr('disabled', true);                                        // Fixing the last option to avoid over-selection
            previousDom.after(newElem);                                                                                 // Concatenating the new element

            $(this).siblings('#remove-input-card-btn').attr('disabled', false);                                         // Enabling "remove input card" button
        }
    });

    $(document).on('click', '#add-output-card-btn', function() {                                                        // "Add input card" button behaviour
        var num = $(this).siblings('.repeat-output-card').length;
        var newNum = new Number(num + 1);
        var previousDom = $(this).siblings('#repeat-output-card-' + num);
        var newElem = $(this).siblings('#repeat-output-card-' + num).clone().attr('id', 'repeat-output-card-' + newNum);

        if (newNum > $("#hidden-output-cards-num").val()) {                                                             // Limiting the number of adds
            $(this).attr('disabled', true);
        } else {
            newElem.children(".selector-output-card").children("option[value='"+ previousDom.children(".selector-"+     // Disabling last choice
            "output-card").val() +"']").attr('disabled', true);

            newElem.children(".selector-output-card").children('option:not(:disabled)').each(function() {               // Enabling the ones left
                $(this).prop('selected', true);
            });

            newElem.children(".selector-num-output-card").val(1);                                                       // Initializing the number of input cards
            newElem.children("#add-output-card-server").prop('checked', true);                                          // Initializing the server option
            newElem.children("#add-output-card-io").prop('checked', true);                                              // Initializing the io option

            previousDom.children(".selector-output-card").attr('disabled', true);                                       // Fixing the last option to avoid over-selection
            previousDom.after(newElem);                                                                                 // Concatenating the new element

            $(this).siblings('#remove-output-card-btn').attr('disabled', false);                                        // Enabling "remove input card" button
        }
    });

    $(document).on('click', '#remove-input-card-btn', function() {
        var num = $(this).siblings('.repeat-input-card').length;
        var newNum = new Number(num - 1);
        var previousDom = $(this).siblings('#repeat-input-card-' + newNum);
        var actualDom = $(this).siblings('#repeat-input-card-' + num);

        if (newNum == 1) {                                                                                              // If only one element remains, disabling the "remove button"
            $(this).attr('disabled', true);
        } else {
            actualDom.remove();                                                                                         // Removing the last element
            $(this).siblings('#add-input-card-btn').attr('disabled', false);                                            // Enabling the "add input card" button
            previousDom.children(".selector-input-card").attr('disabled', false);                                       // Enabling the "input card" section
        }
    });

    $(document).on('click', '#remove-output-card-btn', function() {
        var num = $(this).siblings('.repeat-output-card').length;
        var newNum = new Number(num - 1);
        var previousDom = $(this).siblings('#repeat-output-card-' + newNum);
        var actualDom = $(this).siblings('#repeat-output-card-' + num);

        if (newNum == 1) {                                                                                              // If only one element remains, disabling the "remove button"
            $(this).attr('disabled', true);
        } else {
            actualDom.remove();                                                                                         // Removing the last element
            $(this).siblings('#add-output-card-btn').attr('disabled', false);                                           // Enabling the "add output card" button
            previousDom.children(".selector-output-card").attr('disabled', false);                                      // Enabling the "output card" section
        }
    });

    $(document).on('focus', '.selector-device', function() {                                                            // Event concatenation in order to register the device before a change
        lastDeviceName = this.value;
    });

    $(document).on('change', '.selector-device', function() {
        var deviceName = $(this).val()
        var root = $(this).parent()

        $("#device-list").children('#' + lastDeviceName).remove();                                                      // Removing the last device before the change, from the signal configurator

        const index = device_list.indexOf(lastDeviceName);                                                              // Removing the last device before the change, from the device list
        if (index > -1) {
            device_list.splice(index, 1);
        }
        ajax_processing(deviceName, root);                                                                              // ajax to process DB options of the device after the change
        lastDeviceName = this.value;
    });

    $(document).on('click', '#add-device-btn', function() {
        var num = $(this).siblings('.repeat-device').length;
        var newNum = new Number(num + 1);
        var previousDom = $(this).siblings('#repeat-device-' + num);
        var newElem = $(this).siblings('#repeat-device-' + num).clone().attr('id', 'repeat-device-' + newNum);
        var deviceName;
        var root;

        if (newNum > $("#hidden-devices-num").val()) {
            $(this).attr('disabled', true);
        } else {
            newElem.children(".selector-device").children("option[value='"+ previousDom.children(".selector-"           // Disabling the previous choice
            + "device").val() +"']").attr('disabled', true);
            newElem.children(".selector-device").children('option:not(:disabled)').each(function() {                    // Enabling the ones left
                $(this).prop('selected', true);
            });
            newElem.children(".selector-num-device").val(1);                                                            // Initializing the number of devices

            deviceName = newElem.children(".selector-device").val()                                                     // Data for ajax
            root = newElem
            ajax_processing(deviceName, root);                                                                          // ajax to process DB options of the new device

            previousDom.children(".selector-device").attr('disabled', true);                                            // Fixing the last option to avoid over-selection

            previousDom.after(newElem);                                                                                 // Concatenating the new element
            $(this).siblings('#remove-device-btn').attr('disabled', false);                                             // Enabling "remove device" button
        }
    });

    $(document).on('click', '#remove-device-btn', function() {
        var num = $(this).siblings('.repeat-device').length;
        var newNum = new Number(num - 1);
        var previousDom = $(this).siblings('#repeat-device-' + newNum);
        var actualDom = $(this).siblings('#repeat-device-' + num);
        var deviceName = actualDom.children('.selector-device').val();

        $("#device-list").children('#' + deviceName).remove();                                                          // Removing the last device from the signal configurator
        const index = device_list.indexOf(deviceName);                                                                  // Removing the last device from the device list
        if (index > -1) {
            device_list.splice(index, 1);
        }
        actualDom.remove();                                                                                             // Removing the last element

        $(this).siblings('#add-device-btn').attr('disabled', false);                                                    // Enabling the "add device" button
        previousDom.children(".selector-device").attr('disabled', false);                                               // Enabling the device selector

        if (newNum == 1) {                                                                                              // if only one element remains, disabling the "remove device" button
            $(this).attr('disabled', true);
        }
    });

    $(document).on('click', '.enable-cards', function() {
        if(this.checked) {                                                                                              // Behaviour of "generate" and "add center" buttons
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

    $(document).on('click', '.enable-input-cards', function() {                                                         // Behaviour of "generate" and "add center" buttons
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

    $(document).on('click', '.enable-output-cards', function() {                                                        // Behaviour of "generate" and "add center" buttons
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

    function ajax_processing(deviceName, root) {                                                                        // ajax for server and getting device signals data
        $.ajax({
            url: '/ajax/validate_parameters/',
            data: {
              'device_name': deviceName
            },
            dataType: 'json',
            success: function (data) {
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

                if (!device_list.includes(deviceName)) {                                                                // Only adding if it is not already there
                    device_list.push(deviceName);
                    device_processing(deviceName, data.device_data);
                }
            }
        });
    }

    /*LOGIC FOR DEVICE SIGNALS DYNAMIC CODE*/
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

    $('#form-data').submit(function(event) {                                                                            // Construction of the request (xml format)
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
