// Function Collection
// --TOOLS--

// Main AJAX function
function jsonPostRequest(url, data, successCallback) {
    // Send a JSON request with POST ( bottle handle this with request.forms.get('toto'), params response is received response
    $.ajax({
        url: url,
        contentType: "application/json; charset=utf-8",
        data: data,
        type: 'POST',
        // Response must be JSON
        dataType: 'json',
        success: function(response) {
            // Execute success function
            successCallback(response)
        }
    });

};

// Declare GLOBAL vars contain displayed category and sub category list like [ [index, value], [index, value] ]

GLOBAL_DISPLAYED_CATEGORY = []
GLOBAL_DISPLAYED_SUB_CATEGORY = []


function getSubCategory() {
    // Get Subcategory and display them. Change global variable : GLOBAL_DISPLAYED_SUB_CATEGORY
    GLOBAL_DISPLAYED_SUB_CATEGORY = []

    // Catch category to send
    var selected_category = $("#category_selector option:selected").val();
    // Destroy select box
    $("#sub_category_selector").empty();
    // Create a default sub-category item
    $("#sub_category_selector").append("<option value='' selected='selected'>All Sub-Category</option>");
    jsonPostRequest("/_sub_category", {
            'to_search_category': selected_category
        },

        function(response) {
            $("#sub_category_selector").empty();
            // For each item on JSON response, create option box.

            $.each(response, function(index, value) {

                $("#sub_category_selector").append("<option value='" + value[0] + "'>" + value[1] + "</option>");
                GLOBAL_DISPLAYED_SUB_CATEGORY.push([value[0], value[1]])
            });

        }
    );

};




function getCategory() {
    // Get category and display them. Change global variable : GLOBAL_DISPLAYED_CATEGORY
    GLOBAL_DISPLAYED_CATEGORY = []

    jsonPostRequest("/_category", { }, // Send empty Data

        function(response) {
            $("#category_selector").empty();
            request_received = true
            $.each(response, function(index, value) {


                GLOBAL_DISPLAYED_CATEGORY.push([value[0], value[1]])
                if (index == (response.length - 1)) {
                    $("#category_selector").append("<option value='" + value[0] + "' selected='selected' >" + value[1] + "</option>");
                    getSubCategory();
                } else {
                    $("#category_selector").append("<option value='" + value[0] + "'>" + value[1] + "</option>");
                }
            });

        }

    );

};



function contentReponseParser(response) {
    // Json response passed on parametter must be a list of list. Funnction append content on article Tag

    // If boxes exist, append before them the new content.
    if ($(".content_boxes").length) {
        $(".content_boxes").before("<div id='new_empty_item' class='content_boxes'></div>");
    // If not exist, create a new box who'll be changed
    } else {
        $("article").append("<div id='new_empty_item' class='content_boxes'></div>");
    }

    var numItems = $('.content_boxes').length;

    var new_box = $('#new_empty_item').attr('id', 'content_box_' + numItems);
    // Add content on new content box.
    $.each(response, function(index, value) {

        $('#content_box_' + numItems).append("<div id='content_" + value[0] + "_box_" + numItems + "' class='content_boxe'><p class='content_date'>" + value[1] + "<div class='for_del' id='for_del_"+ value[0] +"'> Delete </div></p><p class='content_description'>" + value[2] + "</p><p class='content_content'>" + value[3] + "</p></div>");
        // Create the cleck handler for deleting content on call.
        $( "#for_del_" +  + value[0] ).click(function() {
            // Send Json request for deleting content, display success or fazilure request.
            jsonPostRequest("/_delete_content", {'to_delete_content' :  value[0] }, function(response){
            if (response[0] == 1){
                        $( "#for_del_" +  + value[0] ).remove()
            }else{
            alert("Erreur lors de la suppression.")
            }


             })
         });
    });
}

function getContentAndAddToBody() {

    // Catch category to send and send it with AJAX
    var selected_category = $("#category_selector option:selected").val();
    var selected_sub_category = $("#sub_category_selector option:selected").val();
    var user_description = $("#to_search_description").val();

    jsonPostRequest("/_content", {
            'to_search_category': selected_category,
            'to_search_sub_category': selected_sub_category,
            'to_search_description': user_description
        },

        function(response) {
            contentReponseParser(response)

        }
    );
};

// Functions who parse GLOBAL vars for autocomplete function.

function returnCategoryNames() {
    var displayedCategoryNames = []
    for (i = 0; i < GLOBAL_DISPLAYED_CATEGORY.length; i++) {
        displayedCategoryNames.push(GLOBAL_DISPLAYED_CATEGORY[i][1])
    }
    return displayedCategoryNames

}

function returnSubCategoryNames() {
    var displayedSubCategoryNames = []
    for (i = 0; i < GLOBAL_DISPLAYED_SUB_CATEGORY.length; i++) {
        displayedSubCategoryNames.push(GLOBAL_DISPLAYED_SUB_CATEGORY[i][1])

    }

    return displayedSubCategoryNames

}


function replaceSubCategoryGlobalVar() {
    // Refresh Sub category autocomplete Global VAR : GLOBAL_DISPLAYED_SUB_CATEGORY

    if (returnCategoryNames().indexOf($("#insert_category").val()) >= 0) {
        var category_index = returnCategoryNames().indexOf($("#insert_category").val());
        selected_category = GLOBAL_DISPLAYED_CATEGORY[category_index][0];
        jsonPostRequest("/_sub_category", {
                'to_search_category': selected_category
            },
            function(response) {
                GLOBAL_DISPLAYED_SUB_CATEGORY = []
                $.each(response, function(index, value) {
                    GLOBAL_DISPLAYED_SUB_CATEGORY.push([value[0], value[1]])
                });
            }
        );
    }

};


function deleteContentById(){

}


function sendContentForSave() {
    // Releve les erruer et envoie un requette afin de sauvegarder le contennu ainsi que de nouvelles catégories.

    var to_add_category = $("#insert_category").val();
    var to_add_sub_category = $("#insert_sub_category").val();

    var to_send_description = $("#insert_description").val();
    var to_send_content = $("#insert_content").val();
    var to_send_category = null;
    var to_send_sub_category = null;

    $('#alert_box_insert_box').empty()

    // Get ID of category if it exist on displayed category <option>, if not exist, give the string for save a new cat
    if (to_add_category != "") {
        if (returnCategoryNames().indexOf(to_add_category) >= 0) {
            var category_index = returnCategoryNames().indexOf(to_add_category);
            to_send_category = GLOBAL_DISPLAYED_CATEGORY[category_index][0];
        } else {
            to_send_category = to_add_category;
        }
    }
    // Get ID of sub category if it exist on displayed category <option>, if not exist, give the string for save a new sub_cat
    if (returnSubCategoryNames().indexOf(to_add_sub_category) >= 0) {
        var sub_category_index = returnSubCategoryNames().indexOf(to_add_sub_category);
        to_send_sub_category = GLOBAL_DISPLAYED_SUB_CATEGORY[sub_category_index][0];
    } else {
        to_send_sub_category = to_add_sub_category;
    }

    if (to_send_category != null && (to_send_sub_category == null || to_send_sub_category == "")) {
        var old = $('#alert_box_insert_box').text()
        $('#alert_box_insert_box').text("La catégorie doit contenir une sous-catégorie." + old)

    }
    if (to_send_category == null && to_send_sub_category != null) {

        var old = $('#alert_box_insert_box').text()
        $('#alert_box_insert_box').text("La sous catégorie doit appartenir à une catégorie. " + old)

    }


    if (to_send_category != null && to_send_sub_category != null) {
        if (to_send_content == null) {
        } else {
            jsonPostRequest("/_add_category_content", {
                    "to_insert_category": to_send_category,
                    "to_insert_sub_category": to_send_sub_category,
                    "to_insert_description": to_send_description,
                    "to_insert_content": to_send_content
                },
                function(response) {
                    $.each(response, function(index, value) {
                        if (index == "valid") {
                            contentReponseParser(value);
                        }
                        if (index == "error") {
                            var old = $('#alert_box_insert_box').text()
                            $('#alert_box_insert_box').text("La sous catégorie doit appartenir à une catégorie. " + old)
                        }
                    });

                }
            );
        }

    }

    getCategory();


};


// END Of Function Collection -------------------------------------

// Main function

$(document).ready(

    function() {
        // Docuemnt Ready Start
        getCategory();



        // Handlers
        $("#category_selector").change(function() {
            getSubCategory();

        });

        $("#search_button").click(function() {
            getContentAndAddToBody();
        });

        // Autocomplete category. Use the current displayed Category on Select Box
        $("#insert_category").focus(function() {

            // Use the list build with Cattegory on Var list
            $('#insert_category').autocomplete({

                source: returnCategoryNames(),
                minLength: 1,
            });
        });

        // Reload autocomplete list of sub category when insert_category loose focus.

        $("#insert_category").focusout(function() {
            replaceSubCategoryGlobalVar();
            $('#insert_sub_category').autocomplete({

                source: returnSubCategoryNames(),
                minLength: 1,
            });
        });


        $("#insert_content").focus(function() {
            if ($("#insert_content").val() == "" || $("#insert_content").val() == null) {
                $('#alert_box_insert_box').text("Associer une description au contenu n'est pas obligatoire mais recommandé. ");
            }
        });

        // Button handler for send Content to the server.
        $("#add_category_button").click(function() {
            sendContentForSave();
        });


        // End Handlers

        // Docuemnt Ready End
    }
);
