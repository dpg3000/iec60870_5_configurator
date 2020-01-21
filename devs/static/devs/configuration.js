$(document).ready(function(){
    jQuery('#add-center-btn').click(function() {
        var num = jQuery('.repeat-center').length;
        var newNum = new Number(num + 1);
        var previousDom = jQuery('#repeat-center-' + num);
        var newElem = jQuery('#repeat-center-' + num).clone().attr('id', 'repeat-center-' + newNum);                    // Cloning the previous element
        var numOfCards = newElem.children('.enable-cards-section').children('.repeat-card').length;
        var numOfDevices = newElem.children('.enable-devices-section').children('.repeat-device').length;

        previousDom.children('#table-cards').children('#body-cards').children('#row-cards').children('#cell-'+          // disable the add card checkbox
        'cards').children('.enable-cards').prop("disabled", true);

        previousDom.children('#table-devices').children('#body-devices').children('#row-devices').children('#cell-'+    // disable the add card checkbox
        'devices').children('.enable-devices').prop("disabled", true);

        previousDom.css("background", "#dfd url(../static/admin/img/icon-yes.svg) 100px 11px no-repeat");
        previousDom.children('#table-cards').children('#body-cards').children('#row-center').children('#cell-center-'+
        'name').children('#center-name').css("background", "#edffed");

        /*Cleaning add center status*/
        $(this).attr('disabled', true);

        /*Cleaning generate status*/
        $('#generate').attr('disabled', true);

        /*Cleaning Center*/
        newElem.children('#table-cards').children('#body-cards').children('#row-center').children('#cell-center-'+
        'name').children('#center-name').val("");

        /*Cleaning cards*/
        newElem.children('#table-cards').children('#body-cards').children('#row-cards').children('#cell-'+              //Uncheck the add card checkbox
        'cards').children('.enable-cards').prop("checked", false);

        newElem.children('.enable-cards-section').hide();                                                               //hide the card configurator dialog

        for (i = numOfCards; i > 1; i--) {                                                                              //Remove any card but first
            newElem.children('.enable-cards-section').children('#repeat-card-' + i).remove();
        }

        newElem.children('.enable-cards-section').children('#repeat-card-1').children('.selector-'+
        'card').attr('disabled', false);

        newElem.children('.enable-cards-section').children('#repeat-card-1').children('.selector-num-card').val(1);

        newElem.children('.enable-cards-section').children('#add-card-btn').attr('disabled', false);                    //Enable add button

        newElem.children('.enable-cards-section').children('#remove-card-btn').attr('disabled', true);                  //Disable remove button

        /*Cleaning devices*/
        newElem.children('#table-devices').children('#body-devices').children('#row-devices').children('#cell-'+           //Uncheck the add card checkbox
        'devices').children('.enable-devices').prop("checked", false);

        newElem.children('.enable-devices-section').hide();                                                               //hide the card configurator dialog

        for (i = numOfDevices; i > 1; i--) {                                                                              //Remove any card but first
            newElem.children('.enable-devices-section').children('#repeat-device-' + i).remove();
        }

        newElem.children('.enable-devices-section').children('#repeat-device-1').children('.selector-'+
        'device').attr('disabled', false);

        newElem.children('.enable-devices-section').children('#repeat-device-1').children('.selector-num-device').val(1);

        newElem.children('.enable-devices-section').children('#add-device-btn').attr('disabled', false);                //Enable add button

        newElem.children('.enable-devices-section').children('#remove-devices-btn').attr('disabled', true);             //Disable remove button

        previousDom.after(newElem);                                                                                     // Adding the new element after the previous
        jQuery('#remove-center-btn').attr('disabled', false);                                                           // Enabling 'remove center' possibility
    });

    jQuery('#remove-center-btn').click(function() {
        var num = jQuery('.repeat-center').length;
        var newNum = new Number(num - 1);
        var actualDom = jQuery('#repeat-center-' + newNum);

        actualDom.children('#table-cards').children('#body-cards').children('#row-cards').children('#cell-'+            // enable the add card checkbox
        'cards').children('.enable-cards').prop("disabled", false);

        actualDom.children('#table-devices').children('#body-devices').children('#row-devices').children('#cell-'+      // enable the add device checkbox
        'devices').children('.enable-devices').prop("disabled", false);

        if(actualDom.children('#table-cards').children('#body-cards').children('#row-cards').children('#cell-'+
        'cards').children('.enable-cards').prop('checked') || actualDom.children('#table-devices').children('#body-'+
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

    $(document).on('click', '.enable-cards', function() {
        if(this.checked) {
            $(this).parent().parent().parent().parent().siblings('.enable-cards-section').show();
        } else {
            $(this).parent().parent().parent().parent().siblings('.enable-cards-section').hide();
        }
    });

    $(document).on('click', '.enable-devices', function() {
        var deviceName = $(this).parent().parent().parent().parent().siblings('.enable-devices-'+
        'section').children('.repeat-device').children('.selector-device').val();
        var root = $(this).parent().parent().parent().parent().siblings('.enable-devices-section').children('.repeat-'+
        'device')

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
            }
        });
    });

    $(document).on('click', '.enable-devices', function() {
        if(this.checked) {
            $(this).parent().parent().parent().parent().siblings('.enable-devices-section').show();
        } else {
            $(this).parent().parent().parent().parent().siblings('.enable-devices-section').hide();
        }
    });

    $(document).on('click', '#add-card-server', function() {
        if($(this).prop('checked') == false) {
            $(this).siblings('#add-card-io').prop('checked', true)
        }
    });

    $(document).on('click', '#add-card-io', function() {
        if($(this).prop('checked') == false) {
            $(this).siblings('#add-card-server').prop('checked', true)
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

    $(document).on('click', '#add-card-btn', function() {
        var num = $(this).siblings('.repeat-card').length;
        var newNum = new Number(num + 1);
        var previousDom = $(this).siblings('#repeat-card-' + num);
        var newElem = $(this).siblings('#repeat-card-' + num).clone().attr('id', 'repeat-card-' + newNum);

        newElem.children(".selector-card").children("option[value='"+ previousDom.children(".selector-"                     // unable the previous choice
        + "card").val() +"']").attr('disabled', true);

        newElem.children(".selector-card").children('option:not(:disabled)').each(function() {
            $(this).prop('selected', true);
        });

        newElem.children(".selector-num-card").val(1);

        newElem.children("#add-card-server").prop('checked', true);
        newElem.children("#add-card-io").prop('checked', true);

        previousDom.children(".selector-card").attr('disabled', true);

        previousDom.after(newElem);
        $(this).siblings('#remove-card-btn').attr('disabled', false);

        if (newNum == $("#hidden-cards-num").val()) {
            $(this).attr('disabled', true);
        }
    });

    $(document).on('click', '#remove-card-btn', function() {
        var num = $(this).siblings('.repeat-card').length;
        var newNum = new Number(num - 1);
        var previousDom = $(this).siblings('#repeat-card-' + newNum);
        var actualDom = $(this).siblings('#repeat-card-' + num);

        actualDom.remove();                                                                                                 // remove the last element
        $(this).siblings('#add-card-btn').attr('disabled', false);                                                          // enable the "add" button
        previousDom.children(".selector-card").attr('disabled', false);                                                     // enable card selection

        if (newNum == 1) {
            $(this).attr('disabled', true);                                                                                 // if only one element remains, disable the "remove" button
        }
    });

    $(document).on('change', '.selector-device', function() {
        var deviceName = $(this).val()
        var root = $(this).parent()

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
            }
        });
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
            }
        });

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

        actualDom.remove();                                                                                                 // remove the last element
        $(this).siblings('#add-device-btn').attr('disabled', false);                                                        // enable the "add" button
        previousDom.children(".selector-device").attr('disabled', false);                                                   // enable device selection

        if (newNum == 1) {
            $(this).attr('disabled', true);                                                                                 // if only one element remains, disable the "remove" button
        }
    });

    $(document).on('click', '.enable-cards', function() {
        if(this.checked) {
            $('#add-center-btn').attr('disabled', false);
            $('#generate').attr('disabled', false);
        } else {
            $('#add-center-btn').attr('disabled', true);
            $('#generate').attr('disabled', true);
        }

        if($(this).parent().parent().parent().parent().siblings('#table-devices').children('#body-'+
        'devices').children('#row-devices').children('#cell-devices').children('.enable-devices').prop('checked')) {
            $('#add-center-btn').attr('disabled', false);
            $('#generate').attr('disabled', false);
        }
    });

    $(document).on('click', '.enable-devices', function() {
        if(this.checked) {
            $('#add-center-btn').attr('disabled', false);
            $('#generate').attr('disabled', false);
        } else {
            $('#add-center-btn').attr('disabled', true);
            $('#generate').attr('disabled', true);
        }

        if($(this).parent().parent().parent().parent().siblings('#table-cards').children('#body-'+
        'cards').children('#row-cards').children('#cell-cards').children('.enable-cards').prop('checked')) {
            $('#add-center-btn').attr('disabled', false);
            $('#generate').attr('disabled', false);
        }
    });

    $('#form-data').submit(function(event) {
        var xmlString = "";

        xmlString += '<?xml version="1.0" encoding="UTF-8"?>';
        xmlString += "<root>";
        $('.repeat-center').each(function() {
            xmlString += "<center name='";
            xmlString += $(this).children("#table-cards").children("#body-cards").children("#row-"+
            "center").children("#cell-center-name").children("#center-name").val();
            xmlString += "'>";

            if($(this).children("#table-cards").children("#body-cards").children("#row-cards").children('#cell-'+
            'cards').children('.enable-cards').prop('checked')) {
                $(this).children(".enable-cards-section").children('.repeat-card').each(function() {
                    xmlString += "<card ";
                    xmlString += "number='";
                    xmlString += $(this).children('.selector-num-card').val();
                    xmlString += "' ";
                    xmlString += "server='";
                    if($(this).children('#add-card-server').prop('checked')) {
                        xmlString += "yes";
                    } else {
                        xmlString += "no";
                    }
                    xmlString += "'";
                    xmlString += " io='";
                    if($(this).children('#add-card-io').prop('checked')) {
                        xmlString += "yes";
                    } else {
                        xmlString += "no";
                    }
                    xmlString += "'>";
                    xmlString += $(this).children('.selector-card').val();
                    xmlString += "</card>";
                });
            }

            if($(this).children("#table-devices").children("#body-devices").children("#row-devices").children('#cell-'+
            'devices').children('.enable-devices').prop('checked')) {
                $(this).children(".enable-devices-section").children('.repeat-device').each(function() {
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