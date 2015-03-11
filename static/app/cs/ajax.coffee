jQuery ->
  $('#btn-next-img').click(
    ->
      $.ajax '/get_photo',
               type: 'GET'
               dataType: 'html'
               error: (jqXHR, textStatus, errorThrown) -> $('body').append "AJAX Error: #{textStatus}"
               success: (data, textStatus, jqXHR) -> $('#rec-photo').html data
  )

# alert "DOM is ready" # for syntax test

