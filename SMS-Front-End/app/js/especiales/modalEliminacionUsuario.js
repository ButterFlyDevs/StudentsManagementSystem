var eventHandlerType = (UIkit.support.touch) ? 'tap' : 'click',
  modal = UIkit.modal('#Modal', {
    bgclose: false
  });

console.log('eventHandlerType: ' + eventHandlerType);

$('#openModal').on(eventHandlerType, function(e) {
  e.preventDefault();
  console.log("Mostrando mensaje de confirmación de eliminación.")
  modal.show();
});

$('#DelButton').on(eventHandlerType, function(e) {
  console.log("Eliminación en modalEliminacionClase.")
  e.preventDefault();
  //Oculta el modal
  modal.hide();
});

$('#CancelButton').on(eventHandlerType, function(e) {
  console.log("Cancelando eliminacioń.")
  e.preventDefault();
  //Oculta el modal
  modal.hide();
});
