// {% load staticfiles %}
//
// $(window).ready(function() {
// 	//$('#btnCrop').click();$("#idName").css("cssText","background-color:red!important");
//
// 	//$(".imageBox").css("cssText","background-position:88px 88px!important");$(".imageBox").css("cssText","background-size:222px 222px!important");
// 	var options =
// 	{
// 		thumbBox: '.thumbBox',
// 		spinner: '.spinner',
// 		imgSrc: ''
// 	};
// 	var cropper = $('.imageBox').cropbox(options);
// 	var img="";
// 	$('#upload-file').on('change', function(){
// 		var reader = new FileReader();
// 		reader.onload = function(e) {
// 			options.imgSrc = e.target.result;
// 			cropper = $('.imageBox').cropbox(options);
// 			getImg();
// 		};
// 		reader.readAsDataURL(this.files[0]);
// 		getImg();
// 		// this.files = [];
//         // mouse_up();
//         // console.log("************************************************");
// 	    //  console.log("upload-file:",this);
// 	    //  console.log("upload-file:",this.files);
//         // console.log("************************************************");
// 	    //  console.log("img:",img);
// 	});
//
// 	// 此函数为悬浮窗中的确定按钮
// 	$('#btnCrop').on('click', function(){
// 	    console.log("^^^^^^^^^^^^^^^^^^^^^^^^^^^^");
// 	    console.log("img:",img);
// 	    $.ajax({
//             url: '{% url "account:my_image" %}',
//             type: 'POST',
//             data: {"img":img},
//             success:function (e) {
//                 // location.href = "{% url 'account:my_information' %}"
//               if(e==="1"){
//                   parent.location.reload();
//               }else{
//                   alert("sorry,you are not lucky,the picture can not upload")
//               }
//             },
//         });
// 		// alert("图片上传喽");
// 	});
// 	function getImg(){
// 		img = cropper.getDataURL();
//
// 		$('.cropped').html('');
// 		$('.cropped').append('<img src="'+img+'" align="absmiddle" style="width:180px;margin-top:4px;border-radius:180px;box-shadow:0px 0px 12px #7E7E7E;"><p>180px*180px</p>');
// 		$('.cropped').append('<img src="'+img+'" align="absmiddle" style="width:128px;margin-top:4px;border-radius:128px;box-shadow:0px 0px 12px #7E7E7E;"><p>128px*128px</p>');
// 		$('.cropped').append('<img src="'+img+'" align="absmiddle" style="width:64px;margin-top:4px;border-radius:64px;box-shadow:0px 0px 12px #7E7E7E;" ><p>64px*64px</p>');
//
//         console.log("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$");
//         console.log(cropper);
//         console.log("img:",img);
// 	}
//
//     // function mouse_up(){
// 	// $(".imageBox").on("mouseup",function(){
//  	// 	getImg();
//     //     console.log("&&&&&&&&&&&&&&&");
//     //     console.log("img:",img);
//   	// 	});
//     // }
//     // function start_click(){
//     //     $(".imageBox").on("click",function () {
//     //
//     //          		getImg();
//     //     console.log("%%%%%%%%%%%%%%%%");
//     //     console.log("img:",img);
//     //     })
//     //
//     // }
// 	$(".imageBox").on("mouseup",function(){
//  		getImg();
//  		           //  console.log("&&&&&&&&&&&&&&&");
// 		            // console.log("img:",img);
//   		});
//
//
// 	$('#btnZoomIn').on('click', function(){
// 		cropper.zoomIn();
// 	});
// 	$('#btnZoomOut').on('click', function(){
// 		cropper.zoomOut();
// 	})
// });
