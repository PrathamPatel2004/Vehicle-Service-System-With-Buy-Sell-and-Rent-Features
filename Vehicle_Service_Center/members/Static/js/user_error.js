Swal.fire({
  title: 'Login Error',
  text: '{{ error_message|escapejs }}',
  icon: 'info',
  confirmButtonText: 'OK',
}).then((result) => {
  if (result.isConfirmed) {
    window.location.href = "login";
  }
});

