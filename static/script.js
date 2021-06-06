$(document).on("click", "#profile", function(data){
    $("#profile-modal-outer").show()
}
)
$(document).on("click", "#profile-modal-outer", function(data){
    if(data.target.id=="profile-modal-outer"){
        $("#profile-modal-outer").hide()
    }   
}
)

