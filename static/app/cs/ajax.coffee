jQuery ->
  $('#btn-next-img').click(
    ->
      $.ajax '/',
               type: 'GET'
               dataType: 'json'
               error: (jqXHR, textStatus, errorThrown) -> $('body').append "AJAX Error: #{textStatus}"
               success: (data, textStatus, jqXHR) ->
                 $('#rec-photo p').text('Photo identifier: '+ data['id'])
                 $('#rec-photo img').attr('src', data['url'])
  )

# alert "DOM is ready" # for syntax test

