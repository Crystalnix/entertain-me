jQuery ->
  $('#btn-next-img').click(
    ->
      make_active = () ->
        $('#btn-next-img').prop('disabled', false)
        $('#btn-like').prop('hidden', false)
        $('#btn-like').prop('disabled', false)
      $(this).prop('disabled', true)
      $('#btn-like').prop('disabled', true)
      $('#rec-photo img').attr('src', '/static/app/gif/ajaxSpinner.gif')
      $.ajax '/',
               type: 'GET'
               dataType: 'json'
               error: (jqXHR, textStatus, errorThrown) -> $('body').append "AJAX Error: #{textStatus}"
               success: (data, textStatus, jqXHR) ->
                 $('#rec-photo').attr('data-id', data['id'])
                 $('#rec-photo img').attr('src', data['url'])
                 #alert $(this).children('span').attr('class')
                 make_active()
  )
  $('#btn-like').click(
    ->
      $.ajax '/like',
               type: 'GET'
               dataType: 'json'
               data: {id: $('#rec-photo').attr("data-id")}
               error: (jqXHR, textStatus, errorThrown) -> $('body').append "AJAX Error: #{textStatus}"
               success: (data, textStatus, jqXHR) ->
                 $('#btn-like').prop('hidden', true)
  )

# alert "DOM is ready" # for syntax test

