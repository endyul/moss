function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}

$(document).ready(function() {
  $('#receivers .list-group-item-deletable').hover(function() {
    $(this).prepend('<span id="delete-icon" class="glyphicon glyphicon-minus"></span>');
    $('#delete-icon').click(function() {
      uid = $(this).parent().attr('id');
      var r = confirm('确定删除该接受者吗？'+ $(this).parent().text());
      if(r){
        $(this).parent().hide();
        $.post('receivers/delete', {uid: uid}, function(data, status){

        });
      }
    });
  }, function() {
    $('#delete-icon').remove();
  });

  $('#add-receiver').click(function(){
    var email = $('#new-receiver-input').val();
    if(!validateEmail(email)) {
      console.log('invalid email');
      return;
    }
    $.post('receivers/add', {email: email}, function(data, status){
      if(data['status'] == 'ok'){
        console.log(data['user']['id']);
        console.log(data['user']['email']);
        $('#receivers').append('<li class="list-group-item list-group-item-deletable" id="'+data['user']['id']+'">'+data['user']['email']+'</li>');
        $('#new-receiver-input').val("");
      }
    });
  });

});
