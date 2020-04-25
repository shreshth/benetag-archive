function insertAlertMarkup(alertDivId, alertText, alertKind) {
document.getElementById(alertDivId).innerHTML = '<div class="alert fade in out "+alertKind><a class="close" href="#" data-dismiss="alert">&times;</a>'+alertText+'</div>';
}
