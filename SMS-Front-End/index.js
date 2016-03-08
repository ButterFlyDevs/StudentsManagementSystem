var eventHandlerType = (UIkit.support.touch) ? 'tap' : 'click',
  modal = UIkit.modal('#wellnessDashboardModal', {
    bgclose: false
  });

console.log('eventHandlerType: ' + eventHandlerType);

$('#openModal').on(eventHandlerType, function(e) {
  e.preventDefault();
  modal.show();
});

$('#wellnessDashboardModalSaveButton, #wellnessDashboardModalCancelButton').on(eventHandlerType, function(e) {
  console.log("closing")
  e.preventDefault();
  modal.hide();
});
