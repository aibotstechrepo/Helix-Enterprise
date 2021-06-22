var excel_data_arr = [''];
//var excel_data_arr = ['abc','ddasd','asd,asd'];


        /*function image_push()
        {   
            var temp = "<img src='images/image.jpg' style='height:80px;border-style: dashed;width:70px;";
            var temp1 = "";

            for (var i = 0; i < 20; i++) {
                temp1 = temp1 + temp + "' id=" + i +" onclick='image_view(this.id)'><br><br>";
            }
            document.getElementById('image_push').innerHTML = temp1;
        }*/

$(function() {
    $('#upload-file-btn').click(function() {
        var form_data = new FormData($('#upload-file')[0]);
        $.ajax({
            type: 'POST',
            url: 'pdf_preprocess',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                alert("Preprocessing Completed"); 
                var imag = document.getElementById('image_push');
                var temp="";
                for (var i = 0; i < data.image.length; i++)
                {
                    temp = temp + "<img src='" + data.image[i] + "' id='" + data.image[i] +"' width='100%'' height='30%' class='img-responsive' onclick='image_view_(this.id);' style='height:80px;border-style: dashed;width:70px;'><br><br>" 
                }
                imag.innerHTML = temp; 


            },
        });
    });
});


function image_view_(id)
{
    var src = document.getElementById(id).src;
    //document.getElementById('image_view_').innerHTML = "<img src='" + src + "' style='height:100%;width:100%;'>";

    var res = src.split("/");
    excel_data_arr.splice(0,excel_data_arr.length);
    alert(res[4]);

    $.ajax({

        type : 'POST',
        url : 'pdf_ocrprocess_hocr',
        data :{
            img_name : res[4],
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },
        success:function(data){
            var insert_data = document.getElementById('table-data');
            var insert_temp = "";
            for (var i = 0; i<data.length;i++){
            insert_temp = insert_temp + "<tr><td><span>data"+i+"</span></td><td><input type='textbox' class='form-control' id='e"+i+"' style='height:10px;' value='"+ data[i]+"''></td></tr>";
                excel_data_arr[i] = data[i];
            }

            insert_data.innerHTML = insert_temp;
            document.getElementById('image_view_').innerHTML = "<img src='http://127.0.0.1:8000/media/t" + res[4] + "' style='height:100%;width:100%;'>";
            document.getElementById('template_id').value = "01";
            document.getElementById('template_name').value = "Indigo";


        } 
    })
}

function continue_process()
{   

    var form_data = new FormData($('#upload-file')[0]);
    excel_data_arr.splice(0,excel_data_arr.length);
    if (form_data === null )
    {
        alert("Please Select the file");
    }
    else
    {
        $.ajax({
        type: 'POST',
        url: 'pdf_preprocess',
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        success: function(data) { 
            var imag = document.getElementById('image_push');
            var temp="";
            for (var i = 0; i < data.image.length; i++)
            {
                temp = temp + "<img src='" + data.image[i] + "' id='" + data.image[i] +"' width='100%'' height='30%' class='img-responsive' onclick='image_view_(this.id);' style='height:80px;border-style: dashed;width:70px;'><br><br>";

            }
            imag.innerHTML = temp;
            //document.getElementById('image_view_').innerHTML = "<img src='output_img/" + data.image[0] + "' style='height:100%;width:100%;'>";

            var insert_data = document.getElementById('table-data');
            var insert_temp = "";
            for (var i = 0; i<data.ocr_v.length;i++){
            insert_temp = insert_temp + "<tr><td><span>data"+i+"</span></td><td><input id='e"+i+"' type='textbox' class='form-control' style='height:10px;' value='"+ data.ocr_v[i]+"''></td></tr>";
                excel_data_arr[i] = data.ocr_v[i];
            }

            insert_data.innerHTML = insert_temp;
            var res1 = data.image[0].split("/");
            //alert(res1);
            document.getElementById('image_view_').innerHTML = "<img src='http://127.0.0.1:8000/media/t" + res1[1] + "' style='height:100%;width:100%;'>";
            document.getElementById('template_id').value = "01";
            document.getElementById('template_name').value = "Indigo";


            },
        }); 
    }
    
}

function display_pdf(input)
{
    var pdf_disp_temp="<embed src='' id='taget_pdf' width='100%' height='100%' style='border:1px solid black;'>";
    if (input.files && input.files[0])
    {
        var reader = new FileReader(); 

        reader.onload = function (e) {
            //$('#image_view_') 
                //.attr('src', e.target.result)
                //.width('100%')
                //.height('100%'); 
            $('#file_name_display')
                .text(input.files[0].name);
            $('#upload-file-btn')
                .attr("disabled", false);
            $('#preview_process')
                .attr("disabled", false);
                //console.log(input.files[0].name);
        };

        reader.readAsDataURL(input.files[0]);
    }
}

function write_data_to_excel()
{
    //alert(excel_data_arr.length);
    var temp_exc = [];
    for (var i = 0 ; i < excel_data_arr.length ; i++)
    {
        temp_exc[i]  = document.getElementById("e" + i).value;
    }
    var json = JSON.stringify(temp_exc);
    //var json = JSON.stringify(excel_data_arr);
    var file_name = document.getElementById('file_name_display').innerText;
    file_name = file_name.trimLeft(".pdf");
    $.ajax({

            type : 'POST',
            url : 'excel_data_write',
            data :{'a':json,
            'filename':file_name,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },
            success:function(data){
                alert("Data has return to Excel");
            } 
        })
}