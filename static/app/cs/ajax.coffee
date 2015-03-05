#$(document).ready ->
#        $.ajax '/test',
#               type: 'GET'
#               dataType: 'json'
#               error: (jqXHR, textStatus, errorThrown) -> $('body').append "AJAX Error: #{textStatus}"
#               success: (data, textStatus, jqXHR) -> $('body').append "Successful AJAX call: #{data}"

jQuery ->
  $('#btn-next-img').click(
#  $('#test').click(
    ->
      # function one content
      $.ajax '/test',
               type: 'GET'
               dataType: 'html'
               error: (jqXHR, textStatus, errorThrown) -> $('body').append "AJAX Error: #{textStatus}"
               success: (data, textStatus, jqXHR) -> $('#rec-photo').append data
  )
  $('#test').click(
    ->
#      alert 'JQuery alert'
#      $('#test_coffee').text("Some text")
      $.ajax '/testa',
               type: 'GET'
               dataType: 'html'
               error: (jqXHR, textStatus, errorThrown) -> $('body').append "AJAX Error: #{textStatus}"
               success: (data, textStatus, jqXHR) -> $('body').append "Successful AJAX call: #{data}"
  )


alert "DOM is ready"

