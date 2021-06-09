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

$(document).on("click", ".question p", function(data){
   if (data.target.classList.contains("correct")){
       data.target.classList.add("correct-selected")
       $("#answer_"+ data.target.getAttribute("questionID")).show()
   }else{
       data.target.classList.add("incorrect-selected")
   }
   data.target.classList.remove("unselected")
})

$(document).on("click", "#thumbs-up", function(data){
    //this should send a message to the server to add an entry to dynamodb
    questionID= data.target.getAttribute("questionID")
    origin=data.target.getAttribute("origin")
    $("#thumbs-up-selected." + questionID).show()
    $("#thumbs-up."+ questionID).hide()
    window.location.replace("/question/"+ questionID +  "/like?origin=" + origin)  
 })

$(document).on("click", "#thumbs-up-selected", function(data){
    //this should send a message to the server to remove an entry from dynamodb
    questionID= data.target.getAttribute("questionID")
    origin=data.target.getAttribute("origin")
    $("#thumbs-up." + questionID).show()
    $("#thumbs-up-selected." + questionID).hide()
    window.location.replace("/question/"+ questionID + "/unlike?origin=" + origin)
 })

 $(document).on("click", "#view-liked-questions", function(data){
   window.location="/liked_questions"
})

$(document).on("click", ".question-preview", function(data){
    console.log(data.target)
    window.location="/question/"+ data.target.id
 })

 $(document).on("click", "#logout_btn", function(data){
    window.location="/logout"
 })