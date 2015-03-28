jQuery ->
  $('#btn-next-img').click(
    ->
      make_active = () ->
        $('#btn-next-img span').toggleClass('glyphicon-chevron-right').toggleClass('glyphicon-refresh')
        $('#btn-next-img').prop('disabled', false)
        $('#btn-like').prop('hidden', false)
        $('#btn-like').prop('disabled', false)
      $(this).children('span').toggleClass('glyphicon-chevron-right').toggleClass('glyphicon-refresh')
      $(this).prop('disabled', true)
      $('#btn-like').prop('disabled', true)
      $.ajax '/',
               type: 'GET'
               dataType: 'json'
               error: (jqXHR, textStatus, errorThrown) -> $('body').append "AJAX Error: #{textStatus}"
               success: (data, textStatus, jqXHR) ->
                 $('#rec-photo').attr('data-id', data['id'])
                 $('#rec-photo img').attr('src', data['url'])
                 #alert $(this).children('span').attr('class')
                 setTimeout(make_active, 3000)
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

