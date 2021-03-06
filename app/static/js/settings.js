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
      alert('非法邮箱');
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

  $('#alert-switch').change(function(){
    var checked = $(this).prop('checked');
    console.log('switch: '+checked);
    $.post('settings/alert-switch', {alert_switch_value: checked}, function(){});
  });

  $('#set-fire-value').click(function(){
    var fire = $('#fire-value-input').val();
    if(!(Math.floor(fire) == fire)) {
      alert('非法温度，请输入整数');
      return;
    }
    $.post('settings/fire-value', {fire_value: Math.floor(fire)}, function(data, status){
      if(data['status'] == 'ok') {
        $('#fire-value-input').val(data['fire_value']);
        $('#set-fire-value').append('<span class="glyphicon glyphicon-ok" style="color: #0a0; display:inline;" id="set-ok"></span>');
        setTimeout(function(){$('#set-ok').fadeOut(1500, function(){$('#set-ok').remove();});}, 500);
      }
    });
  });

});
