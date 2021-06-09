const baseURL="https://wforpt8850.execute-api.us-east-1.amazonaws.com/"
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
    userID= data.target.getAttribute("userID")
    $("#thumbs-up-selected." + questionID).show()
    $("#thumbs-up."+ questionID).hide()
    $.ajax({
        type: 'GET',
        url: baseURL + "likeDoc?questionID="+questionID+"&userID="+userID,
    });  
 })

$(document).on("click", "#thumbs-up-selected", function(data){
    //this should send a message to the server to remove an entry from dynamodb
    questionID= data.target.getAttribute("questionID")
    userID= data.target.getAttribute("userID")
    $("#thumbs-up." + questionID).show()
    $("#thumbs-up-selected." + questionID).hide()
    $.ajax({
        type: 'GET',
        url: baseURL + "unlikeDoc?questionID="+questionID+"&userID="+userID,
    });
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
