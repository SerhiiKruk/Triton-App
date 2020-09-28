var pageHeight = $('body').height(),
  footerHeight = $('footer').height();
if (pageHeight < $(window).height() - footerHeight) {
  $('footer').css({
    'position': 'absolute',
    'bottom': '0'
  });
} else {
  $('footer').css({
    'position': '',
    'bottom': ''
  });
}