$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            headers: { "key": "qjhdsbvfihfajb" },
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (total) {
                // Get and display the result
                $('.loader').hide();
                $('#result').fadeIn(600);
                var html = '<h2>Top 2 Results</h2>';
                $.each(total, function(weed,data){
                    if(Object.keys(data).length>1){
                        html += '<p><b>Botanical Name:</b>'+data['name']+'&nbsp;&nbsp;&nbsp;&nbsp;<b>Common Name:</b>'+data['common']+'&nbsp;&nbsp;&nbsp;&nbsp;<b>Category:</b>'+data['category']+'&nbsp;&nbsp;&nbsp;&nbsp;<b>Telugu Name:</b>'+data['telugu']+'</p>';
                        html += '<table><tr><th>Crop</th><th>Herbicides</th><th>Bio Methods</th></tr>';
                        $.each(data['crop'],function(i,crop){
                            html += '<tr><td>'+crop[0]+'</td><td>'+crop[2]+'</td><td>'+crop[1]+'</td></tr>';
                        });
                        html += '</table>'
                    }else{
                        html += '<p><b>Botanical Name:</b>'+data['name']+'</p>';
                    }
                });
                $('#result').append(html);
                console.log('Success!');
            },
        });
    });

});
