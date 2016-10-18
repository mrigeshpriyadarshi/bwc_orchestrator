$(document).ready(function(){
$('#loader').click(function(event){
event.preventDefault();

var form = $(this).closest("#loader").attr('name');
//alert (form);

if (form == 'firewall')
{

$.ajax({
type: "POST",
url: './resetfirewall.php',
success: function()
{
alert ("System reset done");
},
error: function()
{
alert ('Error!');
}
});
}
else if (form =='tunnel')
{
$.ajax({
type: "POST",
url: './resettunnel.php',
success: function()
{
alert ("System reset done");
},
error: function()
{
alert ('Error!');
}
});
}
else 
{
return false;
}

});
});
