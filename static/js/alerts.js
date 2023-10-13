function alert_message(msg, type){
    title='' 
    icon=''
    switch (type) {
      case 'info': 
        title = 'Информация'
        icon = 'info'
        break;
      case 'error': 
        title = 'Ошибка'
        icon = 'error'
        break;
      case 'success': 
        title = 'Информация'
        icon = 'success'
        break;
    }
  
    $.toast({
        heading: title,
        text: msg,
        showHideTransition: 'slide',
        icon: icon,
        position: 'top-right',
        hideAfter: 6000   // in milli seconds
    })
  }