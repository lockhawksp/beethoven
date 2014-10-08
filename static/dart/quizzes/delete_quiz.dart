import 'dart:convert';
import 'dart:html';


Map cookiesToMap() {
  Map cookies = {};
  List items = document.cookie.split(new RegExp(r'; '));
  for (String item in items) {
    int i = item.indexOf('=');
    String key = item.substring(0, i);
    String value = item.substring(i+1, item.length);
    cookies[key] = value;
  }
  return cookies;
}


void deleteQuiz(Event e) {
  ButtonElement deleteButton = e.target;
  String url = deleteButton.attributes['data-delete-quiz-url'];

  HttpRequest request = new HttpRequest();
  request.onReadyStateChange.listen((_) {
    Map data = JSON.decode(request.responseText);
    if (data.containsKey('msg') && data['msg'] == 'deleted') {
      window.location.assign(window.location.href);
    }
  });
  request.open('POST', url);
  request.setRequestHeader('X-CSRFToken', cookiesToMap()['csrftoken']);
  request.send();
}


void main() {
  querySelectorAll('.delete-quiz').forEach((Element e) {
    e.onClick.listen(deleteQuiz);
  });
}
