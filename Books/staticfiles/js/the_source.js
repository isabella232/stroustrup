/**
 * Created with JetBrains WebStorm.
 * User: konstantin.oficerov
 * Date: 7/29/13
 * Time: 12:48 PM
 * To change this template use File | Settings | File Templates.
 */

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
function comment(num)
{

    /*add text to a field*/
    return false;

}

function comment_branch(sender)
{

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