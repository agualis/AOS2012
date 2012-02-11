logger = {
	login: function(event) {

		if (!event) event = window.event;
		event.cancelBubble = true;
	    if (event.stopPropagation) {
			// this code is for Mozilla and Opera
			event.stopPropagation();
				
			var form = $(event.target).parents('.form');
			form.find('input').removeClass('input_error');
			var user_id_input = form.find('input[name=user_id]');
			var pass_input = form.find('input[name=passphrase]');
			var country_input = form.find('select[name=countrycode]');
			var user_id = user_id_input.val()
			var pass = pass_input.val();
			var countrycode = country_input.val();
		} else if (window.event) {
			// this code is for IE
			window.event.cancelBubble = true;			
			$('#login_form_status').hide();
			var pass = document.loginForm.passphrase.value;
			var user_id = document.loginForm.user_id.value;
			var countrycode = document.loginForm.countrycode.value;
		}
		
		if (user_id == undefined || user_id == "") {
			user_id_input.addClass('input_error');
		}
		if (pass == undefined || pass == "") {
			pass_input.addClass('input_error');
		}
		if ((user_id == undefined || user_id == "") || (pass == undefined || pass == "")){
			return false;
		}
		var token = $('head').attr('id');
		var passhash = $.sha1(token + $.sha1(pass));
		$.ajax({
			type: 'POST',
			data: {
				token: token,
				user_id: user_id,
				passhash: passhash,
				countrycode: countrycode
			},
			dataType: 'json',
			success: function(data, textStatus) {
				if (data.error) {
					$('head').attr('id', data.token);
					
					form.find('input[name=' + data.error[0] +']').addClass('input_error');
					$('#login_form_status').text(data.error[1]).addClass('error_msg').show();
				}
				else {
					window.location = data.return_url;
				}
			},
			error: function(XMLHttpRequest, textStatus, errorThrown) {
				
			}
		})
		return false;
	},
	
	logout: function(event) {
		if (!event) event = window.event;
		event.cancelBubble = true;
	    if (event.stopPropagation) {
			// this code is for Mozilla and Opera
			event.stopPropagation();
	    }else if (window.event) {
			// this code is for IE
			window.event.cancelBubble = true;
	    }
		$.ajax({
			url: '/logout',
			type: 'POST',
			data: {foo: 'bar'},
			dataType: 'json',
			success: function(data, textStatus) {
				window.location = data.return_url;
			},
			error: function(XMLHttpRequest, textStatus, errorThrown) {
				window.location = '/'; 	
			}
		});
	},
	
	submit: function(event) {
		if (!event) event = window.event;
		event.cancelBubble = true;
	    event.stopPropagation();
		var form = $(event.target).parents('.form');
		form.find('input').removeClass('input_error');
		$('#form_status').hide();
		var token = $('head').attr('id');
		var form_data = form.serialize()+"&token=" + token;
		$.ajax({
			type: 'POST',
			data: form_data,
			dataType: 'json',
			success: function(data, textStatus) {
				if (data.error) {
					$('head').attr('id', data.token);
					form.find('input[name=' + data.error[0] +']').addClass('input_error');
					$('#form_status').text(data.error[1]).addClass('error_msg').show();
				}
				else {
					if (data.return_url){
						window.location = data.return_url;
					}
					if (data.msg) {
						$('#form_status').text(data.msg[1]).addClass(data.msg[1] + '_msg').show();
					}
				}
			},
			error: function(XMLHttpRequest, textStatus, errorThrown) {
				$('#form_status').text(textStatus).addClass('error_msg').show();
				form.reset();
			}
		})
		return false;
		
	}
}