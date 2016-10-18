$(function() {
$("form").submit(function() {
//$(".submit").click(function() {
$('.success').fadeIn(200).hide();
$('.error').fadeOut(200).hide();
$('.loading').html('<img src="images/loader.gif" width="" height="" class="img-loading">Loading..').show();

function done(){
$('.loading').fadeOut(200).hide();
$('.success').fadeIn(200).show();
}

function fail(){
$('.loading').fadeOut(200).hide();
$('.error').fadeIn(200).show();
}

//check which process
//var form = document.getElementById("form").name;
var form = $(this).closest("form").attr('name');
//alert (form);

////////////////////////////////////// VDX-VLAN CHange///////////////////////

if (form == 'vlan') 
	{
var port = $("#port").val();
var vlan = $("#vlan").val();
var url ='vdx-accessvlan.php?port='+port+'&vlan='+vlan;

$.ajax({
type: "POST",
url: url,
success: function()
{
setTimeout(done, 2000);
},
error: function()
{
setTimeout(fail, 2000);
}
});
return false;

	} 

/////////////////////////////////// CLIconf modify port //////////////

else if (form == 'cliconf')
        {
var port = $("#port").val();
var ip = $("#ip").val();
var url ='cliconf-process.php?port='+port+'&ip='+ip;

$.ajax({
type: "POST",
url: url,
success: function()
{
setTimeout(done, 2000);
},
error: function()
{
setTimeout(fail, 2000);
}

});

return false;

        }



/////////////////////////////////// SD Change BW //////////////

else if (form == 'sd')
	{
var bw = $("#bw").val();
var instance = $("#hostname").val();
var url ='sd-process.php?instance='+instance+'&bw='+bw;

$.ajax({
type: "POST",
url: url,
success: function()
{
setTimeout(done, 2000);
},
error: function()
{
setTimeout(fail, 2000);
}

});

return false;

	}

////////////////////////////// Vrouter ADD ACL //////////////////////////

else if (form == 'add-acl') 
	{
var Subnet = $("#Subnet").val();
var Mask = $("#Mask").val();
var Item = $("#Item").val();
var Action = $("#Action:checked").val();
var Hostname = $("#hostname").val();
var url ='vrouter-process.php?t=addacl&hostname='+ Hostname +'&data='+ Subnet +'/'+Mask+'&item='+Item+'&action='+Action;

$.ajax({
type: "POST",
url: url,
success: function(){
setTimeout(done, 2000);
},
error: function(){
setTimeout(fail, 2000);
}
});
return false;

	}

//////////////////////// vrouter ADD GRE ////////////////////////////

else if (form=='add-gre') 
	{
var tip1 = $("#tip1").val();
var tid1 = $("#tid1").val();
var tip2 = $("#tip2").val();
var tid2 = $("#tid2").val();
var hostname = $("#hostname").val();
var wanip = $("#wanip").val();
var lan = $("#lan").val();
var url ='vrouter-process.php?t=addgre&tip1='+ tip1 +'&tid1='+tid1+'&tip2='+tip2+'&tid2='+tid2+'&remote='+hostname+'&wan='+wanip+'&lan='+lan;

$.ajax({
type: "POST",
url: url,
success: function(){
setTimeout(done, 2000);
},
error: function(){
setTimeout(fail, 2000);
}
});

return false;

	}

//////////////////////////////// vRouter COnfig Push //////////////

else if (form=='configpush')
        {
var hostname = $("#hostname").val();
var ip = $("#ip").val();
var mask = $("#mask").val();
var url ='vrouter-process.php?t=configpush&ip='+ip+'/'+mask+'&hostname='+hostname;

$.ajax({
type: "POST",
url: url,
success: function(){
setTimeout(done, 2000);

},
error: function(){
setTimeout(fail,2000);

}
});


return false;

        }


///////////////////////////////VDX vlan change ////////////////////

else if (form=='access')
        {
var port = $("#port").val();
var vlan = $("#vlan").val();
var vf = $("#vf");
if(vf.is(":checked")){
var url ='vdx-process.php?t=access&port='+ port +'&vlan='+vlan+'&vf=yes';
}
else {
var url ='vdx-process.php?t=access&port='+ port +'&vlan='+vlan+'&vf=no';
}
$.ajax({
type: "POST",
url: url,
success: function(){
setTimeout(done, 2000);

},
error: function(){
setTimeout(fail, 2000);
}
});

return false;

        }

//////////////////////////////// VDX add trunk  //////////////

else if (form=='trunk')
        {
var tport = $("#tport").val();
var vcsvf = $("#vcsvf:checked").val();

//alert (vcsvf);
if(vcsvf=="svf"){
var url ='vdx-process.php?t=trunk&port='+ tport +'&vf=svf';
}
else if(vcsvf=="tvf")  {
var url ='vdx-process.php?t=trunk&port='+ tport +'&vf=tvf';
}
else {
var url ='vdx-process.php?t=trunk&port='+ tport +'&vf=error';	
	}

$.ajax({
type: "POST",
url: url,
success: function(){
setTimeout(done, 2000);
},
error: function(){
setTimeout(fail, 2000);
}
});

return false;

        }

//////////////////////////////// VDX Reset Port //////////////

else if (form=='reset')
        {
var rport = $("#rport").val();
var url ='vdx-process.php?t=reset&port='+rport;

$.ajax({
type: "POST",
url: url,
success: function(){
setTimeout(done, 2000);

},
error: function(){
setTimeout(fail,2000);

}
});


return false;

        }

////////////////////////////// ADD Device to BSC //////////////////////////

else if (form == 'add-device')
        {

var port = $("#port").val();
var ip = $("#ip").val();
var hostname = $("#hostname").val();
var uname = $("#username").val();
var pwd = $("#password").val();
var url ='vrouter-process.php?t=add-device&hostname='+ hostname +'&ip='+ ip +'&port='+port+'&uname='+uname+'&pwd='+pwd;



$.ajax({
type: "POST",
url: url,
success: function(){
setTimeout(done, 2000);
},
error: function(){
setTimeout(fail, 2000);
}
});
return false;

        }

//////////////////////// Delete Device from BSC ////////////////////////////

else if (form=='del-device')
        {
var hostname = $("#dhostname").val();
var url ='vrouter-process.php?t=del-device&hostname='+ hostname;

$.ajax({
type: "POST",
url: url,
success: function(){
setTimeout(done, 2000);
},
error: function(){
setTimeout(fail, 2000);
}
});

return false;
	}



/////////////////////////////// Last Match //////////////
else
	{
return false;
	}


});
});
