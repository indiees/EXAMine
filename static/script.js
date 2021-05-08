window.addEventListener('load', function () {
  document.getElementById('sign-out').onclick = function () {
    window.location.href = "logout";
  };
});

function editpost(datetime){
    var image = document.getElementById(datetime + "image");
    var subject = document.getElementById(datetime + "subject").innerHTML;
    var message = document.getElementById(datetime + "message").innerHTML;
    console.log(image);
    document.getElementById(datetime + "container").innerHTML =
        '<form class="chat-box flex-row dark" enctype="multipart/form-data" action="edit_process" method="post">'+
        '<div class="forum-form-body dark">'+
            '<div style="justify-content: space-around;" class="flex-row container dark">'+
                '<div class="">'+
                    '<label style="margin: 5px;" for="id"><b>Subject</b></label>'+
                    '<input type="text" placeholder="Subject" name="subject" value="' + subject + '" required>'+
                '</div>'+
                '<div>'+
                    '<label style="margin: 5px;" for="id"><b>Message</b></label>'+
                    '<input type="textarea" placeholder="Message..." name="message" value="' + message + '" required>'+
                '</div>'+
            '</div>'+
            '<div class="flex-row container dark">'+
                '<div class="">'+
                    '<label style="margin: 5px;" for="img"><b>Attach Image</b></label>'+
                    '<input type="file" id="img" name="file" accept="image/*">'+
                '</div>'+
                '<div style="display: grid;">'+
                    '<label style="margin: 5px;" for="img"><b>or use previous image</b></label>'+
                    '<img class="pfp-small" src="' + image.getAttribute('src') +'">'+
                '</div>'+
            '</div>'+
        '</div>'+
        '<input type="hidden" name="datetime" value="' + datetime + '">'+
        '<div class="container forum-submit dark">'+
            '<button class="forum-submit" type="submit">Update</button>'+
        '</div>'+
    '</form>';
}
