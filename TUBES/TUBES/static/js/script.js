$('#edit').on('click', function (){
  if ($('#edit-modal').hasClass('on')) {
    $('#edit-modal').removeClass('on')
  } else {
    $('#edit-modal').addClass('on')
  }
})

$('#add').on('click', function (){
  if ($('#add-modal').hasClass('on')) {
    $('#add-modal').removeClass('on')
  } else {
    $('#add-modal').addClass('on')
  }
})

$('.close').on('click', function (){
  $('#add-modal,#edit-modal').removeClass('on')
})


$('#delete').on('click', function (){
  Swal.fire({
    title: 'Are you sure?',
    text: "You won't be able to revert this!",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#86d383',
    cancelButtonColor: '#e65454',
    confirmButtonText: 'Yes, delete it!'
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire(
        'Deleted!',
        'Your data has been deleted.',
        'success'
      )
    }
  })
})