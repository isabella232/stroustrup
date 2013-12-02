/**
 * Created with JetBrains WebStorm.
 * User: konstantin.oficerov
 * Date: 7/29/13
 * Time: 12:48 PM
 * To change this template use File | Settings | File Templates.
 */

function book_action(action, url, book_id){

    switch  (action)
    {
        case 'take':

            jQuery.ajax({
                type: 'get',
                url: url,
                data: {ID:book_id},
                dataType: 'json',
                success: function(data){
                $('#take_return_send_button').animate({right: 999}, 600, function(){
                    $(this).animate({right:0}, 600)
                        .attr('class', 'take_return_button btn btn-warning  btn-lg')
                        .attr('onclick',"book_action('return','return/"+book_id+"',"+book_id+");")
                        .text('Return...');
                }).end();
                    $('#status_row').animate({right: 999}, 600, function(){
                        $(this).animate({right: 0}, 600)
                            .attr('class', 'label label-warning take_return_button')
                            .text('Busy').end();  }).end();
                    $('#owner').fadeIn(600);




                }

            });
            break;
        case 'return':
            jQuery.ajax({
                type: 'get',
                url: url,
                data: 'take',
                dataType: 'json',
                success: function(data){
                    $('#take_return_send_button').animate({right: 999}, 600, function(){
                        $(this).animate({right:0}, 600)
                            .attr('class', 'take_return_button btn btn-success  btn-lg')
                            .attr('onclick',"book_action('take','take/"+book_id+"',"+book_id+");")
                            .text('Take!').end();
                    }).end();
                    $('#status_row').animate({right: 999}, 600, function(){
                        $(this).animate({right: 0}, 600)
                            .attr('class', 'label label-success take_return_button')
                            .text('Free').end();  }).end();
                    $('#owner').fadeOut(600);


                }

            });
            break;
        case  'ask':
            $('#take_return_send_button').animate({right: 999}, 600);

            $('#action').fadeOut(200);
            $('<p id="remove_after_sent"> <span class="glyphicon glyphicon-send"></span> Sending... </p>').insertAfter('#action').fadeIn(100);
            jQuery.ajax({
                type: 'get',
                url: url,
                data: {ID:book_id},
                dataType: 'json',
                success: function(data){
                    $('#remove_after_sent').fadeOut(100);
                    $('<p class="label label-success"> <span class="glyphicon glyphicon-ok"></span> Sent!</p>').insertAfter('#action').fadeOut(3200);
                }

            });
            break;
    }
}

function book_return (url, book_id){
    jQuery.ajax({
                type: 'get',
                url: url,
                data: 'take',
                dataType: 'json',
                success: function(data){
                    $("td:contains('"+book_id+"')").parent().remove();
                }
            });
}

function colored_button(id,color)
{

    var x=$('#'+id);

    x.css('background',color);


}

function add_comment_list(num)
{
    $("#panel"+num).slideToggle("slow");
    $(this).toggleClass("active");


}

function enter(event, num, id)
{


    if (event.keyCode == 13 || event.which == 13)
        return comment(num, id);
    return false;
}

function comment(num, user_id)
{

    var _comment = $('#input'+num).val();
    $('#input'+num).css('background', '#FFDFFD');

    if(_comment!='')
    {
    jQuery.ajax({
        type: 'get',
        url: 'comment/'+num.toString()+'/',
        data: {Comment:_comment},
        success: function(){
            $('#input'+num).animate({opacity: 0}, 'fast', function() {
                $(this)
                    .css({'background': 'white'})
                    .animate({opacity: 1});
            });

        }

    });
        if($('#empty_board'+num))
            $('#empty_board'+num).fadeOut('300');
        $('#input'+num).val('');
        $('<div class="row" >'+'<span class="glyphicon glyphicon-time"> </span> Just now'+
            '<div class="well well-sm">'+
            '<a onclick="'+'document.location.assign(\'/profile/'+user_id.toString()+'\')\"'+
            ' class="text-primary">'+'You'+': </a>'+_comment +
            '</div></div>').fadeIn(600).appendTo('#row_panel'+num);

    }
    return false;
}


function like_request(num){

    jQuery.ajax({
        type: 'get',
        url: 'like/'+num.toString()+'/',
        data: 'like',
        dataType: 'json',
        success:function(data){
            $('#counter'+num).animate({opacity: 0}, 'fast', function() {
                $(this)
                    .text(data.vote)
                    .animate({opacity: 1},'fast');
            });
            $('#userslist'+num).animate({opacity:0},'fast',function() {
                $(this)
                    .text(data.listuser)
                    .animate({opacity:1},'fast');
            });
        }
    });

}


function equals()
{
    var first_pass=$('#password_field').val();
    var conf_pass=$('#confirm_password_field').val();
    if(first_pass!=conf_pass)
    {
        $('#wrong_pass').css('display', 'block');
        $('#button1').attr('class','disabled success button submit_button');
        return false;
    }
    else
    {
        $('#wrong_pass').css('display', 'none');
        $('#button1').attr('class',' success button submit_button');
        return true;
    }
}

function valid_pass(){
    if(!equals)
    {
      $('#password_field').val('');
      $('#confirm_password_field').val('');
      throw Error('password dismatch');

    }
    return true;
}

function remove_error_box()
{
    $('#wrong_email').css('display','none');
}

function open_modal_window(id){
    $('#'+id).css('display', 'block');
    $('#modal_bg').css('opacity','1').css('display', 'block');

}
function close_modal_window(id){
    $('#modal_bg').css('display', 'none');
    $('#'+id).css('display', 'none');

}
function close_modal_windows(){

  $("div[class='modal_window']").css('display', 'none');

  close_modal_window(1);
}
function ajax_loader(id,url)
{

    $('#'+id).load(url);
}